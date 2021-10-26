import os
import pandas as pd
from modelUtilities import (
    lookupCorrespondingValue, reclassifyYearType,
)


#### Input directories and filenames
dirname = os.path.dirname(__file__)

### DEMAND Inputs
totalDemandsInput = "../inputData/totalDemandsData.csv"
hydroYearTypeInput = "../inputData/hydrologyAssumptions.csv"
hydroRegionInput = "../inputData/contractorInformation.csv"
baseConservationInput = "../inputData/baseLongTermConservationData.csv"
inputDemandsFile = os.path.join(dirname, totalDemandsInput)
inputHydroYearTypeFile = os.path.join(dirname, hydroYearTypeInput)
inputBaseConservationFile = os.path.join(dirname, baseConservationInput)
inputHydroRegionFile = os.path.join(dirname, hydroRegionInput)

### SUPPLIES Inputs
recyclingSupplyDataInput = "../inputData/recyclingSupplyData.csv"
potableReuseSupplyDataInput = "../inputData/potableReuseSupplyData.csv"
desalinationSupplyDataInput = "../inputData/desalinationSupplyData.csv"
contractualTransfersSupplyDataInput = "../inputData/contractualTransfersSupplyData.csv"
localSurfaceSupplyDataInput = "../inputData/localSurfaceSupplyData.csv"
otherImportedSupplyDataInput = "../inputData/otherImportedSupplyData.csv"
localGroundwaterSupplyDataInput = "../inputData/localGroundwaterSupplyData.csv"
swpCVPSupplyDataInput = "../inputData/swpCVPSupplyData.csv"
supplyPriorityInput = '../inputData/supplyPriorityData.csv'
inputRecyclingSupplyDataFile = os.path.join(dirname, recyclingSupplyDataInput)
inputPotableReuseSupplyDataFile = os.path.join(dirname, potableReuseSupplyDataInput)
inputDesalinationSupplyDataFile = os.path.join(dirname, desalinationSupplyDataInput)
inputContractualTransfersSupplyDataFile = os.path.join(dirname, contractualTransfersSupplyDataInput)
inputLocalSurfaceSupplyDataFile = os.path.join(dirname, localSurfaceSupplyDataInput)
inputOtherImportedSupplyDataFile = os.path.join(dirname, otherImportedSupplyDataInput)
inputLocalGroundwaterSupplyDataFile = os.path.join(dirname, localGroundwaterSupplyDataInput)
inputSWPCVPSupplyDataFile = os.path.join(dirname, swpCVPSupplyDataInput)
inputHydroYearTypeFile = os.path.join(dirname, hydroYearTypeInput)
inputHydroRegionFile = os.path.join(dirname, hydroRegionInput)
inputSupplyPriorityFile = os.path.join(dirname, supplyPriorityInput)


### Hydrology Assumptions
hydroYearType = pd.read_csv(inputHydroYearTypeFile)
hydroRegion = pd.read_csv(inputHydroRegionFile)


### Demand Assumptions
demandsData = pd.read_csv(inputDemandsFile)
baseConservation = pd.read_csv(inputBaseConservationFile)

### Supply Assumptions
recyclingSupplyData = pd.read_csv(inputRecyclingSupplyDataFile)
potableReuseSupplyData = pd.read_csv(inputPotableReuseSupplyDataFile)
desalinationSupplyData = pd.read_csv(inputDesalinationSupplyDataFile)
contractualTransfersSupplyData = pd.read_csv(inputContractualTransfersSupplyDataFile)
localSurfaceSupplyData = pd.read_csv(inputLocalSurfaceSupplyDataFile)
otherImportedSupplyData = pd.read_csv(inputOtherImportedSupplyDataFile)
localGroundwaterSupplyData = pd.read_csv(inputLocalGroundwaterSupplyDataFile)
swpCVPSupplyDataDf = pd.read_csv(inputSWPCVPSupplyDataFile)
supplyPriorityDf = pd.read_csv(inputSupplyPriorityFile)


#### Set up variable dataframes

futureYear = '2030'  # TODO Temporary assumption, will be input from streamlit

### Set up time series of hydrological year type based on contractor's hydrological region
hydroRegionDf = hydroRegion[['Contractor', 'Hydro. Region']]
historicHydrologyYears = hydroYearType['Year'].values  # 1922 to 2003 or 2015 depending on whether it is Calsim II or 3 input for SWP CVP deliveries
sacYearType = hydroYearType['Sacramento Valley'].values
sjYearType = hydroYearType['San Joaquin Valley'].values
reclassSacYearType = reclassifyYearType(sacYearType) # Reclassify CDEC's classifications to the UWMP demand classifications of Normal or Better, Single-Dry and Multi-Dry Years
reclassSjYearType = reclassifyYearType(sjYearType)
reclassYearType = pd.DataFrame({
    'sacYearType': reclassSacYearType,
    'sjYearType': reclassSjYearType,
    'Year': historicHydrologyYears,
    }
)


