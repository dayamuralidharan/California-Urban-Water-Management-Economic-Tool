import base64
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
from sklearn import datasets
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import traceback
from load_css import local_css
from demandsHelper import load_data, summary_poster
from contextlib import contextmanager
import sys, os
from streamlit.hashing import _CodeHasher
# from streamlit.report_thread import get_repo
from DemandsUiState import DemandsUiState
from appsUtilities import opt_echo

def app():

# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():
        # Initialize Session State for this page
        demandsUiState = DemandsUiState()

        #Set font styling (currently used for green text)
        local_css("style.css")

        st.title('Demand Assumptions Page')
        st.header("Steps to use this page")


        st.write("There are three variables that need to be set on this page in the steps below. After making your selection for all three variables, review the input data by ensure this page's test pass and checking the data in the plots below.")
        
        #demandsDatasetChoice = st.checkbox('Use UWMP reported demand scenarios for all hydrologic year types (default)', value = demandsUiState.getDefaultDemandsDatasetChoice)
        demandsDatasetChoice = st.radio("1. Select the Total Demand Scenario Dataset from the options below. If the last option is selected, update the data in the Total Demand Scenarios table in the first collapsible section below.", ('UWMP reported values', 'ETAW adjusted demands', 'Input demands in table below'))
        demandsUiState.setDemandsDatasetChoice(demandsDatasetChoice)

        useBySectorDatasetChoice = st.radio("2. Select the Use by Sector Dataset from the options below. If the last option is selected, update the data in the Demand Use by Sector table in the second collapsible section below.", ('UWMP reported values', 'Input Use By Sector in table below'))
        demandsUiState.setUseBySectorDatasetChoice(useBySectorDatasetChoice)

        intExtUseBySectorDatasetChoice = st.radio("""3. Select the Input Interior and Exterior Use by Sector Dataset from the options below. 
        If the last option is selected, update the data in the Interior and Exterior Use by Sector table in the third collapsible section below.""", 
        ('UWMP reported values', 'Input Use By Sector in table below'))
        demandsUiState.setIntExtUseBySectorDatasetChoice(intExtUseBySectorDatasetChoice)

        
        st.write("4. Confirm there are no errors in the input data by checking the message below:")
        st.write("<span class='font'> ✔ Tests on this page pass! (or error message if it does not pass indicating what the error is) </span>", unsafe_allow_html=True)
        


        st.header("Demand Assumptions Overview")
  
        stats_df = load_data("inputData/totalDemandsGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_demands.csv")

        sorted_contractors = stats_df.groupby('Year')['Contractor'].sum()\
            .sort_values(ascending=True).index

        st.subheader("Total Demand Scenarios")
        st.write("""Total demands include all wholesale and retail, and all interior and exterior demands for all sectors including residential, industrial, commercial and governmental, 
        agricultural and large landscape for each contractor, and each future planning year.
        Generally, to estimate future demands, statistical methods are applied based on historical demand patterns related to household income, consumer response to the price of water and 
        weather along with future demographic and economic projections. Single dry-year demands incorporate a demand response to high temperature and low rainfall weather parameters experienced 
        for a single year, and multiple dry-year demands incorporate consumption response to extended drought conditions. These total demands exclude any conservation reduction assumptions. 
        Conservation is incorporated in the model through the assumptions included in the Demand Management page.
        Users can select to use Normal or Better Year demands adjusted by an ETAW adjustment factor derived from CalSIMETAW, rather than using the Urban Water Management Plan's Single and Multiple Dry-Year Demands. 
        More information can be found in the model documentation <add hyperlink to Total Demand Scenarios section of model documentation.>""")

        col1, col2 = st.beta_columns(2)
        with col1:
            st.markdown("#### **Select Future Planning Year:**")
            select_contractor = []
            select_contractor.append(st.selectbox('', sorted_contractors, key=1))  
        
        with col2:
            st.markdown("#### **Select Year Type:**")
            select_demands = []

            #Filter df based on selection
            contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

            sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
                .sort_values(ascending=True).index

            select_demands.append(st.selectbox('', sorted_demands, key=2))
            demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

            major_cluster = demands_df.groupby('Study Region')['Type'].count()\
                .sort_values(ascending=True).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2 = st.beta_columns(2)

        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        stats_df = load_data("inputData/useBySectorGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_demands.csv")

    
        sorted_contractors = stats_df.groupby('Year')['Contractor'].sum()\
            .sort_values().index

        st.subheader("Demand Scenario by Sector")
        st.write("""Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
        demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
        Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
        uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
        air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
        Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
        street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
        Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")
        
        col1, col2 = st.beta_columns(2)
        with col1:
            st.markdown("#### **Select Future Planning Year:**")
            select_contractor = []
            select_contractor.append(st.selectbox('', sorted_contractors, key=3))  
        
        with col2:
            st.markdown("#### **Select Sector:**")
            select_demands = []

            #Filter df based on selection
            contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

            sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
                .sort_values().index

            select_demands.append(st.selectbox('', sorted_demands, key=4))
            demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

            major_cluster = demands_df.groupby('Study Region')['Type'].count()\
                .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2 = st.beta_columns(2)

        st.text("")
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        stats_df = load_data("inputData/intAndExtUseBySectorGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_demands.csv")

        # st.write(stats_df)
    
        sorted_contractors = stats_df.groupby('Year')['Contractor'].sum()\
            .sort_values().index

        st.subheader("Interior and Exterior Use By Sector")
        st.write("""The model accounts for interior and exterior uses in discerning how conservation and rationing reductions are applie, as well as water available for reuse assumptions. 
        Various conservation programs target demand reductions specifically by sector and by interior versus exterior consumption. Rationing programs typically cut back interior 
        use at a lower rate than exterior use during shortage events. Adjustments in the use associated with conservation and rationing programs impact the amount of water available 
        for reuse and wastewater treatment costs. Interior use that results in water available for reuse includes urban wastewater that is deep percolated from septic tanks, while 
        exterior use includes irrigation infiltrated to groundwater systems. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")

        col1, col2 = st.beta_columns(2)
        with col1:
            st.markdown("#### **Select Future Planning Year:**")
            select_contractor = []
            select_contractor.append(st.selectbox('', sorted_contractors, key=5))  
        
        with col2:
            st.markdown("#### **Select Sector:**")
            select_demands = []

            #Filter df based on selection
            contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

            sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
                .sort_values(ascending=True).index

            select_demands.append(st.selectbox('', sorted_demands, key=6))
            demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

            major_cluster = demands_df.groupby('Study Region')['Type'].count()\
                .sort_values(ascending=False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2 = st.beta_columns(2)

        #---------------------------------------------------------------#
        # COLLAPSIBLE SECTIONS WTIH EDITABLE TABLES
        #---------------------------------------------------------------#
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        #Table 1 - Total Demand Scenario
        with st.beta_expander("Total Demand Scenarios (default values as reported by 2020 UWMPs)"):


            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
            #     if path:
            #         demands = pd.read_csv(path)
                    
                # else:
                demands = pd.read_csv("inputData/totalDemands.csv")
                return pd.DataFrame(demands)

            #Example controllers
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

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
            gb.configure_column("Notes", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')

            #configures last row to use custom styles based on cell's value, injecting JsCode on components front end
            # cellsytle_jscode = JsCode("""
            # function(params) {
            #     if (params.value == 'Normal') {
            #         return {
            #             'color': 'white',
            #             'backgroundColor': 'darkred'
            #         }
            #     } else {
            #         return {
            #             'color': 'black',
            #             'backgroundColor': 'white'
            #         }
            #     }
            # };
            # """)
            # gb.configure_column("", cellStyle=cellsytle_jscode)

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
                # height=grid_height, 
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

                # object_to_download (str, pd.DataFrame):  The object to be downloaded.
                # download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
                # download_link_text (str): Text to display for download link.

                if isinstance(object_to_download,pd.DataFrame):
                    object_to_download = object_to_download.to_csv(index=False)
                # some strings <-> bytes conversions necessary here
                b64 = base64.b64encode(object_to_download.encode()).decode()
                return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
                
            if st.button('Download Dataframe to CSV format', key = "6"):
                tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the bar chart
                chart_data = df.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

                if not selected_df.empty:
                    selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
                    chart_data = pd.concat([chart_data, selected_data])


                chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand (acre-feet/year)")

                #st.dataframe(chart_data)
                chart = alt.Chart(data=chart_data).mark_bar().encode(
                    x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("sum(Water Demand (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

            st.markdown("""
            Users can select multiple agencies from the table above to highlight in the chart below:
            """)

            st.altair_chart(chart, use_container_width=True)

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            # st.subheader("Returned grid data:")
            # st.dataframe(grid_response['data'])

            # sum2025 = int(df["2025"].sum())
            # st.write("The total demand in 2025 will be:", sum2025)

            #s = st.text_input('Enter text here')
            #st.write(s)
            #if st.button('Download input as a text file'):
            #   tmp_download_link = download_link(s, 'YOUR_INPUT.txt', 'Click here to download your text!')
            #   st.markdown(tmp_download_link, unsafe_allow_html=True)

        #Table 2
        with st.beta_expander("Demand Scenarios By Sector"):
            
            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/useBySector.csv")
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
            gb.configure_column("Notes", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')

            gb.configure_grid_options(domLayout='normal')
            gridOptions = gb.build()

            #Display the grid
            grid_response = AgGrid(
                df, 
                gridOptions=gridOptions,
                # height=grid_height, 
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

            if st.button('Download Dataframe to CSV format', key = "7"):
                tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = df.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

                if not selected_df.empty:
                    selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
                    chart_data = pd.concat([chart_data, selected_data])

                chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand (acre-feet/year)")
                
                #st.dataframe(chart_data)
                chart = alt.Chart(data=chart_data).mark_bar().encode(
                    x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("sum(Water Demand(acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

            st.markdown("""
            Users can select multiple agencies from the table above to highlight in the chart below:
            """)

            st.altair_chart(chart, use_container_width=True)

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            # st.subheader("Returned grid data:")
            # st.dataframe(grid_response['data'])

        #Table 3
        with st.beta_expander("Interior and Exterior Use by Sector"):

            # path = st.text_input('CSV File Path', key = "3")

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/intAndExtUseBySector.csv")
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
            gb.configure_column("Notes", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')

            gb.configure_grid_options(domLayout='normal')
            gridOptions = gb.build()

            #Display the grid
            grid_response = AgGrid(
                df, 
                gridOptions=gridOptions,
                # height=grid_height, 
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

            if st.button('Download Dataframe to CSV format', key = "8"):
                tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = df.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

                if not selected_df.empty:
                    selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
                    chart_data = pd.concat([chart_data, selected_data])

                chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand (acre-feet/year)")
                
                #st.dataframe(chart_data)
                chart = alt.Chart(data=chart_data).mark_bar().encode(
                    x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("sum(Water Demand (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

                st.markdown("""
                Users can select multiple agencies from the table above to highlight in the chart below:
                """)

                st.altair_chart(chart, use_container_width=True)

                df = grid_response['data']
                selected = grid_response['selected_rows']
                selected_df = pd.DataFrame(selected)

                # st.subheader("Returned grid data:")
                # st.dataframe(grid_response['data'])
