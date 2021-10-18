import streamlit as st
from multiapp import MultiApp
# import your app modules here
from apps import home, demands, modeloverview, hydrologyassumptions, editcontractors, systemoperations, results, faq, returnTest, watermanagement
from globalUtilities import fetch_data


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
inputDataDemandByUseType = fetch_data("inputData/demandsInput_useByTypeData.csv")
inputDataIntExtDemandsByUseType = fetch_data("inputData/demandsInput_intAndExtUseByTypeData.csv")
inputDataBaseLongTermConservation = fetch_data("inputData/demandsInput_baseLongTermConservationData.csv")


#---------------------------------------------------------------#
# INITIALIZE DEMAND ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#

# Initialize radio button indices with default values
if 'totalDemandScenarioRadioButtonIndex' not in st.session_state:
    st.session_state['totalDemandScenarioRadioButtonIndex'] = 0

if 'useByTypeRadioButtonIndex' not in st.session_state:
    st.session_state['useByTypeRadioButtonIndex'] = 0

if 'intExtUseByTypeRadioButtonIndex' not in st.session_state:
    st.session_state['intExtUseByTypeRadioButtonIndex'] = 0

if 'baseLongTermConservationRadioButtonIndex' not in st.session_state:
    st.session_state['baseLongTermConservationRadioButtonIndex'] = 0

#### Initialize input datasets with default values 
if 'totalDemandsdf' not in st.session_state:
    st.session_state['totalDemandsdf'] = inputDataTotalDemands

if 'useByTypedf' not in st.session_state:
    st.session_state['useByTypedf'] = inputDataDemandByUseType

if 'intExtUseByTypedf' not in st.session_state:
    st.session_state['intExtUseByTypedf'] = inputDataIntExtDemandsByUseType

if 'baseLongTermConservationdf' not in st.session_state:
    st.session_state['baseLongTermConservationdf'] = inputDataBaseLongTermConservation