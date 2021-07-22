import streamlit as st
import traceback
from load_css import local_css
from appsUtilities import opt_echo

def app():

    with opt_echo():
        # Declare variables
        futurePlanningYear = [2025, 2030, 2035, 2040, 2045]
        local_css("style.css")

        st.subheader("Welcome to the California Urban Water Management Economics Tool")
        # st.write("""
        # """)
        st.write("""
        CaUWMET is an open source model that simulates future planning scenarios to optimize the economic benefits 
        and costs of changes to urban water supply reliability. This tool utilizes the principle 
        of least-cost-planning to provide users information on 1) the cost of a water supply reliability
        enhancement and 2) the cost of unreliability.""")
        st.write("")
        st.write("""Users can learn about the model approach, edit model assumptions and review results by navigating through the pages in the navigation tree
        to the left. If you're curious or would like to modify the source code, please visit the GitHub repository at: <repository link>.
        Additional information on the model approach, documentation, and video tutorials can be found in the Model Overview page.""")        

        st.markdown("""<div><span class='font'>
        Steps to use this tool are summarized in green below. </span></div>""", unsafe_allow_html=True)
 
        st.markdown("""<div><span class='font'>
        1. Select a pre-made scenario or create a new scenario </span></div>""", unsafe_allow_html=True)

        st.button('Create a New Scenario', help="""Creating a new scenario will automatically populate all assumptions with default values.
        These values are primarily based on data in each contractor's 2020 Urban Water Management Plans (UWMPs) and other references as described
        in the Model Documentation <hyperlink to documentation>.""")
        st.write("")
        st.selectbox("Or Choose a Pre-made Scenario",(''), help="<MORE INFO TO BE ADDED ON PRE-MADE SCENARIO.>")

        st.markdown("""<div><span class='font'>
        2. Select Future Planning Year </span></div>""", unsafe_allow_html=True)
        
        st.selectbox('Select which future planning year you would like the model to simulate.', futurePlanningYear)

        st.markdown("""<div><span class='font'>
        3. Update input assumptions </span></div>""", unsafe_allow_html=True)
        st.write("""Update scenario assumptions through the Input Data pages located in the tree to the left related to 
        Demands, Supplies, System Operations, Water Management Options and associated cost assumptions.""")

        st.button('Download Input Data Template in Excel Format', help="""Users can download the input data template in Excel format to update via Excel
        if it is preferred over inputting through the Assumptions pages. Once the data is updated in the template, upload the data in the button below.""")
        st.write("")

        st.button('Upload Input Data in Excel Format', help="""Users can download the input data template in Excel format from the button above to update via Excel
        if it is preferred over inputting through the Assumptions pages. Once the data is updated in the template, upload the data by clicking this button.""")
        st.write("")

        st.markdown("""<div><span class='font'>
        4. Verify the tool's tests pass to avoid errors </span></div>""", unsafe_allow_html=True)
        st.write("""Ensure the input data passes the required tests. If there are any errors, the 
        box to the right will show a red X and a message describing the source of the error.""") 
        st.write("")
        st.write("<span class='font'>✔</span> All tests pass!", unsafe_allow_html=True)

        st.markdown("""<div><span class='font'>
        5. View results </span></div>""", unsafe_allow_html=True)
        st.write("""View results at the Results page provided in the tree on the left side of this page.
        Results can also be downloaded to Excel format from this page.""")        