import streamlit as st
import pandas as pd 
import numpy as np
from load_css import local_css
from appsUtilities import opt_echo, fetch_data
from demandsHelper import load_data, summary_poster
from editableTable import editableTable

def setTotalDemandsInputData():
    if st.session_state.totalDemandsChoice == 'UWMP reported values':
        st.session_state.totalDemandScenarioRadioButtonIndex = 0
        st.session_state.totalDemandsdf = fetch_data("inputData/inputDemands_totalDemands.csv")
    elif st.session_state.totalDemandsChoice == 'ETAW adjusted demands':
        st.session_state.totalDemandScenarioRadioButtonIndex = 1
    else:
        st.session_state.totalDemandScenarioRadioButtonIndex = 2

#TODO Update plot input data in functions below
#TODO Fix use by sector to use by type
def setUseBySectorInputData():
    if st.session_state.useBySectorChoice == 'UWMP reported values':
        st.session_state.useBySectorPlotInputdf = load_data("inputData/useBySectorGraphData.csv")
        st.session_state.useBySectorRadioButtonIndex = 0
    else:
        st.session_state.useBySectorPlotInputdf = load_data("inputData/useBySectorGraphData.csv") ################################ Data needs updating
        st.session_state.useBySectorRadioButtonIndex = 1

def setIntExtUseBySectorInputData():
    if st.session_state.intExtUseBySectorChoice == 'UWMP reported values':
        st.session_state.intExtUseBySectorPlotInputdf = load_data("inputData/intAndExtUseBySectorGraphData.csv")
        st.session_state.intExtuseBySectorRadioButtonIndex = 0
    else:
        st.session_state.intExtUseBySectorPlotInputdf = load_data("inputData/intAndExtUseBySectorGraphData.csv") ################################ Data needs updating
        st.session_state.intExtUseBySectorRadioButtonIndex = 1

def setBaseLongTermConservationInputData():
    if st.session_state.baseLongTermConservationChoice == 'UWMP reported values':
        st.session_state.baseLongTermConservationRadioButtonIndex = 0
    else:
        st.session_state.baseLongTermConservationRadioButtonIndex = 1

# Functions used to set variables equal to user-defined values in the editable tables, also known as "grids"
def setTotalDemandsDataToUserInput(gridResponseData): 
    st.session_state.totalDemandsdf = gridResponseData

def setDemandsByUseTypeDataToUserInput(gridResponseData): 
    st.session_state.useBySectordf = gridResponseData

def setIntExtByUseTypeDataToUserInput(gridResponseData): 
    st.session_state.intExtUseBySectordf = gridResponseData

def setBaseLongtermConservationDataToUserInput(gridResponseData): 
    st.session_state.baseLongTermConservationdf = gridResponseData

