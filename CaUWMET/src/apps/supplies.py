import streamlit as st
from load_css import local_css
from globalUtilities import opt_echo
from pageUtilities.editableTable import editableTable
from pageUtilities.selectData_Supplies import setSupplyDatasetsFromRadioButtons
from pageUtilities.summaryPlots_Supplies import displaySummaryPlots

#TODO Plot in collapsible section should average, not sum (Nira)
#TODO Kensey and Nira to review the color_map_df in demandsHelper file. I don't really understand the labeling. Also, why are colors input here but also declared in line ~129?
#TODO See if we can get demandsHelper file into pageUtilities folder (Kensey)
#TODO Make green text again (Nira)
#TODO Make bar plots color code by region too (Nira)

# Functions used to set variables equal to user-defined values in the editable tables if user-defined data is selected over default, also known as "grids"
def setLocalSurfaceWaterDataToUserInput(gridResponseData): 
    st.session_state.localSurfaceWaterdf = gridResponseData

def setGroundwaterDataToUserInput(gridResponseData): 
    st.session_state.groundwaterdf = gridResponseData

def setDesalinationDataToUserInput(gridResponseData): 
    st.session_state.desalinationdf = gridResponseData

def setRecyclingDataToUserInput(gridResponseData): 
    st.session_state.recyclingdf = gridResponseData

def setPotableReuseDataToUserInput(gridResponseData): 
    st.session_state.potableReusedf = gridResponseData

def setContractualTransfersDataToUserInput(gridResponseData): 
    st.session_state.contractualTransfersdf = gridResponseData

def setOtherImportedSuppliesDataToUserInput(gridResponseData): 
    st.session_state.otherImportedSuppliesdf = gridResponseData

def setSWPCVPDataToUserInput(gridResponseData): 
    st.session_state.swpCVPSuppliesdf = gridResponseDataset

def setCostBySupplyTypeDataToUserInput(gridResponseData): 
    st.session_state.costBySupplyTypedf = gridResponseDataset

def setSupplyPriorityDataToUserInput(gridResponseData): 
    st.session_state.supplyPrioritydf = gridResponseData

def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)
        local_css("style.css")

        st.title('Supply Assumptions Page')
        st.header("Steps to use this page")

        st.write("<span class='font'>There are four categories of variables that need to be set on this page including:</span>", unsafe_allow_html=True) 
        st.write("<span class='font'>1)	Local and imported supplies (other than SWP/CVP). This includes local surface, ground, desalinated, recycled, potable reuse, transfers, and other imported water.</span>", unsafe_allow_html=True)
        st.write("<span class='font'>2)	SWP/CVP supplies</span>", unsafe_allow_html=True)
        st.write("<span class='font'>3)	Cost by supply type, and</span>", unsafe_allow_html=True)
        st.write("<span class='font'>4)	Order of priority to deliver each supply</span>", unsafe_allow_html=True)
        st.write("<span class='font'>A detailed description of each variable is provided in the Supply Assumptions Overview section below.</span>", unsafe_allow_html=True)
        st. write("")
        st.write("First, select which datasets to use for each variable from the options below. Each dataset has the option to use default data or input data through a table. If input through the table option is selected, please note the table is in a ""collapsable"" section at the very bottom of this page.")
        st.write("After making your selection for all variables, review the data in the plots below.")

        #---------------------------------------------------------------#
        # RADIO BUTTONS TO SELECT DATASETS
        #---------------------------------------------------------------# 
        
        setSupplyDatasetsFromRadioButtons()
        
        #---------------------------------------------------------------#
        # SUMMARY POSTER FOR TOTAL DEMANDS
        #---------------------------------------------------------------#  
        
        displaySummaryPlots()
        
        #---------------------------------------------------------------#
        # COLLAPSIBLE SECTIONS WTIH EDITABLE TABLES
        #---------------------------------------------------------------#
       
        ####  TABLE 1 LOCAL SURFACE WATER
        if st.session_state.localSurfaceWaterRadioButtonIndex == 1:
            editableTable(st.session_state.localSurfaceWaterdf, st.session_state.futurePlanningYear, setLocalSurfaceWaterDataToUserInput, "Local Surface Water", "Local surface water supply volume (acre-feet/year)")

        ####  TABLE 2 GROUNDWATER
        if st.session_state.groundwaterRadioButtonIndex == 1:
            editableTable(st.session_state.groundwaterdf, st.session_state.futurePlanningYear, setGroundwaterDataToUserInput, "Groundwater", "Groundwater supply volume (acre-feet/year)")

        ####  TABLE 3 DESALINATION
        if st.session_state.desalinationRadioButtonIndex == 1:
            editableTable(st.session_state.desalinationdf, st.session_state.futurePlanningYear, setDesalinationDataToUserInput, "Desalination", "Desalination supply volume (acre-feet/year)")

        #### TABLE 4 RECYCLING
        if st.session_state.recyclingRadioButtonIndex == 1:
            editableTable(st.session_state.recyclingdf, st.session_state.futurePlanningYear, setRecyclingDataToUserInput, "Recycling", "Recycling supply volume (acre-feet/year)")
        
        ####  TABLE 5 POTABLE REUSE
        if st.session_state.potableReuseRadioButtonIndex == 1:
            editableTable(st.session_state.potableReusedf, st.session_state.futurePlanningYear, setPotableReuseDataToUserInput, "Potable Reuse", "Potable Reuse supply volume (acre-feet/year)")

        ####  TABLE 6 CONTRACTUAL TRANSFERS
        if st.session_state.contractualTransfersRadioButtonIndex == 1:
            editableTable(st.session_state.contractualTransfersdf, st.session_state.futurePlanningYear, setContractualTransfersDataToUserInput, "Long-term Contractual Transfers and Exchanges", "Long-term Contractual Transfers and Exchanges supply volume (acre-feet/year)")

        ####  TABLE 7 OTHER IMPORTED SUPPLIES
        if st.session_state.otherImportedSuppliesRadioButtonIndex == 1:
            editableTable(st.session_state.otherImportedSuppliesdf, st.session_state.futurePlanningYear, setOtherImportedSuppliesDataToUserInput, "Other Imported Supply", "Other imported supply volume (acre-feet/year)")

        ####  TABLE 8 SWP CVP SUPPLIES
        if st.session_state.swpCVPRadioButtonIndex == 1:
            editableTable(st.session_state.swpCVPSuppliesdf, st.session_state.futurePlanningYear, setSWPCVPDataToUserInput, "SWP and CVP Supplies", "SWP and CVP Supplies (acre-feet/year)")

        #### TABLE 9 COST BY SUPPLY TYPE
        if st.session_state.costBySupplyTypeRadioButtonIndex == 1:
            editableTable(st.session_state.costBySupplyTypedf, st.session_state.futurePlanningYear, setCostBySupplyTypeDataToUserInput, "Cost by Supply Type", "Cost by Supply Type ($/acre-feet-year)")

        ####  TABLE 10 SWP CVP SUPPLIES
        if st.session_state.supplyPriorityRadioButtonIndex == 1:
            editableTable(st.session_state.supplyPrioritydf, st.session_state.futurePlanningYear, setSupplyPriorityDataToUserInput, "Supply Priority", "Supply Priority")