

import os
import numpy as np
import pandas as pd
from totalDemandsLogic import (
    returnHydroRegion, reclassifyYearType,
)

# Input directories and filenames
dirname = os.path.dirname(__file__)
recyclingSuppliesInput = "../inputData/recyclingSupplies.csv"
potableReuseSuppliesInput = "../inputData/potableReuseSupplies.csv"
desalinationSuppliesInput = "../inputData/desalinationSupplies.csv"
contractualTransfersSuppliesInput = "../inputData/potableReuselongTermContractualTransfersAndExchangesSupplies.csv"
localSurfaceWaterSuppliesInput = "../inputData/localSurfaceWaterSupplies.csv"
otherImportedSuppliesInput = "../inputData/otherSupplies.csv"
localGroundwaterSuppliesInput = "../inputData/groundwaterPumpingCostsSupplies.csv"

hydroYearTypeInput = "../inputData/hydrologyAssumptions.csv"
hydroRegionInput = "../inputData/contractorInformation.csv"
inputHydroYearTypeFile = os.path.join(dirname, hydroYearTypeInput)
inputHydroRegionFile = os.path.join(dirname, hydroRegionInput)

# Read input files into pandas dataframes
hydroYearType = pd.read_csv(inputHydroYearTypeFile)
hydroRegion = pd.read_csv(inputHydroRegionFile)
hydroRegionDf = hydroRegion[['Contractor', 'Hydro. Region']]   # df with contractor - hydro region mapping

# Test for returnHydroRegion:
assert(
    returnHydroRegion(hydroRegionDf, 'City of Lindsay', colA='Contractor', colB='Hydro. Region') == 'San Joaquin'
)

## Coding the logic
futureYear = '2030'  # Current assumption
historicHydrologyYears = hydroYearType['Year'].values  # 1922 to 2015
sacYearType = hydroYearType['Sacramento Valley'].values
sjYearType = hydroYearType['San Joaquin Valley'].values
reclassSacYearType = reclassifyYearType(sacYearType)
reclassSjYearType = reclassifyYearType(sjYearType)
reclassYearType = pd.DataFrame({
    'sacYearType': reclassSacYearType,
    'sjYearType': reclassSjYearType,
    'Year': historicHydrologyYears,
    }
)

contractors = list(hydroRegionDf['Contractor'].values)
totalLocalSupplies = {'Year': historicHydrologyYears}
contractor = contractors[-1]
for contractor in contractors:
    contractorRegion = returnHydroRegion(hydroRegionDf, contractor, colA='Contractor', colB='Hydro. Region')
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
    for i in range(len(historicHydrologyYears)):
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