# Initialize variables with blank dictionaries
totalDemands = {'Year': historicHydrologyYears}
demandsAfterBaseConservation = {'Year': historicHydrologyYears}

#

contractorsList = list(hydroRegionDf['Contractor'].values) ####TODO: contractors will need to be dynamically read in from streamlit instead of read in from hydro region dataframe

# Set up contractor total demand time series based on hydrologic year type.
for contractor in contractorsList:
    contractorRegion = lookupCorrespondingValue(hydroRegionDf, contractor, colA='Contractor', colB='Hydro. Region')
    if contractorRegion == 'San Joaquin':
        conYearType = reclassSjYearType
    else:
        conYearType = reclassSacYearType
    totalDemandsInput = demandsData[demandsData['Contractor'] == contractor]
    totalDemandsInput = totalDemandsInput[['Variable', 'Contractor', futureYear]]
    contractorDemands = []
    demandsAfterBaseConservation = []
    mapYearType = {
        'NB': 'Normal or Better Demands (acre-feet/year)',
        'SD': 'Single Dry-Year Demands (acre-feet/year)',
        'MD': 'Multiple Dry-Year Demands (acre-feet/year)',
    }
    for i in range(len(historicHydrologyYears)): 
        contractorDemands.append(
            totalDemandsInput[totalDemandsInput['Variable'] == mapYearType[conYearType[i]]][futureYear].values[0]
        )
        baseLongTermConservation = baseConservation[baseConservation['Contractor'] == contractor][futureYear].values[0]
        #demandsAfterBaseConservation.append(contractorDemands[-1] - baseLongTermConservation)

    totalDemands[contractor] = contractorDemands
    #demandsAfterBaseConservation[contractor] = demandsAfterBaseConservation

totalDemands = pd.DataFrame(totalDemands)
#demandsAfterBaseConservation = pd.DataFrame(demandsAfterBaseConservation)




#Summing supply values from different csv files to create a dataframe
# totalInputSupplyData2025 = recyclingSupplyData['2025'].values + potableReuseSupplyData['2025'].values + desalinationSupplyData['2025'].values + contractualTransfersSupplyData['2025'].values + localSurfaceSupplyData['2025'].values + otherImportedSupplyData['2025'].values + localGroundwaterSupplyData['2025'].values
# totalInputSupplyData2030 = recyclingSupplyData['2030'].values + potableReuseSupplyData['2030'].values + desalinationSupplyData['2030'].values + contractualTransfersSupplyData['2030'].values + localSurfaceSupplyData['2030'].values + otherImportedSupplyData['2030'].values + localGroundwaterSupplyData['2030'].values
# totalInputSupplyData2035 = recyclingSupplyData['2035'].values + potableReuseSupplyData['2035'].values + desalinationSupplyData['2035'].values + contractualTransfersSupplyData['2035'].values + localSurfaceSupplyData['2035'].values + otherImportedSupplyData['2035'].values + localGroundwaterSupplyData['2035'].values
# totalInputSupplyData2040 = recyclingSupplyData['2040'].values + potableReuseSupplyData['2040'].values + desalinationSupplyData['2040'].values + contractualTransfersSupplyData['2040'].values + localSurfaceSupplyData['2040'].values + otherImportedSupplyData['2040'].values + localGroundwaterSupplyData['2040'].values
# totalInputSupplyData2045 = recyclingSupplyData['2045'].values + potableReuseSupplyData['2045'].values + desalinationSupplyData['2045'].values + contractualTransfersSupplyData['2045'].values + localSurfaceSupplyData['2045'].values + otherImportedSupplyData['2045'].values + localGroundwaterSupplyData['2045'].values
# supplyDataDf = pd.DataFrame({
#     'Supply': recyclingSupplyData['Supply'],
#     'Study Region': recyclingSupplyData['Study Region'],
#     'Contractor': recyclingSupplyData['Contractor'],
#     '2025': totalInputSupplyData2025,  
#     '2030': totalInputSupplyData2030,
#     '2035': totalInputSupplyData2035,
#     '2040': totalInputSupplyData2040,
#     '2045': totalInputSupplyData2045,
#     }
# )


# suppliesData = pd.read_csv('totalSupplyData.csv')


