import streamlit as st
from src.globalUtilities import opt_echo

def app():

    with opt_echo():

        st.subheader("Welcome to the California Urban Water Management Economics Tool")

        st.write("""
        Urban water suppliers in California can face challenges in water service reliability as their systems are subjected 
        to the impacts of changes in climate, regulations, infrastructure, or other stressors. Understanding the 
        financial and economic implications of adopting reliability enhancement measures, determining which ones to adopt, 
        and determining how much to adopt of each possible measure is a key component in water supply planning 
        decision-making processes and environmental impact studies.
        
        California Department of Water Resources (DWR) recognized the need for a robust open-source tool to provide a 
        quantitative methodology for evaluating the economically optimal portfolio of water supply reliability 
        alternatives for individual water agencies, and working collaboratively with a team of consultants, 
        developed the California Urban Water Management Economic Tool (CaUWMET). CaUWMET is an evolution of the 
        Least-Cost Planning Simulation (LCPSIM) and California Water Economics Spreadsheet Tool (CWEST), 
        building upon these legacy tools to provide contractors with a more modern, flexible, and robust 
        platform that can be tailored to their specific study requirements. """)
        
        st.write("")
        st.write("""Users can learn about the model approach, view model assumptions and review results by navigating through the pages in the navigation tree
        to the left. If you would like to view or modify the source code, please visit the GitHub repository at: <repository link>.
        Additional information on the model approach, and documentation can be found in the Model Overview page.""")