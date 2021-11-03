import streamlit as st
from multiapp import MultiApp
# import your app modules here
from apps import home, demands, modeloverview, hydrologyassumptions, supplies, systemoperations, results, faq, returnTest, watermanagement
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
    #"Contractor Assumptions": editcontractors,
    "Hydrology Assumptions": hydrologyassumptions,
    "Demand Assumptions": demands,
    "Supply Assumptions": supplies,
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

inputDataLocalSurfaceWater = fetch_data("inputData/supplyInput_Surface.csv")
inputDataGroundwater = fetch_data("inputData/supplyInput_Groundwater.csv")
inputDataDesalination = fetch_data("inputData/supplyInput_Desalination.csv")
inputDataRecycling = fetch_data("inputData/supplyInput_Recycled.csv")
inputDataPotableReuse = fetch_data("inputData/supplyInput_PotableReuse.csv")
inputDataContractualTransfers = fetch_data("inputData/supplyInput_ContractualTransfers.csv")
inputDataOtherImportedSupplies = fetch_data("inputData/supplyInput_OtherImported.csv")
inputDataSWPCVP = fetch_data("inputData/supplyInput_SWPCVP.csv")
inputDataCostBySupplyType = fetch_data("inputData/supplyCostInput_GroundwaterPumping.csv")
inputDataSupplyPriority = fetch_data("inputData/supplyInput_supplyPriorities.csv")

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
    
#---------------------------------------------------------------#
# INITIALIZE SUPPLY ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#

# Initialize radio button indices with default values
if 'localSurfaceWaterRadioButtonIndex' not in st.session_state:
    st.session_state['localSurfaceWaterRadioButtonIndex'] = 0

if 'groundwaterRadioButtonIndex' not in st.session_state:
    st.session_state['groundwaterRadioButtonIndex'] = 0

if 'desalinationRadioButtonIndex' not in st.session_state:
    st.session_state['desalinationRadioButtonIndex'] = 0

if 'recyclingRadioButtonIndex' not in st.session_state:
    st.session_state['recyclingRadioButtonIndex'] = 0

if 'potableReuseRadioButtonIndex' not in st.session_state:
    st.session_state['potableReuseRadioButtonIndex'] = 0

if 'contractualTransfersRadioButtonIndex' not in st.session_state:
    st.session_state['contractualTransfersRadioButtonIndex'] = 0

if 'otherImportedSuppliesRadioButtonIndex' not in st.session_state:
    st.session_state['otherImportedSuppliesRadioButtonIndex'] = 0

if 'swpCVPRadioButtonIndex' not in st.session_state:
    st.session_state['swpCVPRadioButtonIndex'] = 0

if 'costBySupplyTypeRadioButtonIndex' not in st.session_state:
    st.session_state['costBySupplyTypeRadioButtonIndex'] = 0

if 'supplyPriorityRadioButtonIndex' not in st.session_state:
    st.session_state['supplyPriorityRadioButtonIndex'] = 0

#### Initialize input datasets with default values 
if 'localSurfaceWaterdf' not in st.session_state:
    st.session_state['localSurfaceWaterdf'] = inputDataLocalSurfaceWater

if 'groundwaterdf' not in st.session_state:
    st.session_state['groundwaterdf'] = inputDataGroundwater

if 'desalinationdf' not in st.session_state:
    st.session_state['desalinationdf'] = inputDataDesalination

if 'recyclingdf' not in st.session_state:
    st.session_state['recyclingdf'] = inputDataRecycling

if 'potableReusedf' not in st.session_state:
    st.session_state['potableReusedf'] = inputDataPotableReuse

if 'contractualTransfersdf' not in st.session_state:
    st.session_state['contractualTransfersdf'] = inputDataContractualTransfers

if 'otherImportedSuppliesdf' not in st.session_state:
    st.session_state['otherImportedSuppliesdf'] = inputDataOtherImportedSupplies

if 'swpCVPSuppliesdf' not in st.session_state:
    st.session_state['swpCVPSuppliesdf'] = inputDataSWPCVP

if 'costBySupplyTypedf' not in st.session_state:
    st.session_state['costBySupplyTypedf'] = inputDataCostBySupplyType

if 'supplyPrioritydf' not in st.session_state:
    st.session_state['supplyPrioritydf'] = inputDataSupplyPriority