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

st.sidebar.write("")
inputDataFile = "src/inputData/CaUWMETInputData.xlsx"

#---------------------------------------------------------------#
# INITIALIZE GLOBAL ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
futurePlanningYear = '2045' #TODO Make future planning year list dynamic based on input data.

if 'futurePlanningYear' not in st.session_state:
    st.session_state['futurePlanningYear'] = futurePlanningYear

if 'contractorInfo' not in st.session_state:
    st.session_state['contractorInfo'] = fetch_data(inputDataFile, sheetname = 'Contractor Assumptions', skiprows = 4, nrows = 44, usecols = 'A:I')

if 'hydrologyAssumptions' not in st.session_state:
    st.session_state['hydrologyAssumptions'] = fetch_data(inputDataFile, sheetname = 'Hydrology Assumptions', skiprows = 3, nrows = 95, usecols = 'A:AR')

if 'contractorList' not in st.session_state:
    st.session_state['contractorList'] = selectSpecifiedRows(st.session_state.contractorInfo, 'Include in model', 'Yes')['Contractor']

if 'dropDownMenuList' not in st.session_state: # Drop down menu used on all pages
    st.session_state['dropDownMenuList'] = st.session_state.contractorList
    st.session_state.dropDownMenuList.loc[0] = "All Contractors"
    st.session_state.dropDownMenuList.sort_index(inplace=True)

#---------------------------------------------------------------#
# INITIALIZE DEMAND ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputData_TotalDemands = fetch_data(inputDataFile, sheetname = 'Demand Assumptions', skiprows = 19, nrows = 135, usecols = 'A:H')
inputData_DemandByUseType = fetch_data(inputDataFile, sheetname = 'Demand Assumptions', skiprows = 257, nrows = 319, usecols = 'A:H')
inputData_BaseLongTermConservation = fetch_data(inputDataFile, sheetname = 'Demand Assumptions', skiprows = 582, nrows = 44, usecols = 'A:H')

# #### Initialize input datasets with input data 
if 'totalDemandsdf' not in st.session_state:
    st.session_state['totalDemandsdf'] = inputData_TotalDemands[inputData_TotalDemands['Contractor'].isin(st.session_state.contractorList)]

if 'useByTypedf' not in st.session_state:
    st.session_state['useByTypedf'] = inputData_DemandByUseType[inputData_DemandByUseType['Contractor'].isin(st.session_state.contractorList)]

if 'baseLongTermConservationdf' not in st.session_state:
    st.session_state['baseLongTermConservationdf'] = inputData_BaseLongTermConservation[inputData_BaseLongTermConservation['Contractor'].isin(st.session_state.contractorList)]

#---------------------------------------------------------------#
# INITIALIZE SUPPLY ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputData_LocalSupplies = fetch_data(inputDataFile, sheetname = 'Supply Assumptions', skiprows = 11, nrows = 965, usecols = 'A:I')
inputData_SWPCVP = fetch_data(inputDataFile, sheetname = 'Supply Assumptions', skiprows = 984, nrows = 95, usecols = 'A:AR')

# #### Initialize input datasets with input data 
if 'localSuppliesdf' not in st.session_state:
    st.session_state['localSuppliesdf'] = inputData_LocalSupplies[inputData_LocalSupplies['Contractor'].isin(st.session_state.contractorList)]

if 'swpCVPSuppliesdf' not in st.session_state:
    st.session_state['swpCVPSuppliesdf'] = inputData_SWPCVP


#---------------------------------------------------------------#
# INITIALIZE SYSTEM OPERATIONS ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputData_excessWaterSwitch = fetch_data(inputDataFile, sheetname = 'System Operations Assumptions', skiprows = 6, nrows = 44, usecols = 'A:E')
inputData_surfaceCarryover = fetch_data(inputDataFile, sheetname = 'System Operations Assumptions', skiprows = 55, nrows = 229, usecols = 'A:I')
inputData_groundwaterBank = fetch_data(inputDataFile, sheetname = 'System Operations Assumptions', skiprows = 289, nrows = 227, usecols = 'A:I')
inputData_storageHedging = fetch_data(inputDataFile, sheetname = 'System Operations Assumptions', skiprows = 522, nrows = 181, usecols = 'A:E')
inputData_storageCosts = fetch_data(inputDataFile, sheetname = 'System Operations Assumptions', skiprows = 709, nrows = 89, usecols = 'A:I')
inputData_deliveryCosts = fetch_data(inputDataFile, sheetname = 'System Operations Assumptions', skiprows = 804, nrows = 319, usecols = 'A:I')

# #### Initialize input datasets with input data 
if 'excessWaterSwitch' not in st.session_state:
    st.session_state['excessWaterSwitch'] = inputData_excessWaterSwitch[inputData_excessWaterSwitch['Contractor'].isin(st.session_state.contractorList)]

if 'surfaceCarryover' not in st.session_state:
    st.session_state['surfaceCarryover'] = inputData_surfaceCarryover[inputData_surfaceCarryover['Contractor'].isin(st.session_state.contractorList)]

if 'groundwaterBank' not in st.session_state:
    st.session_state['groundwaterBank'] = inputData_groundwaterBank[inputData_groundwaterBank['Contractor'].isin(st.session_state.contractorList)]

if 'storageHedging' not in st.session_state:
    st.session_state['storageHedging'] = inputData_storageHedging[inputData_storageHedging['Contractor'].isin(st.session_state.contractorList)]

if 'storageCosts' not in st.session_state:
    st.session_state['storageCosts'] = inputData_storageCosts[inputData_storageCosts['Contractor'].isin(st.session_state.contractorList)]

if 'deliveryCosts' not in st.session_state:
    st.session_state['deliveryCosts'] = inputData_deliveryCosts[inputData_deliveryCosts['Contractor'].isin(st.session_state.contractorList)]