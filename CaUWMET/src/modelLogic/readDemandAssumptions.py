import os
import pandas as pd
from modelUtilities import lookupCorrespondingValue
from readGlobalAssumptions import contractorsList, futureYear, hydroRegionDf, reclassYearType, historicHydrologyYears

#TODO Dynamically connect totalDemandScenarioRadioButtonIndex to the dashboard

# Input directories and filenames
dirname = os.path.dirname(__file__)

# DEMAND Inputs
totalDemandsInputData = "../inputData/demandsInput_totalDemands.csv"
baseConservationInputData = "../inputData/demandsInput_baseLongTermConservationData.csv"
ETAWAdjustmentsInputData = "../inputData/demandsInput_ETAWAdjustments.csv"
inputDemandsFile = os.path.join(dirname, totalDemandsInputData)
inputBaseConservationFile = os.path.join(dirname, baseConservationInputData)
inputETAWAdjustmentsFile = os.path.join(dirname, ETAWAdjustmentsInputData)

demandsData = pd.read_csv(inputDemandsFile)
baseConservation = pd.read_csv(inputBaseConservationFile)
ETAWAdjustments = pd.read_csv(inputETAWAdjustmentsFile).set_index('Year')

# Initialize variable as a time series
totalDemands = {'Year': historicHydrologyYears}
totalDemandScenarioRadioButtonIndex = 1    # Temporary
# Set up total demand time series based on hydrologic year type.
for contractor in contractorsList:
    contractorRegion = lookupCorrespondingValue(hydroRegionDf, contractor, colA='Contractor', colB='Hydro. Region')
    conYearType = reclassYearType[contractor]
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
                totalDemandsInput[totalDemandsInput['Variable'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
    totalDemands[contractor] = contractorDemands

totalDemands = pd.DataFrame(totalDemands)