# supplyYearsForTotalSupplies = {'Year': historicHydrologyYears}
# supplyYearsForRecycleSupplies = {'Year': historicHydrologyYears}
# supplyYearsForPotableReuseSupplies = {'Year': historicHydrologyYears}
# supplyYearsForDesalinationSupplies = {'Year': historicHydrologyYears}
# supplyYearsForContractualTransfersSupplies = {'Year': historicHydrologyYears}
# supplyYearsForLocalSurfaceSupplies = {'Year': historicHydrologyYears}
# supplyYearsForOtherImportedSupplies = {'Year': historicHydrologyYears}
# supplyYearsForGroundwaterSupplies = {'Year': historicHydrologyYears}
# 
# for contractor in contractorsList:
#     contractorRegion = lookupCorrespondingValue(hydroRegionDf, contractor, colA='Contractor', colB='Hydro. Region')
#     if contractorRegion == 'San Joaquin':
#         conYearType = reclassSjYearType
#     else:
#         conYearType = reclassSacYearType
#     contractorDf = suppliesData[suppliesData['Contractor'] == contractor] 
#     contractorDf = contractorDf[['Supply', 'Contractor', futureYear]]
#     recyclingDataDf = recyclingSupplyData[recyclingSupplyData['Contractor'] == contractor] 
#     recyclingDataDf = recyclingDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]    
#     potableReuseDataDf = potableReuseSupplyData[potableReuseSupplyData['Contractor'] == contractor] 
#     potableReuseDataDf = potableReuseDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
#     desalinationDataDf = desalinationSupplyData[desalinationSupplyData['Contractor'] == contractor] 
#     desalinationDataDf = desalinationDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
#     contractualTransfersDataDf = contractualTransfersSupplyData[contractualTransfersSupplyData['Contractor'] == contractor] 
#     contractualTransfersDataDf = contractualTransfersDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
#     localSurfaceDataDf = localSurfaceSupplyData[localSurfaceSupplyData['Contractor'] == contractor] 
#     localSurfaceDataDf = localSurfaceDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
#     otherImportedDataDf = otherImportedSupplyData[otherImportedSupplyData['Contractor'] == contractor] 
#     otherImportedDataDf = otherImportedDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
#     groundwaterDataDf = localGroundwaterSupplyData[localGroundwaterSupplyData['Contractor'] == contractor] 
#     groundwaterDataDf = groundwaterDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
#     contractorSupplies = []
#     recyclingSupplies = []
#     potableReuseSupplies = []
#     desalinationSupplies = []
#     contractualTransfersSupplies = []
#     localSurfaceSupplies = []
#     otherImportedSupplies = []
#     groundwaterSupplies = []
    
#     mapYearType = {
#         'NB': 'Normal or Better Year (acre-feet/year)',
#         'SD': 'Single Dry-Year (acre-feet/year)',
#         'MD': 'Multiple Dry-Year (acre-feet/year)',
#     }
#     for i in range(len(historicHydrologyYears)):
#         contractorSupplies.append(        
#             contractorDf[contractorDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
#             )
#         supplyYearsForTotalSupplies[contractor] = contractorSupplies
#     calculatedTotalSuppliesDf = pd.DataFrame(supplyYearsForTotalSupplies)  
#     calculatedTotalSuppliesDf.to_csv('calculatedTotalSupplies.csv')
    
#     for j in range(len(historicHydrologyYears)):
#         recyclingSupplies.append(
#             recyclingDataDf[recyclingDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
#             )
#         supplyYearsForRecycleSupplies[contractor] = recyclingSupplies
#     calculatedRecyclingSuppliesDf = pd.DataFrame(supplyYearsForRecycleSupplies) 
#     # finalRecyclingSuppliesDf = calculatedRecyclingSuppliesDf.join(recyclingSupplyData['Supply Type'])
    
#     for k in range(len(historicHydrologyYears)):
#         potableReuseSupplies.append(
#             potableReuseDataDf[potableReuseDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
#             )
#         supplyYearsForPotableReuseSupplies[contractor] = potableReuseSupplies
#     calculatedPotableReuseSuppliesDf = pd.DataFrame(supplyYearsForPotableReuseSupplies)
#     # finalPotableReuseSuppliesDf = calculatedPotableReuseSuppliesDf.join(potableReuseSupplyData['Supply Type'])
    
#     for l in range(len(historicHydrologyYears)):
#         desalinationSupplies.append(
#             desalinationDataDf[desalinationDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
#             )
#         supplyYearsForDesalinationSupplies[contractor] = desalinationSupplies
#     calculatedDesalinationSuppliesDf = pd.DataFrame(supplyYearsForDesalinationSupplies)
#     # finalDesalinationSuppliesDf = calculatedDesalinationSuppliesDf.join(desalinationSupplyData['Supply Type'])
    
