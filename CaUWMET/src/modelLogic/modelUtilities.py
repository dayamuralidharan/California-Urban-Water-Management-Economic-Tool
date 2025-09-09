

def lookupCorrespondingValue(df, item, colA, colB):
    """
    :param df: Pandas dataframe
    :param item: Item to look for in column A
    :param colA: Name of the column A
    :param colB: Name of the column B
    :return: Returns corresponding item in column B
    Note: This works only if there are no duplicates (there is only
    one 'item' in colA.
    """
    return df[df[colA] == item][colB].values[0]

def reclassifyYearType(inputYearType):
    """
    Reclassify the hydrologic year type from DWR's weighted water year index (WYI) to UWMP's 3-tiered system.
    Method sourced from CWEST - Assign "multi-dry" year type when:
        WYI = critical
        WYI = dry or critical for 3 or more years in a row
    :param yearType: list or array of strings (W, AN, N, BN, D, C)
    :return rType: list or array of reclassified year type
     (NB - Normal or better, SD - Single Dry, MD - Multiple Dry)
    """
    dryYears = ['D', 'C']
    inputYearType = list(inputYearType)
    cauwmetYearType = []
    dryStreak = 0
    
    for yt in inputYearType:
        if yt in dryYears:
            dryStreak += 1
        else:
            dryStreak = 0

        if yt == 'C' or dryStreak >= 3:
            cauwmetYearType.append('MD')
        else:
            cauwmetYearType.append('NB')
    return cauwmetYearType