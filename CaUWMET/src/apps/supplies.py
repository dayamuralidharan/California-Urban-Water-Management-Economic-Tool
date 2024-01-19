import streamlit as st
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots
import plotly.express as px



def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        st.title('Supply Assumption Inputs')

        st.markdown("""
        :green[There are two groups of base water supply assumptions entered into CaUWMET including:  
                    1) Supply assumptions for local and regional supplies for normal or better, single-dry, and multiple dry year types  
                    2) Supply assumptions for State Water Project and Central Valley Project supplies]""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        :green[A detailed description of each of variable is provided in each expandable section below and Sections 3.4 of the model documentation.]""", unsafe_allow_html=True)

        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)
        
        with st.expander("Local and Regional Base Water Supplies"):
            displaySummaryPlots(st.session_state.localSuppliesdf, localSuppliesExplanationText, "Local and Regional Supply Volumes", "total")
        
        with st.expander("State Water Project and Central Valley Project Base Water Supplies"):
            st.markdown(swpCVPExplanationText)
            st.session_state.swpCVPSuppliesdf.loc[:,st.session_state.swpCVPSuppliesdf.columns != 'Year'].astype(int)
            contractorView = st.selectbox("Select contractor to view SWP/CVP supplies", st.session_state.contractorList)
            fig = px.line(st.session_state.swpCVPSuppliesdf, x= "Year", y = contractorView)
            fig.update_layout(yaxis_title = "Annual SWP and/or CVP Supply (acre-feet)")
            st.write(fig)
            #st.session_state.swpCVPSuppliesdf['City of Folsom'] = st.session_state.swpCVPSuppliesdf['City of Folsom'].map('{:,.0f}'.format)
            st.table(st.session_state.swpCVPSuppliesdf)

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
                         The SWP water input through this variable includes long-term water supply contracts including Table A amounts, transfer and exchange of Table A water, carryover water, Turn-Back Pools A and B water, Multiyear Water Pool Program water, 
                         and Article 21 water. Default data for these supplies were developed from CA DWR and U.S. Bureau of Reclamation's Calsim II 
                         and Calsim 3 water resources planning models. These models simulate operations of the SWP and CVP and much of the water resources infrastructure in the Central 
                         Valley of California and the Sacramento-San Joaquin Delta regions. The default dataset was developed from DWR's  2021 Delivery Capability Report’s Existing Conditions Calsim 3 simulation
                         which simulated delivery capabilities under 1922 - 2015 historic hydrologic conditions. """)
