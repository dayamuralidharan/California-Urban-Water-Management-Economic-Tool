from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd




def displaySummaryPlots_excessSupplySwitch(): 
    st.write(excessWaterSwitchExplanationText)
    st.table(st.session_state.excessWaterSwitch)

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR CARRYOVER STORAGE SYSTEM OPERATIONS
    #---------------------------------------------------------------#

def displaySummaryPlots_carryoverStorage(): 
    st.write(carryoverStorageExplanationText)

    # Set up variables for summary poster plots
    plotInputData = st.session_state.surfaceCarryover[['Variable', 'Study Region','Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor','Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Surface max storage capacity (acre-feet)',
                         'Surface initial storage (acre-feet)',
                         'Surface max put capacity (AFY)',
                         'Surface max take capacity (AFY)',
                         'Surface take loss (AFY)',
                         ]

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        plotInputData['Type'] == vars[2],
        plotInputData['Type'] == vars[3],
        plotInputData['Type'] == vars[4],
        ]
    numberOfVars = [0, 1, 2, 3, 4]
    boxKey = "Surface Carryover Storage Selectbox"
    piePlotLabel = "Surface Carryover Storage by Study Region"
    barPlotLabel = "Surface Carryover Storage by Contractor"
    barPlotXAxisLabel = "Surface Carryover Storage (acre-feet/year)"
    plotColors = ['#F63366', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B']

    plotTypeChoice_surfaceCarryover = st.selectbox('View surface carryover storage data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_surfaceCarryover == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, boxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel, plotColors)
    else:
        displayDataForOneContractor(plotTypeChoice_surfaceCarryover, plotInputData)
    

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR GROUNDWATER BANKING SYSTEM OPERATIONS
    #---------------------------------------------------------------#

def displaySummaryPlots_groundwaterBank(): 
    st.write(groundwaterBankExplanationText)

    # Set up variables for summary poster plots
    plotInputData = st.session_state.groundwaterBank[['Variable', 'Study Region','Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor','Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Groundwater Max Storage Capacity (acre-feet)',
                         'Groundwater Initial Storage Volume (acre-feet)',
                         'Groundwater Max Put Capacity (AFY)',
                         'Groundwater Max Take Capacity (AFY)',
                         'Recharge Effectiveness (%)',
                         ]

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        plotInputData['Type'] == vars[2],
        plotInputData['Type'] == vars[3],
        plotInputData['Type'] == vars[4],
        ]
    numberOfVars = [0, 1, 2, 3, 4]
    boxKey = "Groundwater Bank Storage Selectbox"
    piePlotLabel = "Groundwater Bank Storage by Study Region"
    barPlotLabel = "Groundwater Bank Storage by Contractor"
    barPlotXAxisLabel = "Groundwater Bank Storage (acre-feet/year)"
    plotColors = ['#F63366', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B']

    plotTypeChoice_surfaceCarryover = st.selectbox('View groundwater bank storage data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_surfaceCarryover == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, boxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel, plotColors)
    else:
        displayDataForOneContractor(plotTypeChoice_surfaceCarryover, plotInputData)


excessWaterSwitchExplanationText = ''  
carryoverStorageExplanationText = '' 
groundwaterBankExplanationText = '' 
storageHedgingStrategyExplanationText = '' 
storageCostsExplanationText = '' 
deliveryCostsExplanationText = '' 