from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd 

#---------------------------------------------------------------#
# SUMMARY POSTER FOR CONTINGENCY CONSERVATION CAMPAIGNS
#---------------------------------------------------------------#

def displaySummaryPlotsContingencyConservationCampaign(df, explanationText):
    st.write(explanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor', 'Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Use Reduction with Contingency Conservation Campaign (% of Total Applied Use)', 'Contingency Conservation Publicity Campaign Cost ($/capita)','Urban Population (thousands)', 'Storage Volume Trigger for Contingency Conservation (AF)']

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        plotInputData['Type'] == vars[2],
        plotInputData['Type'] == vars[3],
        ]
    numberOfVars = [0, 1, 2, 3]
    selectBoxKey = "Contingency Conservation Selectbox"

    plotTypeChoice_contingencyConservation = st.selectbox('View total demands data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_contingencyConservation == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_contingencyConservation, plotInputData)
  
#---------------------------------------------------------------#
# SUMMARY POSTER FOR WATER MARKET TRANSFERS
#---------------------------------------------------------------#

def displaySummaryPlotsWaterMarketTransfers(df, explanationText):
    st.write(explanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor', 'Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Shortage Threshold before Water Market Transfer Supplies are Delivered (% of Total Applied Use)', 
            'Water Market Transfer Loss Factor (%)',
            'Transfer Limit for Normal or Better Years (acre-feet/year)', 
            'Transfer Limit for Dry Years (acre-feet/year)',
            'Transfer Limit for 2 or More Consecutive Years (% of Dry-Year limit defined above)',
            'Wet Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)',
            'Above Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)',
            'Below Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)',
            'Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)',
            'Critically Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)']

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        plotInputData['Type'] == vars[2],
        plotInputData['Type'] == vars[3],
        plotInputData['Type'] == vars[4],
        plotInputData['Type'] == vars[5],
        plotInputData['Type'] == vars[6],
        plotInputData['Type'] == vars[7],
        plotInputData['Type'] == vars[8],
        plotInputData['Type'] == vars[9],
        ]
    numberOfVars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    selectBoxKey = "Water Market Transfers Selectbox"

    plotTypeChoice_waterMarketTransfers = st.selectbox('View water market transfers data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_waterMarketTransfers == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_waterMarketTransfers, plotInputData)

  
#---------------------------------------------------------------#
# SUMMARY POSTER FOR RATIONING PROGRAMS
#---------------------------------------------------------------#

def displaySummaryPlotsRationingPrograms(df, explanationText):
    st.write(explanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor', 'Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Storage Volume Trigger for Rationing Programs (acre-feet)', 
            'Cost for Rationing Program ($/capita)',
            'Cut Ratios', 
            'Demand Hardening Adjustment Factor (%)',
            'Elasticity of Demand',
            'Retail Price'
            ]

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        plotInputData['Type'] == vars[2],
        plotInputData['Type'] == vars[3],
        plotInputData['Type'] == vars[4],
        plotInputData['Type'] == vars[5]
        ]
    numberOfVars = [0, 1, 2, 3, 4, 5]
    selectBoxKey = "Rationing Programs Selectbox"

    plotTypeChoice_rationingProgram = st.selectbox('View rationing program assumptions for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_rationingProgram == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_rationingProgram, plotInputData)