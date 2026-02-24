# -*- coding: utf-8 -*-
"""
Calsim 3 M&I extraction and aggregation
- Merges D-part segments per (A,C,E,F) family
- Masks HEC-DSS missing sentinels (-901, -902, ...) to NaN
- Normalizes monthly data to PeriodIndex('M') BEFORE merging (prevents month shifts)
- Converts back to month-end timestamps after merge
- Calendar-year or water-year output (AGGREGATION)
- Debug toggle writes raw monthly CFS + AF and CY/WY annual summaries

Compatible with: pydsstools 2.3.2
"""

import os
import re
import numpy as np
import pandas as pd
import logging
import traceback
import ast
import operator as op
from typing import Dict, List, Tuple, Optional
from pandas.tseries.offsets import MonthBegin, MonthEnd
from pydsstools.heclib.dss import HecDss

# ------------------------- Configuration -------------------------

# Input Excel
NODE_MAPPING_XLSX = '../inputData/CaUWMETInputData.xlsx'
SHEET_NAME = 'Contractor Assumptions'
FORMULA_COL = 'Calsim 3 M&I Delivery Arc'  # column with expressions
CONTRACTOR_COL = 'Contractor'              # column for naming output columns
DSS_FILENAME_CELL_COL = 'H'                # column containing the DSS filename
DSS_FILENAME_CELL_SKIPROWS = 2             # row offset to reach filename cell (0-indexed)
DSS_FILENAME_CELL_NROWS = 1

# Time aggregation for FINAL outputs
AGGREGATION = 'CY'            # 'CY' -> A-DEC (calendar year), 'WY' -> A-SEP (water year)
START_DATE = "1921-10"        # inclusive; YYYY-MM
END_DATE   = "2015-09"        # inclusive; YYYY-MM

# Units and constants
FT3_PER_ACRE = 43560.0
SEC_PER_DAY = 24.0 * 3600.0

# Output
OUTPUT_NAME_PREFIX = "swpCVPSupplyData"
LOG_FILE = 'logfileCalsim3.log'
LOG_LEVEL = logging.INFO

# Pandas Excel engine
PANDAS_EXCEL_ENGINE = 'openpyxl'

# ------------------------- [CONFIG] DEBUG TOGGLE -------------------------
DEBUG_ENABLED = False                 # True to enable targeted debug dumps
DEBUG_BPARTS: List[str] = ["D_THRMF_11_NU1_PMI"]          # e.g., ["D_CCC019_CCWD"]
DEBUG_YEARS:  List[int] = [1929]          # e.g., [1929, 2010]
DEBUG_DIR_NAME = "debug"              # debug subfolder next to script

# Optional: log (A,C,E,F) family counts and D-parts for selected B-parts
DIAG_BPARTS: List[str] = []           # e.g., ["D_THRMF_11_NU1_PMI"]

# ------------------------- Logging setup (explicit, VS Code-safe) -------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(SCRIPT_DIR, LOG_FILE)
DEBUG_DIR = os.path.join(SCRIPT_DIR, DEBUG_DIR_NAME)

root_logger = logging.getLogger()
for h in list(root_logger.handlers):
    root_logger.removeHandler(h)
root_logger.setLevel(LOG_LEVEL)

file_handler = logging.FileHandler(LOG_PATH, mode='w', encoding='utf-8')
file_handler.setLevel(LOG_LEVEL)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(LOG_LEVEL)

fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(fmt)
stream_handler.setFormatter(fmt)

root_logger.addHandler(file_handler)
root_logger.addHandler(stream_handler)

logging.info(f"Logging initialized. File: {LOG_PATH}")

# ------------------------- Helpers -------------------------

def read_node_mapping() -> Tuple[pd.DataFrame, str]:
    """Read the node mapping workbook and infer the DSS input file path."""
    logging.info("Reading node mapping from Excel.")
    node_mapping_df = pd.read_excel(
        NODE_MAPPING_XLSX,
        sheet_name=SHEET_NAME,
        skiprows=4,
        engine=PANDAS_EXCEL_ENGINE
    )

    dss_filename = pd.read_excel(
        NODE_MAPPING_XLSX,
        sheet_name=SHEET_NAME,
        usecols=DSS_FILENAME_CELL_COL,
        skiprows=DSS_FILENAME_CELL_SKIPROWS,
        nrows=DSS_FILENAME_CELL_NROWS,
        engine=PANDAS_EXCEL_ENGINE
    ).iloc[0, 0]

    input_dss_file = os.path.join("..", "inputData", str(dss_filename))
    if not os.path.exists(input_dss_file):
        raise FileNotFoundError(f"Input DSS not found: {input_dss_file}")

    logging.info(f"Node mapping read. DSS file resolved to: {input_dss_file}")
    return node_mapping_df, input_dss_file


