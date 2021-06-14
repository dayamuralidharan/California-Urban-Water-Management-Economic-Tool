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
from demandsManagementHelper import load_data, summary_poster

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
        st.title('Demand Management Assumptions')

        st.title('Steps to use this page')

        st.write("<span class='font'> 1. Update Base Long-term Conservation Assumptions</span>", unsafe_allow_html=True)
        st.write('The base long-term conservation assumptions include base long-term cnservation volume, the demand hardening adjustment factor, and interior and exterior conservation effectiveness. The default values for the base long-term conservation volumes are as reported in the 2020 UWMP plans. The default values for the demand hardening adjustment factors, and exterior and interior conservation are based on <add reference>. More information can be found in the Model Documentation <add hyperlink to conservation section of model document>.')

        st.write("<span class='font'>2. Input Contingency Conservation Campaign Assumptions</span>", unsafe_allow_html=True)
        st.write("The contingency conservation campaign variables include the cost for the publicity campaign, population and the demand reduction assumed to be associated with the campaign. The default values below are based on <add reference>. More information can be found in the Model Documentation <add hyperlink to contingent conservation section of model document>.")

        st.write("<span class='font'>3. Input Rationing Program Assumptions</span>", unsafe_allow_html=True)
        st.write('Methods TBD. The default values below are as reported in <add reference>. More information can be found in the Model Documentation <add hyperlink to rationing section of model document>.')
        st.write('')

        st.write('All assumptions can be reviewed in the plots below and updated in the tables in the collapsible sections at the bottom of this page.')
        
        local_css("style.css")
        st.write("<span class='font'>✔ All tests pass! (or error message if it does not pass indicating what the error is) </span>", unsafe_allow_html=True)

        st.title('Demand Management Overview')

        stats_df = load_data("inputData/baseLongTermConservationGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_demandsManagement.csv")

        # st.write(stats_df)

        sorted_contractors = stats_df.groupby('Year')['Contractor'].sum()\
            .sort_values(ascending=True).index

        st.markdown("### **BASE LONG-TERM CONSERVATION**")
        st.write("""Long-term conservation is incorporated into the model as it is an important component of each contractor's long-term strategy to increase 
            their water supply reliability. These demand reductions typically include programs that target water use efficiency in each sector, turf replacement 
            programs, conservation outreach and communications, reducing conveyance losses, and more.
            Long-term demand management measures that are adopted by water users can have a demand hardening effect. Although they can increase reliability by 
            reducing the size, frequency and duration of shortage events, they can make these events relatively more costly when they do occur. A hardening factor can be set to simulate this effect. <TO ADD: description of conservation effectiveness variables.""")

        st.markdown("### **Select Future Planning Year:**")
        select_contractor = []
        select_contractor.append(st.selectbox('', sorted_contractors, key=1))  
        
        st.markdown("### **Select Base Long-Term Variable:**")
        select_demands = []

        #Filter df based on selection
        contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

        sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
            .sort_values(ascending=True).index

        select_demands.append(st.selectbox('', sorted_demands, key=2))
        demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

        major_cluster = demands_df.groupby('Study Region')['Type'].count()\
            .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2, col3 = st.beta_columns(3)

        st.text("")
        st.write("<TO ADD: Will update plot headers and labels to correspond to variable selected in drop down menu.>")
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        stats_df = load_data("inputData/contingencyConservationGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_demandsManagement.csv")

        # st.write(stats_df)
    
        sorted_contractors = stats_df.groupby('Year')['Contractor'].sum()\
            .sort_values(ascending=True).index

        st.markdown("### **CONTINGENCY CONSERVATION CAMPAIGNS**")
        st.write("""During times of drought, contractors may take further actions to manage shortages to minimize impacts to their region's economy 
            and quality of life. This may include actions such as extraordinary restrictions for specific consumer uses, such as alternate day water 
            regulations, water waster patrols, emergency water pricing programs, and intensive public education campaigns.
            The model assumes contingency conservation campaigns are initiated whenever there is a shortage in available water supplies compared to current
            quantity demanded or in response to low carryover storage availability. The model requires information on the cost for the publicity campaign per capita, population size, and assumed reduction associated with the campaign.""")

        st.markdown("### **Select Future Planning Year:**")
        select_contractor = []
        select_contractor.append(st.selectbox('', sorted_contractors, key=3))  
        
        st.markdown("### **Select Contingency Conservation Campaign Variable:**")
        select_demands = []

        #Filter df based on selection
        contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

        sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
            .sort_values(ascending=True).index

        select_demands.append(st.selectbox('', sorted_demands, key=4))
        demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

        major_cluster = demands_df.groupby('Study Region')['Type'].count()\
            .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2, col3 = st.beta_columns(3)

        st.text("")
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        stats_df = load_data("inputData/rationingProgramsGraphData.csv")
        color_map_df = load_data("inputData/color_map_df_demandsManagement.csv")

        # st.write(stats_df)

        sorted_contractors = stats_df.groupby('Year')['Contractor'].sum()\
            .sort_values(ascending=True).index

        st.markdown("### **RATIONING PROGRAMS**")
        st.write("During times of severe extended drought, contractors may take further actions to manage shortages through rationing programs. <Methods in development.>")

        st.markdown("### **Select Future Planning Year:**")
        select_contractor = []
        select_contractor.append(st.selectbox('', sorted_contractors, key=5))  
        
        st.markdown("### **Select Rationing Program Variable:**")
        select_demands = []

        #Filter df based on selection
        contractor_df = stats_df[stats_df['Year'].isin(select_contractor)]

        sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
            .sort_values(ascending=True).index

        select_demands.append(st.selectbox('', sorted_demands, key=6))
        demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

        major_cluster = demands_df.groupby('Study Region')['Type'].count()\
            .sort_values(ascending = False).index

        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))

        col1, col2, col3 = st.beta_columns(3)

        st.text("")
        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER
        #---------------------------------------------------------------#
        fig = summary_poster(demands_df, color_dict)
        st.write(fig)

        #Table 1
        with st.beta_expander("Base Long-term Conservation"):

            # path = st.text_input('CSV File Path', key = "1")

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
            #     if path:
            #         demands = pd.read_csv(path)
                    
                # else:
                demands = pd.read_csv("inputData/baseLongTermConservation.csv")
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

                if isinstance(object_to_download,pd.DataFrame):
                    object_to_download = object_to_download.to_csv(index=False)
                # some strings <-> bytes conversions necessary here
                b64 = base64.b64encode(object_to_download.encode()).decode()
                return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
                
            if st.button('Download Dataframe to CSV format', key = "6"):
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
                    x=alt.X("Year:O"),
                    y=alt.Y("sum(Water Conservation (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

                st.markdown("""
                Users can select multiple agencies from the table above to highlight in the chart below:
                """)

                st.altair_chart(chart, use_container_width=True)

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)


        #Table 2
        with st.beta_expander("Contingency Conservation Campaigns"):

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/contingencyConservation.csv")
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

            if st.button('Download Dataframe to CSV format', key = "10"):
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
                    x=alt.X("Year:O"),
                    y=alt.Y("sum(Water Conservation (acre-feet/year)):Q", stack=False),
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
        with st.beta_expander("Rationing Programs"):
            # path = st.text_input('CSV File Path', key = "5")

            @st.cache(suppress_st_warning=True)
            def fetch_data(samples):
                demands = pd.read_csv("inputData/rationingPrograms.csv")
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

            if st.button('Download Dataframe to CSV format', key = "11"):
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
                    x=alt.X("Year:O"),
                    y=alt.Y("sum(Water Conservation (acre-feet/year)):Q", stack=False),
                    color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
                )

                st.markdown("""
                Users can select multiple agencies from the table above to highlight in the chart below:
                """)

                st.altair_chart(chart, use_container_width=True)

            df = grid_response['data']
            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)