import streamlit as st
from load_css import local_css
from globalUtilities import opt_echo
from pageUtilities.editableTable import editableTable
from pageUtilities.selectData_Demands import setDemandDatasetsFromRadioButtons
from pageUtilities.summaryPlots_Demands import displaySummaryPlots

#TODO Plot in collapsible section should average, not sum (Nira)
#TODO Kensey and Nira to review the color_map_df in demandsHelper file. I don't really understand the labeling. Also, why are colors input here but also declared in line ~129?
#TODO See if we can get demandsHelper file into pageUtilities folder (Kensey)
#TODO Make green text again (Nira)
#TODO Make bar plots color code by region too (Nira)

# Functions used to set variables equal to user-defined values in the editable tables if user-defined data is selected over default, also known as "grids"
def setTotalDemandsDataToUserInput(gridResponseData): 
    st.session_state.totalDemandsdf = gridResponseData

def setDemandsByUseTypeDataToUserInput(gridResponseData): 
    st.session_state.useByTypedf = gridResponseData

def setIntExtByUseTypeDataToUserInput(gridResponseData): 
    st.session_state.intExtUseByTypedf = gridResponseData

def setBaseLongtermConservationDataToUserInput(gridResponseData): 
    st.session_state.baseLongTermConservationdf = gridResponseData


def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)
        local_css("style.css")

        st.title('Demand Assumptions Page')
        st.header("Steps to use this page")


        st.write("""There are four categories of variables that need to be set on this page including Total Demands, Total Water Use by Type,
        Interior and Exterior use by sector, and Base Long-term Conservation. A description of each of variable is provided in the Demand Assumptions Overview section below.
        """)
        st. write("")
        st.write("""Select which datasets to use for each variable from the options below.
        After making your selection for all four variables, 
        review the data in the plots below.""")

        #---------------------------------------------------------------#
        # RADIO BUTTONS TO SELECT DATASETS
        #---------------------------------------------------------------# 
        
        setDemandDatasetsFromRadioButtons()
        
        #---------------------------------------------------------------#
        # SUMMARY POSTER FOR TOTAL DEMANDS
        #---------------------------------------------------------------#  
        
        displaySummaryPlots()
        
        #---------------------------------------------------------------#
        # COLLAPSIBLE SECTIONS WTIH EDITABLE TABLES
        #---------------------------------------------------------------#
        
        #### TABLE 1 TOTAL DEMAND SCENARIOS
        if st.session_state.totalDemandScenarioRadioButtonIndex == 2:
            editableTable(st.session_state.inputDataTotalDemands, st.session_state.futurePlanningYear, setTotalDemandsDataToUserInput, "Total Demand Scenarios", "Water Demand (acre-feet/year)")
        
        ####  TABLE 2 DEMANDS BY USE TYPE
        if st.session_state.useByTypeRadioButtonIndex == 1:
            editableTable(st.session_state.inputDataDemandByUseType, st.session_state.futurePlanningYear, setDemandsByUseTypeDataToUserInput, "Demands by Use Type", "Demand by Use Type (acre-feet/year)")

        ####  TABLE 3 INTERIOR AND EXTERIOR BY USE TYPE 
        if st.session_state.intExtUseByTypeRadioButtonIndex == 1:
            editableTable(st.session_state.inputDataIntExtDemandsByUseType, st.session_state.futurePlanningYear, setIntExtByUseTypeDataToUserInput, "Interior and Exterior Demands by Use Type", "Interior and Exterior Demands by Use Type (% of Demand by Use Type)")

        ####  TABLE 4 BASE LONG-TERM CONSERVATION 
        if st.session_state.baseLongTermConservationRadioButtonIndex == 1:
            editableTable(st.session_state.inputDataBaseLongTermConservation, st.session_state.futurePlanningYear, setBaseLongtermConservationDataToUserInput, "Base Long-term Conservation", "Base Long-term Conservation (acre-feet/year)")
