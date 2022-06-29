import os
import pandas as pd
from modelUtilities import lookupCorrespondingValue
from readGlobalAssumptions import contractorsList, futureYear, hydroRegionDf, reclassYearType, historicHydrologyYears

# Input directories and filenames
dirname = os.path.dirname(__file__)

# DEMAND Inputs
totalDemandsInputData = "../inputData/demandsInput_totalDemands.csv"
plannedConservationInputData = "../inputData/demandsInput_baseLongTermConservationData.csv"
ETAWAdjustmentsInputData = "../inputData/demandsInput_ETAWAdjustments.csv"
inputDemandsFile = os.path.join(dirname, totalDemandsInputData)
inputPlannedConservationFile = os.path.join(dirname, plannedConservationInputData)
inputETAWAdjustmentsFile = os.path.join(dirname, ETAWAdjustmentsInputData)

demandsData = pd.read_csv(inputDemandsFile)
plannedLongTermConservation = pd.read_csv(inputPlannedConservationFile)
ETAWAdjustments = pd.read_csv(inputETAWAdjustmentsFile).set_index('Year')

# Initialize variable as a time series
totalDemands = {'Year': historicHydrologyYears}
totalDemandScenarioRadioButtonIndex = 1    #TODO - connect to dashboard

# Set up total demand time series based on hydrologic year type.
for contractor in contractorsList:
    contractorRegion = lookupCorrespondingValue(hydroRegionDf, contractor, colA='Contractor', colB='Hydro. Region')
    contractorYearType = reclassYearType[contractor]
    totalDemandsInput = demandsData[demandsData['Contractor'] == contractor]
    totalDemandsInput = totalDemandsInput[['Variable', 'Contractor', futureYear]]
    contractorDemands = []
    
    mapYearType = {
        'NB': 'Normal or Better Demands (acre-feet/year)',
        'SD': 'Single Dry-Year Demands (acre-feet/year)',
        'MD': 'Multiple Dry-Year Demands (acre-feet/year)',
    }
    if totalDemandScenarioRadioButtonIndex == 1:   # Apply ETAW Adjustments to Normal or Better Demands
        for i, Year in enumerate(historicHydrologyYears):
            contractorDemands.append(
                ETAWAdjustments[contractor][Year] *
                totalDemandsInput[totalDemandsInput['Variable'] == mapYearType['NB']][futureYear].values[0]
            )
    elif totalDemandScenarioRadioButtonIndex == 0:
        for i in range(len(historicHydrologyYears)):
            contractorDemands.append(
                totalDemandsInput[totalDemandsInput['Variable'] == mapYearType[contractorYearType[i]]][futureYear].values[0]
            )
    totalDemands[contractor] = contractorDemands

totalDemands = pd.DataFrame(totalDemands)