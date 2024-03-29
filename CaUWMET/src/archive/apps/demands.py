import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo
from src.pageUtilities.editableTable import editableTable
from src.pageUtilities.selectData_Demands import setDemandDatasetsFromRadioButtons
from src.pageUtilities.summaryPlots_Demands import displaySummaryPlots
from src.load_css import local_css

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
        local_css("src/style.css")

        st.title('Demand Assumptions Page')
        st.header("Steps to use this page")


        st.write("<span class='font'>There are four categories of variables that need to be set on this page including:</span>", unsafe_allow_html=True) 
        st.write("<span class='font'>1) Total Demands Scenarios for Normal or Better, Single-Dry, and Multiple Dry year types.</span>", unsafe_allow_html=True)
        st.write("<span class='font'>2) Total Water Use by Type for Single-Family and Multi-Family Residential, Industrial, Commercial and Governmental, Agricultural, Large Landscape and Other use type categories.</span>", unsafe_allow_html=True)
        st.write("<span class='font'>3) Interior and Exterior Use by Type for each category listed above, and</span>", unsafe_allow_html=True)
        st.write("<span class='font'>4) Base Long-term Conservation</span>", unsafe_allow_html=True)
        st.write("<span class='font'>A detailed description of each of variable is provided in the Demand Assumptions Overview section below.</span>", unsafe_allow_html=True)
        st. write("")
        st.write("First, select which datasets to use for each variable from the options below. Each dataset has the option to use default data or input data through a table. If input through the table option is selected, please note the table is in a ""collapsable"" section at the very bottom of this page.")
        st.write("After making your selection for all variables, review the data in the plots below.")

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
            editableTable(st.session_state.totalDemandsdf, st.session_state.futurePlanningYear, setTotalDemandsDataToUserInput, "Total Demand Scenarios", "Water Demand (acre-feet/year)")
        
        ####  TABLE 2 DEMANDS BY USE TYPE
        if st.session_state.useByTypeRadioButtonIndex == 1:
            editableTable(st.session_state.useByTypedf, st.session_state.futurePlanningYear, setDemandsByUseTypeDataToUserInput, "Demands by Use Type", "Demand by Use Type (acre-feet/year)")

        ####  TABLE 3 INTERIOR AND EXTERIOR BY USE TYPE 
        if st.session_state.intExtUseByTypeRadioButtonIndex == 1:
            editableTable(st.session_state.intExtUseByTypedf, st.session_state.futurePlanningYear, setIntExtByUseTypeDataToUserInput, "Interior and Exterior Demands by Use Type", "Interior and Exterior Demands by Use Type (% of Demand by Use Type)")

        ####  TABLE 4 BASE LONG-TERM CONSERVATION 
        if st.session_state.baseLongTermConservationRadioButtonIndex == 1:
            editableTable(st.session_state.baseLongTermConservationdf, st.session_state.futurePlanningYear, setBaseLongtermConservationDataToUserInput, "Base Long-term Conservation", "Base Long-term Conservation (acre-feet/year)")
