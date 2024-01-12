import streamlit as st
from src.globalUtilities import opt_echo

def app():

    with opt_echo():
        st.title('Global Assumption Inputs')

        st.markdown("""
        :green[There are three groups of global assumptions entered into CaUWMET including:  
                    1) The time parameters including the future planning horizon year and hydrologic period applied in the simulation  
                    2) The list of contractors that are included in the model simulation, their study regions, additional details, and Calsim delivery arcs  
                    3)  The hydrology assumptions for each contractor]""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        :green[A detailed description of each of variable is provided in each expandable section below and Sections 3.1 and 3.2 of the model documentation.]""", unsafe_allow_html=True)

        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)

        with st.expander("Simulation Settings"):
            st.write("Planning Horizon: " + st.session_state.futurePlanningYear)
            st.write("Hydrologic reference period: " + str(st.session_state.hydrologicReferencePeriodStartYear) + " - " + str(st.session_state.hydrologicReferencePeriodEndYear))

        with st.expander("Contractor Assumptions"):
            data1 = st.session_state.contractorInfo
            #TODO format table
            st.table(data = data1)

        with st.expander("Hydrology Assumptions"):
            data2 = st.session_state.hydrologyAssumptions
            #TODO format table
            st.table(data = data2)