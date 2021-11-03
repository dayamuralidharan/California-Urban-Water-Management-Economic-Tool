import streamlit as st
from globalUtilities import fetch_data

# Functions to set which option from the radio selector inputs are chosen and UWMP values if that is the chosen dataset.
def setLocalSurfaceWaterInputData():
    if st.session_state.localSurfaceWaterChoice == '2020 UWMP reported values':
        st.session_state.localSurfaceWaterRadioButtonIndex = 0
    else:
        st.session_state.localSurfaceWaterRadioButtonIndex = 1
        st.session_state.localSurfaceWaterdf = fetch_data("inputData/supplyInput_Surface.csv")

def setGroundwaterInputData():
    if st.session_state.groundwaterChoice == '2020 UWMP reported values':
        st.session_state.groundwaterRadioButtonIndex = 0
    else:
        st.session_state.groundwaterRadioButtonIndex = 1
        st.session_state.groundwaterdf = fetch_data("inputData/supplyInput_Groundwater.csv")

def setDesalinationInputData():
    if st.session_state.desalinationChoice == '2020 UWMP reported values':
        st.session_state.desalinationRadioButtonIndex = 0
    else:
        st.session_state.desalinationRadioButtonIndex = 1
        st.session_state.desalinationdf = fetch_data("inputData/supplyInput_Desalination.csv")

def setRecyclingInputData():
    if st.session_state.recyclingChoice == '2020 UWMP reported values':
        st.session_state.recyclingRadioButtonIndex = 0
    else:
        st.session_state.recyclingRadioButtonIndex = 1
        st.session_state.recyclingdf = fetch_data("inputData/supplyInput_Recycled.csv")

def setPotableReuseInputData():
    if st.session_state.potableReuseChoice == '2020 UWMP reported values':
        st.session_state.potableReuseRadioButtonIndex = 0
    else:
        st.session_state.potableReuseRadioButtonIndex = 1
        st.session_state.potableReusedf = fetch_data("inputData/supplyInput_PotableReuse.csv")

def setContractualTransfersInputData():
    if st.session_state.contractualTransfersChoice == '2020 UWMP reported values':
        st.session_state.contractualTransfersRadioButtonIndex = 0
    else:
        st.session_state.contractualTransfersRadioButtonIndex = 1
        st.session_state.contractualTransfersdf = fetch_data("inputData/supplyInput_ContractualTransfers.csv")

def setotherImportedSuppliesInputData():
    if st.session_state.otherImportedSuppliesChoice == '2020 UWMP reported values':
        st.session_state.otherImportedSuppliesRadioButtonIndex = 0
    else:
        st.session_state.otherImportedSuppliesRadioButtonIndex = 1
        st.session_state.otherImportedSuppliesdf = fetch_data("inputData/supplyInput_OtherImported.csv")

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

    groundwaterDatasetOptions = ['2020 UWMP reported values', 'User-defined values in table below']
    st.radio("2. Select the Groundwater Dataset from the options below. If the last option is selected, update the data in the Groundwater Supply table in the second collapsible section below.", options = groundwaterDatasetOptions, index = st.session_state.groundwaterRadioButtonIndex, key = "groundwaterChoice", on_change = setGroundwaterInputData)

    desalinationDatasetOptions = ['2020 UWMP reported values', 'User-defined values in table below']
    st.radio("3. Select the Desalination Dataset from the options below. If the last option is selected, update the data in the Desalination Supply table in the second collapsible section below.", options = desalinationDatasetOptions, index = st.session_state.desalinationRadioButtonIndex, key = "desalinationChoice", on_change = setDesalinationInputData)

    recyclingDatasetOptions = ['2020 UWMP reported values', 'User-defined values in table below']
    st.radio("4. Select the Recycling Dataset from the options below. If the last option is selected, update the data in the Recycling Supply table in the second collapsible section below.", options = recyclingDatasetOptions, index = st.session_state.recyclingRadioButtonIndex, key = "recyclingChoice", on_change = setRecyclingInputData)

    potableReuseDatasetOptions = ['2020 UWMP reported values', 'User-defined values in table below']
    st.radio("5. Select the Potable Reuse Dataset from the options below. If the last option is selected, update the data in the Potable Reuse Supply table in the second collapsible section below.", options = potableReuseDatasetOptions, index = st.session_state.potableReuseRadioButtonIndex, key = "potableReuseChoice", on_change = setPotableReuseInputData)

    contractualTransfersDatasetOptions = ['2020 UWMP reported values', 'User-defined values in table below']
    st.radio("6. Select the Contractual Transfers Dataset from the options below. If the last option is selected, update the data in the Contractual Transfers Supply table in the second collapsible section below.", options = contractualTransfersDatasetOptions, index = st.session_state.contractualTransfersRadioButtonIndex, key = "contractualTransfersChoice", on_change = setContractualTransfersInputData)

    otherImportedSuppliesDatasetOptions = ['2020 UWMP reported values', 'User-defined values in table below']
    st.radio("7. Select the Other Imported Supplies Dataset from the options below. If the last option is selected, update the data in the Other Imported Supplies table in the second collapsible section below.", options = otherImportedSuppliesDatasetOptions, index = st.session_state.otherImportedSuppliesRadioButtonIndex, key = "otherImportedSuppliesChoice", on_change = setotherImportedSuppliesInputData)

    swpCVPDatasetOptions = ['2020 UWMP reported values', 'Calsim II 2020 Benchmark Study', 'Calsim 3 <Study TBD>']
    st.radio("8. Select the SWP CVP Dataset from the options below. If the last option is selected, update the data in the SWP CVP Supply table in the second collapsible section below.", options = swpCVPDatasetOptions, index = st.session_state.swpCVPRadioButtonIndex, key = "swpCVPChoice", on_change = setSWPCVPInputData)

    costBySupplyTypeDatasetOptions = ['Default values from various references', 'User-defined values in table below']
    st.radio("9. Select the Cost by Supply Type Dataset from the options below. If the last option is selected, update the data in the Cost by Supply Type Supply table in the second collapsible section below.", options = costBySupplyTypeDatasetOptions, index = st.session_state.costBySupplyTypeRadioButtonIndex, key = "costBySupplyTypeChoice", on_change = setCostBySupplyTypeInputData)

    supplyPriorityDatasetOptions = ['Default values from various references', 'User-defined values in table below']
    st.radio("""10. Select the Supply Priority Dataset from the options below. If the last option is selected, 
    update the data in the Supply Priority Scenarios table in the first collapsible section below.""", options = supplyPriorityDatasetOptions, index = st.session_state.supplyPriorityRadioButtonIndex, key = "supplyPriorityChoice", on_change = setSupplyPriorityInputData)