#     for m in range(len(historicHydrologyYears)):
#         contractualTransfersSupplies.append(
#             contractualTransfersDataDf[contractualTransfersDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
#             )
#         supplyYearsForContractualTransfersSupplies[contractor] = contractualTransfersSupplies
#     calculatedContractualTransfersSuppliesDf = pd.DataFrame(supplyYearsForContractualTransfersSupplies)
#     # finalContractualTransfersSuppliesDf = calculatedContractualTransfersSuppliesDf.join(contractualTransfersSupplyData['Supply Type'])
    
#     for n in range(len(historicHydrologyYears)):
#         localSurfaceSupplies.append(
#             localSurfaceDataDf[localSurfaceDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
#             )
#         supplyYearsForLocalSurfaceSupplies[contractor] = localSurfaceSupplies
#     calculatedLocalSurfaceSuppliesDf = pd.DataFrame(supplyYearsForLocalSurfaceSupplies)
#     # finalLocalSurfaceSuppliesDf = calculatedLocalSurfaceSuppliesDf.join(localSurfaceSupplyData['Supply Type'])
    
#     for o in range(len(historicHydrologyYears)):
#         otherImportedSupplies.append(
#             otherImportedDataDf[otherImportedDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
#             )
#         supplyYearsForOtherImportedSupplies[contractor] = otherImportedSupplies
#     calculatedOtherImportedSuppliesDf = pd.DataFrame(supplyYearsForOtherImportedSupplies)
#     # finalOtherImportedSuppliesDf = calculatedOtherImportedSuppliesDf.join(otherImportedSupplyData['Supply Type'])
    
#     for p in range(len(historicHydrologyYears)):
#         groundwaterSupplies.append(
#             groundwaterDataDf[groundwaterDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
#             )
#         supplyYearsForGroundwaterSupplies[contractor] = groundwaterSupplies
#     calculatedLocalGroundwaterSuppliesDf = pd.DataFrame(supplyYearsForGroundwaterSupplies)  
#     # finalLocalGroundwaterSuppliesDf = calculatedLocalGroundwaterSuppliesDf.join(localGroundwaterSupplyData['Supply Type'])

# suppliesDataframesCompiled = [calculatedRecyclingSuppliesDf, calculatedPotableReuseSuppliesDf, calculatedDesalinationSuppliesDf, calculatedContractualTransfersSuppliesDf, calculatedLocalSurfaceSuppliesDf, calculatedOtherImportedSuppliesDf, calculatedLocalGroundwaterSuppliesDf, swpCVPSupplyDataDf]
# suppliesDataframesCompiledDf = pd.concat(suppliesDataframesCompiled)

# suppliesDataframesCompiledDfIndexSet = suppliesDataframesCompiledDf.set_index('Year')
# suppliesDataframesCompiledDfTransposed = suppliesDataframesCompiledDfIndexSet.T
# suppliesDataframesCompiledDfTransposedStacked = suppliesDataframesCompiledDfTransposed.stack()
# suppliesDataframesCompiledDfTransposedStacked = suppliesDataframesCompiledDfTransposedStacked.to_frame()
# suppliesDataframesCompiledDfTransposedStackedReset =  suppliesDataframesCompiledDfTransposedStacked.reset_index()
# suppliesDataframesCompiledDfTransposedStackedReset.columns = ['Contractor', 'Year', 'Supply Volume']

# finalSuppliesDf = suppliesDataframesCompiledDfTransposedStackedReset.reset_index([0]).join(supplyPriorityDf['Supply Type']).join(supplyPriorityDf['Supply Priority'])
# del finalSuppliesDf['index']

# demandsAfterBaseConservationDfIndexSet = demandsAfterBaseConservation.set_index('Year')
# demandsAfterBaseConservationDfTransposed = demandsAfterBaseConservationDfIndexSet.T
# demandsAfterBaseConservationDfTransposedStacked = demandsAfterBaseConservationDfTransposed.stack()
# demandsAfterBaseConservationDfTransposedStacked = demandsAfterBaseConservationDfTransposedStacked.to_frame()
# demandsAfterBaseConservationDfTransposedStackedReset = demandsAfterBaseConservationDfTransposedStacked.reset_index()
# demandsAfterBaseConservationDfTransposedStackedReset.columns = ['Contractor', 'Year', 'Supply Volume']
# finalDemandsAfterBaseConservationDf = demandsAfterBaseConservationDfTransposedStackedReset

# #### Outputs to CSV for QAQC
# totalDemands.to_csv('demandsAfterBaseConservation.csv')
# inputSuppliesDataFile = supplyDataDf.to_csv('totalSupplyData.csv')