def build_catalog(d: HecDss) -> pd.DataFrame:
    """Build catalog-like DataFrame (A–F parts + full pathname) and de-duplicate."""
    pathnames = d.getPathnameList("/*/*/*/*/*/*/")
    def _split_af(p: str):
        parts = p.strip("/").split("/")
        parts = (parts + [""] * 6)[:6]
        return parts
    parsed = [_split_af(p) for p in pathnames]
    catdf = pd.DataFrame(parsed, columns=list("ABCDEF"))
    catdf["Pathname"] = pathnames
    before = len(catdf)
    catdf = catdf.drop_duplicates(subset=["Pathname"]).reset_index(drop=True)
    after = len(catdf)
    if after < before:
        logging.info(f"Catalog de-duplicated by Pathname: {before} -> {after}")
    return catdf


def read_monthly_cfs_series(
    d: HecDss,
    pathname: str,
    start_dt: pd.Timestamp,
    end_dt: pd.Timestamp,
    log_read: bool = True
) -> pd.Series:
    """
    Read a regular time series for a pathname and return a monthly mean CFS series,
    properly month-aligned, clipped to [start_dt, end_dt], indexed by month-end timestamps.

    Fixes included:
    - Force explicit read window to avoid truncated reads.
    - Mask HEC-DSS missing sentinels (<= -900) to NaN immediately.
    - Detect 'month-start stamping' (e.g., value for Oct is stamped at 01-Nov 00:00)
      and shift index BACK by one month so values land in the correct month.
    """

    # DSS date strings like '01OCT1921' and '30SEP2015'
    start_str = start_dt.strftime('%d%b%Y').upper()
    end_str   = end_dt.strftime('%d%b%Y').upper()

    # 1) Read raw
    try:
        ts = d.read_ts(pathname, start=start_str, end=end_str)
    except TypeError:
        ts = d.read_ts(pathname)

    dti = pd.to_datetime(list(ts.pytimes))
    vals = np.asarray(ts.values, dtype=float)

    # 2) Mask DSS sentinels to NaN BEFORE any resampling/merging
    missing_mask = vals <= -900.0
    if missing_mask.any() and log_read:
        logging.warning(
            f"Masked {int(missing_mask.sum())} missing value(s) (<= -900) in {pathname} "
            f"within {start_dt.date()}..{end_dt.date()}"
        )
    vals[missing_mask] = np.nan

    s = pd.Series(vals, index=dti).sort_index()

    # 3) Detect 'month-start stamping' and shift back one month when present.
    #    Heuristic: if >=80% of timestamps are on day=1 at 00:00, assume month-start stamping.
    is_month_start = (s.index.day == 1)
    frac_month_start = is_month_start.sum() / max(len(s.index), 1)

    if len(s) and frac_month_start >= 0.8:
        # Log a small sample so you can see the effect
        if log_read:
            sample_before = s.index[:3]
            logging.info(
                f"Detected month-start stamping in {pathname} "
                f"(~{frac_month_start:.0%} of points on day=1). Shifting back 1 month."
            )
            logging.info(f"Index sample BEFORE shift: {list(sample_before.date)}")

        # Shift: convert to monthly Periods based on the current stamps,
        # then subtract one month and place at month-end timestamps.
        s_shifted = s.copy()
        s_shifted.index = (s_shifted.index.to_period('M') - 1).to_timestamp(how='end')

        # Optional: small check & log
        if log_read and len(s_shifted):
            sample_after = s_shifted.index[:3]
            logging.info(f"Index sample AFTER  shift: {list(sample_after.date)}")

        s = s_shifted

    # 4) Now that the stamps are aligned to the intended months, clip to window
    s = s.loc[(s.index >= start_dt) & (s.index <= end_dt)]

    # 5) If we still have sub-monthly data (unlikely here), take monthly mean; otherwise as-is.
    #    Use resample('M') to ensure month-end index uniformly.
    s_monthly = s.resample("M").mean()

    if log_read:
        logging.info(
            f"Read {pathname} | monthly pts={s_monthly.size} | "
            f"range={s_monthly.index.min().date() if len(s_monthly) else None} "
            f"to {s_monthly.index.max().date() if len(s_monthly) else None}"
        )
        if len(s_monthly):
            first_ts = s_monthly.index.min()
            first_val = s_monthly.loc[first_ts]
            logging.info(
                f"First monthly value at {first_ts.date()} = "
                f"{'NaN' if pd.isna(first_val) else float(first_val)}"
            )

    return s_monthly


