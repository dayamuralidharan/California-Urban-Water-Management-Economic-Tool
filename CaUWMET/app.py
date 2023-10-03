import streamlit as st
st.set_page_config(layout="wide")
from src.multiapp import MultiApp
# import your app modules here
from src.apps import home, demands, modeloverview, globalAssumptions, supplies, systemoperations, results, watermanagement
from src.globalUtilities import fetch_data, selectSpecifiedRows

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
    "Global Assumptions": globalAssumptions,
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

#TODO include this on side bar for every page. 
st.sidebar.write("")
inputDataFile = "src/inputData/CaUWMETInputData.xlsx"

#---------------------------------------------------------------#
# INITIALIZE GLOBAL ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
futurePlanningYear = '2045' #TODO Make future planning year list dynamic based on input data.

if 'futurePlanningYear' not in st.session_state:
    st.session_state['futurePlanningYear'] = futurePlanningYear

if 'contractorInfo' not in st.session_state:
    st.session_state['contractorInfo'] = fetch_data(inputDataFile, sheetName = 'Contractor Assumptions', skipRows = 4, nRows = 44, useCols = 'A:I')

if 'hydrologyAssumptions' not in st.session_state:
    st.session_state['hydrologyAssumptions'] = fetch_data(inputDataFile, sheetName = 'Hydrology Assumptions', skipRows = 3, nRows = 95, useCols = 'A:AR')

if 'contractorList' not in st.session_state:
    st.session_state['contractorList'] = selectSpecifiedRows(st.session_state.contractorInfo, 'Include in model', 'Yes')['Contractor']

if 'dropDownMenuList' not in st.session_state: # Drop down menu used on various pages
    st.session_state['dropDownMenuList'] = st.session_state.contractorList
    st.session_state.dropDownMenuList.loc[0] = "All Contractors"
    st.session_state.dropDownMenuList.sort_index(inplace=True)

#---------------------------------------------------------------#
# INITIALIZE DEMAND ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputDataTotalDemands = fetch_data(inputDataFile, sheetName = 'Demand Assumptions', skipRows = 19, nRows = 135, useCols = 'A:H')
inputDataDemandByUseType = fetch_data(inputDataFile, sheetName = 'Demand Assumptions', skipRows = 257, nRows = 319, useCols = 'A:H')
inputDataBaseLongTermConservation = fetch_data(inputDataFile, sheetName = 'Demand Assumptions', skipRows = 582, nRows = 44, useCols = 'A:H')

if 'totalDemandsdf' not in st.session_state:
    st.session_state['totalDemandsdf'] = inputDataTotalDemands[inputDataTotalDemands['Contractor'].isin(st.session_state.contractorList)]

if 'useByTypedf' not in st.session_state:
    st.session_state['useByTypedf'] = inputDataDemandByUseType[inputDataDemandByUseType['Contractor'].isin(st.session_state.contractorList)]

if 'baseLongTermConservationdf' not in st.session_state:
    st.session_state['baseLongTermConservationdf'] = inputDataBaseLongTermConservation[inputDataBaseLongTermConservation['Contractor'].isin(st.session_state.contractorList)]

#---------------------------------------------------------------#
# INITIALIZE SUPPLY ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
# inputDataLocalSupplies = fetch_data("src/inputData/supplyInput_localSupplies.csv")
# inputDataSWPCVP = fetch_data("src/inputData/supplyInput_SWPCVPCalsimII2020BenchmarkStudy.csv")
# # Initialize radio button indices with default values
# if 'localSuppliesRadioButtonIndex' not in st.session_state:
#     st.session_state['localSuppliesRadioButtonIndex'] = 0

# if 'swpCVPRadioButtonIndex' not in st.session_state:
#     st.session_state['swpCVPRadioButtonIndex'] = 0

# if 'costBySupplyTypeRadioButtonIndex' not in st.session_state:
#     st.session_state['costBySupplyTypeRadioButtonIndex'] = 0

# if 'supplyPriorityRadioButtonIndex' not in st.session_state:
#     st.session_state['supplyPriorityRadioButtonIndex'] = 0

# #### Initialize input datasets with default values 
# if 'localSuppliesdf' not in st.session_state:
#     st.session_state['localSuppliesdf'] = inputDataLocalSupplies

# if 'swpCVPSuppliesdf' not in st.session_state:
#     st.session_state['swpCVPSuppliesdf'] = inputDataSWPCVP


#---------------------------------------------------------------#
# INITIALIZE SYSTEM OPERATIONS ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
# inputDataExcessWaterSwitch = fetch_data("src/inputData/systemOperationsInput_ExcessWaterSwitch.csv")
# # Initialize radio button indices with default values
# if 'excessWaterSwitchRadioButtonIndex' not in st.session_state:
#     st.session_state['excessWaterSwitchRadioButtonIndex'] = 0

# if 'carryoverStorageRadioButtonIndex' not in st.session_state:
#     st.session_state['carryoverStorageRadioButtonIndex'] = 0

# if 'carryoverStorageCostRadioButtonIndex' not in st.session_state:
#     st.session_state['carryoverStorageCostRadioButtonIndex'] = 0

# if 'transfersRadioButtonIndex' not in st.session_state:
#     st.session_state['transfersRadioButtonIndex'] = 0

# if 'transfersCostRadioButtonIndex' not in st.session_state:
#     st.session_state['transfersCostRadioButtonIndex'] = 0

# #### Initialize input datasets with default values 
# if 'excessWaterSwitchdf' not in st.session_state:
#     st.session_state['excessWaterSwitchdf'] = inputDataExcessWaterSwitch