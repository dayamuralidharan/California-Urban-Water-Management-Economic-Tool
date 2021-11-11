import streamlit as st
from globalUtilities import fetch_data

# Functions to set which option from the radio selector inputs are chosen and UWMP values if that is the chosen dataset.
# These functions are called in the last function defined in this page, "setSupplyDatasetsFromRadioButtons" which gets called in the supplies.py file.
#TODO abstract radio buttons out to list that is called in each function.

def setExcessWaterSwitchInputData():
    if st.session_state.excessWaterSwitchChoice == 'Default values':
        st.session_state.excessWaterSwitchRadioButtonIndex = 0
        st.session_state.excessWaterSwitchdf = fetch_data("inputData/systemOperationsInput_ExcessWaterSwitch.csv")
    else:
        st.session_state.excessWaterSwitchRadioButtonIndex = 1
        # Dataframe for editable table set in the systemoperations.py file instead of here.

def setCarryoverStorageInputData():
    if st.session_state.carryoverStorageChoice == 'Default values':
        st.session_state.carryoverStorageRadioButtonIndex = 0
        st.session_state.carryoverStoragedf = fetch_data("inputData/systemOperationsInput_CarryoverStorage.csv")
    else:
        st.session_state.carryoverStorageRadioButtonIndex = 1
        # Dataframe for editable table set in the systemoperations.py file instead of here.

def setCarryoverStorageCostInputData():
    if st.session_state.carryoverStorageCostChoice == 'Default values':
        st.session_state.carryoverStorageCostRadioButtonIndex = 0
        st.session_state.carryoverStorageCostdf = fetch_data("inputData/systemOperationsInput_CarryoverStorageCost.csv")
    else:
        st.session_state.carryoverStorageCostRadioButtonIndex = 1
        # Dataframe for editable table set in the systemoperations.py file instead of here.
        
def setTransfersPriorityInputData():
    if st.session_state.transfersChoice == 'Default values':
        st.session_state.transfersRadioButtonIndex = 0
        st.session_state.transfersdf = fetch_data("inputData/systemOperationsInput_Transfers.csv")
    else:
        st.session_state.transfersRadioButtonIndex = 1
        # Dataframe for editable table set in the systemoperations.py file instead of here.
        
def setTransfersCostPriorityInputData():
    if st.session_state.transfersCostChoice == 'Default values':
        st.session_state.transfersCostRadioButtonIndex = 0
        st.session_state.transfersCostdf = fetch_data("inputData/systemOperationsInput_TransfersCost.csv")
    else:
        st.session_state.transfersCostRadioButtonIndex = 1
        # Dataframe for editable table set in the systemoperations.py file instead of here.

def setSystemOperationsDatasetsFromRadioButtons():
    excessWaterSwitchDatasetOptions = ['Default values', 'User-defined values in table below']
    st.radio("1. Select the Excess Water Switch Dataset from the options below. If the last option is selected, update the data in the Excess Water Switch table in the second collapsible section below.", options = excessWaterSwitchDatasetOptions, index = st.session_state.excessWaterSwitchRadioButtonIndex, key = "excessWaterSwitchChoice", on_change = setExcessWaterSwitchInputData)

    carryoverStorageDatasetOptions = ['Default values', 'User-defined values in table below']
    st.radio("2. Select the Carryover Storage Dataset from the options below. If the last option is selected, update the data in the Carryover Storage table in the second collapsible section below.", options = carryoverStorageDatasetOptions, index = st.session_state.swpCVPRadioButtonIndex, key = "carryoverStorageChoice", on_change = setCarryoverStorageInputData)

    carryoverStorageCostDatasetOptions = ['Default values', 'User-defined values in table below']
    st.radio("3. Select the Carryover Storage Cost Dataset from the options below. If the last option is selected, update the data in the Carryover Storage Cost table in the second collapsible section below.", options = carryoverStorageCostDatasetOptions, index = st.session_state.costBySupplyTypeRadioButtonIndex, key = "carryoverStorageCostChoice", on_change = setCarryoverStorageCostInputData)

    transfersPriorityDatasetOptions = ['Default values', 'User-defined values in table below']
    st.radio("""4. Select the Transfers Dataset from the options below. If the last option is selected, 
    update the data in the Transfers table in the first collapsible section below.""", options = transfersPriorityDatasetOptions, index = st.session_state.transfersRadioButtonIndex, key = "transfersChoice", on_change = setTransfersPriorityInputData)

    transfersCostPriorityDatasetOptions = ['Default values', 'User-defined values in table below']
    st.radio("""5. Select the Transfers Cost Dataset from the options below. If the last option is selected, 
    update the data in the Transfers Cost table in the first collapsible section below.""", options = transfersCostPriorityDatasetOptions, index = st.session_state.transfersCostRadioButtonIndex, key = "transfersCostChoice", on_change = setTransfersCostPriorityInputData)
