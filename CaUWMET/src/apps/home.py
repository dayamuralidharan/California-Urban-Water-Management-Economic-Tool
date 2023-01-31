import streamlit as st
import traceback
from load_css import local_css
from globalUtilities import opt_echo

def app():

    with opt_echo():
        local_css("style.css")

        st.subheader("Welcome to the California Urban Water Management Economics Tool")

        st.write("""
        CaUWMET is an open source model that simulates future planning scenarios to optimize the economic benefits 
        and costs of changes to urban water supply reliability. This tool utilizes the principle 
        of least-cost-planning to provide users information on 1) the cost of a water supply reliability
        enhancement and 2) the cost of unreliability.""")
        st.write("")
        st.write("""Users can learn about the model approach, edit model assumptions and review results by navigating through the pages in the navigation tree
        to the left. If you would like to view or modify the source code, please visit the GitHub repository at: <repository link>.
        Additional information on the model approach, documentation, and video tutorials can be found in the Model Overview page.""")        

        st.markdown("""<div><span class='font'>
        Steps to use this tool are summarized in green below. </span></div>""", unsafe_allow_html=True)
        st.write("")
        st.write("")
 
        st.markdown("""<div><span class='font'>
        1. Update and review model inputs on pages with the word "Assumptions" in the title. </span></div>""", unsafe_allow_html=True)

        st.write("")

        st.markdown("""<div><span class='font'>
        2. If preferred, assumptions can also be updated through the Excel template downloaded from the button below. Once the worksheet has been filled out, please upload it through the button below. </span></div>""", unsafe_allow_html=True)

        st.write("")
        st.button('Download Input Data Template in Excel Format', help="""Users can download the input data template in Excel format to update via Excel
        if it is preferred over inputting through the Assumptions pages. Once the data is updated in the template, upload the data in the button below.""")
        st.write("")

        st.button('Upload Input Data in Excel Format', help="""Users can download the input data template in Excel format from the button above to update via Excel
        if it is preferred over inputting through the Assumptions pages. Once the data is updated in the template, upload the data by clicking this button.""")
        st.write("")


        st.markdown("""<div><span class='font'>
        3. View results </span></div>""", unsafe_allow_html=True)
        st.write("""View results at the Results page provided in the tree on the left side of this page.
        Results can also be downloaded to Excel format from this page.""")        