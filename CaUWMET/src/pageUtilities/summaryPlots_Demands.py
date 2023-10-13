from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd 

#---------------------------------------------------------------#
# SUMMARY POSTER FOR TOTAL DEMAND SCENARIOS
#---------------------------------------------------------------#

def displaySummaryPlotsTotalDemandScenarios(df, explanationText):
    st.write(explanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor', 'Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Normal or Better Demands (AFY)', 'Single Dry-Year Demands (AFY)','Multiple Dry-Year Demands (AFY)']

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        plotInputData['Type'] == vars[2],
        ]
    numberOfVars = [0, 1, 2]
    selectBoxKey = "Total Demands Selectbox"

    plotTypeChoice_totalDemands = st.selectbox('View total demands data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_totalDemands == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_totalDemands, plotInputData)

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR TOTAL USE BY TYPE
    #---------------------------------------------------------------#

def displaySummaryPlotsWaterUseByType(df, explanationText):
    st.write(explanationText)

    # Set up variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor','Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = [
        'Single Family Residential Use (AFY)', 
        'Multi-Family Residential Use (AFY)',
        'Industrial Use (AFY)',
        'Commercial and Governmental Use (AFY)',
        'Agricultural Use (AFY)',
        'Landscape Use (AFY)',
        'Other Use (AFY) (i.e. Losses, groundwater recharge, sales to other agencies etc.)'
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
    selectBoxKey = "Use By Type Selectbox"

    plotTypeChoice_demandsByUseType = st.selectbox('View demands by use type data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_demandsByUseType == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_demandsByUseType, plotInputData)

    #---------------------------------------------------------------#
    # CREATE SUMMARY POSTER FOR BASE LONG-TERM CONSERVATION
    #---------------------------------------------------------------#

def displaySummaryPlotsBaseLongTermConservation(df, explanationText):    
    st.write(explanationText)

    # Set up variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor','Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = [
        'Planned Long-term Conservation (AFY)'
        ]

    varsForLabel = [
        plotInputData['Type'] == vars[0]
        ]
    numberOfVars = [0]
    selectBoxKey = "Planned Long-term Conservation Selectbox"

    plotTypeChoice_demandsByUseType = st.selectbox('View planned long-term conservation data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_demandsByUseType == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_demandsByUseType, plotInputData)
