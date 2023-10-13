from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd 

#---------------------------------------------------------------#
# SUMMARY POSTER FOR LONG-TERM WMO AVAILABLE SUPPLY VOLUMES
#---------------------------------------------------------------#

def displaySummaryPlots_longtermWMOVolumes(df, explanationText):
    st.write(explanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor', 'Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = ['Surface Water Supply Volume (acre-feet/year)', 
            'Groundwater Supply Volume (acre-feet/year)',
            'Desalination Supply Volume (acre-feet/year)',
            'Recycled Supply Volume (acre-feet/year)',
            'Potable Reuse Supply Volume (acre-feet/year)',
            'Transfers and Exchanges Supply Volume (acre-feet/year)',
            'Other Supply Volume (acre-feet/year)',
            'Additional Conservation Volume (acre-feet/year)'
            ]

    varsForLabel = [
        plotInputData['Type'] == vars[0],
        plotInputData['Type'] == vars[1],
        plotInputData['Type'] == vars[2],
        plotInputData['Type'] == vars[3],
        plotInputData['Type'] == vars[4],
        plotInputData['Type'] == vars[5],
        plotInputData['Type'] == vars[6],
        plotInputData['Type'] == vars[7]
        ]
    numberOfVars = [0, 1, 2, 3, 4, 5, 6, 7]
    selectBoxKey = "Long-term WMOs Selectbox"

    plotTypeChoice_longtermWMOVolumes = st.selectbox('View long-term WMO volume data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_longtermWMOVolumes == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_longtermWMOVolumes, plotInputData)

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR LONG-TERM WMO COSTS
    #---------------------------------------------------------------#

def displaySummaryPlots_longtermWMOCosts(df, explanationText):
    st.write(explanationText)

    # Set up variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor','Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = [
        'Surface Supply Incremental Cost ($/acre-foot)', 
        'Groundwater Supply Incremental Cost ($/acre-foot)',
        'Desalination Supply Incremental Cost ($/acre-foot)',
        'Recycled Supply Incremental Cost ($/acre-foot)',
        'Potable Reuse Supply Incremental Cost ($/acre-foot)',
        'Long-term Contracts for Transfers and Exchanges Supply Incremental Cost ($/acre-foot)',
        'Other Supply Type Incremental Cost ($/acre-foot)',
        'Additional Conservation Incremental Cost ($/acre-foot)',
        'Surface Supply Base Cost ($/acre-foot)',
        'Groundwater Supply Base Cost ($/acre-foot)',
        'Desalination Supply Base Cost ($/acre-foot)',
        'Recycled Supply Base Cost ($/acre-foot)',
        'Potable Reuse Supply Base Cost ($/acre-foot)',
        'Long-term Contracts for Transfers and Exchanges Supply Base Cost ($/acre-foot)',
        'Other Supply Type Base Cost ($/acre-foot)',
        'Additional Conservation Base Cost ($/acre-foot)'
        ]

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
        plotInputData['Type'] == vars[10],
        plotInputData['Type'] == vars[11],
        plotInputData['Type'] == vars[12],
        plotInputData['Type'] == vars[13],
        plotInputData['Type'] == vars[14],
        plotInputData['Type'] == vars[15]
        ]
    numberOfVars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    selectBoxKey = "Long-term WMO Costs Selectbox"


    plotTypeChoice_longtermWMOCosts = st.selectbox('View long-term WMO costs data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_longtermWMOCosts == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_longtermWMOCosts, plotInputData)