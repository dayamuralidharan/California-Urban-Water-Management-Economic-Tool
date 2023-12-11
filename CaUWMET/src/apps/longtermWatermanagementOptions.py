import streamlit as st
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots

def app():

    with opt_echo():
        st.title('Long-term Water Management Options Assumptions')
        st.markdown("""
        :green[There are two groups of long-term water management option assumptions entered into CaUWMET including:  
                    1) Available volume for options  
                    2) Costs for options]""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        :green[A detailed description of each of variable is provided in each expandable section below and Sections 3.6.1 of the model documentation.]""", unsafe_allow_html=True)


        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)
        
        with st.expander("Long-term Water Management Option Available Supply Volumes"):
            displaySummaryPlots(st.session_state.longermWMOVolumes, longtermWMOVolumeExplanationText, "Long-term Water Management Option Volumes")
        
        with st.expander("Long-term Water Management Option Costs"):
            displaySummaryPlots(st.session_state.longtermWMOCosts, longtermWMOCostExplanationText, "Long-term Water Management Option Costs")

longtermWMOVolumeExplanationText = (""" Here the user can enter information for potential cost-effective long-term conservation or local supply augmentation. These options are assumed to provide a fixed level of supply enhancement or demand reduction, or combination of both each year. The model iterates through WMO volumes incrementally, up to the allowable volume input here.""")

longtermWMOCostExplanationText = ("""The model evaluates the cost of reliability enhancement contribution of additional regional long-term water management measures. The unit cost of any option can be specified as coefficients of a linear function (y=mx+b) where b is the Base Cost and M is the Incremental Cost, representing a unit price that increases linearly as the amount used is increased.""")