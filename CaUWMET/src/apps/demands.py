import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Demands import displaySummaryPlots

#TODO Review the color_map_df in demandsHelper file. I don't really understand the labeling. Also, why are colors input here but also declared in line ~129?


def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)
        local_css("src/style.css")

        st.title('Demand Assumptions Page')
        


        st.write("<span class='font'>There are four demand input datasets including:</span>", unsafe_allow_html=True) 
        st.write("<span class='font'>1) Total Demands Scenarios for Normal or Better, Single-Dry, and Multiple Dry year types.</span>", unsafe_allow_html=True)
        st.write("<span class='font'>2) Total Water Use by Type for Single-Family and Multi-Family Residential, Industrial, Commercial and Governmental, Agricultural, Large Landscape and Other use type categories.</span>", unsafe_allow_html=True)
        st.write("<span class='font'>3) Interior and Exterior Use by Type for each category listed above, and</span>", unsafe_allow_html=True)
        st.write("<span class='font'>4) Base Long-term Conservation</span>", unsafe_allow_html=True)
        st.write("<span class='font'>A detailed description of each of variable is provided in the Demand Assumptions Overview section below.</span>", unsafe_allow_html=True)
        st.write("")


        with st.expander("View Total Demands"):
            displaySummaryPlots()