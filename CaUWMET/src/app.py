import streamlit as st
from multiapp import MultiApp
# import your app modules here
from apps import home, demands, modeloverview, hydrologyassumptions, editcontractors, systemoperations, results, faq, returnTest, watermanagement
from appsUtilities import fetch_data


app = MultiApp()

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("""
    # CaUWMET
    California Urban Water Management Economic Tool
    """)

with col2: 
    st.image('dwrlogo.jpg', width=90)

PAGES = {
    "Home": home,
    "Model Overview": modeloverview,
    "Contractor Assumptions": editcontractors,
    "Hydrology Assumptions": hydrologyassumptions,
    "Demand Assumptions": demands,
    #"Supply Assumptions": supplies,
    "System Operation Assumptions": systemoperations,
    "Water Management Assumptions": watermanagement,
    "Results": results,
    "FAQ and Support": faq,
    "Return Test": returnTest,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to",list(PAGES.keys()))
page = PAGES[selection]
page.app()

#TODO include this on side bar for every page.
st.sidebar.write("")
futurePlanningYearsList = [2025, 2030, 2035, 2040, 2045]
futurePlanningYear = st.sidebar.selectbox('Select which future planning year you would like the model to simulate.', futurePlanningYearsList, key = 'futurePlanningYear')

st.sidebar.write("")
st.sidebar.button('Run Model')

# Initialize session state variables on Demand Assumptions page
if 'totalDemandScenarioRadioButtonIndex' not in st.session_state:
    st.session_state['totalDemandScenarioRadioButtonIndex'] = 0

if 'useBySectorRadioButtonIndex' not in st.session_state:
    st.session_state['useBySectorRadioButtonIndex'] = 0

if 'intExtUseBySectorRadioButtonIndex' not in st.session_state:
    st.session_state['intExtUseBySectorRadioButtonIndex'] = 0

if 'baseLongTermConservationRadioButtonIndex' not in st.session_state:
    st.session_state['baseLongTermConservationRadioButtonIndex'] = 0

if 'totalDemandsdf' not in st.session_state:
    st.session_state['totalDemandsdf'] = fetch_data("inputData/totalDemandsData.csv")

if 'useBySectordf' not in st.session_state:
    st.session_state['useBySectordf'] = fetch_data("inputData/useBySectorData.csv")

if 'intExtUseBySectordf' not in st.session_state:
    st.session_state['intExtUseBySectordf'] = fetch_data("inputData/intAndExtUseBySectorData.csv")

if 'baseLongTermConservationdf' not in st.session_state:
    st.session_state['baseLongTermConservationdf'] = fetch_data("inputData/baseLongTermConservationData.csv")
