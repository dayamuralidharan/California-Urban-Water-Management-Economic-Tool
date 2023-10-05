import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Supplies import displaySummaryPlotsLocalAndRegionalSupplies


def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)
        local_css("src/style.css")

        st.title('Supply Assumptions Page')

        st.markdown("""<div><span class='font'>
        There are two base water supply assumption datasets entered into CaUWMET including:</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        1) Supply assumptions for local and regional supplies for normal or better, single-dry, and multiple dry year types. 
                    These supplies include surface, groundwater, desalination, recycled, potable reuse, long-term contractual transfer and exchanges,
                    and other supplies. These supply assumptions exclude State Water Project and Central Valley Project supplies which are shown below.
                    </span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        2) Supply assumptions for State Water Project and Central Valley Project supplies.</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        A detailed description of each of variable is provided in each expandable section below. These assumptions exclude supplies stored in surface carryover or groundwater banking systems, and contingent water market transfers
                    which are shown on the System Operations and Contingent Water Management Option pages, respectively.</span></div>""", unsafe_allow_html=True)



        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)
        
        with st.expander("Local and Regional Base Water Supplies"):
            displaySummaryPlotsLocalAndRegionalSupplies()
        
        with st.expander("State Water Project and Central Valley Project Base Water Supplies"):
            st.markdown('Hello')

