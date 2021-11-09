import streamlit as st
from globalUtilities import fetch_data

# Functions to set which option from the radio selector inputs are chosen and UWMP values if that is the chosen dataset.
# These functions are called in the last function defined in this page, "setSupplyDatasetsFromRadioButtons" which gets called in the supplies.py file.
#TODO abstract radio buttons out to list that is called in each function.

def setLocalSuppliesInputData():
    if st.session_state.localSuppliesDataChoice == '2020 UWMP reported values':
        st.session_state.localSuppliesRadioButtonIndex = 0
        st.session_state.localSuppliesdf = fetch_data("inputData/supplyInput_localSupplies.csv")
    else:
        st.session_state.localSuppliesRadioButtonIndex = 1
        # Dataframe for editable table set in the supplies.py file instead of here.

def setSWPCVPInputData():
    if st.session_state.swpCVPSupplyChoice == 'Calsim II 2020 Benchmark Study':
        st.session_state.swpCVPRadioButtonIndex = 0
        st.session_state.swpCVPSuppliesdf = fetch_data("inputData/supplyInput_SWPCVPCalsimII2020BenchmarkStudy.csv")
    elif st.session_state.swpCVPSupplyChoice == 'Calsim 3 <Study TBD>':
        st.session_state.swpCVPRadioButtonIndex = 1
        st.session_state.swpCVPSuppliesdf = fetch_data("inputData/supplyInput_SWPCVPCalsim3.csv")
    else:
        st.session_state.swpCVPRadioButtonIndex = 2
        # Dataframe for editable table set in the supplies.py file instead of here.

def setCostBySupplyTypeInputData():
    if st.session_state.costBySupplyTypeChoice == 'Default values from various references (see Section X for more information)':
        st.session_state.costBySupplyTypeRadioButtonIndex = 0
        st.session_state.costBySupplyTypedf = fetch_data("inputData/supplyInput_costsBySupplyType.csv")
    else:
        st.session_state.costBySupplyTypeRadioButtonIndex = 1
        # Dataframe for editable table set in the supplies.py file instead of here.

def setSupplyPriorityInputData():
    if st.session_state.supplyPriorityChoice == 'Default values':
        st.session_state.supplyPriorityRadioButtonIndex = 0
        st.session_state.supplyPrioritydf = fetch_data("inputData/supplyInput_supplyPriorities.csv")
    else:
        st.session_state.supplyPriorityRadioButtonIndex = 1
        # Dataframe for editable table set in the supplies.py file instead of here.

def setSupplyDatasetsFromRadioButtons():
    localSuppliesDatasetOptions = ['2020 UWMP reported values', 'User-defined values in table below']
    st.radio("1. Select the Local Surface Water Dataset from the options below. If the last option is selected, update the data in the Local Surface Water Supply table in the second collapsible section below.", options = localSuppliesDatasetOptions, index = st.session_state.localSuppliesRadioButtonIndex, key = "localSuppliesDataChoice", on_change = setLocalSuppliesInputData)

    swpCVPDatasetOptions = ['Calsim II 2020 Benchmark Study', 'Calsim 3 <Study TBD>', 'User-defined values in table below']
    st.radio("8. Select the SWP CVP Dataset from the options below. If the last option is selected, update the data in the SWP CVP Supply table in the second collapsible section below.", options = swpCVPDatasetOptions, index = st.session_state.swpCVPRadioButtonIndex, key = "swpCVPSupplyChoice", on_change = setSWPCVPInputData)

    costBySupplyTypeDatasetOptions = ['Default values from various references (see Section X for more information)', 'User-defined values in table below']
    st.radio("9. Select the Cost by Supply Type Dataset from the options below. If the last option is selected, update the data in the Cost by Supply Type Supply table in the second collapsible section below.", options = costBySupplyTypeDatasetOptions, index = st.session_state.costBySupplyTypeRadioButtonIndex, key = "costBySupplyTypeChoice", on_change = setCostBySupplyTypeInputData)

    supplyPriorityDatasetOptions = ['Default values', 'User-defined values in table below']
    st.radio("""10. Select the Supply Priority Dataset from the options below. If the last option is selected, 
    update the data in the Supply Priority Scenarios table in the first collapsible section below.""", options = supplyPriorityDatasetOptions, index = st.session_state.supplyPriorityRadioButtonIndex, key = "supplyPriorityChoice", on_change = setSupplyPriorityInputData)
