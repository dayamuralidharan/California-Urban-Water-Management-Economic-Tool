import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots


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
            st.write(excessWaterSwitchExplanationText)
            st.table(st.session_state.excessWaterSwitch)
        
        with st.expander("Surface carryover storage operations"):
            displaySummaryPlots(st.session_state.surfaceCarryover, carryoverStorageExplanationText, "Surface Carryover")
        
        with st.expander("Groundwater banking storage operations"):
            displaySummaryPlots(st.session_state.groundwaterBank, groundwaterBankExplanationText, "Groundwater Banking")
        
        with st.expander("Storage hedging strategy"):
            st.write(storageHedgingStrategyExplanationText)
            st.table(st.session_state.storageHedging)
        
        with st.expander("Storage Operations Costs"):
            displaySummaryPlots(st.session_state.storageCosts, storageCostsExplanationText, "Storage Operations Costs")
        
        with st.expander("Delivery Costs"):
            displaySummaryPlots(st.session_state.deliveryCosts, deliveryCostsExplanationText, "Delivery Costs")

excessWaterSwitchExplanationText = ''  
carryoverStorageExplanationText = '' 
groundwaterBankExplanationText = '' 
storageHedgingStrategyExplanationText = '' 
storageCostsExplanationText = '' 
deliveryCostsExplanationText = '' 
        
        