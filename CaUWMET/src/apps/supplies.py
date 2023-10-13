import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots


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
            displaySummaryPlots(st.session_state.localSuppliesdf, localSuppliesExplanationText, "Local and Regional Supply Volumes")
        
        with st.expander("State Water Project and Central Valley Project Base Water Supplies"):
            st.markdown('Hello')

localSuppliesExplanationText = ("""Local supply data includes all existing and planned sources of water available for 
                                each supplier excluding supplies sourced from the State Water and Central Valley Projects (SWP and CVP). 
                                SWP and CVP supplies are input separately via the second variable on this page. Local supplies are input for
                                anticipated availability under a normal or better water year, single dry, and multiple dry year conditions. Local supplies
                                are input separately by type to account for the varying costs associated with each supply type. 
                                Default data was developed utilizing information reported in each supplier's 2020 Urban Water Management Plan.
                                Local supplies reported on this page should only include verified supplies. Any local supplies that are still 
                                conceptual should be input in the Water Management Options Assumptions page.""")

swpCVPExplanationText = ("""State Water Project (SWP) and Central Valley Project (CVP) sourced supplies are input separately from the local supplies to account for
                         variation that occurs from year to year as it is influenced by annual weather and hydrology, as well as demand by other users, operational and regulatory factors. 
                         The SWP water input through this variable includes long-term water supply contracts including Table A amounts, transfer and exchange of Table A water, carryover water, Turb-Back Pools A and B water, Multiyar Water Pool Program water, 
                         and Article 21 water. Default data for these supplies were developed from CA DWR and U.S. Bureau of Reclamation's Calsim II 
                         and Calsim 3 water resources planning models. These models simulate operations of the SWP and CVP and much of the water resources infrastructure in the Central 
                         Valley of California and the Sacramento-San Joaquin Delta regions. The default Calsim II dataset was developed from the U.S. Bureau's 2020 Benchmark study
                         which simulated delivery capabilities under 1922 - 2003 historic hydrologic conditions. The default Calsim 3 dataset was developed from DWR's <TBD> study
                         which simulated delivery capabilities under 1922 - 2015 historic hydrologic conditions. More details on these Calsim models and associated studies can be found
                         in Section X of the model documentation.""")
