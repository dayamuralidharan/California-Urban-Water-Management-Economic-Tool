import streamlit as st
from src.globalUtilities import opt_echo
from src.pageUtilities.optimizationPlot_Helper import displayOptimizationPlot
from src.pageUtilities.resultsPlots_Helper import formatLongTermWMOResults
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots

def app():
    with opt_echo():      
        st.title('CaUWMET Results Page')
        st.markdown("""<div><span class='font'>
        There are ### results output by CaUWMET including:</span></div>""", unsafe_allow_html=True)
        st.write("")

        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """
        st.markdown(hide, unsafe_allow_html=True)

        with st.expander("Optimization Plots"): displayOptimizationPlot(df=st.session_state.optimizationPlotData)

        with st.expander("Long-term Water Management Options Summary"):
            formatLongTermWMOResults(st.session_state.optimizedLongTermWMOs)
