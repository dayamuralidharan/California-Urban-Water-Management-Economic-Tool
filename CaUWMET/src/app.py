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

#### Fetch input data
inputDataTotalDemands = fetch_data("inputData/demandsInput_totalDemands.csv")
inputDataDemandByUseType = fetch_data("inputData/useBySectorData.csv")
inputDataIntExtDemandsByUseType = fetch_data("inputData/intAndExtUseBySectorData.csv")
inputDataBaseLongTermConservation = fetch_data("inputData/baseLongTermConservationData.csv")

#### Initialize session state variables on Demand Assumptions page. Input matrices are read into two separate variables to keep one dataframe with all future planning year columns, 
# and a second that is filtered for only the selected future planning year.

if 'totalDemandScenarioRadioButtonIndex' not in st.session_state:
    st.session_state['totalDemandScenarioRadioButtonIndex'] = 0

if 'useBySectorRadioButtonIndex' not in st.session_state:
    st.session_state['useBySectorRadioButtonIndex'] = 0

if 'intExtUseBySectorRadioButtonIndex' not in st.session_state:
    st.session_state['intExtUseBySectorRadioButtonIndex'] = 0

if 'baseLongTermConservationRadioButtonIndex' not in st.session_state:
    st.session_state['baseLongTermConservationRadioButtonIndex'] = 0

if 'inputDataTotalDemands' not in st.session_state:
    st.session_state['inputDataTotalDemands'] = inputDataTotalDemands
if 'totalDemandsdf' not in st.session_state:
    st.session_state['totalDemandsdf'] = inputDataTotalDemands

if 'inputDataDemandByUseType' not in st.session_state:
    st.session_state['inputDataDemandByUseType'] = inputDataDemandByUseType
if 'useBySectordf' not in st.session_state:
    st.session_state['useBySectordf'] = inputDataDemandByUseType

if 'inputDataIntExtDemandsByUseType' not in st.session_state:
    st.session_state['inputDataIntExtDemandsByUseType'] = inputDataIntExtDemandsByUseType
if 'intExtUseBySectordf' not in st.session_state:
    st.session_state['intExtUseBySectordf'] = inputDataIntExtDemandsByUseType

if 'inputDataBaseLongTermConservation' not in st.session_state:
    st.session_state['inputDataBaseLongTermConservation'] = inputDataBaseLongTermConservation
if 'baseLongTermConservationdf' not in st.session_state:
    st.session_state['baseLongTermConservationdf'] = inputDataBaseLongTermConservation