def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)
        local_css("style.css")

        st.title('Demand Assumptions Page')
        st.header("Steps to use this page")


        st.write("""There are four categories of variables that need to be set on this page including Total Demands, Total Water Use by Sector,
        Interior and Exterior use by sector, and Base Long-term Conservation. A description of each of variable is provided in the Demand Assumptions Overview section below.
        """)
        st. write("")
        st.write("""Select which datasets to use for each variable from the options below.
        After making your selection for all four variables, 
        review the data in the plots below.""")

        #---------------------------------------------------------------#
        # RADIO BUTTONS TO SELECT DATASETS
        #---------------------------------------------------------------# 

        # Radio buttons to select data source for each variable
        demandsDatasetOptions = ['UWMP reported values', 'ETAW adjusted demands', 'Input demands in table below']
        st.radio("""1. Select the Total Demand Scenario Dataset from the options below. If the last option is selected, 
        update the data in the Total Demand Scenarios table in the first collapsible section below.""", options = demandsDatasetOptions, index = st.session_state.totalDemandScenarioRadioButtonIndex, key = "totalDemandsChoice", on_change = setTotalDemandsInputData)

        useBySectorDatasetOptions = ['UWMP reported values', 'Input Use By Sector in table below']
        useBySectorDatasetChoice = st.radio("2. Select the Use by Sector Dataset from the options below. If the last option is selected, update the data in the Demand Use by Sector table in the second collapsible section below.", options = useBySectorDatasetOptions, index = st.session_state.useBySectorRadioButtonIndex, key = "useBySectorChoice", on_change = setUseBySectorInputData)

        intExtUseBySectorDatasetOptions = ['UWMP reported values', 'Input Use By Sector in table below']
        intExtUseBySectorDatasetChoice = st.radio("""3. Select the Input Interior and Exterior Use by Sector Dataset from the options below. 
        If the last option is selected, update the data in the Interior and Exterior Use by Sector table in the third collapsible section below.""", options = intExtUseBySectorDatasetOptions, index = st.session_state.intExtUseBySectorRadioButtonIndex, key = "intExtUseBySectorChoice", on_change = setIntExtUseBySectorInputData)

        baseLongTermConservationDatasetOptions = ['UWMP reported values', 'Input Conservation variables in table below']
        intExtUseBySectorDatasetChoice = st.radio("""4. Select the Base Long-Term Conservation Dataset from the options below. 
        If the last option is selected, update the data in the Base Long Term Conservation table in the last collapsible section below.""", options = baseLongTermConservationDatasetOptions, index = st.session_state.baseLongTermConservationRadioButtonIndex, key = "baseLongTermConservationChoice", on_change = setBaseLongTermConservationInputData)

        #---------------------------------------------------------------#
        # SUMMARY POSTER FOR TOTAL DEMANDS
        #---------------------------------------------------------------#  

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
        
     
        color_map_df = load_data("inputData/color_map_df_demands.csv")


        # Reformat total demands dataframe for plots
        demandsPlotInputData = st.session_state.inputDataTotalDemands[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
        #print(demandsPlotInputData)
        demandsPlotInputData = pd.melt(demandsPlotInputData, id_vars=['Variable','Contractor','Study Region'])
        demandsPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
        demandVars = [
            demandsPlotInputData['Type'] == 'Normal or Better Demands (acre-feet/year)',
            demandsPlotInputData['Type'] == 'Single Dry-Year Demands (acre-feet/year)',
            demandsPlotInputData['Type'] == 'Multiple Dry-Year Demands (acre-feet/year)',
         ]
        k_labelValues = [0, 1, 2]
        demandsPlotInputData['k_labels'] = np.select(demandVars, k_labelValues)
        colors = ['#F63366', '#2BB1BB', '#22466B']
        demandsPlotInputData['colors'] = np.select(demandVars, colors)

        sorted_contractors = demandsPlotInputData.groupby('Year')['Contractor'].sum()\
            .sort_values(ascending=True).index
        
        st.write(sorted_contractors)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### **Select Year Type:**")
            select_demands = []
            sorted_demands = demandsPlotInputData.groupby('Type')['Contractor'].count()\
                .sort_values(ascending=True).index

            select_demands.append(st.selectbox('', sorted_demands, key='2', help="Select hydrologic year type to display in plots below."))
            demands_df = demandsPlotInputData[demandsPlotInputData['Type'].isin(select_demands)]
        
        #Setting up color palette dict
        color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))
        fig = summary_poster(demands_df, color_dict, "Demands by Study Region", "Demands by Contractor", "Demands (acre-feet/year)")
        st.write(fig)

        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER FOR TOTAL USE BY SECTOR
        #---------------------------------------------------------------#

        useBySectorPlotInputData = load_data("inputData/useBySectorGraphData.csv")
        
        sorted_useBySector = useBySectorPlotInputData.groupby('Year')['Contractor'].sum()\
            .sort_values().index

        st.subheader("Demands by Use Type")
        st.write("""Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
        demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
        Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
        uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
        air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
        Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
        street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
        Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### **Select Future Planning Year:**")
            select_useBySector = []
            select_useBySector.append(st.selectbox('', sorted_useBySector, key='3', help="explanation for tooltip to be added"))  
        
        with col2:
            st.markdown("#### **Select Sector:**")
            select_useBySector = []

            #Filter df based on selection
            useBySector_df = useBySectorPlotInputData[useBySectorPlotInputData['Year'].isin(select_useBySector)]

            sorted_useBySector = useBySector_df.groupby('Type')['Contractor'].count()\
                .sort_values().index

            select_useBySector.append(st.selectbox('', sorted_useBySector, key='4', help="explanation for tooltip to be added"))
            useBySector_df = useBySector_df[useBySector_df['Type'].isin(select_useBySector)]

        
        col1, col2 = st.columns(2)
        st.text("")
        fig_useBySector = summary_poster(useBySector_df, color_dict, "Use by Study Region", "Use by Contractor", "Use (acre-feet/year)")
        st.write(fig_useBySector)

        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER FOR INTERIOR AND EXTERIOR USE BY SECTOR
        #---------------------------------------------------------------#

        intExtUseBySectorPlotInputData = load_data("inputData/intAndExtUseBySectorGraphData.csv")
    
        sorted_contractors = intExtUseBySectorPlotInputData.groupby('Year')['Contractor'].sum()\
            .sort_values().index

        st.subheader("Interior and Exterior Use By Sector")
        st.write("""The model accounts for interior and exterior uses in discerning how conservation and rationing reductions are applie, as well as water available for reuse assumptions. 
        Various conservation programs target demand reductions specifically by sector and by interior versus exterior consumption. Rationing programs typically cut back interior 
        use at a lower rate than exterior use during shortage events. Adjustments in the use associated with conservation and rationing programs impact the amount of water available 
        for reuse and wastewater treatment costs. Interior use that results in water available for reuse includes urban wastewater that is deep percolated from septic tanks, while 
        exterior use includes irrigation infiltrated to groundwater systems. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### **Select Future Planning Year:**")
            select_contractor = []
            select_contractor.append(st.selectbox('', sorted_contractors, key='5', help="explanation for tooltip to be added"))  
        
        with col2:
            st.markdown("#### **Select Sector:**")
            select_demands = []

            #Filter df based on selection
            contractor_df = intExtUseBySectorPlotInputData[intExtUseBySectorPlotInputData['Year'].isin(select_contractor)]

            sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
                .sort_values(ascending=True).index

            select_demands.append(st.selectbox('', sorted_demands, key='6', help="explanation for tooltip to be added"))
            demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

        col1, col2 = st.columns(2)
        fig = summary_poster(demands_df, color_dict, "Use by Study Region", "Use by Contractor", "Use (acre-feet/year)")
        st.write(fig)

        #---------------------------------------------------------------#
        # CREATE SUMMARY POSTER FOR BASE LONG-TERM CONSERVATION
        #---------------------------------------------------------------#

        baseLongTermConservationPlotInputData = st.session_state.baseLongTermConservationdf.drop(labels = 'Notes', axis = 1)
        baseLongTermConservationPlotInputData = pd.melt(baseLongTermConservationPlotInputData, id_vars=['Variable','Contractor','Study Region'])
        baseLongTermConservationPlotInputData.rename(columns = {'Variable' : 'Type', 'variable': 'Year', 'value': 'Value'}, inplace=True)

        conservationVars = [
            baseLongTermConservationPlotInputData['Type'] == 'Base Long-term Conservation (acre-feet)',
            baseLongTermConservationPlotInputData['Type'] == 'Demand hardening adjustment factor (% of total long-term conservation including base and additional from Water Management Options)',
        ]

        k_labelValuesConservation = [0, 1]
        colorsConservation = ['#F63366', '#2BB1BB']

        baseLongTermConservationPlotInputData['k_labels'] = np.select(conservationVars, k_labelValuesConservation)
        baseLongTermConservationPlotInputData['colors'] = np.select(conservationVars, colorsConservation)
    
        sorted_contractors = baseLongTermConservationPlotInputData.groupby('Year')['Contractor'].sum()\
            .sort_values().index

        st.subheader("Base Long-Term Conservation")
        st.write("""Long-term conservation is incorporated into the model as it is an important component of each contractor's long-term strategy to increase 
        their water supply reliability. These demand reductions typically include programs that target water use efficiency in each sector, turf replacement programs, 
        conservation outreach and communications, reducing conveyance losses, and more. Long-term demand management measures that are adopted by water users can 
        have a demand hardening effect. Although they can increase reliability by reducing the size, frequency and duration of shortage events, they can make these 
        events relatively more costly when they do occur.  A hardening factor can be set to simulate this effect.>""")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### **Select Future Planning Year:**")
            select_contractor = []
            select_contractor.append(st.selectbox('', sorted_contractors, key='7', help="Select year to display in plots."))  
        
        with col2:
            st.markdown("#### **Select Conservation Variable:**")
            select_demands = []

            #Filter df based on selection
            contractor_df = baseLongTermConservationPlotInputData[baseLongTermConservationPlotInputData['Year'].isin(select_contractor)]

            sorted_demands = contractor_df.groupby('Type')['Contractor'].count()\
                .sort_values(ascending=True).index

            select_demands.append(st.selectbox('', sorted_demands, key='8', help="Select variable to display in plots."))
            demands_df = contractor_df[contractor_df['Type'].isin(select_demands)]

        col1, col2 = st.columns(2)
        fig = summary_poster(demands_df, color_dict, "Conservation by Study Region", "Conservation by Contractor", "Conservation (acre-feet/year)")
        st.write(fig)


        #---------------------------------------------------------------#
        # COLLAPSIBLE SECTIONS WTIH EDITABLE TABLES
        #---------------------------------------------------------------#

        #### TABLE 1 - TOTAL DEMAND SCENARIOS
        
        if st.session_state.totalDemandScenarioRadioButtonIndex == 2:
            editableTable(st.session_state.inputDataTotalDemands, st.session_state.futurePlanningYear, setTotalDemandsDataToUserInput, "Total Demand Scenarios", "Water Demand (acre-feet/year)")


        ####  TABLE 2 DEMANDS BY USE TYPE
        if st.session_state.useBySectorRadioButtonIndex == 1:
            editableTable(st.session_state.inputDataDemandByUseType, st.session_state.futurePlanningYear, setDemandsByUseTypeDataToUserInput, "Demands by Use Type", "Demand by Use Type (acre-feet/year)")

#TODO Plot in collapsible section should average, not sum
        ####  TABLE 3 INTERIOR AND EXTERIOR BY USE TYPE 
        if st.session_state.intExtUseBySectorRadioButtonIndex == 1:
            editableTable(st.session_state.inputDataIntExtDemandsByUseType, st.session_state.futurePlanningYear, setIntExtByUseTypeDataToUserInput, "Interior and Exterior Demands by Use Type", "Interior and Exterior Demands by Use Type (% of Demand by Use Type)")

        ####  TABLE 4 BASE LONG-TERM CONSERVATION 
        if st.session_state.baseLongTermConservationRadioButtonIndex == 1:
            editableTable(st.session_state.inputDataBaseLongTermConservation, st.session_state.futurePlanningYear, setBaseLongtermConservationDataToUserInput, "Base Long-term Conservation", "Base Long-term Conservation (acre-feet/year)")