def monthly_cfs_to_annual_af(monthly_cfs: pd.Series, aggregation: str) -> pd.Series:
    """Convert monthly mean CFS -> monthly AF (time-weighted), then sum to annual (CY or WY)."""
    if monthly_cfs.empty:
        return monthly_cfs

    days_in_month = monthly_cfs.index.days_in_month
    monthly_af = monthly_cfs * (days_in_month * SEC_PER_DAY) / FT3_PER_ACRE

    if aggregation.upper() == 'WY':
        annual_af = monthly_af.resample("A-SEP").sum()
    elif aggregation.upper() == 'CY':
        annual_af = monthly_af.resample("A-DEC").sum()
    else:
        raise ValueError(f"Unsupported aggregation '{aggregation}' (use 'WY' or 'CY').")

    logging.info(
        f"Annual series range: {annual_af.index.min().date() if len(annual_af) else None} "
        f"to {annual_af.index.max().date() if len(annual_af) else None}, n={len(annual_af)}"
    )
    return annual_af


def build_master_index(start_dt: pd.Timestamp, end_dt: pd.Timestamp, aggregation: str) -> pd.DatetimeIndex:
    """Build a master annual index based on aggregation."""
    if aggregation.upper() == 'WY':
        return pd.date_range(start=start_dt, end=end_dt, freq="A-SEP")
    return pd.date_range(start=start_dt, end=end_dt, freq="A-DEC")


def select_and_merge_family_for_b(
    d: HecDss,
    catdf: pd.DataFrame,
    bpart: str,
    start_dt: pd.Timestamp,
    end_dt: pd.Timestamp
) -> Tuple[Optional[str], Optional[pd.Series]]:
    """
    For a given B-part:
      1) Group by (A,C,E,F) family (ignore D).
      2) For each family, read *all* pathnames (various D-parts),
         force [start_dt, end_dt], produce monthly means,
         NORMALIZE to PeriodIndex('M') BEFORE merging, then coalesce via combine_first.
      3) Score families by: latest end (maximizes end coverage), overlap months, earliest start.

    Returns: (family_key_str, merged_monthly_series) or (None, None).
    """
    sub = catdf[catdf["B"] == bpart]
    if sub.empty:
        return None, None

    fam_groups = sub.groupby(["A", "C", "E", "F"], dropna=False)

    best = None  # (series_end, overlap, -series_start.value, key_str, merged_series_period)
    for fam_key, fam_df in fam_groups:
        a, c, e, f = fam_key
        key_str = f"A={a}, C={c}, E={e}, F={f}"

        monthly_list: List[pd.Series] = []
        for pth in fam_df["Pathname"].tolist():
            try:
                s_month = read_monthly_cfs_series(d, pth, start_dt, end_dt, log_read=False)
                if len(s_month):
                    # Normalize to monthly PeriodIndex so all October values align, regardless of stamp
                    s_month = s_month.copy()
                    s_month.index = s_month.index.to_period('M')
                    # Paranoia guard: ensure no sentinel remains
                    s_month = s_month.where(~(s_month <= -900.0), np.nan)
                    monthly_list.append(s_month)
            except Exception as ex:
                logging.warning(f"B='{bpart}' family '{key_str}' segment read failed: {ex}")

        if not monthly_list:
            continue

        # Coalesce across segments on PeriodIndex('M'): first non-NaN wins
        merged = monthly_list[0].copy()
        for s2 in monthly_list[1:]:
            overlap_idx = merged.index.intersection(s2.index)
            if len(overlap_idx):
                diff = (
                    merged.loc[overlap_idx].notna()
                    & s2.loc[overlap_idx].notna()
                    & (merged.loc[overlap_idx].values != s2.loc[overlap_idx].values)
                )
                if np.any(diff):
                    logging.warning(
                        f"B='{bpart}' family '{key_str}' has overlapping months with differing values; "
                        f"keeping first segment's values for those months."
                    )
            s2 = s2.where(~(s2 <= -900.0), np.nan)
            merged = merged.combine_first(s2)

        merged_nonan = merged.dropna()
        if merged_nonan.empty:
            continue

        # Score (convert to timestamps for comparisons)
        s_start = merged_nonan.index.min().to_timestamp(how='end')
        s_end   = merged_nonan.index.max().to_timestamp(how='end')
        overlap = len(merged_nonan)

        score = (s_end, overlap, -s_start.value, key_str, merged)
        if (best is None) or (score > best):
            best = score

    if best is None:
        logging.error(f"No readable monthly data for B='{bpart}' in any (A,C,E,F) family.")
        return None, None

    s_end, overlap, _, key_str, merged_period = best
    # Convert PeriodIndex back to month-end timestamps
    merged_ts = merged_period.sort_index().to_timestamp(how='end')

    logging.info(
        f"Selected family for B='{bpart}': {key_str} | "
        f"merged range={merged_ts.dropna().index.min().date()}..{merged_ts.dropna().index.max().date()} | "
        f"months={merged_ts.dropna().size}"
    )
    return key_str, merged_ts

