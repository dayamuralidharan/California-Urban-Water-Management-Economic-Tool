from src.demandsHelper import displayPieAndBarPlots, demandsExplainationText, useByTypeExplainationText, intExtUseByTypeExplainationText, baseLongTermConservationText
import streamlit as st
import pandas as pd 

st.header("Demand Assumptions Overview")
    
#---------------------------------------------------------------#
# SUMMARY POSTER FOR TOTAL DEMAND SCENARIOS
#---------------------------------------------------------------#

def displaySummaryPlotsTotalDemandScenarios():
    st.subheader("Total Demand Scenarios")
    st.write(demandsExplainationText)

    # Set up total demand variables for summary poster plots
    # demandsPlotInputData = st.session_state.totalDemandsdf[['Variable', 'Study Region','Contractor']]
    demandsPlotInputData = st.session_state.totalDemandsdf[['Variable', 'Study Region','Contractor', '2025', '2030', '2035', '2040', '2045']]
    demandsPlotInputData = pd.melt(demandsPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    demandsPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    demandVars = ['Normal or Better Demands (acre-feet/year)', 'Single Dry-Year Demands (acre-feet/year)','Multiple Dry-Year Demands (acre-feet/year)']

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
    useByTypePlotInputData = st.session_state.useByTypedf[['Variable', 'Study Region','Contractor', '2025', '2030', '2035', '2040', '2045']]
    useByTypePlotInputData = pd.melt(useByTypePlotInputData, id_vars=['Variable','Contractor','Study Region'])
    useByTypePlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    useByTypeVars = [
        'Single Family Residential Use (acre-feet/year)', 
        'Multi-Family Residential Use (acre-feet/year)',
        'Industrial Use (acre-feet/year)',
        'Commercial and Governmental Use (acre-feet/year)',
        'Agricultural Use (acre-feet/year)',
        'Landscape Use (acre-feet/year)',
        'Other (acre-feet/year)'
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
    useByTypeColors = ['#F63366', '#2BB1BB', '#22466B', '#FF7F50','#DFFF00', '#6495ED', '#CCCCFF']

    displayPieAndBarPlots(useByTypeVars, useByTypeVarsForLabel, useByTypeNumberOfVars, useByTypePlotInputData, useByTypeSelectBoxKey, useByTypePiePlotLabel, useByTypeBarPlotLabel, useByTypeBarPlotXAxisLabel, useByTypeColors)

    #---------------------------------------------------------------#
    # CREATE SUMMARY POSTER FOR INTERIOR AND EXTERIOR USE BY TYPE
    #---------------------------------------------------------------#

def displaySummaryPlotsIntExtUseByType(): 
    st.subheader("Interior and Exterior Use By Type")
    st.write(intExtUseByTypeExplainationText)

    # Set up variables for summary poster plots
    intExtUseByTypePlotInputData = st.session_state.intExtUseByTypedf[['Variable', 'Study Region','Contractor', '2025', '2030', '2035', '2040', '2045']]
    intExtUseByTypePlotInputData = pd.melt(intExtUseByTypePlotInputData, id_vars=['Variable','Contractor','Study Region'])
    intExtUseByTypePlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    intExtUseByTypeVars = [
        'Fraction of single-family residential use that is interior (%)', 
        'Fraction of multi-family residential use that is interior (%)',
        'Fraction of commercial use that is interior (%)',
        'Fraction of industrial use that is interior (%)',
        'Share of exterior use unaffected by ETAW (% of total exterior use)',
        ]

    intExtUseByTypeVarsForLabel = [
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[0],
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[1],
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[2],
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[3],
        intExtUseByTypePlotInputData['Type'] == intExtUseByTypeVars[4]
        ]
    intExtUseByTypeNumberOfVars = [0, 1, 2, 3, 4]
    intExtUseByTypeSelectBoxKey = "Interior and Exterior Use By Type Selectbox"
    intExtUseByTypePiePlotLabel = "Interior and Exterior Use By Type by Study Region"
    intExtUseByTypeBarPlotLabel = "Interior and Exterior Use By Type by Contractor"
    intExtUseByTypeBarPlotXAxisLabel = "Interior and Exterior Use By Type (acre-feet/year)"
    intExtUseByTypeColors = ['#F63366', '#2BB1BB', '#22466B', '#FF7F50','#DFFF00']

    displayPieAndBarPlots(intExtUseByTypeVars, intExtUseByTypeVarsForLabel, intExtUseByTypeNumberOfVars, intExtUseByTypePlotInputData, intExtUseByTypeSelectBoxKey, intExtUseByTypePiePlotLabel, intExtUseByTypeBarPlotLabel, intExtUseByTypeBarPlotXAxisLabel, intExtUseByTypeColors)

    #---------------------------------------------------------------#
    # CREATE SUMMARY POSTER FOR BASE LONG-TERM CONSERVATION
    #---------------------------------------------------------------#

def displaySummaryPlotsBaseLongTermConservation():    
    st.subheader("Base Long-term Conservation")
    st.write(baseLongTermConservationText)

    # Set up variables for summary poster plots
    baseLongTermConservationPlotInputData = st.session_state.baseLongTermConservationdf[['Variable', 'Study Region','Contractor', '2025', '2030', '2035', '2040', '2045']]
    baseLongTermConservationPlotInputData = pd.melt(baseLongTermConservationPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    baseLongTermConservationPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    baseLongTermConservationVars = [
        'Base Long-term Conservation (acre-feet)'
        ]

    baseLongTermConservationVarsForLabel = [
        baseLongTermConservationPlotInputData['Type'] == baseLongTermConservationVars[0]
        ]
    baseLongTermConservationNumberOfVars = [0]
    baseLongTermConservationSelectBoxKey = "Base Long-term Conservation Selectbox"
    baseLongTermConservationPiePlotLabel = "Base Long-term Conservation by Study Region"
    baseLongTermConservationBarPlotLabel = "Base Long-term Conservation by Contractor"
    baseLongTermConservationBarPlotXAxisLabel = "Base Long-term Conservation (acre-feet/year)"
    baseLongTermConservationColors = ['#F63366']

    displayPieAndBarPlots(baseLongTermConservationVars, baseLongTermConservationVarsForLabel, baseLongTermConservationNumberOfVars, baseLongTermConservationPlotInputData, baseLongTermConservationSelectBoxKey, baseLongTermConservationPiePlotLabel, baseLongTermConservationBarPlotLabel, baseLongTermConservationBarPlotXAxisLabel, baseLongTermConservationColors)
