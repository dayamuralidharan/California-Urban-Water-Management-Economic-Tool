from src.demandsHelper import displayPieAndBarPlots, demandsExplainationText, useByTypeExplainationText, intExtUseByTypeExplainationText, baseLongTermConservationText
import streamlit as st
import pandas as pd 

#---------------------------------------------------------------#
# SUMMARY POSTER FOR TOTAL DEMAND SCENARIOS
#---------------------------------------------------------------#

def displaySummaryPlotsTotalDemandScenarios():
    st.subheader("Total Demand Scenarios")
    st.write(demandsExplainationText)

    # Set up total demand variables for summary poster plots
    # demandsPlotInputData = st.session_state.totalDemandsdf[['Variable', 'Study Region','Contractor']]
    demandsPlotInputData = st.session_state.totalDemandsdf[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    demandsPlotInputData = pd.melt(demandsPlotInputData, id_vars=['Variable','Contractor', 'Study Region'])
    demandsPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    demandVars = ['Normal or Better Demands (AFY)', 'Single Dry-Year Demands (AFY)','Multiple Dry-Year Demands (AFY)']

    demandVarsForLabel = [
        demandsPlotInputData['Type'] == demandVars[0],
        demandsPlotInputData['Type'] == demandVars[1],
        demandsPlotInputData['Type'] == demandVars[2],
        ]
    demandsNumberOfVars = [0, 1, 2]
    demandsSelectBoxKey = "Total Demands Selectbox"
    demandsPiePlotLabel = "Demands by Study Region"
    demandsBarPlotLabel = "Demands by Contractor"
    demandsBarPlotXAxisLabel = "Demands (acre-feet/year)"
    demandsColors = ['#F63366', '#2BB1BB', '#22466B']

    displayPieAndBarPlots(demandVars, demandVarsForLabel, demandsNumberOfVars, demandsPlotInputData, demandsSelectBoxKey, demandsPiePlotLabel, demandsBarPlotLabel, demandsBarPlotXAxisLabel,demandsColors)

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR TOTAL USE BY TYPE
    #---------------------------------------------------------------#

def displaySummaryPlotsWaterUseByType():
    st.subheader("Water Use By Type")
    st.write(useByTypeExplainationText)

    # Set up variables for summary poster plots
    useByTypePlotInputData = st.session_state.useByTypedf[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    useByTypePlotInputData = pd.melt(useByTypePlotInputData, id_vars=['Variable','Contractor','Study Region'])
    useByTypePlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    useByTypeVars = [
        'Single Family Residential Use (AFY)', 
        'Multi-Family Residential Use (AFY)',
        'Industrial Use (AFY)',
        'Commercial and Governmental Use (AFY)',
        'Agricultural Use (AFY)',
        'Landscape Use (AFY)',
        'Other Use (AFY) (i.e. Losses, groundwater recharge, sales to other agencies etc.)'
        ]

    useByTypeVarsForLabel = [
        useByTypePlotInputData['Type'] == useByTypeVars[0],
        useByTypePlotInputData['Type'] == useByTypeVars[1],
        useByTypePlotInputData['Type'] == useByTypeVars[2],
        useByTypePlotInputData['Type'] == useByTypeVars[3],
        useByTypePlotInputData['Type'] == useByTypeVars[4],
        useByTypePlotInputData['Type'] == useByTypeVars[5],
        useByTypePlotInputData['Type'] == useByTypeVars[6],
        ]
    useByTypeNumberOfVars = [0, 1, 2, 3, 4, 5, 6]
    useByTypeSelectBoxKey = "Use By Type Selectbox"
    useByTypePiePlotLabel = "Use By Type by Study Region"
    useByTypeBarPlotLabel = "Use By Type by Contractor"
    useByTypeBarPlotXAxisLabel = "Use By Type (acre-feet/year)"
    useByTypeColors = ['#FF7F50','#DFFF00', '#6495ED', '#CCCCFF', '#9FE2BF', 'FFBF00', '800000']

    displayPieAndBarPlots(useByTypeVars, useByTypeVarsForLabel, useByTypeNumberOfVars, useByTypePlotInputData, useByTypeSelectBoxKey, useByTypePiePlotLabel, useByTypeBarPlotLabel, useByTypeBarPlotXAxisLabel, useByTypeColors)

    #---------------------------------------------------------------#
    # CREATE SUMMARY POSTER FOR INTERIOR AND EXTERIOR USE BY TYPE
    #---------------------------------------------------------------#

def displaySummaryPlotsIntExtUseByType(): 
    st.subheader("Interior and Exterior Use By Type")
    st.write(intExtUseByTypeExplainationText)

    # Set up variables for summary poster plots
    intExtUseByTypePlotInputData = st.session_state.intExtUseByTypedf[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    intExtUseByTypePlotInputData = pd.melt(intExtUseByTypePlotInputData, id_vars=['Variable','Contractor','Study Region'])
    intExtUseByTypePlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    intExtUseByTypeVars = [
        'Fraction of single family residential use that is interior (%)', 
        'Fraction of multi-family residential use that is interior (%)',
        'Fraction of commercial use that is interior (%)',
        'Fraction of industrial use that is interior (%)',
        ]

    intExtUseByTypeVarsForLabel = [
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[0],
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[1],
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[2],
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[3],
        ]
    intExtUseByTypeNumberOfVars = [0, 1, 2, 3]
    intExtUseByTypeSelectBoxKey = "Interior and Exterior Use By Type Selectbox"
    intExtUseByTypePiePlotLabel = "Interior and Exterior Use By Type by Study Region"
    intExtUseByTypeBarPlotLabel = "Interior and Exterior Use By Type by Contractor"
    intExtUseByTypeBarPlotXAxisLabel = "Interior and Exterior Use By Type (acre-feet/year)"
    intExtUseByTypeColors = ['#808000', '#008000', '#0000FF', '#000080']

    displayPieAndBarPlots(intExtUseByTypeVars, intExtUseByTypeVarsForLabel, intExtUseByTypeNumberOfVars, intExtUseByTypePlotInputData, intExtUseByTypeSelectBoxKey, intExtUseByTypePiePlotLabel, intExtUseByTypeBarPlotLabel, intExtUseByTypeBarPlotXAxisLabel, intExtUseByTypeColors)

    #---------------------------------------------------------------#
    # CREATE SUMMARY POSTER FOR BASE LONG-TERM CONSERVATION
    #---------------------------------------------------------------#

def displaySummaryPlotsBaseLongTermConservation():    
    st.subheader("Planned Long-term Conservation")
    st.write(baseLongTermConservationText)

    # Set up variables for summary poster plots
    baseLongTermConservationPlotInputData = st.session_state.baseLongTermConservationdf[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    baseLongTermConservationPlotInputData = pd.melt(baseLongTermConservationPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    baseLongTermConservationPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    baseLongTermConservationVars = [
        'Planned Long-term Conservation (AFY)'
        ]

    baseLongTermConservationVarsForLabel = [
        baseLongTermConservationPlotInputData['Type'] == baseLongTermConservationVars[0]
        ]
    baseLongTermConservationNumberOfVars = [0]
    baseLongTermConservationSelectBoxKey = "Planned Long-term Conservation Selectbox"
    baseLongTermConservationPiePlotLabel = "Planned Long-term Conservation by Study Region"
    baseLongTermConservationBarPlotLabel = "Planned Long-term Conservation by Contractor"
    baseLongTermConservationBarPlotXAxisLabel = "Planned Long-term Conservation (acre-feet/year)"
    baseLongTermConservationColors = ['#00FF00']

    displayPieAndBarPlots(baseLongTermConservationVars, baseLongTermConservationVarsForLabel, baseLongTermConservationNumberOfVars, baseLongTermConservationPlotInputData, baseLongTermConservationSelectBoxKey, baseLongTermConservationPiePlotLabel, baseLongTermConservationBarPlotLabel, baseLongTermConservationBarPlotXAxisLabel, baseLongTermConservationColors)
