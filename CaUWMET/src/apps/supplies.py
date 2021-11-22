import streamlit as st
from load_css import local_css
from globalUtilities import opt_echo
from pageUtilities.editableTable import editableTable
from pageUtilities.editableTableForTimeSeriesByContractor import editableTableForTimeSeriesByContractor
from pageUtilities.selectData_Supplies import setSupplyDatasetsFromRadioButtons
from pageUtilities.summaryPlots_Supplies import displaySummaryPlots

#TODO Plot in collapsible section should average, not sum (Nira)
#TODO Kensey and Nira to review the color_map_df in demandsHelper file. I don't really understand the labeling. Also, why are colors input here but also declared in line ~129?
#TODO See if we can get demandsHelper file into pageUtilities folder (Kensey)
#TODO Make green text again (Nira)
#TODO Make bar plots color code by region too (Nira)

# Functions used to set variables equal to user-defined values in the editable tables if user-defined data is selected over default, also known as "grids"
def setLocalSuppliesDataToEditableTableInput(gridResponseData): 
    st.session_state.localSuppliesWaterdf = gridResponseData

def setSWPCVPDataToEditableTableInput(gridResponseData): 
    st.session_state.swpCVPSuppliesdf = gridResponseData

def setCostBySupplyTypeDataToEditableTableInput(gridResponseData): 
    st.session_state.costBySupplyTypedf = gridResponseData

def setSupplyPriorityDataToEditableTableInput(gridResponseData): 
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
        st.write("First, select which datasets to use for each variable from the options below. Each dataset has the option to use default data or input data through a table. If input through the table option is selected, please note the table is in a ""collapsible"" section at the very bottom of this page.")
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
       
        ####  TABLE 1 LOCAL SUPPLIES
        if st.session_state.localSuppliesRadioButtonIndex == 1:
            editableTable(st.session_state.localSuppliesdf, st.session_state.futurePlanningYear, setLocalSuppliesDataToEditableTableInput, "Local Supplies", "Local water supply volume (acre-feet/year)")


        #### TABLE 2 SWP CVP SUPPLIES
        if st.session_state.swpCVPRadioButtonIndex == 2:
            editableTableForTimeSeriesByContractor(st.session_state.swpCVPSuppliesdf, setSWPCVPDataToEditableTableInput, "SWP and CVP Supplies")

        ####  TABLE 3 COST BY SUPPLY TYPE
        if st.session_state.costBySupplyTypeRadioButtonIndex == 1:
            editableTable(st.session_state.costBySupplyTypedf, st.session_state.futurePlanningYear, setCostBySupplyTypeDataToEditableTableInput, "Cost by Supply Type", "Cost by Supply Type ($/acre-foot)")
            
        ####  TABLE 4 COST BY SUPPLY TYPE
        if st.session_state.supplyPriorityRadioButtonIndex == 1:
            editableTable(st.session_state.supplyPrioritydf, st.session_state.futurePlanningYear, setSupplyPriorityDataToEditableTableInput, "Priority of Use by Supply Type", "Priority of Use by Supply Type")
