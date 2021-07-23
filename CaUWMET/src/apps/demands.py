import base64
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import traceback
from load_css import local_css
from demandsHelper import load_data, summary_poster
from contextlib import contextmanager
import sys, os
from appsUtilities import opt_echo

def setTotalDemandsInputData():
    if st.session_state.totalDemandsChoice == 'UWMP reported values':
        st.session_state.totalDemandsdf = load_data("inputData/totalDemandsData.csv")
        st.session_state.demandsPlotInputdf = load_data("inputData/totalDemandsGraphData.csv")
    elif st.session_state.totalDemandsChoice == 'ETAW adjusted demands':
        st.session_state.totalDemandsdf = load_data("inputData/totalDemandsData.csv") ################################ Data needs updating
        st.session_state.demandsPlotInputdf = load_data("inputData/totalDemandsGraphData.csv") ################################ Data needs updating
    else:
        st.session_state.totalDemandsdf = load_data("inputData/totalDemandsData.csv") ################################ Data needs updating
        st.session_state.demandsPlotInputdf = load_data("inputData/totalDemandsGraphData.csv") ################################ Data needs updating


def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():
        # Initialize Session State with Default Values
        st.session_state['totalDemandsdf'] = load_data("inputData/totalDemandsData.csv")
        st.session_state['demandsPlotInputdf'] = load_data("inputData/totalDemandsGraphData.csv")

        #Set font styling (currently used for green text)
        local_css("style.css")

        st.title('Demand Assumptions Page')
        st.header("Steps to use this page")


        st.write("""There are three variables that need to be set on this page in the steps below including total demands, total water use by sector, and
        interior and exterior use by sector. More information on what each of these variables are is described in the Demand Assumptions Overview section below.
        Select which datasets to use for each variable from the options below.
        After making your selection for all three variables, 
        review the input data by ensure this page's test pass and checking the data in the plots below.""")


        
        demandsDatasetOptions = ['UWMP reported values', 'ETAW adjusted demands', 'Input demands in table below']
        demandsDatasetChoice = st.radio("""1. Select the Total Demand Scenario Dataset from the options below. If the last option is selected, 
        update the data in the Total Demand Scenarios table in the first collapsible section below.""", demandsDatasetOptions, key = "totalDemandsChoice", on_change = setTotalDemandsInputData)

        useBySectorDatasetOptions = ['UWMP reported values', 'Input Use By Sector in table below']
        useBySectorDatasetChoice = st.radio("2. Select the Use by Sector Dataset from the options below. If the last option is selected, update the data in the Demand Use by Sector table in the second collapsible section below.", useBySectorDatasetOptions)

        intExtUseBySectorDatasetOptions = ['UWMP reported values', 'Input Use By Sector in table below']
        intExtUseBySectorDatasetChoice = st.radio("""3. Select the Input Interior and Exterior Use by Sector Dataset from the options below. 
        If the last option is selected, update the data in the Interior and Exterior Use by Sector table in the third collapsible section below.""", intExtUseBySectorDatasetOptions)

        
        st.write("4. Confirm there are no errors in the input data by checking the message below:")
        st.write("<span class='font'> ✔ Tests on this page pass! (or error message if it does not pass indicating what the error is) </span>", unsafe_allow_html=True)


        st.header("Demand Assumptions Overview")

        st.subheader("Total Demand Scenarios")
        st.write("""Total demands include all wholesale and retail, and all interior and exterior demands for all sectors including residential, industrial, commercial and governmental, 
        agricultural and large landscape for each contractor, and each future planning year.
        Generally, to estimate future demands, statistical methods are applied based on historical demand patterns related to household income, consumer response to the price of water and 
        weather along with future demographic and economic projections. Single dry-year demands incorporate a demand response to high temperature and low rainfall weather parameters experienced 
        for a single year, and multiple dry-year demands incorporate consumption response to extended drought conditions. These total demands exclude any conservation reduction assumptions. 
        Conservation is incorporated in the model through the assumptions included in the Demand Management page.
        Users can select to use Normal or Better Year demands adjusted by an ETAW adjustment factor derived from CalSIMETAW, rather than using the Urban Water Management Plan's Single and Multiple Dry-Year Demands. 
        More information can be found in the model documentation <add hyperlink to Total Demand Scenarios section of model documentation.>""")
        
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER FOR TOTAL DEMANDS
        #---------------------------------------------------------------#       
        

        demandsPlotInputData = st.session_state.demandsPlotInputdf
        color_map_df = load_data("inputData/color_map_df_demands.csv")

        sorted_contractors = demandsPlotInputData.groupby('Year')['Contractor'].sum()\
            .sort_values(ascending=True).index

        col1, col2 = st.beta_columns(2)
        with col1:
            st.markdown("#### **Select Future Planning Year:**")
            select_contractor = []
            select_contractor.append(st.selectbox('', sorted_contractors, key='1'))  
        
        with col2:
            st.markdown("#### **Select Year Type:**")
            select_demands = []

            #Filter df based on selection
            contractor_df = demandsPlotInputData[demandsPlotInputData['Year'].isin(select_contractor)]

            sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
                .sort_values(ascending=True).index

            select_demands.append(st.selectbox('', sorted_demands, key='2'))
            demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]
        
        col1, col2 = st.beta_columns(2)

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER FOR TOTAL USE BY SECTOR
        #---------------------------------------------------------------#

        useBySectorPlotInputData = load_data("inputData/useBySectorGraphData.csv")
        
        sorted_contractors = useBySectorPlotInputData.groupby('Year')['Contractor'].sum()\
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
            select_contractor.append(st.selectbox('', sorted_contractors, key='3'))  
        
        with col2:
            st.markdown("#### **Select Sector:**")
            select_demands = []

            #Filter df based on selection
            contractor_df = useBySectorPlotInputData[useBySectorPlotInputData['Year'].isin(select_contractor)]

            sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
                .sort_values().index

            select_demands.append(st.selectbox('', sorted_demands, key='4'))
            demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

        
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER FOR INTERIOR AND EXTERIOR USE BY SECTOR
        #---------------------------------------------------------------#
        col1, col2 = st.beta_columns(2)
        st.text("")
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        intExtUseBySectorPlotInputData = load_data("inputData/intAndExtUseBySectorGraphData.csv")
    
        sorted_contractors = intExtUseBySectorPlotInputData.groupby('Year')['Contractor'].sum()\
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
            select_contractor.append(st.selectbox('', sorted_contractors, key='5'))  
        
        with col2:
            st.markdown("#### **Select Sector:**")
            select_demands = []

            #Filter df based on selection
            contractor_df = intExtUseBySectorPlotInputData[intExtUseBySectorPlotInputData['Year'].isin(select_contractor)]

            sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
                .sort_values(ascending=True).index

            select_demands.append(st.selectbox('', sorted_demands, key='6'))
            demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]


        #---------------------------------------------------------------#
        # COLLAPSIBLE SECTIONS WTIH EDITABLE TABLES
        #---------------------------------------------------------------#
        col1, col2 = st.beta_columns(2)
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        ########################### TABLE 1 - TOTAL DEMAND SCENARIOS
        with st.beta_expander("Total Demand Scenarios (default values as reported by 2020 UWMPs)"):
            demandsEditableTabledf = st.session_state.totalDemandsdf

            #Infer basic colDefs from dataframe types
            gb = GridOptionsBuilder.from_dataframe(demandsEditableTabledf)

            #customize gridOptions
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("Notes", type=["textColumn"])

            selection_mode = 'multiple'
            gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=False, suppressRowDeselection=False)

            gb.configure_grid_options(domLayout='normal')
            gridOptions = gb.build()

            #Display the grid
            return_mode = 'FILTERED'
            return_mode_value = DataReturnMode.__members__[return_mode]
            update_mode = 'MODEL_CHANGED'
            update_mode_value = GridUpdateMode.__members__[update_mode]

            grid_response = AgGrid(
                demandsEditableTabledf, 
                gridOptions=gridOptions,
                # height=grid_height, 
                width='100%',
                data_return_mode=return_mode_value, 
                update_mode=update_mode_value,
                # fit_columns_on_grid_load=fit_columns_on_grid_load,
                allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
                )
            
            demandsEditableTabledf = grid_response['data']
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
                
            if st.button('Download Dataframe to CSV format', key = "Total Demand Scenarios"):
                tmp_download_link = download_link(demandsEditableTabledf, 'Total_Demand_Scenarios.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the bar chart
                chart_data = demandsEditableTabledf.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

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


        ##########################  TABLE 2 USE BY SECTOR
        with st.beta_expander("Demand Scenarios By Sector"):
            
            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/useBySector.csv")
                return pd.DataFrame(demands)    
            sample_size = 10

            useBySectorEditableTable = fetch_data(sample_size)

            #Infer basic colDefs from dataframe types
            gb = GridOptionsBuilder.from_dataframe(useBySectorEditableTable)

            #customize gridOptions
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
            gb.configure_column("Notes", type=["textColumn"])

            gb.configure_grid_options(domLayout='normal')
            gridOptions = gb.build()

            #Display the grid
            grid_response = AgGrid(
                useBySectorEditableTable, 
                gridOptions=gridOptions,
                # height=grid_height, 
                width='100%',
                data_return_mode=return_mode_value, 
                update_mode=update_mode_value,
                # fit_columns_on_grid_load=fit_columns_on_grid_load,
                allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
                # enable_enterprise_modules=enable_enterprise_modules,
                )

            useBySectorEditableTable = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            if st.button('Download Dataframe to CSV format', key = "Use By Sector"):
                tmp_download_link = download_link(useBySectorEditableTable, 'Use_By_Sector.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = useBySectorEditableTable.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

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



        ########################### TABLE 3 INTERIOR AND EXTERIOR USE BY SECTOR
        with st.beta_expander("Interior and Exterior Use by Sector"):

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/intAndExtUseBySector.csv")
                return pd.DataFrame(demands)    

            intExtUsebySectorEditableTabledf = fetch_data(sample_size)

            #Infer basic colDefs from dataframe types
            gb = GridOptionsBuilder.from_dataframe(intExtUsebySectorEditableTabledf)

            #customize gridOptions
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

            gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='sum')
            gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='sum')
            gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='sum')
            gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='sum')
            gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='sum')
            gb.configure_column("Notes", type=["textColumn"])

            gb.configure_grid_options(domLayout='normal')
            gridOptions = gb.build()

            #Display the grid
            grid_response = AgGrid(
                intExtUsebySectorEditableTabledf, 
                gridOptions=gridOptions,
                # height=grid_height, 
                width='100%',
                data_return_mode=return_mode_value, 
                update_mode=update_mode_value,
                # fit_columns_on_grid_load=fit_columns_on_grid_load,
                allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
                # enable_enterprise_modules=enable_enterprise_modules,
                )

            intExtUsebySectorEditableTabledf = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            if st.button('Download Dataframe to CSV format', key = "Interior and Exterior Use By Sector"):
                tmp_download_link = download_link(intExtUsebySectorEditableTabledf, 'Interior_Exterior_Use_By_Sector.csv', 'Click here to download your data!')
                st.markdown(tmp_download_link, unsafe_allow_html=True)

            with st.spinner("Displaying results..."):
                #displays the chart
                chart_data = intExtUsebySectorEditableTabledf.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

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
                st.write(st.session_state)