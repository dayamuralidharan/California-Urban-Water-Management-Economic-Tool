from src.suppliesHelper import displayPieAndBarPlots, localSuppliesExplanationText,  swpCVPExplanationText, costBySupplyTypeExplanationText, supplyPriorityTypeExplanationText
import streamlit as st
import pandas as pd

def displaySummaryPlots(): 
    st.header("Supply Assumptions Overview")
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR LOCAL SUPPLIES
    #---------------------------------------------------------------#

    st.subheader("Local Supply Scenarios")
    st.write(localSuppliesExplanationText)

    # Set up total demand variables for summary poster plots
    localSuppliesPlotInputData = st.session_state.localSuppliesdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
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
    localSuppliesNumberOfVars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    localSuppliesBoxKey = "Supplies Selectbox"
    localSuppliesPiePlotLabel = "Supplies by Study Region"
    localSuppliesBarPlotLabel = "Supplies by Contractor"
    localSuppliesBarPlotXAxisLabel = "Supplies (acre-feet/year)"
    localSuppliesColors = ['#F63366', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#2BB1BB', '#22466B', '#22466B', '#22466B']

    displayPieAndBarPlots(localSuppliesVars, localSuppliesVarsForLabel, localSuppliesNumberOfVars, localSuppliesPlotInputData, localSuppliesBoxKey, localSuppliesPiePlotLabel, localSuppliesBarPlotLabel, localSuppliesBarPlotXAxisLabel, localSuppliesColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR SWP CVP SUPPLIES
    #---------------------------------------------------------------#

    st.subheader("SWP and CVP Supply Scenarios")
    st.write(swpCVPExplanationText)

    # Set up total demand variables for summary poster plots
    # swpCVPPlotInputData = st.session_state.swpCVPSuppliesdf[['Variable', contractorsList]]
    # swpCVPPlotInputData = pd.melt(swpCVPPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    # swpCVPPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    # swpCVPVars = ['SWP CVP']

    # swpCVPVarsForLabel = [
    #     swpCVPPlotInputData['Type'] == swpCVPVars[0],
    #     ]
    # swpCVPNumberOfVars = [0]
    # swpCVPBoxKey = "SWP CVP Supplies Selectbox"
    # swpCVPPiePlotLabel = "SWP CVP Supplies by Study Region"
    # swpCVPBarPlotLabel = "SWP CVP Supplies by Contractor"
    # swpCVPBarPlotXAxisLabel = "SWP CVP Supplies (acre-feet/year)"
    # swpCVPColors = ['#F63366']

    # displayPieAndBarPlots(swpCVPVars, swpCVPVarsForLabel, swpCVPNumberOfVars, swpCVPPlotInputData, swpCVPBoxKey, swpCVPPiePlotLabel, swpCVPBarPlotLabel, swpCVPBarPlotXAxisLabel, swpCVPColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR COST BY SUPPLY TYPE
    #---------------------------------------------------------------#

    st.subheader("Cost by Supply Type")
    st.write(costBySupplyTypeExplanationText)

    # Set up total demand variables for summary poster plots
    # costBySupplyTypePlotInputData = st.session_state.costBySupplyTypedf[['Year', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    # costBySupplyTypePlotInputData = pd.melt(costBySupplyTypePlotInputData, id_vars=['Variable','Contractor','Study Region'])
    # costBySupplyTypePlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    # costBySupplyTypeVars = ['Cost by Supply Type']

    # costBySupplyTypeVarsForLabel = [
    #     costBySupplyTypePlotInputData['Type'] == costBySupplyTypeVars[0],
    #     ]
    # costBySupplyTypeNumberOfVars = [0]
    # costBySupplyTypeBoxKey = "Cost by Supply Type Selectbox"
    # costBySupplyTypePiePlotLabel = "Cost by Supply Type by Study Region"
    # costBySupplyTypeBarPlotLabel = "Cost by Supply Type by Contractor"
    # costBySupplyTypeBarPlotXAxisLabel = "Cost by Supply Type ($/acre-feet-year)"
    # costBySupplyTypeColors = ['#F63366']

    # displayPieAndBarPlots(costBySupplyTypeVars, costBySupplyTypeVarsForLabel, costBySupplyTypeNumberOfVars, costBySupplyTypePlotInputData, costBySupplyTypeBoxKey, costBySupplyTypePiePlotLabel, costBySupplyTypeBarPlotLabel, costBySupplyTypeBarPlotXAxisLabel, costBySupplyTypeColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR SUPPLY PRIORITY
    #---------------------------------------------------------------#

    st.subheader("Supply Priorities")
    st.write(supplyPriorityTypeExplanationText)

    # # Set up total demand variables for summary poster plots
    # supplyPriorityPlotInputData = st.session_state.supplyPrioritydf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    # supplyPriorityPlotInputData = pd.melt(supplyPriorityPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    # supplyPriorityPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    # supplyPriorityVars = ['Supply Priority By Type']

    # supplyPriorityVarsForLabel = [
    #     supplyPriorityPlotInputData['Type'] == supplyPriorityVars[0],
    #     ]
    # supplyPriorityNumberOfVars = [0]
    # supplyPriorityBoxKey = "Supply Priority Selectbox"
    # supplyPriorityPiePlotLabel = "Supply Priority by Study Region"
    # supplyPriorityBarPlotLabel = "Supply Priority by Contractor"
    # supplyPriorityBarPlotXAxisLabel = "Supply Priority"
    # supplyPriorityColors = ['#F63366']

    # displayPieAndBarPlots(supplyPriorityVars, supplyPriorityVarsForLabel, supplyPriorityNumberOfVars, supplyPriorityPlotInputData, supplyPriorityBoxKey, supplyPriorityPiePlotLabel, supplyPriorityBarPlotLabel, supplyPriorityBarPlotXAxisLabel, supplyPriorityColors)
