import streamlit as st
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots

def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        st.title('Demand Assumption Inputs')

        st.markdown("""
        :green[There are three groups of demand assumptions entered into CaUWMET including:  
                    1) Total Demands Scenarios for Normal or Better, Single-Dry, and Multiple Dry year types  
                    2) Total Water Use by Type for Single-Family and Multi-Family Residential, Industrial, Commercial and Governmental, Agricultural, Large Landscape and Other use type categories  
                    3)  Planned Long-term Conservation]""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        :green[A detailed description of each of variable is provided in each expandable section below and Section 3.3 of the model documentation.]""", unsafe_allow_html=True)
        

        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)
        
        with st.expander("Total Demand Scenarios"):
            displaySummaryPlots(st.session_state.totalDemandsdf, demandsExplanationText, "Total Demand Scenarios", "total")
            
        with st.expander("Water Use By Type"):
            displaySummaryPlots(st.session_state.useByTypedf, useByTypeExplanationText, "Water Use By Type", "total")

        with st.expander("Planned Long-term Conservation"):
            displaySummaryPlots(st.session_state.baseLongTermConservationdf, baseLongTermConservationExplanationText, "Planned Long-term Conservation", "total")

demandsExplanationText = """Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can 
be found in the model documentation."""

useByTypeExplanationText = ("""Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")


baseLongTermConservationExplanationText = ("""Long-term conservation is incorporated into the model as it is an important component of each contractor's long-term strategy to increase 
their water supply reliability. These demand reductions typically include programs that target water use efficiency in each sector, turf replacement programs, 
conservation outreach and communications, reducing conveyance losses, and more. Long-term demand management measures that are adopted by water users can 
have a demand hardening effect. Although they can increase reliability by reducing the size, frequency and duration of shortage events, they can make these 
events relatively more costly when they do occur.  A hardening factor can be set to simulate this effect.>""")