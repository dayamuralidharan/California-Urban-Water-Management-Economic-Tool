import streamlit as st
from globalUtilities import fetch_data

# Functions to set which option from the radio selector inputs are chosen and UWMP values if that is the chosen dataset.
def setLocalSurfaceWaterInputData():
    if st.session_state.localSurfaceWaterChoice == '2020 UWMP reported values':
        st.session_state.localSurfaceWaterRadioButtonIndex = 0
    else:
        st.session_state.localSurfaceWaterRadioButtonIndex = 1
        st.session_state.localSurfaceWaterdf = fetch_data("inputData/supplyInput_Surface.csv")

def setSWPCVPInputData():
    if st.session_state.swpCVPChoice == '2020 UWMP reported values':
        st.session_state.swpCVPRadioButtonIndex = 0
    elif st.session_state.swpCVPChoice == 'Calsim II 2020 Benchmark Study':
        st.session_state.swpCVPRadioButtonIndex = 1
        st.session_state.swpCVPSuppliesdf = fetch_data("inputData/supplyInput_SWPCVP.csv")
    else:
        st.session_state.swpCVPRadioButtonIndex = 2
        st.session_state.swpCVPSuppliesdf = fetch_data("inputData/supplyInput_SWPCVP.csv")

def setCostBySupplyTypeInputData():
    if st.session_state.costBySupplyTypeChoice == 'Default values from various references':
        st.session_state.costBySupplyTypeRadioButtonIndex = 0
    else:
        st.session_state.costBySupplyTypeRadioButtonIndex = 1
        st.session_state.costBySupplyTypedf = fetch_data("inputData/supplyCostInput_GroundwaterPumping.csv")

def setSupplyPriorityInputData():
    if st.session_state.supplyPriorityChoice == 'Default values from various references':
        st.session_state.supplyPriorityRadioButtonIndex = 0
    else:
        st.session_state.supplyPriorityRadioButtonIndex = 1
        st.session_state.supplyPrioritydf = fetch_data("inputData/supplyInput_supplyPriorities.csv")

def setSupplyDatasetsFromRadioButtons():
    localSurfaceWaterDatasetOptions = ['2020 UWMP reported values', 'User-defined values in table below']
    st.radio("1. Select the Local Surface Water Dataset from the options below. If the last option is selected, update the data in the Local Surface Water Supply table in the second collapsible section below.", options = localSurfaceWaterDatasetOptions, index = st.session_state.localSurfaceWaterRadioButtonIndex, key = "localSurfaceWaterChoice", on_change = setLocalSurfaceWaterInputData)

    swpCVPDatasetOptions = ['2020 UWMP reported values', 'Calsim II 2020 Benchmark Study', 'Calsim 3 <Study TBD>']
    st.radio("8. Select the SWP CVP Dataset from the options below. If the last option is selected, update the data in the SWP CVP Supply table in the second collapsible section below.", options = swpCVPDatasetOptions, index = st.session_state.swpCVPRadioButtonIndex, key = "swpCVPChoice", on_change = setSWPCVPInputData)

    costBySupplyTypeDatasetOptions = ['Default values from various references', 'User-defined values in table below']
    st.radio("9. Select the Cost by Supply Type Dataset from the options below. If the last option is selected, update the data in the Cost by Supply Type Supply table in the second collapsible section below.", options = costBySupplyTypeDatasetOptions, index = st.session_state.costBySupplyTypeRadioButtonIndex, key = "costBySupplyTypeChoice", on_change = setCostBySupplyTypeInputData)

    supplyPriorityDatasetOptions = ['Default values from various references', 'User-defined values in table below']
    st.radio("""10. Select the Supply Priority Dataset from the options below. If the last option is selected, 
    update the data in the Supply Priority Scenarios table in the first collapsible section below.""", options = supplyPriorityDatasetOptions, index = st.session_state.supplyPriorityRadioButtonIndex, key = "supplyPriorityChoice", on_change = setSupplyPriorityInputData)