# ------------------------- DEBUG Utilities -------------------------

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def monthly_cfs_to_af(monthly_cfs: pd.Series) -> pd.Series:
    """Monthly mean CFS -> monthly AF (time-weighted)."""
    if monthly_cfs.empty:
        return monthly_cfs
    return monthly_cfs * (monthly_cfs.index.days_in_month * SEC_PER_DAY) / FT3_PER_ACRE

def debug_bpart_years(
    d,
    catdf: pd.DataFrame,
    bpart: str,
    years: List[int],
    start_dt: pd.Timestamp,
    end_dt: pd.Timestamp,
    out_dir: str,
):
    """
    DEBUG:
      - Merge segments (production behavior),
      - Output raw monthly CFS (post-merge, clipped to [start_dt, end_dt]),
      - Output monthly AF with DaysInMonth and SecondsPerDay,
      - For each requested year, compute CY and WY totals,
      - Write:
          1) debug_<B>_monthly_CFS_AF.csv
          2) debug_<B>_annual_summary.csv
    """
    fam_key, monthly_cfs_merged = select_and_merge_family_for_b(d, catdf, bpart, start_dt, end_dt)
    if fam_key is None or monthly_cfs_merged is None or monthly_cfs_merged.empty:
        logging.error(f"[DEBUG] No monthly data for B='{bpart}'")
        return

    monthly_cfs = monthly_cfs_merged.copy().sort_index()

    days_in_month = monthly_cfs.index.days_in_month
    sec_per_day = np.full_like(monthly_cfs.values, fill_value=SEC_PER_DAY, dtype=float)
    monthly_af = monthly_cfs * (days_in_month * SEC_PER_DAY) / FT3_PER_ACRE

    dbg = pd.DataFrame({
        "Monthly_CFS": monthly_cfs.values.astype(float),
        "DaysInMonth": days_in_month.astype(int),
        "SecondsPerDay": sec_per_day.astype(float),
        "Monthly_AF": monthly_af.values.astype(float),
    }, index=monthly_cfs.index)

    ensure_dir(out_dir)
    mfile = os.path.join(out_dir, f"debug_{bpart}_monthly_CFS_AF.csv")
    dbg_rounded = dbg.copy()
    dbg_rounded["Monthly_CFS"] = dbg_rounded["Monthly_CFS"].round(6)
    dbg_rounded["Monthly_AF"] = dbg_rounded["Monthly_AF"].round(6)
    dbg_rounded.to_csv(mfile, float_format="%.6f", date_format="%Y-%m-%d")
    logging.info(f"[DEBUG] Wrote monthly CFS/AF for B='{bpart}' to: {mfile} (Family={fam_key})")

    rows = []
    for yr in years:
        cy_start = pd.Timestamp(year=yr, month=1, day=1)
        cy_end   = pd.Timestamp(year=yr, month=12, day=31)
        cy_mask = (monthly_af.index >= cy_start) & (monthly_af.index <= cy_end)
        cy_total = monthly_af.loc[cy_mask].sum()

        wy_start = pd.Timestamp(year=yr-1, month=10, day=1)
        wy_end   = pd.Timestamp(year=yr, month=9, day=30)
        wy_mask = (monthly_af.index >= wy_start) & (monthly_af.index <= wy_end)
        wy_total = monthly_af.loc[wy_mask].sum()

        rows.append((yr, float(cy_total), float(wy_total)))
        logging.info(
            f"[DEBUG] B='{bpart}' | Family={fam_key} | CY {yr}: {cy_total:,.3f} AF | "
            f"WY {yr}: {wy_total:,.3f} AF (Oct {yr-1}–Sep {yr})"
        )

    if rows:
        adf = pd.DataFrame(rows, columns=["Year", "CY_AF", "WY_AF"])
        afile = os.path.join(out_dir, f"debug_{bpart}_annual_summary.csv")
        adf.to_csv(afile, index=False)
        logging.info(f"[DEBUG] Wrote annual summary for B='{bpart}' to: {afile}")

