from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd

#---------------------------------------------------------------#
# SUMMARY POSTER FOR LOCAL AND REGIONAL SUPPLIES
#---------------------------------------------------------------#

def displaySummaryPlots_localAndRegionalSupplies(df, explanationText): 
    st.write(explanationText)

    # Set up total demand variables for summary poster plots
    localSuppliesPlotInputData = df[['Variable', 'Study Region','Contractor', int(st.session_state.futurePlanningYear)]]
    localSuppliesPlotInputData = pd.melt(localSuppliesPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    localSuppliesPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    localSuppliesVars = ['Surface for Normal or Better Years (acre-feet/year)',
                         'Surface for Single Dry Years (acre-feet/year)',
                         'Surface for Multiple Dry Years (acre-feet/year)',
                         'Groundwater for Normal or Better Years (acre-feet/year)',
                         'Groundwater for Single Dry Years (acre-feet/year)',
                         'Groundwater for Multiple Dry Years (acre-feet/year)',
                         'Recycled for Normal or Better Years (acre-feet/year)',
                         'Recycled for Single Dry Years (acre-feet/year)',
                         'Recycled for Multiple Dry Years (acre-feet/year)',
                         'Potable Reuse for Normal or Better Years (acre-feet/year)',
                         'Potable Reuse for Single Dry Years (acre-feet/year)',
                         'Potable Reuse for Multiple Dry Years (acre-feet/year)',
                         'Desalination for Normal or Better Years (acre-feet/year)',
                         'Desalination for Single Dry Years (acre-feet/year)',
                         'Desalination for Multiple Dry Years (acre-feet/year)',
                         'Transfers and Exchanges for Normal or Better Years (acre-feet/year)',
                         'Transfers and Exchanges for Single Dry Years (acre-feet/year)',
                         'Transfers and Exchanges for Multiple Dry Years (acre-feet/year)',
                         'Other Supply Types for Normal or Better Years (acre-feet/year)',
                         'Other Supply Types for Single Dry Years (acre-feet/year)',
                         'Other Supply Types for Multiple Dry Years (acre-feet/year)',
                         ]

    localSuppliesVarsForLabel = [
        localSuppliesPlotInputData['Type'] == localSuppliesVars[0],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[1],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[2],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[3],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[4],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[5],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[6],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[7],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[8],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[9],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[10],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[11],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[12],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[13],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[14],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[15],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[16],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[17],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[18],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[19],
        localSuppliesPlotInputData['Type'] == localSuppliesVars[20],
        ]
    numberOfVars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    boxKey = "Supplies Selectbox"

    plotTypeChoice_localRegionalSupplies = st.selectbox('View local and regional supply data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_localRegionalSupplies == 'All Contractors':
        displayPieAndBarPlots(localSuppliesVars, localSuppliesVarsForLabel, numberOfVars, localSuppliesPlotInputData, boxKey)
    else:
        displayDataForOneContractor(plotTypeChoice_localRegionalSupplies, localSuppliesPlotInputData)
    
    
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR SWP CVP SUPPLIES
    #---------------------------------------------------------------#

    st.subheader("SWP and CVP Supply Scenarios")
    st.write(explanationText)
