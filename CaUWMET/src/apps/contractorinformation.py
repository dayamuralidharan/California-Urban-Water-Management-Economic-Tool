import base64
import streamlit as st
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from src.globalUtilities import opt_echo

def app():

    with opt_echo():
        st.title('Contractor Information')
        st.write("")
        st.write("<Description of Hydrology Assumptions and Steps to use this page to be added.>")
        st.write("")

        @st.cache(suppress_st_warning=True)
        def fetch_data(path):
        #     if path:
        #         demands = pd.read_csv(path)
                
            # else:
            demands = pd.read_csv(path)
            return pd.DataFrame(demands)

        #Example controlers
        # st.sidebar.subheader("Data Filter options")

        # sample_size = st.sidebar.number_input("Rows", min_value=1, value=10)
        sample_size = 10

        # return_mode = st.sidebar.selectbox("Returned Grid Update Mode", list(DataReturnMode.__members__), index=1)
        return_mode_value = DataReturnMode.__members__["FILTERED"]

        # update_mode = st.sidebar.selectbox("Chart Update Mode", list(GridUpdateMode.__members__), index=6)
        update_mode_value = GridUpdateMode.__members__["COLUMN_RESIZED"]

        #enterprise modules
        # enable_enterprise_modules = st.sidebar.checkbox("Enable Enterprise Modules")
        # if enable_enterprise_modules:
        #     enable_sidebar =st.sidebar.checkbox("Enable grid sidebar", value=False)
        # else:
        #     enable_sidebar = False

        #features
        # fit_columns_on_grid_load = st.sidebar.checkbox("Fit Grid Columns on Load")

        # enable_selection=st.sidebar.checkbox("Enable row selection", value=True)
        # if enable_selection:
        #     st.sidebar.subheader("Selection options")
        #     selection_mode = st.sidebar.radio("Selection Mode", ['single','multiple'])

        #     use_checkbox = st.sidebar.checkbox("Use check box for selection")
        #     if use_checkbox:
        #         groupSelectsChildren = st.sidebar.checkbox("From all elements", value=True)
        #         groupSelectsFiltered = st.sidebar.checkbox("From filtered elements", value=True)

        #     if ((selection_mode == 'multiple') & (not use_checkbox)):
        #         rowMultiSelectWithClick = st.sidebar.checkbox("Multiselect with click (instead of holding CTRL)", value=False)
        #         if not rowMultiSelectWithClick:
        #             suppressRowDeselection = st.sidebar.checkbox("Suppress deselection (while holding CTRL)", value=False)
        #         else:
        #             suppressRowDeselection=False
        #     st.sidebar.text("___")

        # enable_pagination = st.sidebar.checkbox("Enable pagination", value=False)
        # if enable_pagination:
        #     st.sidebar.subheader("Pagination options")
        #     paginationAutoSize = st.sidebar.checkbox("Auto pagination size", value=True)
        #     if not paginationAutoSize:
        #         paginationPageSize = st.sidebar.number_input("Page size", value=5, min_value=0, max_value=sample_size)
        #     st.sidebar.text("___")

        df1 = fetch_data("src/inputData/contractorInput_contractorAssumptions.csv")
        df2 = fetch_data("src/inputData/contractorInput_hydrologyAssumptions.csv")

    #Infer basic colDefs from dataframe types
        gb1 = GridOptionsBuilder.from_dataframe(df1)
        gb2 = GridOptionsBuilder.from_dataframe(df2)

        #customize gridOptions
        gb1.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        gb2.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

        # if enable_selection:
        #     gb.configure_selection(selection_mode)
        #     if use_checkbox:
        #         gb.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=groupSelectsChildren, groupSelectsFiltered=groupSelectsFiltered)
        #     if ((selection_mode == 'multiple') & (not use_checkbox)):
        #         gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=rowMultiSelectWithClick, suppressRowDeselection=suppressRowDeselection)

        # if enable_pagination:
        #     if paginationAutoSize:
        #         gb.configure_pagination(paginationAutoPageSize=True)
        #     else:
        #         gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

        gb1.configure_grid_options(domLayout='normal')
        gridOptions1 = gb1.build()
        gridOptions2 = gb2.build()

        #Display the grid
        grid_response = AgGrid(
            df1, 
            key="1",
            gridOptions=gridOptions1,
            width='100%',
            data_return_mode=return_mode_value, 
            update_mode=update_mode_value,
            # fit_columns_on_grid_load=fit_columns_on_grid_load,
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            # enable_enterprise_modules=enable_enterprise_modules,
            )

        #downloading the dataframe data to a .csv file
        def download_link(object_to_download, download_filename, download_link_text):

            if isinstance(object_to_download,pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=False)
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(object_to_download.encode()).decode()
            return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
        
        if st.button('Download Dataframe to CSV format', key = "2"):
            tmp_download_link = download_link(df1, 'YOUR_DF.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)
        
        grid_response2 = AgGrid(
            df2, 
            key="3",
            gridOptions=gridOptions2,
            width='100%',
            data_return_mode=return_mode_value, 
            update_mode=update_mode_value,
            # fit_columns_on_grid_load=fit_columns_on_grid_load,
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            # enable_enterprise_modules=enable_enterprise_modules,
            )     
        if st.button('Download Dataframe to CSV format', key = "4"):
            tmp_download_link = download_link(df2, 'YOUR_DF.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)
        
        selected = grid_response['selected_rows']
        selected_df = pd.DataFrame(selected)