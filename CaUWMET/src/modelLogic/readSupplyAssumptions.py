import os
import pandas as pd
from readGlobalAssumptions import contractorsList, futureYear, historicHydrologyYears


# Input directories and filenames
dirname = os.path.dirname(__file__)

# SUPPLIES Inputs
recyclingSupplyDataInput = "../inputData/supplyInput_Recycling.csv"
potableReuseSupplyDataInput = "../inputData/supplyInput_PotableReuse.csv"
desalinationSupplyDataInput = "../inputData/supplyInput_Desalination.csv"
contractualTransfersSupplyDataInput = "../inputData/supplyInput_ContractualTransfers.csv"
localSurfaceSupplyDataInput = "../inputData/supplyInput_Surface.csv"
otherImportedSupplyDataInput = "../inputData/supplyInput_OtherImported.csv"
localGroundwaterSupplyDataInput = "../inputData/supplyInput_Groundwater.csv"
swpCVPSupplyDataInput = "../inputData/supplyInput_SWPCVP.csv"
supplyPriorityInput = '../inputData/supplyInput_supplyPriorities.csv'
inputRecyclingSupplyDataFile = os.path.join(dirname, recyclingSupplyDataInput)
inputPotableReuseSupplyDataFile = os.path.join(dirname, potableReuseSupplyDataInput)
inputDesalinationSupplyDataFile = os.path.join(dirname, desalinationSupplyDataInput)
inputContractualTransfersSupplyDataFile = os.path.join(dirname, contractualTransfersSupplyDataInput)
inputLocalSurfaceSupplyDataFile = os.path.join(dirname, localSurfaceSupplyDataInput)
inputOtherImportedSupplyDataFile = os.path.join(dirname, otherImportedSupplyDataInput)
inputLocalGroundwaterSupplyDataFile = os.path.join(dirname, localGroundwaterSupplyDataInput)
inputSWPCVPSupplyDataFile = os.path.join(dirname, swpCVPSupplyDataInput)
inputSupplyPriorityFile = os.path.join(dirname, supplyPriorityInput)


# Supply Assumptions
recyclingSupplyData = pd.read_csv(inputRecyclingSupplyDataFile)
potableReuseSupplyData = pd.read_csv(inputPotableReuseSupplyDataFile)
desalinationSupplyData = pd.read_csv(inputDesalinationSupplyDataFile)
contractualTransfersSupplyData = pd.read_csv(inputContractualTransfersSupplyDataFile)
localSurfaceSupplyData = pd.read_csv(inputLocalSurfaceSupplyDataFile)
otherImportedSupplyData = pd.read_csv(inputOtherImportedSupplyDataFile)
localGroundwaterSupplyData = pd.read_csv(inputLocalGroundwaterSupplyDataFile)
swpCVPSupplyDataDf = pd.read_csv(inputSWPCVPSupplyDataFile)
supplyPriorityDf = pd.read_csv(inputSupplyPriorityFile)




#Summing supply values from different csv files to create a dataframe
totalInputSupplyData2025 = recyclingSupplyData['2025'].values + potableReuseSupplyData['2025'].values + desalinationSupplyData['2025'].values + contractualTransfersSupplyData['2025'].values + localSurfaceSupplyData['2025'].values + otherImportedSupplyData['2025'].values + localGroundwaterSupplyData['2025'].values
totalInputSupplyData2030 = recyclingSupplyData['2030'].values + potableReuseSupplyData['2030'].values + desalinationSupplyData['2030'].values + contractualTransfersSupplyData['2030'].values + localSurfaceSupplyData['2030'].values + otherImportedSupplyData['2030'].values + localGroundwaterSupplyData['2030'].values
totalInputSupplyData2035 = recyclingSupplyData['2035'].values + potableReuseSupplyData['2035'].values + desalinationSupplyData['2035'].values + contractualTransfersSupplyData['2035'].values + localSurfaceSupplyData['2035'].values + otherImportedSupplyData['2035'].values + localGroundwaterSupplyData['2035'].values
totalInputSupplyData2040 = recyclingSupplyData['2040'].values + potableReuseSupplyData['2040'].values + desalinationSupplyData['2040'].values + contractualTransfersSupplyData['2040'].values + localSurfaceSupplyData['2040'].values + otherImportedSupplyData['2040'].values + localGroundwaterSupplyData['2040'].values
totalInputSupplyData2045 = recyclingSupplyData['2045'].values + potableReuseSupplyData['2045'].values + desalinationSupplyData['2045'].values + contractualTransfersSupplyData['2045'].values + localSurfaceSupplyData['2045'].values + otherImportedSupplyData['2045'].values + localGroundwaterSupplyData['2045'].values
supplyDataDf = pd.DataFrame({
    'Supply': recyclingSupplyData['Supply'],
    'Study Region': recyclingSupplyData['Study Region'],
    'Contractor': recyclingSupplyData['Contractor'],
    '2025': totalInputSupplyData2025,  
    '2030': totalInputSupplyData2030,
    '2035': totalInputSupplyData2035,
    '2040': totalInputSupplyData2040,
    '2045': totalInputSupplyData2045,
    }
)


