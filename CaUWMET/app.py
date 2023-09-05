import streamlit as st
st.set_page_config(layout="wide")
from src.multiapp import MultiApp
# import your app modules here
from src.apps import home, demands, modeloverview, contractorinformation, supplies, systemoperations, results, watermanagement
from src.globalUtilities import fetch_data

app = MultiApp()

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("""
    # CaUWMET
    California Urban Water Management Economic Tool
    """)

with col2: 
    st.image('src/dwrlogo.jpg', width=90)

PAGES = {
    "Home": home,
    "Model Overview": modeloverview,
    "Contractor Assumptions": contractorinformation,
    "Input Demand Assumptions": demands,
    "Input Supply Assumptions": supplies,
    "Input System Operation Assumptions": systemoperations,
    "Input Water Management Options Assumptions": watermanagement,
    "View Results": results,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to",list(PAGES.keys()))
page = PAGES[selection]
page.app()

#TODO include this on side bar for every page. Make future planning year list dynamic based on input data.
st.sidebar.write("")
futurePlanningYearsList = [2025, 2030, 2035, 2040, 2045]
futurePlanningYear = '2045'

if 'futurePlanningYear' not in st.session_state:
    st.session_state['futurePlanningYear'] = futurePlanningYear



#---------------------------------------------------------------#
# INITIALIZE DEMAND ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
inputDataTotalDemands = fetch_data("src/inputData/demandsInput_totalDemands.csv")
inputDataDemandByUseType = fetch_data("src/inputData/demandsInput_useByTypeData.csv")
inputDataBaseLongTermConservation = fetch_data("src/inputData/demandsInput_baseLongTermConservationData.csv")

if 'totalDemandsdf' not in st.session_state:
    st.session_state['totalDemandsdf'] = inputDataTotalDemands

if 'useByTypedf' not in st.session_state:
    st.session_state['useByTypedf'] = inputDataDemandByUseType


if 'baseLongTermConservationdf' not in st.session_state:
    st.session_state['baseLongTermConservationdf'] = inputDataBaseLongTermConservation
    
#---------------------------------------------------------------#
# INITIALIZE SUPPLY ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputDataLocalSupplies = fetch_data("src/inputData/supplyInput_localSupplies.csv")
inputDataSWPCVP = fetch_data("src/inputData/supplyInput_SWPCVPCalsimII2020BenchmarkStudy.csv")
# Initialize radio button indices with default values
if 'localSuppliesRadioButtonIndex' not in st.session_state:
    st.session_state['localSuppliesRadioButtonIndex'] = 0

if 'swpCVPRadioButtonIndex' not in st.session_state:
    st.session_state['swpCVPRadioButtonIndex'] = 0

if 'costBySupplyTypeRadioButtonIndex' not in st.session_state:
    st.session_state['costBySupplyTypeRadioButtonIndex'] = 0

if 'supplyPriorityRadioButtonIndex' not in st.session_state:
    st.session_state['supplyPriorityRadioButtonIndex'] = 0

#### Initialize input datasets with default values 
if 'localSuppliesdf' not in st.session_state:
    st.session_state['localSuppliesdf'] = inputDataLocalSupplies

if 'swpCVPSuppliesdf' not in st.session_state:
    st.session_state['swpCVPSuppliesdf'] = inputDataSWPCVP


#---------------------------------------------------------------#
# INITIALIZE SYSTEM OPERATIONS ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputDataExcessWaterSwitch = fetch_data("src/inputData/systemOperationsInput_ExcessWaterSwitch.csv")
# Initialize radio button indices with default values
if 'excessWaterSwitchRadioButtonIndex' not in st.session_state:
    st.session_state['excessWaterSwitchRadioButtonIndex'] = 0

if 'carryoverStorageRadioButtonIndex' not in st.session_state:
    st.session_state['carryoverStorageRadioButtonIndex'] = 0

if 'carryoverStorageCostRadioButtonIndex' not in st.session_state:
    st.session_state['carryoverStorageCostRadioButtonIndex'] = 0

if 'transfersRadioButtonIndex' not in st.session_state:
    st.session_state['transfersRadioButtonIndex'] = 0

if 'transfersCostRadioButtonIndex' not in st.session_state:
    st.session_state['transfersCostRadioButtonIndex'] = 0

#### Initialize input datasets with default values 
if 'excessWaterSwitchdf' not in st.session_state:
    st.session_state['excessWaterSwitchdf'] = inputDataExcessWaterSwitch