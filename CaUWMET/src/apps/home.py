import streamlit as st
from src.globalUtilities import opt_echo

def app():

    with opt_echo():

        st.subheader("Welcome to the California Urban Water Management Economics Tool")

        st.write("""
        California Department of Water Resources (DWR) recognized the need for a robust open-source tool to provide a 
        quantitative methodology for evaluating the economically optimal portfolio of water supply reliability 
        alternatives for individual water agencies, and working collaboratively with a team of consultants, 
        developed the California Urban Water Management Economic Tool (CaUWMET). CaUWMET is an evolution of the 
        Least-Cost Planning Simulation (LCPSIM) and California Water Economics Spreadsheet Tool (CWEST), 
        building upon these legacy tools to provide contractors with a more modern, flexible, and robust 
        platform that can be tailored to their specific study requirements. """)
        
        st.write("")
        st.write("""This dashboard tool was developed to visualize CaUWMET input and output data. Users can learn about CaUWMET
        and review model input and output data by navigating through the pages in the navigation tree to the left. These pages include:""")
        st.write("""- Model Overview: Provides a description of the model approach""")
        st.write("""- Input Global Assumptions: Includes an overview of contractor details and hydrology assumptions""")
        st.write("""- Input Demand Assumptions: Includes an overview of contractor total demand, water use by type, and conservation assumptions""")
        st.write("""- Input Supply Assumptions: Includes an overview of local, regional, and State Water and Central Valley Project supply assumptions""")
        st.write("""- Input System Operations Assumptions: Includes an overview of excess supply and storage management, as well as delivery cost assumptions""")
        st.write("""- Input Contingency Water Management Options Assumptions: Includes an overview of contingency conservation campaigns, water market transfers, and rationing program assumptions""")
        st.write("""- Input Long-term Water Management Options Assumptions: Includes an overview of new long-term supply and demand management options to explore with the model optimization method""")
        st.write("""- Results: Review CaUWMET model results""")
        
        st.write("")
        st.write("""If you would like to view or modify the source code, please visit the GitHub repository at: <repository link>.
        Additional information on the model approach, and documentation can be found in the Model Overview page.""")