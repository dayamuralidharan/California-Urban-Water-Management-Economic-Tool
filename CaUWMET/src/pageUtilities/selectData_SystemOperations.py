import streamlit as st
from src.globalUtilities import fetch_data

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


def setSystemOperationsDatasetsFromRadioButtons():
    excessWaterSwitchDatasetOptions = ['Default values', 'User-defined values in table below']
    st.radio("1. Select the Excess Water Switch Dataset from the options below. If the last option is selected, update the data in the Excess Water Switch table in the second collapsible section below.", options = excessWaterSwitchDatasetOptions, index = st.session_state.excessWaterSwitchRadioButtonIndex, key = "excessWaterSwitchChoice", on_change = setExcessWaterSwitchInputData)