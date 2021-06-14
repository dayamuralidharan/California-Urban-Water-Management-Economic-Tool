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

            # For some reason I need to import this again.
            import traceback

            traceback.extract_stack = self.orig_extract_stack

    with opt_echo():
        st.title('System Operations')

        st.write('This is the `System Operations` page of the dashboard.')
    #     st.subheader("Welcome to the California Urban Water Management Economics Tool")
    #     # st.write("""
    #     # """)
    #     st.write("""
    #     CaUWMET is an open source model to simulate & optimize the economic benefits 
    #     and costs of increasing urban water surface reliability. This tool utilizes the principle 
    #     of least-cost-planning to provide users information on 1) the cost of a water supply reliability
    #     enhancement and 2) the cost of unreliability.""")

    #     local_css("style.css")
    #     t = """<div><span class='font'>
    #     Steps to use this tool are summarized in green below </span></div>"""
    #     st.markdown(t, unsafe_allow_html=True)
    #     st.write("""Additional information can be found in the Model Information pages including video
    #     tutorials information on contractors included in this model.""")

    #     col1, col2 = st.beta_columns(2)   
        
    #     with col1:
    #         local_css("style.css")
    #         t = """<div><span class='font'>
    #         1. Select model scenario or create a new scenario </span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)
    #         st.write("""Creating a new sceanario will automatically populate all assumptions with default values.
    #         These assumptions are largely based on data in each contractor's latest Urban Water Management Plan.
    #         More information on the assumptions included in these values is in the Model Documentation.""")

    #         local_css("style.css")
    #         t = """<div><span class='font'>
    #         2. Select Planning Horizon Year </span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)
    #         st.write("""Creating a new sceanario will automatically populate all assumptions with default values.
    #         These assumptions are largely based on data in each contractor's latest Urban Water Management Plan.
    #         More information on the assumptions included in these values is in the Model Documentation.""")   

    #         local_css("style.css")
    #         t = """<div><span class='font'>
    #         3. Update input assumptions </span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)
    #         st.write("""Update assumptions through the Input Data pages located in the tree to the left for 
    #         Demands, Supplies, System Operations and Water Management Options.""")   

    #         local_css("style.css")
    #         t = """<div><span class='font'>
    #         4. Verify the water balance tests pass to avoid errors </span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)
    #         st.write("""Ensure the input data passes the mass balance checks. If there are any errors, the 
    #         box to the right will show a red X and a message describing the source of the error.""") 

    #         local_css("style.css")
    #         t = """<div><span class='font'>
    #         5. View results </span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)
    #         st.write("""View results at the Results page provided in the tree on the left side of this page.
    #         Results can also be downloaded in Excel""")        

    #     with col2:
    #         st.write("")
    #         st.write("")
    #         local_css("style.css")
    #         t = """<div><span class='center'>
    #         Create New Scenario </span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)

    #         # local_css("style.css")
    #         # t = """<div><span class='center'>
    #         # Choose a Pre-mode Scenario </span></div>"""
    #         st.write("")
    #         st.write("")
    #         st.write("")
    #         st.write("")
    #         st.write("")

    #         a=['Choose a Pre-mode Scenario']
    #         st.write("")
    #         st.selectbox('',a)

    #         st.write("")
    #         st.write("")
    #         st.write("")

    #         local_css("style.css")
    #         t = """<div><span class='center'>
    #         Download Input Data Template </span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)

    #         local_css("style.css")
    #         t = """<div><span class='center'>
    #         Upload Scenario Input Data</span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)

    #         st.write("")
    #         st.write("")
    #         st.write("<span class='font'>✔</span>Demand assumptions check pass!", unsafe_allow_html=True)
    #         st.write("<span class='font'>✔</span>Supply assumptions checks pass!", unsafe_allow_html=True)
    #         st.write("<span class='font'>✔</span>System operation assumptions check pass!", unsafe_allow_html=True)

    #         local_css("style.css")
    #         t = """<div><span class='center'>
    #         Download Results to Excel</span></div>"""
    #         st.markdown(t, unsafe_allow_html=True)