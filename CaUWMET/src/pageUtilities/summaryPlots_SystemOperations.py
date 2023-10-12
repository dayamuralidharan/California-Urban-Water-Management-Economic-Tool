from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd


    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR EXCESS WATER MANAGEMENT SWITCH OPERATIONS
    #---------------------------------------------------------------#

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

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR EXCESS WATER MANAGEMENT SWITCH OPERATIONS
    #---------------------------------------------------------------#

def displaySummaryPlots_StorageHedgingStrategy():
    st.write(storageHedgingStrategyExplanationText)
    st.table(st.session_state.storageHedging)


    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR STORAGE OPERATIONS COSTS
    #---------------------------------------------------------------#

def displaySummaryPlots_storageOperationsCosts(): 
    st.write(storageCostsExplanationText)

    # Set up variables for summary poster plots
    plotInputData = st.session_state.storageCosts[['Variable', 'Study Region','Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor','Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Groundwater bank put cost ($/acre-feet)',
                         'Groundwater bank take cost ($/acre-feet)',
                         ]

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        ]
    numberOfVars = [0, 1]
    boxKey = "Storage Operations Costs Selectbox"
    piePlotLabel = "Costs by Study Region"
    barPlotLabel = "Costs by Contractor"
    barPlotXAxisLabel = "Cost ($/acre-feet)"
    plotColors = ['#F63366', '#2BB1BB']

    plotTypeChoice_storageCosts = st.selectbox('View storage cost data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_storageCosts == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, boxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel, plotColors)
    else:
        displayDataForOneContractor(plotTypeChoice_storageCosts, plotInputData)



    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR Delivery Costs
    #---------------------------------------------------------------#

def displaySummaryPlots_deliveryCosts(): 
    st.write(deliveryCostsExplanationText)

    # Set up variables for summary poster plots
    plotInputData = st.session_state.deliveryCosts[['Variable', 'Study Region','Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor','Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Groundwater Pumping (Single Dry or Better Year Types)',
                         'Groundwater Pumping (Multi-Dry Year Types)',
                         'SWP or CVP Delivery Costs ($/acre-foot)',
                         'Cost of M&I potable water treatment ($/acre-foot)',
                         'Cost of M&I Distribution ($/acre-foot)',
                         'Wastewater Treatment Cost ($/acre-foot)',
                         'Fraction of wastewater treated (%)',
                         ]

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        plotInputData['Type'] == vars[2],
        plotInputData['Type'] == vars[3],
        plotInputData['Type'] == vars[4],
        plotInputData['Type'] == vars[5],
        plotInputData['Type'] == vars[6],
        ]
    numberOfVars = [0, 1, 2, 3, 4, 5, 6]
    boxKey = "Delivery Cost Selectbox"
    piePlotLabel = "Delivery Cost by Study Region"
    barPlotLabel = "Delivery Cost by Contractor"
    barPlotXAxisLabel = "Delivery Cost ($/acre-foot)"
    plotColors = ['#F63366', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B']

    plotTypeChoice_deliveryCosts = st.selectbox('View delivery cost data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_deliveryCosts == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, boxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel, plotColors)
    else:
        displayDataForOneContractor(plotTypeChoice_deliveryCosts, plotInputData)
    



excessWaterSwitchExplanationText = ''  
carryoverStorageExplanationText = '' 
groundwaterBankExplanationText = '' 
storageHedgingStrategyExplanationText = '' 
storageCostsExplanationText = '' 
deliveryCostsExplanationText = '' 