import numpy as np
import streamlit as st
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import traceback
from suppliesHelper import load_data, summary_poster
import base64
import pandas as pd 
import altair as alt
from itertools import cycle
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from appsUtilities import opt_echo

def app():

    with opt_echo():
        st.title('Supply Assumptions')

        st.title('Summary')

        st.markdown("### **LOCAL-FIXED YIELD**")
        stats_df = load_data("inputData/contractorSuppliesGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_supplies.csv")

        sorted_contractors = stats_df.groupby('Year')['Contractor'].count()\
            .sort_values(ascending=True).index

        st.markdown("### **Select Future Planning Year:**")
        select_contractor = []

        select_contractor.append(st.selectbox('', sorted_contractors, key='1'))  

        #Filter df based on selection
        contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

        major_cluster = contractor_df.groupby('Study Region')['Type'].count()\
            .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2 = st.beta_columns(2)

        st.text("")
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(contractor_df, color_dict)
        st.write(fig)

        st.markdown("### **CARRYOVER STORAGE**")

        stats_df = load_data("inputData/carryoverStorageGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_supplies.csv")

        sorted_contractors = stats_df.groupby('Year')['Contractor'].count()\
            .sort_values(ascending=True).index

        st.markdown("### **Select Future Planning Year:**")
        select_contractor = []

        select_contractor.append(st.selectbox('', sorted_contractors, key='2'))  

        #Filter df based on selection
        contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

        major_cluster = contractor_df.groupby('Study Region')['Type'].count()\
            .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2 = st.beta_columns(2)

        st.text("")
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(contractor_df, color_dict)
        st.write(fig)

        st.markdown("### **IMPORTED SUPPLIES**")

        stats_df = load_data("inputData/importedSuppliesGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_supplies.csv")

        sorted_contractors = stats_df.groupby('Year')['Contractor'].count()\
            .sort_values(ascending=True).index

        st.markdown("### **Select Future Planning Year:**")
        select_contractor = []

        select_contractor.append(st.selectbox('', sorted_contractors, key='3'))  

        #Filter df based on selection
        contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

        major_cluster = contractor_df.groupby('Study Region')['Type'].count()\
            .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2 = st.beta_columns(2)

        st.text("")
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(contractor_df, color_dict)
        st.write(fig)

        st.markdown("### **REUSE**")
        stats_df = load_data("inputData/reuseGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_supplies.csv")

        sorted_contractors = stats_df.groupby('Year')['Contractor'].count()\
            .sort_values(ascending=True).index

        st.markdown("### **Select Future Planning Year:**")
        select_contractor = []

        select_contractor.append(st.selectbox('', sorted_contractors, key='4'))  

        #Filter df based on selection
        contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

        major_cluster = contractor_df.groupby('Study Region')['Type'].count()\
            .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2 = st.beta_columns(2)

        st.text("")
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(contractor_df, color_dict)
        st.write(fig)

        st.markdown("### **WATER MARKET TRANSFERS**")

        stats_df = load_data("inputData/waterMarketTransfersGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_supplies.csv")

        sorted_contractors = stats_df.groupby('Year')['Contractor'].count()\
            .sort_values(ascending=True).index

        st.markdown("### **Select Future Planning Year:**")
        select_contractor = []

        select_contractor.append(st.selectbox('', sorted_contractors, key='5'))  

        #Filter df based on selection
        contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

        major_cluster = contractor_df.groupby('Study Region')['Type'].count()\
            .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2 = st.beta_columns(2)

        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(contractor_df, color_dict)
        st.write(fig)

        #Table 1
        with st.beta_expander("Local-Fixed Yield"):
            st.title('Local-Fixed Yield')

            st.write("")

            # path = st.text_input('CSV File Path', key = "1")

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
            #     if path:
            #         demands = pd.read_csv(path)
                    
                # else:
                demands = pd.read_csv("inputData/localFixedYield.csv")
                return pd.DataFrame(demands)

            #Example controlers
            st.sidebar.subheader("Data Filter options")

            sample_size = st.sidebar.number_input("Rows", min_value=1, value=10)

            return_mode = st.sidebar.selectbox("Returned Grid Update Mode", list(DataReturnMode.__members__), index=1)
            return_mode_value = DataReturnMode.__members__[return_mode]

            update_mode = st.sidebar.selectbox("Chart Update Mode", list(GridUpdateMode.__members__), index=6)
            update_mode_value = GridUpdateMode.__members__[update_mode]

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

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')

            #configures last row to use custom styles based on cell's value, injecting JsCode on components front end
            cellsytle_jscode = JsCode("""
            function(params) {
                if (params.value == 'Normal') {
                    return {
                        'color': 'white',
                        'backgroundColor': 'darkred'
                    }
                } else {
                    return {
                        'color': 'black',
                        'backgroundColor': 'white'
                    }
                }
            };
            """)
            gb.configure_column("Normal or Better Demands (acre-feet)", cellStyle=cellsytle_jscode)

            # if enable_sidebar:
            #     gb.configure_side_bar()

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
                # Generates a link to download the given object_to_download.

                if isinstance(object_to_download,pd.DataFrame):
                    object_to_download = object_to_download.to_csv(index=False)

                b64 = base64.b64encode(object_to_download.encode()).decode()
                return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
                
            if st.button('Download Dataframe as CSV', key = "Local Supplies"):
                tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = df.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

                if not selected_df.empty:
                    selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
                    chart_data = pd.concat([chart_data, selected_data])

                chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand")

                #st.dataframe(chart_data)
                chart = alt.Chart(data=chart_data).mark_bar().encode(
                    x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("sum(Water Supply (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

                st.header("Local-Fixed Yield")
                st.markdown("""
                The chart depicts total or selected Local-Fixed Yield
                """)

                st.altair_chart(chart, use_container_width=True)

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            # st.subheader("Returned grid data:")
            # st.dataframe(grid_response['data'])

        #Table 2
        with st.beta_expander("Carryover Storage (including surface and groundwater storage)"):
            st.title('Carryover Storage (including surface and groundwater storage)')

            st.write("")
            

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/carryoverStorage.csv")
                return pd.DataFrame(demands)    

            df = fetch_data(sample_size)

            #Infer basic colDefs from dataframe types
            gb = GridOptionsBuilder.from_dataframe(df)

            #customize gridOptions
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')

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

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            if st.button('Download Dataframe as CSV', key = "Carryover Storage"):
                tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = df.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

                if not selected_df.empty:
                    selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
                    chart_data = pd.concat([chart_data, selected_data])

                chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand")
                
                #st.dataframe(chart_data)
                chart = alt.Chart(data=chart_data).mark_bar().encode(
                    x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("sum(Water Supply (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

                st.header("Carryover Storage (including surface and groundwater storage)")
                st.markdown("""
                The chart depicts selected and total Carryover Storage
                """)

                st.altair_chart(chart, use_container_width=True)

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            # st.subheader("Returned grid data:")
            # st.dataframe(grid_response['data'])

        #Table 3
        with st.beta_expander("Imported Supplies"):
            st.title('Imported Supplies')

            st.write("")

            # path = st.text_input('CSV File Path', key = "3")

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/importedSupplies.csv")
                return pd.DataFrame(demands)    

            df = fetch_data(sample_size)

            #Infer basic colDefs from dataframe types
            gb = GridOptionsBuilder.from_dataframe(df)

            #customize gridOptions
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')

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

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)
    
            if st.button('Download Dataframe as CSV', key = "Imported Supplies"):
                tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = df.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

                if not selected_df.empty:
                    selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
                    chart_data = pd.concat([chart_data, selected_data])

                chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand")
                
                #st.dataframe(chart_data)
                chart = alt.Chart(data=chart_data).mark_bar().encode(
                    x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("sum(Water Supply (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

                st.header("Imported Supplies")
                st.markdown("""
                The chart depicts total or selected Imported Supplies
                """)

                st.altair_chart(chart, use_container_width=True)

                df = grid_response['data']
                selected = grid_response['selected_rows']
                selected_df = pd.DataFrame(selected)

                # st.subheader("Returned grid data:")
                # st.dataframe(grid_response['data'])

        #Table 4
        with st.beta_expander("Reuse"):
            st.title('Reuse')

            st.write("")

            # path = st.text_input('CSV File Path', key = "3")

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/reuse.csv")
                return pd.DataFrame(demands)    

            df = fetch_data(sample_size)

            #Infer basic colDefs from dataframe types
            gb = GridOptionsBuilder.from_dataframe(df)

            #customize gridOptions
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')

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

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            if st.button('Download Dataframe as CSV', key = "Reuse"):
                tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = df.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

                if not selected_df.empty:
                    selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
                    chart_data = pd.concat([chart_data, selected_data])

                chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand")
                
                #st.dataframe(chart_data)
                chart = alt.Chart(data=chart_data).mark_bar().encode(
                    x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("sum(Water Supply (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

                st.header("Reuse")
                st.markdown("""
                The chart depicts total or selected Reuse
                """)

                st.altair_chart(chart, use_container_width=True)

                df = grid_response['data']
                selected = grid_response['selected_rows']
                selected_df = pd.DataFrame(selected)

                # st.subheader("Returned grid data:")
                # st.dataframe(grid_response['data'])

        #Table 5
        with st.beta_expander("Water Market Transfers"):
            st.title('Water Market Transfers')

            st.write("")

            # path = st.text_input('CSV File Path', key = "3")

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/waterMarketTransfers.csv")
                return pd.DataFrame(demands)    

            df = fetch_data(sample_size)

            #Infer basic colDefs from dataframe types
            gb = GridOptionsBuilder.from_dataframe(df)

            #customize gridOptions
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')

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

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            if st.button('Download Dataframe as CSV', key = "Water Market Transfers"):
                tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = df.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

                if not selected_df.empty:
                    selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
                    chart_data = pd.concat([chart_data, selected_data])

                chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand")
                
                #st.dataframe(chart_data)
                chart = alt.Chart(data=chart_data).mark_bar().encode(
                    x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("sum(Water Supply (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

                st.header("Water Market Transfers")
                st.markdown("""
                The chart depicts total or selected Water Market Transfers
                """)

                st.altair_chart(chart, use_container_width=True)

                df = grid_response['data']
                selected = grid_response['selected_rows']
                selected_df = pd.DataFrame(selected)