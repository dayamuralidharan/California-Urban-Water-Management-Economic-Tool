import streamlit as st
from globalUtilities import fetch_data

# Functions to set which option from the radio selector inputs are chosen and UWMP values if that is the chosen dataset.
def setTotalDemandsInputData():
    if st.session_state.totalDemandsChoice == 'UWMP reported values':
        st.session_state.totalDemandScenarioRadioButtonIndex = 0
        st.session_state.totalDemandsdf = fetch_data("inputData/demandsInput_totalDemands.csv")
    elif st.session_state.totalDemandsChoice == 'ETAW adjusted demands':
        st.session_state.totalDemandScenarioRadioButtonIndex = 1
    else:
        st.session_state.totalDemandScenarioRadioButtonIndex = 2
        # Dataframe for editable table set in the demands.py file instead of here.

def setUseByTypeInputData():
    if st.session_state.useByTypeChoice == 'UWMP reported values':
        st.session_state.useByTypedf = fetch_data("inputData/demandsInput_useByTypeData.csv")
        st.session_state.useByTypeRadioButtonIndex = 0
    else:
        st.session_state.useByTypeRadioButtonIndex = 1
        # Dataframe for editable table set in the demands.py file instead of here.

def setIntExtUseByTypeInputData():
    if st.session_state.intExtUseByTypeChoice == 'UWMP reported values':
        st.session_state.intExtUseByTypePlotInputdf = fetch_data("inputData/demandsInput_intAndExtUseByTypeData.csv")
        st.session_state.intExtuseByTypeRadioButtonIndex = 0
    else:
        st.session_state.intExtUseByTypeRadioButtonIndex = 1
        # Dataframe for editable table set in the demands.py file instead of here.

def setBaseLongTermConservationInputData():
    if st.session_state.baseLongTermConservationChoice == 'UWMP reported values':
        st.session_state.intExtUseByTypePlotInputdf = fetch_data("inputData/demandsInput_baseLongTermConservationData.csv")
        st.session_state.baseLongTermConservationRadioButtonIndex = 0
    else:
        st.session_state.baseLongTermConservationRadioButtonIndex = 1
        # Dataframe for editable table set in the demands.py file instead of here.

def setDemandDatasetsFromRadioButtons():
    demandsDatasetOptions = ['UWMP reported values', 'ETAW adjusted demands', 'Input demands in table below']
    st.radio("""1. Select the Total Demand Scenario Dataset from the options below. If the last option is selected, 
    update the data in the Total Demand Scenarios table in the first collapsible section below.""", options = demandsDatasetOptions, index = st.session_state.totalDemandScenarioRadioButtonIndex, key = "totalDemandsChoice", on_change = setTotalDemandsInputData)

    useByTypeDatasetOptions = ['UWMP reported values', 'Input Use By Type in table below']
    st.radio("2. Select the Use by Type Dataset from the options below. If the last option is selected, update the data in the Demand Use by Type table in the second collapsible section below.", options = useByTypeDatasetOptions, index = st.session_state.useByTypeRadioButtonIndex, key = "useByTypeChoice", on_change = setUseByTypeInputData)

    intExtUseByTypeDatasetOptions = ['UWMP reported values', 'Input Use By Type in table below']
    st.radio("""3. Select the Input Interior and Exterior Use by Type Dataset from the options below. 
    If the last option is selected, update the data in the Interior and Exterior Use by Type table in the third collapsible section below.""", options = intExtUseByTypeDatasetOptions, index = st.session_state.intExtUseByTypeRadioButtonIndex, key = "intExtUseByTypeChoice", on_change = setIntExtUseByTypeInputData)

    baseLongTermConservationDatasetOptions = ['UWMP reported values', 'Input Conservation variables in table below']
    st.radio("""4. Select the Base Long-Term Conservation Dataset from the options below. 
    If the last option is selected, update the data in the Base Long Term Conservation table in the last collapsible section below.""", options = baseLongTermConservationDatasetOptions, index = st.session_state.baseLongTermConservationRadioButtonIndex, key = "baseLongTermConservationChoice", on_change = setBaseLongTermConservationInputData)