suppliesData = pd.read_csv('totalSupplyData.csv')


supplyYearsForTotalSupplies = {'Year': historicHydrologyYears}
supplyYearsForRecycleSupplies = {'Year': historicHydrologyYears}
supplyYearsForPotableReuseSupplies = {'Year': historicHydrologyYears}
supplyYearsForDesalinationSupplies = {'Year': historicHydrologyYears}
supplyYearsForContractualTransfersSupplies = {'Year': historicHydrologyYears}
supplyYearsForLocalSurfaceSupplies = {'Year': historicHydrologyYears}
supplyYearsForOtherImportedSupplies = {'Year': historicHydrologyYears}
supplyYearsForGroundwaterSupplies = {'Year': historicHydrologyYears}

for contractor in contractorsList:
    contractorDf = suppliesData[suppliesData['Contractor'] == contractor] 
    contractorDf = contractorDf[['Supply', 'Contractor', futureYear]]
    recyclingDataDf = recyclingSupplyData[recyclingSupplyData['Contractor'] == contractor] 
    recyclingDataDf = recyclingDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]    
    potableReuseDataDf = potableReuseSupplyData[potableReuseSupplyData['Contractor'] == contractor] 
    potableReuseDataDf = potableReuseDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
    desalinationDataDf = desalinationSupplyData[desalinationSupplyData['Contractor'] == contractor] 
    desalinationDataDf = desalinationDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
    contractualTransfersDataDf = contractualTransfersSupplyData[contractualTransfersSupplyData['Contractor'] == contractor] 
    contractualTransfersDataDf = contractualTransfersDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
    localSurfaceDataDf = localSurfaceSupplyData[localSurfaceSupplyData['Contractor'] == contractor] 
    localSurfaceDataDf = localSurfaceDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
    otherImportedDataDf = otherImportedSupplyData[otherImportedSupplyData['Contractor'] == contractor] 
    otherImportedDataDf = otherImportedDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
    groundwaterDataDf = localGroundwaterSupplyData[localGroundwaterSupplyData['Contractor'] == contractor] 
    groundwaterDataDf = groundwaterDataDf[['Supply', 'Contractor', 'Supply Type', futureYear]]
    contractorSupplies = []
    recyclingSupplies = []
    potableReuseSupplies = []
    desalinationSupplies = []
    contractualTransfersSupplies = []
    localSurfaceSupplies = []
    otherImportedSupplies = []
    groundwaterSupplies = []
    

    for i in range(len(historicHydrologyYears)):
        contractorSupplies.append(        
            contractorDf[contractorDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
        supplyYearsForTotalSupplies[contractor] = contractorSupplies
    calculatedTotalSuppliesDf = pd.DataFrame(supplyYearsForTotalSupplies)  
    calculatedTotalSuppliesDf.to_csv('calculatedTotalSupplies.csv')
    
    for j in range(len(historicHydrologyYears)):
        recyclingSupplies.append(
            recyclingDataDf[recyclingDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
        supplyYearsForRecycleSupplies[contractor] = recyclingSupplies
    calculatedRecyclingSuppliesDf = pd.DataFrame(supplyYearsForRecycleSupplies) 
    # finalRecyclingSuppliesDf = calculatedRecyclingSuppliesDf.join(recyclingSupplyData['Supply Type'])
    
    for k in range(len(historicHydrologyYears)):
        potableReuseSupplies.append(
            potableReuseDataDf[potableReuseDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
        supplyYearsForPotableReuseSupplies[contractor] = potableReuseSupplies
    calculatedPotableReuseSuppliesDf = pd.DataFrame(supplyYearsForPotableReuseSupplies)
    # finalPotableReuseSuppliesDf = calculatedPotableReuseSuppliesDf.join(potableReuseSupplyData['Supply Type'])
    
    for l in range(len(historicHydrologyYears)):
        desalinationSupplies.append(
            desalinationDataDf[desalinationDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
        supplyYearsForDesalinationSupplies[contractor] = desalinationSupplies
    calculatedDesalinationSuppliesDf = pd.DataFrame(supplyYearsForDesalinationSupplies)
    # finalDesalinationSuppliesDf = calculatedDesalinationSuppliesDf.join(desalinationSupplyData['Supply Type'])
    
    for m in range(len(historicHydrologyYears)):
        contractualTransfersSupplies.append(
            contractualTransfersDataDf[contractualTransfersDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
        supplyYearsForContractualTransfersSupplies[contractor] = contractualTransfersSupplies
    calculatedContractualTransfersSuppliesDf = pd.DataFrame(supplyYearsForContractualTransfersSupplies)
    # finalContractualTransfersSuppliesDf = calculatedContractualTransfersSuppliesDf.join(contractualTransfersSupplyData['Supply Type'])
    
    for n in range(len(historicHydrologyYears)):
        localSurfaceSupplies.append(
            localSurfaceDataDf[localSurfaceDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
        supplyYearsForLocalSurfaceSupplies[contractor] = localSurfaceSupplies
    calculatedLocalSurfaceSuppliesDf = pd.DataFrame(supplyYearsForLocalSurfaceSupplies)
    # finalLocalSurfaceSuppliesDf = calculatedLocalSurfaceSuppliesDf.join(localSurfaceSupplyData['Supply Type'])
    
    for o in range(len(historicHydrologyYears)):
        otherImportedSupplies.append(
            otherImportedDataDf[otherImportedDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
        supplyYearsForOtherImportedSupplies[contractor] = otherImportedSupplies
    calculatedOtherImportedSuppliesDf = pd.DataFrame(supplyYearsForOtherImportedSupplies)
    # finalOtherImportedSuppliesDf = calculatedOtherImportedSuppliesDf.join(otherImportedSupplyData['Supply Type'])
    
    for p in range(len(historicHydrologyYears)):
        groundwaterSupplies.append(
            groundwaterDataDf[groundwaterDataDf['Supply'] == mapYearType[conYearType[i]]][futureYear].values[0]
            )
        supplyYearsForGroundwaterSupplies[contractor] = groundwaterSupplies
    calculatedLocalGroundwaterSuppliesDf = pd.DataFrame(supplyYearsForGroundwaterSupplies)  
    # finalLocalGroundwaterSuppliesDf = calculatedLocalGroundwaterSuppliesDf.join(localGroundwaterSupplyData['Supply Type'])

suppliesDataframesCompiled = [calculatedRecyclingSuppliesDf, calculatedPotableReuseSuppliesDf, calculatedDesalinationSuppliesDf, calculatedContractualTransfersSuppliesDf, calculatedLocalSurfaceSuppliesDf, calculatedOtherImportedSuppliesDf, calculatedLocalGroundwaterSuppliesDf, swpCVPSupplyDataDf]
suppliesDataframesCompiledDf = pd.concat(suppliesDataframesCompiled)

suppliesDataframesCompiledDfIndexSet = suppliesDataframesCompiledDf.set_index('Year')
suppliesDataframesCompiledDfTransposed = suppliesDataframesCompiledDfIndexSet.T
suppliesDataframesCompiledDfTransposedStacked = suppliesDataframesCompiledDfTransposed.stack()
suppliesDataframesCompiledDfTransposedStacked = suppliesDataframesCompiledDfTransposedStacked.to_frame()
suppliesDataframesCompiledDfTransposedStackedReset =  suppliesDataframesCompiledDfTransposedStacked.reset_index()
suppliesDataframesCompiledDfTransposedStackedReset.columns = ['Contractor', 'Year', 'Supply Volume']

finalSuppliesDf = suppliesDataframesCompiledDfTransposedStackedReset.reset_index([0]).join(supplyPriorityDf['Supply Type']).join(supplyPriorityDf['Supply Priority'])
del finalSuppliesDf['index']