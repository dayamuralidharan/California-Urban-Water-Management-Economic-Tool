from src.systemOperationsHelper import displayPieAndBarPlots, excessWaterSwitchExplanationText,  carryoverStorageExplanationText, carryoverStorageCostsExplanationText, transfersExplanationText, transfersCostExplanationText
import streamlit as st
import pandas as pd

def displaySummaryPlots(): 
    st.header("System Operation Assumptions Overview")

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR EXCESS WATER SWITCH SYSTEM OPERATIONS
    #---------------------------------------------------------------#

    # st.subheader("Excess Water Switch Scenarios")
    # st.write(excessWaterSwitchExplanationText)

    # Set up excess water switch variables for summary poster plots
    # excessWaterSwitchPlotInputData = st.session_state.excessWaterSwitchdf[['Variable', contractorsList]]
    # excessWaterSwitchPlotInputData = pd.melt(excessWaterSwitchPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    # excessWaterSwitchPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    # excesssWaterSwitchVars = ['Excess Water Switch']

    # excesssWaterSwitchVarsForLabel = [
    #     excessWaterSwitchPlotInputData['Type'] == excesssWaterSwitchVars[0],
    #     ]
    # excesssWaterSwitchNumberOfVars = [0]
    # excesssWaterSwitchBoxKey = "Excess Water Switch System Operations Selectbox"
    # excesssWaterSwitchPiePlotLabel = "Excess Water Switch System Operations by Study Region"
    # excesssWaterSwitchBarPlotLabel = "Excess Water Switch System Operations by Contractor"
    # excesssWaterSwitchBarPlotXAxisLabel = "Excess Water Switch"
    # excesssWaterSwitchColors = ['#F63366']

    # displayPieAndBarPlots(excesssWaterSwitchVars, excesssWaterSwitchVarsForLabel, excesssWaterSwitchNumberOfVars, excessWaterSwitchPlotInputData, excesssWaterSwitchBoxKey, excesssWaterSwitchPiePlotLabel, excesssWaterSwitchPiePlotLabel, excesssWaterSwitchBarPlotXAxisLabel, excesssWaterSwitchColors)

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR CARRYOVER STORAGE SYSTEM OPERATIONS
    #---------------------------------------------------------------#

    st.subheader("Carryover Storage Scenarios")
    st.write(carryoverStorageExplanationText)

    # Set up carryover storage variables for summary poster plots
    carryoverStoragePlotInputData = st.session_state.carryoverStoragedf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    carryoverStoragePlotInputData = pd.melt(carryoverStoragePlotInputData, id_vars=['Variable','Contractor','Study Region'])
    carryoverStoragePlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    carryoverStorageVars = ['Surface max storage capacity (acre-feet)',
                         'Surface initial storage (acre-feet)',
                         'Surface max put capacity (acre-feet)',
                         'Surface max take capacity (acre-feet)',
                         'Surface take loss (% of take)',
                         'Groundwater max storage capacity (acre-feet)',
                         'Groundwater initial storage (acre-feet)',
                         'Groundwater max put capacity (acre-feet)',
                         'Groundwater max take capacity (acre-feet)',
                         'Groundwater put loss (% of put)',
                         'Groundwater take loss (% of take)',
                         ]

    carryoverStorageVarsForLabel = [
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[0],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[1],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[2],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[3],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[4],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[5],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[6],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[7],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[8],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[9],
        carryoverStoragePlotInputData['Type'] == carryoverStorageVars[10],
        ]
    carryoverStorageNumberOfVars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    carryoverStorageBoxKey = "Supplies Selectbox"
    carryoverStoragePiePlotLabel = "Supplies by Study Region"
    carryoverStorageBarPlotLabel = "Supplies by Contractor"
    carryoverStorageBarPlotXAxisLabel = "Supplies (acre-feet/year)"
    carryoverStorageColors = ['#F63366', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B']

    displayPieAndBarPlots(carryoverStorageVars, carryoverStorageVarsForLabel, carryoverStorageNumberOfVars, carryoverStoragePlotInputData, carryoverStorageBoxKey, carryoverStoragePiePlotLabel, carryoverStorageBarPlotLabel, carryoverStorageBarPlotXAxisLabel, carryoverStorageColors)

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR CARRYOVER STORAGE SYSTEM OPERATIONS COSTS
    #---------------------------------------------------------------#

    st.subheader("Carryover Storage Costs Scenarios")
    st.write(carryoverStorageCostsExplanationText)

    # Set up carryover storage costs variables for summary poster plots
    carryoverStorageCostsPlotInputData = st.session_state.carryoverStorageCostdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    carryoverStorageCostsPlotInputData = pd.melt(carryoverStorageCostsPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    carryoverStorageCostsPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    carryoverStorageCostsVars = ['Surface put cost ($/acre-feet)',
                         'Surface take cost ($/acre-feet)',
                         'Groundwater put cost ($/acre-feet)',
                         'Groundwater take cost ($/acre-feet)',
                         ]

    carryoverStorageCostsVarsForLabel = [
        carryoverStorageCostsPlotInputData['Type'] == carryoverStorageCostsVars[0],
        carryoverStorageCostsPlotInputData['Type'] == carryoverStorageCostsVars[1],
        carryoverStorageCostsPlotInputData['Type'] == carryoverStorageCostsVars[2],
        carryoverStorageCostsPlotInputData['Type'] == carryoverStorageCostsVars[3],
        ]
    carryoverStorageCostsNumberOfVars = [0, 1, 2, 3]
    carryoverStorageCostsBoxKey = "Carryover Costs Storage Selectbox"
    carryoverStorageCostsPiePlotLabel = "Carryover Storage Costs by Study Region"
    carryoverStorageCostsBarPlotLabel = "Carryover Storage Costs by Contractor"
    carryoverStorageCostsBarPlotXAxisLabel = "Carryover Storage Costs ($/acre-feet)"
    carryoverStorageCostsColors = ['#F63366', '#2BB1BB', '#22466B', '#2BB1BB']

    displayPieAndBarPlots(carryoverStorageCostsVars, carryoverStorageCostsVarsForLabel, carryoverStorageCostsNumberOfVars, carryoverStorageCostsPlotInputData, carryoverStorageCostsBoxKey, carryoverStorageCostsPiePlotLabel, carryoverStorageCostsBarPlotLabel, carryoverStorageCostsBarPlotXAxisLabel, carryoverStorageCostsColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR TRANSFERS SYSTEM OPERATIONS
    #---------------------------------------------------------------#

    st.subheader("Transfer Scenarios")
    st.write(transfersExplanationText)

    # Set up transfers variables for summary poster plots
    transfersPlotInputData = st.session_state.transfersdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    transfersPlotInputData = pd.melt(transfersPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    transfersPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    transfersVars = ['Max Transfer Capacity (acre-feet/year)']

    transfersVarsForLabel = [
        transfersPlotInputData['Type'] == transfersVars[0],
        ]
    transfersNumberOfVars = [0]
    transfersBoxKey = "Transfers Selectbox"
    transfersPiePlotLabel = "Transfers by Study Region"
    transfersBarPlotLabel = "Transfers by Contractor"
    transfersBarPlotXAxisLabel = "Max transfer capacity (acre-feet/year)"
    transfersColors = ['#F63366']

    displayPieAndBarPlots(transfersVars, transfersVarsForLabel, transfersNumberOfVars, transfersPlotInputData, transfersBoxKey, transfersPiePlotLabel, transfersBarPlotLabel, transfersBarPlotXAxisLabel, transfersColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR TRANSFERS SYSTEM OPERATIONS COST
    #---------------------------------------------------------------#

    st.subheader("Transfer Cost Scenarios")
    st.write(transfersCostExplanationText)

    # Set up transfers cost variables for summary poster plots
    transfersCostPlotInputData = st.session_state.transfersCostdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    transfersCostPlotInputData = pd.melt(transfersCostPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    transfersCostPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    transfersCostVars = ['Max Transfer Capacity Cost ($/acre-feet)']

    transfersCostVarsForLabel = [
        transfersCostPlotInputData['Type'] == transfersCostVars[0],
        ]
    transfersCostNumberOfVars = [0]
    transfersCostBoxKey = "Transfers Cost Selectbox"
    transfersCostPiePlotLabel = "Transfers Cost by Study Region"
    transfersCostBarPlotLabel = "Transfers Cost by Contractor"
    transfersCostBarPlotXAxisLabel = "Transfer Cost ($/acre-feet)"
    transfersCostColors = ['#F63366']

    displayPieAndBarPlots(transfersCostVars, transfersCostVarsForLabel, transfersCostNumberOfVars, transfersCostPlotInputData, transfersCostBoxKey, transfersCostPiePlotLabel, transfersCostBarPlotLabel, transfersCostBarPlotXAxisLabel, transfersCostColors)