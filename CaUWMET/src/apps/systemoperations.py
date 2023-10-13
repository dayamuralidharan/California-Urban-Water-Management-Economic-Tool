import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_SystemOperations import displaySummaryPlots_excessSupplySwitch, displaySummaryPlots_carryoverStorage, displaySummaryPlots_groundwaterBank, displaySummaryPlots_StorageHedgingStrategy, displaySummaryPlots_storageOperationsCosts, displaySummaryPlots_deliveryCosts


def app():
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)
        local_css("src/style.css")

        st.title('System Operations Assumptions Page')

        st.markdown("""<div><span class='font'>
        There are six system operations assumption datasets entered into CaUWMET for each contractor, including:</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        1) Excess project supply management strategy
                    </span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        2) Surface carryover storage operations</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        3) Groundwater banking storage operations</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        4) Storage hedging strategy</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        5) Storage operations costs</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        6) Delivery costs</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        A detailed description of each of variable is provided in each expandable section below.</span></div>""", unsafe_allow_html=True)


        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)
        
        with st.expander("Excess project supply management strategy"):
            displaySummaryPlots_excessSupplySwitch(st.session_state.excessWaterSwitch, excessWaterSwitchExplanationText)
        
        with st.expander("Surface carryover storage operations"):
            displaySummaryPlots_carryoverStorage(st.session_state.surfaceCarryover, carryoverStorageExplanationText)
        
        with st.expander("Groundwater banking storage operations"):
            displaySummaryPlots_groundwaterBank(st.session_state.groundwaterBank, groundwaterBankExplanationText)
        
        with st.expander("Storage hedging strategy"):
            displaySummaryPlots_StorageHedgingStrategy(st.session_state.storageHedging, storageHedgingStrategyExplanationText)
        
        with st.expander("Storage operations costs"):
            displaySummaryPlots_storageOperationsCosts(st.session_state.storageCosts, storageCostsExplanationText)
        
        with st.expander("Delivery costs"):
            displaySummaryPlots_deliveryCosts(st.session_state.deliveryCosts, deliveryCostsExplanationText)

excessWaterSwitchExplanationText = ''  
carryoverStorageExplanationText = '' 
groundwaterBankExplanationText = '' 
storageHedgingStrategyExplanationText = '' 
storageCostsExplanationText = '' 
deliveryCostsExplanationText = '' 
        
        