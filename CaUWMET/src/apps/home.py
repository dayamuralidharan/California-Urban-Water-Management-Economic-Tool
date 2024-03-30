import streamlit as st
from src.globalUtilities import opt_echo

def app():

    with opt_echo():

        st.subheader("Welcome to the California Urban Water Management Economics Tool")

        st.write("""
        California Department of Water Resources (DWR) recognizes the need for a user-friendly tool to provide a 
        quantitative methodology for evaluating the economically optimal portfolio of water supply reliability 
        alternatives for individual water agencies. The California Urban Water Management Economic Tool (CaUWMET) 
        applies the Least-Cost Planning method to provide State Water Project and Central Valley Project contractors with a more 
        modern, flexible, and robust platform that can be tailored to their specific study requirements. """)
        
        st.write("")
        st.markdown("""
        :green[This dashboard tool was developed to visualize CaUWMET input and output datasets. Users can learn about CaUWMET
        and review model input and output data by navigating through the pages in the navigation tree to the left. These pages include:  
        - Model Overview: Provides a description of the model approach  
        - Input Global Assumptions: Includes an overview of contractor details and hydrology assumptions  
        - Input Demand Assumptions: Includes an overview of contractor total demand, water use by type, and conservation assumptions  
        - Input Supply Assumptions: Includes an overview of local, regional, and State Water and Central Valley Project supply assumptions  
        - Input System Operations Assumptions: Includes an overview of excess supply and storage management, as well as delivery cost assumptions  
        - Input Contingency Water Management Options Assumptions: Includes an overview of contingency conservation campaigns, water market transfers, and rationing program assumptions  
        - Input Long-term Water Management Options Assumptions: Includes an overview of new long-term supply and demand management options to explore with the model optimization method  
        - Results: Review CaUWMET model results
]""", unsafe_allow_html=True)
        st.write("")
        st.write("""If you would like to view or modify the source code, please visit the GitHub repository at: <repository link>.
        Additional information on the model approach, and documentation can be found in the Model Overview page.""")