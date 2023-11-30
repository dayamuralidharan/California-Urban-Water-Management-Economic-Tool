import streamlit as st
from src.globalUtilities import opt_echo

def app():

    with opt_echo():
        st.title('Global Assumptions')
        st.markdown("""<div><span class='font'>
        There are three input datasets including:</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        1) The time parameters including the future planning horizon year and hydrologic period applied in the simulation.</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div><span class='font'>
        2) The list of contractors that are included in the model simulation, their study regions, additional details, and Calsim delivery arcs.</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div><span class='font'>
        3) The hydrology assumptions for each contractor.</span></div>""", unsafe_allow_html=True)

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
        #TODO add time parameters
        with st.expander("Contractor Assumptions"):
            data1 = st.session_state.contractorInfo
            #TODO format table
            st.table(data = data1)

        with st.expander("Hydrology Assumptions"):
            data2 = st.session_state.hydrologyAssumptions
            #TODO format table
            st.table(data = data2)