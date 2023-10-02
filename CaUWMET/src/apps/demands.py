import streamlit as st
from src.load_css import local_css
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Demands import displaySummaryPlotsTotalDemandScenarios, displaySummaryPlotsWaterUseByType, displaySummaryPlotsIntExtUseByType, displaySummaryPlotsBaseLongTermConservation
from src.colors import colors

def app():
    
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)
        local_css("src/style.css")

        st.title('Demand Assumptions Page')
        
        st.markdown("""<div><span class='font'>
        There are three Demand input datasets including:</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        1) Total Demands Scenarios for Normal or Better, Single-Dry, and Multiple Dry year types.</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div><span class='font'>
        2) Total Water Use by Type for Single-Family and Multi-Family Residential, Industrial, Commercial and Governmental, Agricultural, Large Landscape and Other use type categories.</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div><span class='font'>
        3) Planned Long-term Conservation</span></div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div><span class='font'>
        A detailed description of each of variable is provided in each expandable section below.</span></div>""", unsafe_allow_html=True)


        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)
        
        with st.expander("Total Demand Scenarios"):
            
            displaySummaryPlotsTotalDemandScenarios()
            data = st.session_state.totalDemandsdf.filter(items=['Variable','Study Region','Contractor',int(st.session_state.futurePlanningYear)])
            data[int(st.session_state.futurePlanningYear)] = data[int(st.session_state.futurePlanningYear)].apply(roundValues)
            st.table(data = data)
            
        with st.expander("Water Use By Type"):
            displaySummaryPlotsWaterUseByType()
            data = st.session_state.useByTypedf.filter(items=['Variable','Study Region','Contractor',int(st.session_state.futurePlanningYear)])
            data[int(st.session_state.futurePlanningYear)] = data[int(st.session_state.futurePlanningYear)].apply(roundValues)
            st.table(data = data)
        with st.expander("Planned Long-term Conservation"):
            displaySummaryPlotsBaseLongTermConservation()
            data = st.session_state.baseLongTermConservationdf.filter(items=['Variable','Study Region','Contractor',int(st.session_state.futurePlanningYear)])
            data[int(st.session_state.futurePlanningYear)] = data[int(st.session_state.futurePlanningYear)].apply(roundValues)
            st.table(data = data)

def roundValues(value): 
    try: 
        value = round(float(str(value)))
        return f"{value:,d}"
    except ValueError: 
        return str(value) 

