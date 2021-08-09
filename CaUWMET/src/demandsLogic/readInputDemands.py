

import os
import numpy as np
import pandas as pd
from totalDemandsLogic import (
    returnHydroRegion, reclassifyYearType,
)

# Input directories and filenames
dirname = os.path.dirname(__file__)
totalDemandsCSV = "../inputData/totalDemands.csv"
hydroYearTypeCSV = "../inputData/hydrologyAssumptions.csv"
baseConservationCSV = "../inputData/baseLongTermConservation.csv"
inputDemandsFile = os.path.join(dirname, totalDemandsCSV)
inputHydroYearTypeFile = os.path.join(dirname, hydroYearTypeCSV)
inputBaseConservationFile = os.path.join(dirname, baseConservationCSV)
tempHydroRegionDir = r"C:\Users\nudurus\OneDrive - Jacobs\Documents\Projects\2021_05_CVFPP\tasks\20210806_codingDemandsLogic"
tempHydroRegionFile = os.path.join(tempHydroRegionDir, "CaUWMET Python Code Dev.xlsx")
tempHydroRegionSheet = "contractorInformation"

# Read input files into pandas dataframes
demandsData = pd.read_csv(inputDemandsFile)
hydroYearType = pd.read_csv(inputHydroYearTypeFile)
baseConservation = pd.read_csv(inputBaseConservationFile)
hydroRegion = pd.read_excel(tempHydroRegionFile, sheet_name=tempHydroRegionSheet, index_col=0)
hydroRegionDf = hydroRegion[['Contractor', 'Hydrologic Region 2']]   # df with contractor - hydro region mapping

# Test for returnHydroRegion:
assert(
    returnHydroRegion(hydroRegionDf, 'City of Lindsay', colA='Contractor', colB='Hydrologic Region 2') == 'San Joaquin'
)

## Coding the logic
futureYear = '2030'  # Current assumption
years = hydroYearType['Year'].values  # 1922 to 2015
sacYearType = hydroYearType['Sacramento Valley'].values
sjYearType = hydroYearType['San Joaquin Valley'].values
reclassSacYearType = reclassifyYearType(sacYearType)
reclassSjYearType = reclassifyYearType(sjYearType)
reclassYearType = pd.DataFrame({
    'sacYearType': reclassSacYearType,
    'sjYearType': reclassSjYearType,
    'Year': years,
    }
)

contractors = list(hydroRegionDf['Contractor'].values)
totalDemands = {'Year': years}
demandsAfterBaseConservation = {'Year': years}
contractor = contractors[-1]
for contractor in contractors:
    contractorRegion = returnHydroRegion(hydroRegionDf, contractor, colA='Contractor', colB='Hydrologic Region 2')
    if contractorRegion == 'San Joaquin':
        conYearType = reclassSjYearType
    else:
        conYearType = reclassSacYearType
    contractorDf = demandsData[demandsData['Contractor'] == contractor]
    contractorDf = contractorDf[['Demands', 'Contractor', futureYear]]
    contractorDemands = []
    contractorDemandsAfterBaseConservation = []
    mapYearType = {
        'NB': 'Normal or Better Demands (acre-feet/year)',
        'SD': 'Single Dry-Year Demands (acre-feet/year)',
        'MD': 'Multiple Dry-Year Demands (acre-feet/year)',
    }
    for i in range(len(years)):
        contractorDemands.append(
            contractorDf[contractorDf['Demands'] == mapYearType[conYearType[i]]][futureYear].values[0]
        )
        baseCons = baseConservation[baseConservation['Contractor'] == contractor][futureYear].values[0]
        contractorDemandsAfterBaseConservation.append(contractorDemands[-1] - baseCons)

    totalDemands[contractor] = contractorDemands
    demandsAfterBaseConservation[contractor] = contractorDemandsAfterBaseConservation

calculatedTotalDemandsDf = pd.DataFrame(totalDemands)
calculatedTotalDemandsDf.to_csv('calculatedTotalDemands.csv')
demandsAfterBaseConservationDf = pd.DataFrame(demandsAfterBaseConservation)
calculatedTotalDemandsDf.to_csv('demandsAfterBaseConservation.csv')

