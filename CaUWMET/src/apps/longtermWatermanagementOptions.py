import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots

def app():

    with opt_echo():
        st.title('Long-term Water Management Options Assumptions')
        st.write("")
        st.write("<Description of Long-term Water Management Options Assumptions and Steps to use this page to be added.>")
        st.write("")

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

longtermWMOVolumeExplanationText = ("""X""")

longtermWMOCostExplanationText = ("""X""")