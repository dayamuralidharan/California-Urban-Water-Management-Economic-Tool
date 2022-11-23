import os
import pandas as pd
from modelLogic.readGlobalAssumptions import contractorsList, historicHydrologyYears, hydroYearType, UWMPhydrologicYearType, futureYear

# Input directories and filenames
dirname = os.path.dirname(__file__)

# Input Assumptions
contingentConservationInputData = "src/inputData/contingentWMOsInput_Conservation.csv"
waterMarketTransfersInputData = "src/inputData/contingentWMOsInput_WaterMarketTransfers.csv"

#inputContingentConservationFile = os.path.join(dirname, contingentConservationInputData)


# contingentConservationData = pd.read_csv(inputContingentConservationFile)
contingentConservationData = pd.read_csv(contingentConservationInputData)
waterMarketTransfersData = pd.read_csv(waterMarketTransfersInputData)

#contingentConservationData.set_index('Contractor', inplace = True)
waterMarketTransfersData.set_index('Contractor', inplace = True)

# Definition of Contingent Conservation Variables
contingentConservationUseReduction = contingentConservationData[contingentConservationData['Variable'] == 'Use Reduction with Contingency Conservation Campaign (% of Total Applied Use)']
contingentConservationStorageTrigger = contingentConservationData[contingentConservationData['Variable'] == 'Storage Volume Trigger for Contingency Conservation (AF)']

# Definition of Water Market Transfers Variables
shortageThresholdForWaterMarketTransfers = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Shortage Threshold before Water Market Transfer Supplies are Delivered (% of Total Applied Use)']
waterMarketLossFactor = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Water Market Transfer Loss Factor (%)']

transferLimit_NormalOrBetterYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Transfer Limit for Normal or Better Years (AFY)']
transferLimit_DryYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Transfer Limit for Dry Years (AFY)']
transferLimit_ConsecutiveDryYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Transfer Limit for 2 or More Consecutive Years (% of Dry-Year limit defined above)']

waterMarketTransferCost_WetYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Wet Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
waterMarketTransferCost_AboveNormalYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Above Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
waterMarketTransferCost_BelowNormalYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Below Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
waterMarketTransferCost_DryYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
waterMarketTransferCost_CriticallyDryYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Critically Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']


transferLimit_NormalOrBetterYears.drop('Variable', axis=1, inplace=True)
transferLimit_DryYears.drop('Variable', axis=1, inplace=True)
transferLimit_ConsecutiveDryYears.drop('Variable', axis=1, inplace=True)
waterMarketTransferCost_WetYears.drop('Variable', axis=1, inplace=True)
waterMarketTransferCost_AboveNormalYears.drop('Variable', axis=1, inplace=True)
waterMarketTransferCost_BelowNormalYears.drop('Variable', axis=1, inplace=True)
waterMarketTransferCost_DryYears.drop('Variable', axis=1, inplace=True)
waterMarketTransferCost_CriticallyDryYears.drop('Variable', axis=1, inplace=True)

# Set up time series of water market transfer limits and costs based on the hydrologic year type
waterMarketTransferCost = {'Year': historicHydrologyYears}
transferLimit = {'Year': historicHydrologyYears}

for contractor in contractorsList:
    contractorYearType = hydroYearType[contractor] # Wet, Above Normal, Below Normal, Dry, Critically Dry
    contractorUWMPYearType = UWMPhydrologicYearType[contractor] # Normal or Better, Single Dry, Multi-Dry
    contractorTransferLimit = []
    contractorWaterMarketTransferCost = []
    
    for i in range(len(historicHydrologyYears)):
        
        if contractorYearType[i] == "W":
            contractorWaterMarketTransferCost.append(waterMarketTransferCost_WetYears.loc[contractor][futureYear])
        elif contractorYearType[i] == "AN":
            contractorWaterMarketTransferCost.append(waterMarketTransferCost_AboveNormalYears.loc[contractor][futureYear])
        elif contractorYearType[i] == "BN":
            contractorWaterMarketTransferCost.append(waterMarketTransferCost_BelowNormalYears.loc[contractor][futureYear])
        elif contractorYearType[i] == "D":
            contractorWaterMarketTransferCost.append(waterMarketTransferCost_DryYears.loc[contractor][futureYear])
        elif contractorYearType[i] == "C":
            contractorWaterMarketTransferCost.append(waterMarketTransferCost_CriticallyDryYears.loc[contractor][futureYear])
            
        if contractorUWMPYearType[i] == 'NB':
            contractorTransferLimit.append(transferLimit_NormalOrBetterYears.loc[contractor][futureYear])
        elif contractorUWMPYearType[i] == 'SD':
            contractorTransferLimit.append(transferLimit_DryYears.loc[contractor][futureYear])  
        elif contractorUWMPYearType[i] == 'MD':
            contractorTransferLimit.append(transferLimit_ConsecutiveDryYears.loc[contractor][futureYear])
    
    transferLimit[contractor] = contractorTransferLimit
    waterMarketTransferCost[contractor] = contractorWaterMarketTransferCost

transferLimit = pd.DataFrame(transferLimit)    
waterMarketTransferCost = pd.DataFrame(waterMarketTransferCost)
