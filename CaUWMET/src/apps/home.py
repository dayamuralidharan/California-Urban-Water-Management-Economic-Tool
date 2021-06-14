import streamlit as st
import traceback
from load_css import local_css

def app():
    
    class opt_echo:
        def __init__(self):
            self.checkbox = st.sidebar.checkbox("Show source code")
            self.orig_extract_stack = traceback.extract_stack

            if self.checkbox:
                traceback.extract_stack = lambda: self.orig_extract_stack()[:-2]
                self.echo = st.echo()

        def __enter__(self):
            if self.checkbox:
                return self.echo.__enter__()

        def __exit__(self, type, value, traceback):
            if self.checkbox:
                self.echo.__exit__(type, value, traceback)

            import traceback

            traceback.extract_stack = self.orig_extract_stack

    with opt_echo():
        st.subheader("Welcome to the California Urban Water Management Economics Tool")
        # st.write("""
        # """)
        st.write("""
        CaUWMET is an open source model that simulates future planning scenarios to optimize the economic benefits 
        and costs of changes to urban water supply reliability. This tool utilizes the principle 
        of least-cost-planning to provide users information on 1) the cost of a water supply reliability
        enhancement and 2) the cost of unreliability.""")

        local_css("style.css")
        t = """<div><span class='font'>
        Steps to use this tool are summarized in green below. </span></div>"""
        st.markdown(t, unsafe_allow_html=True)
        st.write("""Users can learn about the model approach, edit model assumptions and review results by navigating through the pages in the navigation tree
        to the left. If you're curious or would like to modify the source code, please visit the GitHub repository at: <repository link>.
        Additional information on the model approach, documentation, and video tutorials can be found in the Model Overview page.""")

        col1, col2 = st.beta_columns(2)   
        
        with col1:
            local_css("style.css")
            t = """<div><span class='font'>
            1. Select a pre-made or create a new scenario </span></div>"""
            st.markdown(t, unsafe_allow_html=True)
            st.write("""Creating a new scenario will automatically populate all assumptions with default values.
            These values are primarily based on data in each contractor's 2020 Urban Water Management Plans (UWMPs) and other references as described
            in the Model Documentation <hyperlink to documentation>. 
            <MORE INFO TO BE ADDED ON PRE-MADE SCENARIO.>""")

            local_css("style.css")
            t = """<div><span class='font'>
            2. Select Planning Horizon Year </span></div>"""
            st.markdown(t, unsafe_allow_html=True)
            st.write("""Select which future planning year you would like the model to simulate.""")   

            local_css("style.css")
            t = """<div><span class='font'>
            3. Update input assumptions </span></div>"""
            st.markdown(t, unsafe_allow_html=True)
            st.write("""Update scenario assumptions through the Input Data pages located in the tree to the left related to 
            Demands, Supplies, System Operations, Water Management Options and associated cost assumptions.""")   

            local_css("style.css")
            t = """<div><span class='font'>
            4. Verify the tool's tests pass to avoid errors </span></div>"""
            st.markdown(t, unsafe_allow_html=True)
            st.write("""Ensure the input data passes the required tests. If there are any errors, the 
            box to the right will show a red X and a message describing the source of the error.""") 

            local_css("style.css")
            t = """<div><span class='font'>
            5. View results </span></div>"""
            st.markdown(t, unsafe_allow_html=True)
            st.write("""View results at the Results page provided in the tree on the left side of this page.
            Results can also be downloaded to Excel format from this page.""")        

        with col2:
            st.write("")
            st.write("")
            local_css("style.css")
            t = """<div><span class='center'>
            Create a New Scenario </span></div>"""
            st.markdown(t, unsafe_allow_html=True)
            a=['Or Choose a Pre-made Scenario']
            st.write("")
            st.selectbox('',a)
            st.write("")
            st.write("")
            st.write("")

            a=['Select the Planning Horizon Year']
            st.write("")
            st.selectbox('',a)
            st.write("")
            st.write("")
            st.write("")

            local_css("style.css")
            t = """<div><span class='center'>
            Download Input Data Template in Excel format</span></div>"""
            st.markdown(t, unsafe_allow_html=True)

            local_css("style.css")
            t = """<div><span class='center'>
            Upload Scenario Input Data from Excel format</span></div>"""
            st.markdown(t, unsafe_allow_html=True)

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("<span class='font'>✔</span> All tests pass!", unsafe_allow_html=True)
