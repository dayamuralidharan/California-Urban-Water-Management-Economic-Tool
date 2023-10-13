from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd 

#---------------------------------------------------------------#
# SUMMARY POSTER FOR TOTAL DEMAND SCENARIOS
#---------------------------------------------------------------#

def displaySummaryPlotsTotalDemandScenarios():
    st.write(demandsExplainationText)

    # Set up total demand variables for summary poster plots
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

    plotTypeChoice_totalDemands = st.selectbox('View total demands data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_totalDemands == 'All Contractors':
        displayPieAndBarPlots(demandVars, demandVarsForLabel, demandsNumberOfVars, demandsPlotInputData, demandsSelectBoxKey, demandsPiePlotLabel, demandsBarPlotLabel, demandsBarPlotXAxisLabel,demandsColors)
    else:
        displayDataForOneContractor(plotTypeChoice_totalDemands, demandsPlotInputData)

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR TOTAL USE BY TYPE
    #---------------------------------------------------------------#

def displaySummaryPlotsWaterUseByType():
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


    plotTypeChoice_demandsByUseType = st.selectbox('View demands by use type data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_demandsByUseType == 'All Contractors':
        displayPieAndBarPlots(useByTypeVars, useByTypeVarsForLabel, useByTypeNumberOfVars, useByTypePlotInputData, useByTypeSelectBoxKey, useByTypePiePlotLabel, useByTypeBarPlotLabel, useByTypeBarPlotXAxisLabel, useByTypeColors)
    else:
        displayDataForOneContractor(plotTypeChoice_demandsByUseType, useByTypePlotInputData)

    #---------------------------------------------------------------#
    # CREATE SUMMARY POSTER FOR INTERIOR AND EXTERIOR USE BY TYPE
    #---------------------------------------------------------------#

def displaySummaryPlotsIntExtUseByType(): 
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

    plotTypeChoice_demandsByUseType = st.selectbox('View planned long-term conservation data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_demandsByUseType == 'All Contractors':
        displayPieAndBarPlots(baseLongTermConservationVars, baseLongTermConservationVarsForLabel, baseLongTermConservationNumberOfVars, baseLongTermConservationPlotInputData, baseLongTermConservationSelectBoxKey, baseLongTermConservationPiePlotLabel, baseLongTermConservationBarPlotLabel, baseLongTermConservationBarPlotXAxisLabel, baseLongTermConservationColors)
    else:
        displayDataForOneContractor(plotTypeChoice_demandsByUseType, baseLongTermConservationPlotInputData)
    

demandsExplainationText = """Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can 
be found in the model documentation."""

useByTypeExplainationText = ("""Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")


baseLongTermConservationText = ("""Long-term conservation is incorporated into the model as it is an important component of each contractor's long-term strategy to increase 
their water supply reliability. These demand reductions typically include programs that target water use efficiency in each sector, turf replacement programs, 
conservation outreach and communications, reducing conveyance losses, and more. Long-term demand management measures that are adopted by water users can 
have a demand hardening effect. Although they can increase reliability by reducing the size, frequency and duration of shortage events, they can make these 
events relatively more costly when they do occur.  A hardening factor can be set to simulate this effect.>""")