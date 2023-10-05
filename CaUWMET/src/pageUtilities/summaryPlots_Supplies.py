from src.summaryPlots_Helper import displayPieAndBarPlots, displayDataForOneContractor
import streamlit as st
import pandas as pd

#---------------------------------------------------------------#
# SUMMARY POSTER FOR LOCAL AND REGIONAL SUPPLIES
#---------------------------------------------------------------#

def displaySummaryPlots_localAndRegionalSupplies(): 
    st.write(localSuppliesExplanationText)

    # Set up total demand variables for summary poster plots
    localSuppliesPlotInputData = st.session_state.localSuppliesdf[['Variable', 'Study Region','Contractor', int(st.session_state.futurePlanningYear)]]
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

    plotTypeChoice_localRegionalSupplies = st.selectbox('View local and regional supply data for:', st.session_state.dropDownMenuList, )
    if plotTypeChoice_localRegionalSupplies == 'All Contractors':
        displayPieAndBarPlots(localSuppliesVars, localSuppliesVarsForLabel, localSuppliesNumberOfVars, localSuppliesPlotInputData, localSuppliesBoxKey, localSuppliesPiePlotLabel, localSuppliesBarPlotLabel, localSuppliesBarPlotXAxisLabel, localSuppliesColors)
    else:
        displayDataForOneContractor(plotTypeChoice_localRegionalSupplies, localSuppliesPlotInputData)
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR SWP CVP SUPPLIES
    #---------------------------------------------------------------#

    st.subheader("SWP and CVP Supply Scenarios")
    st.write(swpCVPExplanationText)


localSuppliesExplanationText = ("""Local supply data includes all existing and planned sources of water available for 
                                each supplier excluding supplies sourced from the State Water and Central Valley Projects (SWP and CVP). 
                                SWP and CVP supplies are input separately via the second variable on this page. Local supplies are input for
                                anticipated availability under a normal or better water year, single dry, and multiple dry year conditions. Local supplies
                                are input separately by type to account for the varying costs associated with each supply type. 
                                Default data was developed utilizing information reported in each supplier's 2020 Urban Water Management Plan.
                                Local supplies reported on this page should only include verified supplies. Any local supplies that are still 
                                conceptual should be input in the Water Management Options Assumptions page.""")

swpCVPExplanationText = ("""State Water Project (SWP) and Central Valley Project (CVP) sourced supplies are input separately from the local supplies to account for
                         variation that occurs from year to year as it is influenced by annual weather and hydrology, as well as demand by other users, operational and regulatory factors. 
                         The SWP water input through this variable includes long-term water supply contracts including Table A amounts, transfer and exchange of Table A water, carryover water, Turb-Back Pools A and B water, Multiyar Water Pool Program water, 
                         and Article 21 water. Default data for these supplies were developed from CA DWR and U.S. Bureau of Reclamation's Calsim II 
                         and Calsim 3 water resources planning models. These models simulate operations of the SWP and CVP and much of the water resources infrastructure in the Central 
                         Valley of California and the Sacramento-San Joaquin Delta regions. The default Calsim II dataset was developed from the U.S. Bureau's 2020 Benchmark study
                         which simulated delivery capabilities under 1922 - 2003 historic hydrologic conditions. The default Calsim 3 dataset was developed from DWR's <TBD> study
                         which simulated delivery capabilities under 1922 - 2015 historic hydrologic conditions. More details on these Calsim models and associated studies can be found
                         in Section X of the model documentation.""")