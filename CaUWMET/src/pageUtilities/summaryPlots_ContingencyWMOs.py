from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd 

#---------------------------------------------------------------#
# SUMMARY POSTER FOR CONTINGENCY CONSERVATION CAMPAIGNS
#---------------------------------------------------------------#

def displaySummaryPlotsContingencyConservationCampaign():
    st.write(contingencyConservationExplanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = st.session_state.contingencyConservation[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
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
    piePlotLabel = "Contingency Conservation Assumptions by Region"
    barPlotLabel = "Contingency Conservation Assumptions by Contractor"
    barPlotXAxisLabel = "Contingency Conservation Assumption"
    colors = ['#F63366', '#2BB1BB', '#22466B', '800000']

    plotTypeChoice_contingencyConservation = st.selectbox('View total demands data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_contingencyConservation == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel,colors)
    else:
        displayDataForOneContractor(plotTypeChoice_contingencyConservation, plotInputData)
  
#---------------------------------------------------------------#
# SUMMARY POSTER FOR WATER MARKET TRANSFERS
#---------------------------------------------------------------#

def displaySummaryPlotsWaterMarketTransfers():
    st.write(waterMarketTransfersExplanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = st.session_state.waterMarketTransfers[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
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
    piePlotLabel = "Water Market Transfers Assumptions by Region"
    barPlotLabel = "Water Market Transfers Assumptions by Contractor"
    barPlotXAxisLabel = "Water Market Transfers Assumption"
    colors = ['#F63366', '#2BB1BB', '#22466B', '800000', '800000','800000','800000','800000','800000', '800000']

    plotTypeChoice_waterMarketTransfers = st.selectbox('View water market transfers data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_waterMarketTransfers == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel,colors)
    else:
        displayDataForOneContractor(plotTypeChoice_waterMarketTransfers, plotInputData)

  
#---------------------------------------------------------------#
# SUMMARY POSTER FOR RATIONING PROGRAMS
#---------------------------------------------------------------#

def displaySummaryPlotsRationingPrograms():
    st.write(rationingProgramExplanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = st.session_state.rationingPrograms[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
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
    piePlotLabel = "Rationing Program Assumptions by Region"
    barPlotLabel = "Rationing Program Assumptions by Contractor"
    barPlotXAxisLabel = "Rationing Programs Assumption"
    colors = ['#F63366', '#2BB1BB', '#22466B', '800000', '800000','800000']

    plotTypeChoice_rationingProgram = st.selectbox('View rationing program assumptions for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_rationingProgram == 'All Contractors':
        displayPieAndBarPlots(vars, varsForLabel, numberOfVars, plotInputData, selectBoxKey, piePlotLabel, barPlotLabel, barPlotXAxisLabel,colors)
    else:
        displayDataForOneContractor(plotTypeChoice_rationingProgram, plotInputData)

contingencyConservationExplanationText = """The model assumes contingency conservation campaigns are initiated whenever there is a 
shortage in available water supplies compared to current quantity demanded or in response to low carryover storage availability. 
Here users define the sse reduction with contingency conservation campaign,  the ratio of that reduction that is cut from interior 
use, the cost for contingency conservation campaigns, the demand hardening adjustment factor, population, 
and storage volume threshold to trigger contingency conservation management options."""

waterMarketTransfersExplanationText = ("""If supplies are less than demand in the dry or critical year type, and the marginal 
                                       water supply for the provider is a water transfer, then end-use shortages up to a percentage
                                        are applied first. Then, providers can acquire transfer supplies to eliminate shortfalls 
                                       up to the maximum transfer limit indicated on the System Operations Assumptions page. 
                                       These supplies have unit costs specific to the dry and critical condition. Thereafter it 
                                       is assumed that end-users must take additional shortage. 
                                       Water Transfer costs represent the cost each water district faces in acquiring water through a market transfer in a
                                        given water year. Costs are based on the unit values developed for the Water Storage 
                                       Investment Program's technical guidance, which modelled values by region (Sacramento Valley,
                                        Delta Export, Friant Service Area, and Eastside San Joaquin), water year type (wet, above 
                                       normal, below normal, dry, and critical), and future condition (2030, and 2045 after full 
                                       SGMA implementation). In the model, years 2035 and 2040 are interpolated values between the 
                                       2030 and 2045 future conditions. 2025 unit values are set at 2030 values to avoid 
                                       extrapolation. Single dry year or wetter transfer costs are set at the dry year unit value, 
                                       and multi-dry year transfer costs are set at the critical year unit value.>""")


rationingProgramExplanationText = ("""“Rationing” is shorthand for a water allocation method designed to minimize the overall 
                                   economic costs of a shortage by “balancing” the costs of forgone use among customer classes. 
                                   The allocation method in LCPSIM is intended to mimic water agencies by maintaining provisions for 
                                   exemptions due to serious adverse economic impacts, especially for businesses. 
                                   Here the user can enter the cost of a rationing program, the storage volume threshold to
                                    trigger rationing program, Cut Ratios by Use Type, Elasticity Variables and Upper and Lower 
                                   Loss Boundaries, and Retail Prices. 
                                   Retail prices are from the American Water Works Association 2020 California Water Survey, 
                                   where available. Those agencies not covered in the survey were collected from rate information 
                                   published on agency websites. All costs are in 2020 dollars, and presented as cost per acre-foot.>""")