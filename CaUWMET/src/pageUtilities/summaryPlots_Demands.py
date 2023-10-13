from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd 

#---------------------------------------------------------------#
# SUMMARY POSTER FOR TOTAL DEMAND SCENARIOS
#---------------------------------------------------------------#

def displaySummaryPlotsTotalDemandScenarios():
    st.write(demandsExplanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = st.session_state.totalDemandsdf[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
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
    piePlotLabel = "Demands by Study Region"
    barPlotLabel = "Demands by Contractor"
    barPlotXAxisLabel = "Demands (acre-feet/year)"
    colors = ['#F63366', '#2BB1BB', '#22466B']

    plotTypeChoice_totalDemands = st.selectbox('View total demands data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_totalDemands == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel,colors)
    else:
        displayDataForOneContractor(plotTypeChoice_totalDemands, plotInputData)

    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR TOTAL USE BY TYPE
    #---------------------------------------------------------------#

def displaySummaryPlotsWaterUseByType():
    st.write(useByTypeExplanationText)

    # Set up variables for summary poster plots
    plotInputData = st.session_state.useByTypedf[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
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
    piePlotLabel = "Use By Type by Study Region"
    barPlotLabel = "Use By Type by Contractor"
    barPlotXAxisLabel = "Use By Type (acre-feet/year)"
    colors = ['#FF7F50','#DFFF00', '#6495ED', '#CCCCFF', '#9FE2BF', 'FFBF00', '800000']


    plotTypeChoice_demandsByUseType = st.selectbox('View demands by use type data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_demandsByUseType == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel, colors)
    else:
        displayDataForOneContractor(plotTypeChoice_demandsByUseType, plotInputData)

    #---------------------------------------------------------------#
    # CREATE SUMMARY POSTER FOR BASE LONG-TERM CONSERVATION
    #---------------------------------------------------------------#

def displaySummaryPlotsBaseLongTermConservation():    
    st.write(baseLongTermConservationExplanationText)

    # Set up variables for summary poster plots
    plotInputData = st.session_state.baseLongTermConservationdf[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
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
    piePlotLabel = "Planned Long-term Conservation by Study Region"
    barPlotLabel = "Planned Long-term Conservation by Contractor"
    barPlotXAxisLabel = "Planned Long-term Conservation (acre-feet/year)"
    conservationColors = ['#00FF00']

    plotTypeChoice_demandsByUseType = st.selectbox('View planned long-term conservation data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_demandsByUseType == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel, conservationColors)
    else:
        displayDataForOneContractor(plotTypeChoice_demandsByUseType, plotInputData)
    

demandsExplanationText = """Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can 
be found in the model documentation."""

useByTypeExplanationText = ("""Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")


baseLongTermConservationExplanationText = ("""Long-term conservation is incorporated into the model as it is an important component of each contractor's long-term strategy to increase 
their water supply reliability. These demand reductions typically include programs that target water use efficiency in each sector, turf replacement programs, 
conservation outreach and communications, reducing conveyance losses, and more. Long-term demand management measures that are adopted by water users can 
have a demand hardening effect. Although they can increase reliability by reducing the size, frequency and duration of shortage events, they can make these 
events relatively more costly when they do occur.  A hardening factor can be set to simulate this effect.>""")