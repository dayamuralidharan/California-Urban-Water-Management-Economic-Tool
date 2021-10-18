import os
import pandas as pd
from modelUtilities import lookupCorrespondingValue
from readGlobalAssumptions import contractorsList, futureYear, hydroRegionDf, reclassSjYearType, reclassSacYearType, historicHydrologyYears


# Input directories and filenames
dirname = os.path.dirname(__file__)

# DEMAND Inputs
totalDemandsInputData = "../inputData/demandsInput_totalDemands.csv"
baseConservationInputData = "../inputData/demandsInput_baseLongTermConservationData.csv"
inputDemandsFile = os.path.join(dirname, totalDemandsInputData)
inputBaseConservationFile = os.path.join(dirname, baseConservationInputData)

demandsData = pd.read_csv(inputDemandsFile)
baseConservation = pd.read_csv(inputBaseConservationFile)

# Initialize variable as a time series
totalDemands = {'Year': historicHydrologyYears}

# Set up total demand time series based on hydrologic year type.
for contractor in contractorsList:
    contractorRegion = lookupCorrespondingValue(hydroRegionDf, contractor, colA='Contractor', colB='Hydro. Region')
    if contractorRegion == 'San Joaquin':
        conYearType = reclassSjYearType
    else:
        conYearType = reclassSacYearType
    totalDemandsInput = demandsData[demandsData['Contractor'] == contractor]
    totalDemandsInput = totalDemandsInput[['Variable', 'Contractor', futureYear]]
    contractorDemands = []
    
    mapYearType = {
        'NB': 'Normal or Better Demands (acre-feet/year)',
        'SD': 'Single Dry-Year Demands (acre-feet/year)',
        'MD': 'Multiple Dry-Year Demands (acre-feet/year)',
    }
    for i in range(len(historicHydrologyYears)): 
        contractorDemands.append(
            totalDemandsInput[totalDemandsInput['Variable'] == mapYearType[conYearType[i]]][futureYear].values[0]
        )
    totalDemands[contractor] = contractorDemands

totalDemands = pd.DataFrame(totalDemands)