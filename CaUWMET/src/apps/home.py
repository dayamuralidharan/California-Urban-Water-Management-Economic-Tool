import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo

def app():

    with opt_echo():
        local_css("src/style.css")

        st.subheader("Welcome to the California Urban Water Management Economics Tool")

        st.write("""
        CaUWMET is an open source model that simulates future planning scenarios to optimize the economic benefits 
        and costs of changes to urban water supply reliability. This tool utilizes the principle 
        of least-cost-planning to provide users information on 1) the cost of a water supply reliability
        enhancement and 2) the cost of unreliability.""")
        st.write("")
        st.write("""Users can learn about the model approach, view model assumptions and review results by navigating through the pages in the navigation tree
        to the left. If you would like to view or modify the source code, please visit the GitHub repository at: <repository link>.
        Additional information on the model approach, documentation, and video tutorials can be found in the Model Overview page.""")        

        st.markdown("""<div><span class='font'>
        Steps to use CaUWMET are summarized in green below. </span></div>""", unsafe_allow_html=True)
        st.markdown("""<div><span class='font'>
        1. Update input data in the CSV files found in the inputData folder of the model package.  </span></div>""", unsafe_allow_html=True)
        st.markdown("""<div><span class='font'>
        2. Review input data in the pages that include the terms "Input Assumptions" </span></div>""", unsafe_allow_html=True)
        st.markdown("""<div><span class='font'>
        3. Run the CaUWMET.exe file to run the model. </span></div>""", unsafe_allow_html=True) 
        st.markdown("""<div><span class='font'>
        4. View results on the "View Results" page and/or CSV files in the outputData folder </span></div>""", unsafe_allow_html=True)        