# ------------------------- Safe expression evaluation -------------------------

ALLOWED_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
}
ALLOWED_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

class SafeArrayEvaluator(ast.NodeVisitor):
    """Restricted evaluator for arrays + numeric constants + + - * / only."""
    def __init__(self, var):
        self.var = var  # list[np.ndarray]

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        fn = ALLOWED_BIN_OPS.get(type(node.op))
        if fn is None:
            raise ValueError(f"Operator {type(node.op)} not allowed.")
        return fn(left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        fn = ALLOWED_UNARY_OPS.get(type(node.op))
        if fn is None:
            raise ValueError(f"Unary operator {type(node.op)} not allowed.")
        return fn(operand)

    def visit_Constant(self, node):  # Py>=3.8
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Only numeric constants are allowed.")

    def visit_Num(self, node):       # Py<3.8
        return float(node.n)

    def visit_Name(self, node):
        if node.id != "var":
            raise ValueError(f"Name '{node.id}' not allowed.")
        return self.var

    def visit_Subscript(self, node):
        container = self.visit(node.value)
        if hasattr(ast, "Index") and isinstance(node.slice, ast.Index):   # Py<3.9
            idx_node = node.slice.value
        else:                                                             # Py>=3.9
            idx_node = node.slice
        idx = self.visit(idx_node)
        if isinstance(idx, float):
            idx = int(idx)
        if not isinstance(idx, (int, np.integer)):
            raise ValueError("Subscript index must be an integer.")
        return container[idx]

    def generic_visit(self, node):
        raise ValueError(f"Expression element not allowed: {type(node).__name__}")


def tokenize_expression(expr: str) -> List[str]:
    """Tokenize expression into identifiers, numbers, and single-char operators."""
    expr_ns = expr.replace(" ", "").replace("\n", "")
    tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|[\(\)\+\-\*/]', expr_ns)
    return tokens


def build_var_and_parsed_expr(expr: str, bparts_universe: set,
                              series_cache: Dict[str, pd.Series],
                              annual_index: pd.DatetimeIndex) -> Tuple[List[np.ndarray], str]:
    """
    Map B-part identifiers in expr to var[i], fetch/calc their annual series from cache,
    align to annual_index, and return (var_list, parsed_expr_string).
    """
    tokens = tokenize_expression(expr)
    var_arrays: List[np.ndarray] = []
    parsed_tokens: List[str] = []
    b_to_var_idx: Dict[str, int] = {}

    for tok in tokens:
        if tok in {"+", "-", "*", "/", "(", ")"}:
            parsed_tokens.append(tok)
        elif tok in bparts_universe:
            if tok not in b_to_var_idx:
                if tok not in series_cache:
                    raise ValueError(f"B-part '{tok}' not found in series cache.")
                aligned = series_cache[tok].reindex(annual_index)
                var_arrays.append(aligned.values.astype(float))
                b_to_var_idx[tok] = len(var_arrays) - 1
            parsed_tokens.append(f"var[{b_to_var_idx[tok]}]")
        else:
            # numeric?
            try:
                float(tok)
                parsed_tokens.append(tok)
            except Exception:
                raise ValueError(f"Unsupported token '{tok}' in expression: '{expr}'")
    parsed_expr = "".join(parsed_tokens)
    return var_arrays, parsed_expr


def safe_eval_array_expr(parsed_expr: str, var_arrays: List[np.ndarray]) -> np.ndarray:
    """Safely evaluate parsed expression string that references var[i]."""
    tree = ast.parse(parsed_expr, mode='eval')
    evaluator = SafeArrayEvaluator(var_arrays)
    result = evaluator.visit(tree)
    return result

# ------------------------- Main processing -------------------------

def main():
    try:
        # Read mapping and DSS file
        node_mapping_df, input_dss_file = read_node_mapping()

        # Pull formulas and contractor names
        formulas_raw = node_mapping_df[FORMULA_COL].astype(str).tolist()
        contractors  = node_mapping_df[CONTRACTOR_COL].astype(str).tolist()

        # Parse date bounds and normalize to monthly boundaries
        start_dt = pd.to_datetime(START_DATE) + MonthBegin(0)
        end_dt   = pd.to_datetime(END_DATE)   + MonthEnd(0)
        logging.info(f"Clipping monthly data to: {start_dt.date()} through {end_dt.date()}")

        # Open DSS and build catalog
        logging.info(f"Opening DSS: {input_dss_file}")
        with HecDss.Open(input_dss_file) as d:
            catdf = build_catalog(d)
            bparts_universe = set(catdf["B"].unique())

            # Optional diagnostics: enumerate families & D-parts for selected B-parts
            if DIAG_BPARTS:
                for b in DIAG_BPARTS:
                    fams = catdf[catdf["B"] == b].groupby(["A","C","E","F"], dropna=False)
                    logging.info(f"[DIAG] B='{b}' has {len(fams)} families (by A,C,E,F).")
                    for fam_key, fam_df in fams:
                        a,c,e,f = fam_key
                        ds = list(fam_df["D"].unique())
                        logging.info(f"[DIAG]   Family A={a}, C={c}, E={e}, F={f}, segments={len(fam_df)}, D-parts={ds}")

            # DEBUG block
            if DEBUG_ENABLED and DEBUG_BPARTS and DEBUG_YEARS:
                ensure_dir(DEBUG_DIR)
                logging.info(f"[DEBUG] Running targeted CY/WY checks for B-parts={DEBUG_BPARTS}, years={DEBUG_YEARS}")
                for btest in DEBUG_BPARTS:
                    debug_bpart_years(
                        d=d,
                        catdf=catdf,
                        bpart=btest,
                        years=DEBUG_YEARS,
                        start_dt=start_dt,
                        end_dt=end_dt,
                        out_dir=DEBUG_DIR,
                    )

            # Determine B-parts used across formulas in first-appearance order
            used_bparts_list: List[str] = []
            seen = set()
            for expr in formulas_raw:
                for tok in tokenize_expression(expr):
                    if tok in bparts_universe and tok not in seen:
                        used_bparts_list.append(tok)
                        seen.add(tok)

            logging.info(f"Total unique B-parts referenced in formulas: {len(used_bparts_list)}")

            # Resolve and cache annual series per B-part (merge across D-part segments)
            annual_cache: Dict[str, pd.Series] = {}
            bpart_to_family: Dict[str, Optional[str]] = {}
            missing_bparts: List[str] = []

            for b in used_bparts_list:
                try:
                    fam_key, monthly_cfs_merged = select_and_merge_family_for_b(d, catdf, b, start_dt, end_dt)
                    if fam_key is None or monthly_cfs_merged is None or monthly_cfs_merged.empty:
                        raise ValueError(f"No usable monthly series for B-part '{b}' after merging segments.")
                    bpart_to_family[b] = fam_key

                    annual_af = monthly_cfs_to_annual_af(monthly_cfs_merged, AGGREGATION)
                    annual_cache[b] = annual_af

                except Exception as e:
                    logging.error(f"Failed to cache B-part '{b}': {e}")
                    bpart_to_family[b] = None
                    annual_cache[b] = None
                    missing_bparts.append(b)

        # Build master annual index
        master_index = build_master_index(start_dt, end_dt, AGGREGATION)
        if master_index.empty:
            raise ValueError("Master annual index is empty—check START_DATE/END_DATE and AGGREGATION.")
        logging.info(
            f"Master annual index: {master_index.min().date() if len(master_index) else None} "
            f"-> {master_index.max().date() if len(master_index) else None}, n={len(master_index)}"
        )

        # Fill missing B-parts with NaN series (same index)
        if missing_bparts:
            for b in missing_bparts:
                annual_cache[b] = pd.Series(index=master_index, dtype=float)
            base_dss_name = os.path.basename(input_dss_file)
            missing_report = f"{OUTPUT_NAME_PREFIX}_{base_dss_name}_missing_bparts.csv"
            pd.Series(missing_bparts, name="Missing_BParts").to_csv(missing_report, index=False)
            logging.warning(f"Missing B-parts filled with NaN. See: {missing_report}")

        # Evaluate each contractor formula safely
        results: Dict[int, np.ndarray] = {}
        final_expr_strings: List[str] = []

        for i, expr in enumerate(formulas_raw):
            expr_str = str(expr).strip()
            if not expr_str or expr_str.lower() in ("nan", "none"):
                logging.warning(f"Empty/invalid formula for row {i}. Filling with NaN.")
                results[i] = np.full(master_index.size, np.nan)
                final_expr_strings.append("Invalid")
                continue

            try:
                var_arrays, parsed_expr = build_var_and_parsed_expr(
                    expr_str, set(annual_cache.keys()), annual_cache, master_index
                )
                if not var_arrays and parsed_expr:
                    const_val = float(parsed_expr)
                    results[i] = np.full(master_index.size, const_val, dtype=float)
                else:
                    result_arr = safe_eval_array_expr(parsed_expr, var_arrays)
                    result_arr = np.asarray(result_arr, dtype=float).reshape(-1)
                    if result_arr.size != master_index.size:
                        raise ValueError(f"Result length {result_arr.size} != master index length {master_index.size}")
                    results[i] = result_arr

                final_expr_strings.append(parsed_expr)
                logging.info(f"Processed formula for row {i}: '{expr_str}' -> '{parsed_expr}'")

            except Exception as e:
                logging.error(f"Error evaluating formula at row {i}: '{expr_str}' | {e}")
                results[i] = np.full(master_index.size, np.nan)
                final_expr_strings.append("Invalid")

        # Build output DataFrame (annual)
        flow_df = pd.DataFrame(results, index=master_index)
        name_map = {col_ix: contractors[col_ix] if col_ix < len(contractors) else f"Contractor_{col_ix}"
                    for col_ix in flow_df.columns}
        flow_df.rename(columns=name_map, inplace=True)

        # Write main outputs
        base_dss_name = os.path.basename(input_dss_file)
        output_file = f"{OUTPUT_NAME_PREFIX}_{base_dss_name}.csv"
        logging.info(f"Writing data to CSV: {output_file}")
        flow_df.to_csv(output_file, float_format="%.6f")

        mapping_out = f"{OUTPUT_NAME_PREFIX}_{base_dss_name}_bpart_family_mapping.csv"
        pd.Series(bpart_to_family).rename("Chosen_Family_(A,C,E,F)").to_csv(mapping_out, header=True)

        # QA summary: non-NaN counts and first/last non-NaN year per contractor
        summary = []
        for col in flow_df.columns:
            s = flow_df[col]
            nnz = s.notna().sum()
            first = s.dropna().index.min().date() if nnz else None
            last  = s.dropna().index.max().date() if nnz else None
            summary.append((col, int(nnz), first, last))
        qa_df = pd.DataFrame(summary, columns=["Contractor", "NonNaN_years", "First_year", "Last_year"])
        qa_file = f"{OUTPUT_NAME_PREFIX}_{base_dss_name}_qa_summary.csv"
        qa_df.to_csv(qa_file, index=False)
        logging.info(f"Wrote QA summary: {qa_file}")

        logging.info("Processing complete.")

    except Exception as exception:
        logging.error(traceback.format_exc())
        print("An error occurred. Check the log file for details.")


if __name__ == "__main__":
    main()
    logging.shutdown()