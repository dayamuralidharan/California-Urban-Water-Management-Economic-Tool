import streamlit as st
import streamlit as st
from load_css import local_css
from globalUtilities import opt_echo
from pageUtilities.editableTable import editableTable
from pageUtilities.selectData_SystemOperations import setSystemOperationsDatasetsFromRadioButtons
from pageUtilities.summaryPlots_SystemOperations import displaySummaryPlots

#TODO Plot in collapsible section should average, not sum (Nira)
#TODO Kensey and Nira to review the color_map_df in demandsHelper file. I don't really understand the labeling. Also, why are colors input here but also declared in line ~129?
#TODO See if we can get demandsHelper file into pageUtilities folder (Kensey)
#TODO Make green text again (Nira)
#TODO Make bar plots color code by region too (Nira) 

# Functions used to set variables equal to user-defined values in the editable tables if user-defined data is selected over default, also known as "grids"
def setExcessWaterSwitchDataToEditableTableInput(gridResponseData): 
    st.session_state.excessWaterSwitchdf = gridResponseData

def setCarryoverStorageDataToEditableTableInput(gridResponseData): 
    st.session_state.carryoverStoragedf = gridResponseData

def setCarryoverStorageCostsDataToEditableTableInput(gridResponseData): 
    st.session_state.carryoverStorageCostdf = gridResponseData

def setTransfersDataToEditableTableInput(gridResponseData): 
    st.session_state.transfersdf = gridResponseData

def setTransfersCostPriorityDataToEditableTableInput(gridResponseData): 
    st.session_state.transfersCostdf = gridResponseData

def app():
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)
        local_css("style.css")

        st.title('System Operation Assumptions Page')
        st.header("Steps to use this page")

        st.write("<span class='font'>There are five categories of assumptions to set on this page including:</span>", unsafe_allow_html=True) 
        st.write("<span class='font'>1)	A switch to indicate where to send excess supplies</span>", unsafe_allow_html=True)
        st.write("<span class='font'>2)	Surface and groundwater carryover storage constraints</span>", unsafe_allow_html=True)
        st.write("<span class='font'>3)	Carryover storage costs</span>", unsafe_allow_html=True)
        st.write("<span class='font'>4)	Transfer constraints, and</span>", unsafe_allow_html=True)
        st.write("<span class='font'>5)	Transfer costs</span>", unsafe_allow_html=True)
        st.write("<span class='font'>A detailed description of each variable is provided in the System Operations Assumptions Overview section below.</span>", unsafe_allow_html=True)
        st. write("")
        st.write("First, select which datasets to use for each variable from the options below. Each dataset has the option to use default data or input data through a table. If input through the table option is selected, please note the table is in a ""collapsible"" section at the very bottom of this page.")
        st.write("After making your selection for all variables, review the data in the plots below.")

        #---------------------------------------------------------------#
        # RADIO BUTTONS TO SELECT DATASETS
        #---------------------------------------------------------------# 
        
        setSystemOperationsDatasetsFromRadioButtons()
        
        #---------------------------------------------------------------#
        # SUMMARY POSTER FOR TOTAL DEMANDS
        #---------------------------------------------------------------#  
        
        displaySummaryPlots()
        
        #---------------------------------------------------------------#
        # COLLAPSIBLE SECTIONS WTIH EDITABLE TABLES
        #---------------------------------------------------------------#
       
        ####  TABLE 1 EXCESS WATER SWITCH
        if st.session_state.excessWaterSwitchRadioButtonIndex == 1:
            editableTable(st.session_state.excessWaterSwitchdf, st.session_state.futurePlanningYear, setExcessWaterSwitchInputData, "Excess Water Switch System Operations", "Excess Water Switch")

        #### TABLE 2 CARRYOVER STORAGE
        if st.session_state.carryoverStorageRadioButtonIndex == 1:
            editableTable(st.session_state.carryoverStoragedf, st.session_state.futurePlanningYear, setCarryoverStorageInputData, "Carryover Storage Systems Operations", "Carryover Storage (acre-feet/year)")

        ####  TABLE 3 CARRYOVER STORAGE COSTS
        if st.session_state.carryoverStorageCostRadioButtonIndex == 1:
            editableTable(st.session_state.carryoverStorageCostdf, st.session_state.futurePlanningYear, setCarryoverStorageCostInputData, "Carryover Storage System Operations", "Carryover Storage Costs ($/acre-feet)")
            
        ####  TABLE 4 TRANSFERS
        if st.session_state.transfersRadioButtonIndex == 1:
            editableTable(st.session_state.transfersdf, st.session_state.futurePlanningYear, setTransfersPriorityInputData, "Transfers System Operations", "Max transfer capacity (acre-feet/year)")

        ####  TABLE 5 TRANSFERS COSTS
        if st.session_state.transfersCostRadioButtonIndex == 1:
            editableTable(st.session_state.transfersCostdf, st.session_state.futurePlanningYear, setTransfersCostPriorityInputData, "Transfers Costs System Operations", "Transfer Cost ($/acre-feet)")