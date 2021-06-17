import base64
from typing import ValuesView
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
from sklearn import datasets
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import traceback
from load_css import local_css

def app():

    class opt_echo:
        def __init__(self):
            self.checkbox = st.sidebar.checkbox("Show source code")

            self.orig_extract_stack = traceback.extract_stack

            if self.checkbox:
                traceback.extract_stack = lambda: self.orig_extract_stack()[:-2]
                self.echo = st.echo()

        def __enter__(self):
            if self.checkbox:
                return self.echo.__enter__()

        def __exit__(self, type, value, traceback):
            if self.checkbox:
                self.echo.__exit__(type, value, traceback)

            # For some reason I need to import this again.
            import traceback

            traceback.extract_stack = self.orig_extract_stack

    with opt_echo():
        st.title('Hydrology Assumptions')
        st.write("")
        st.write("<Description of Hydrology Assumptions and Steps to use this page to be added.>")
        st.write("")

        @st.cache(suppress_st_warning=True)
        def fetch_data(samples):
        #     if path:
        #         demands = pd.read_csv(path)
                
            # else:
            demands = pd.read_csv("inputData/hydrologyAssumptions.csv")
            return pd.DataFrame(demands)

        #Example controlers
        st.sidebar.subheader("Data Filter options")

        sample_size = st.sidebar.number_input("Rows", min_value=1, value=10)

        return_mode = st.sidebar.selectbox("Returned Grid Update Mode", list(DataReturnMode.__members__), index=1)
        return_mode_value = DataReturnMode.__members__[return_mode]

        update_mode = st.sidebar.selectbox("Chart Update Mode", list(GridUpdateMode.__members__), index=6)
        update_mode_value = GridUpdateMode.__members__[update_mode]

        #enterprise modules
        # enable_enterprise_modules = st.sidebar.checkbox("Enable Enterprise Modules")
        # if enable_enterprise_modules:
        #     enable_sidebar =st.sidebar.checkbox("Enable grid sidebar", value=False)
        # else:
        #     enable_sidebar = False

        #features
        # fit_columns_on_grid_load = st.sidebar.checkbox("Fit Grid Columns on Load")

        enable_selection=st.sidebar.checkbox("Enable row selection", value=True)
        if enable_selection:
            st.sidebar.subheader("Selection options")
            selection_mode = st.sidebar.radio("Selection Mode", ['single','multiple'])

            use_checkbox = st.sidebar.checkbox("Use check box for selection")
            if use_checkbox:
                groupSelectsChildren = st.sidebar.checkbox("From all elements", value=True)
                groupSelectsFiltered = st.sidebar.checkbox("From filtered elements", value=True)

            if ((selection_mode == 'multiple') & (not use_checkbox)):
                rowMultiSelectWithClick = st.sidebar.checkbox("Multiselect with click (instead of holding CTRL)", value=False)
                if not rowMultiSelectWithClick:
                    suppressRowDeselection = st.sidebar.checkbox("Suppress deselection (while holding CTRL)", value=False)
                else:
                    suppressRowDeselection=False
            st.sidebar.text("___")

        enable_pagination = st.sidebar.checkbox("Enable pagination", value=False)
        if enable_pagination:
            st.sidebar.subheader("Pagination options")
            paginationAutoSize = st.sidebar.checkbox("Auto pagination size", value=True)
            if not paginationAutoSize:
                paginationPageSize = st.sidebar.number_input("Page size", value=5, min_value=0, max_value=sample_size)
            st.sidebar.text("___")

        df = fetch_data(sample_size)

    #Infer basic colDefs from dataframe types
        gb = GridOptionsBuilder.from_dataframe(df)

        #customize gridOptions
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

        if enable_selection:
            gb.configure_selection(selection_mode)
            if use_checkbox:
                gb.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=groupSelectsChildren, groupSelectsFiltered=groupSelectsFiltered)
            if ((selection_mode == 'multiple') & (not use_checkbox)):
                gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=rowMultiSelectWithClick, suppressRowDeselection=suppressRowDeselection)

        if enable_pagination:
            if paginationAutoSize:
                gb.configure_pagination(paginationAutoPageSize=True)
            else:
                gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()

        #Display the grid
        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            width='100%',
            data_return_mode=return_mode_value, 
            update_mode=update_mode_value,
            # fit_columns_on_grid_load=fit_columns_on_grid_load,
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            # enable_enterprise_modules=enable_enterprise_modules,
            )
        
        selected = grid_response['selected_rows']
        selected_df = pd.DataFrame(selected)

        #downloading the dataframe data to a .csv file
        def download_link(object_to_download, download_filename, download_link_text):

            if isinstance(object_to_download,pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=False)
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(object_to_download.encode()).decode()
            return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
            
        if st.button('Download Dataframe to CSV format', key = "1"):
            tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)