import os
import pandas as pd
from readGlobalAssumptions import contractorsList, historicHydrologyYears, hydroYearType, futureYear

# Input directories and filenames
dirname = os.path.dirname(__file__)

# Input Assumptions
contingentConservationInputData = "../inputData/contingentWMOsInput_Conservation.csv"
waterMarketTransfersInputData = "../inputData/contingentWMOsInput_WaterMarketTransfers.csv"

#inputContingentConservationFile = os.path.join(dirname, contingentConservationInputData)


# contingentConservationData = pd.read_csv(inputContingentConservationFile)
contingentConservationData = pd.read_csv(contingentConservationInputData)
waterMarketTransfersData = pd.read_csv(waterMarketTransfersInputData)

# Definition of Contingent Conservation Variables
contingentConservationUseReduction = contingentConservationData[contingentConservationData['Variable'] == 'Use Reduction with Contingency Conservation Campaign (% of Total Applied Use)']
contingentConservationStorageTrigger = contingentConservationData[contingentConservationData['Variable'] == 'Storage Volume Trigger for Contingency Conservation (AF)']

# Definition of Water Market Transfers Variables
shortageThresholdForWaterMarketTransfers = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Shortage Threshold before Water Market Transfer Supplies are Delivered (% of Total Applied Use)']
waterMarketLossFactor = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Water Market Transfer Loss Factor (%)']
transferLimit_NormalOrBetterYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Transfer Limit for Normal or Better Years (AFY)']
transferLimit_DryYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Transfer Limit for Dry Years (AFY)']
transferLimit_ConsecutiveYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Transfer Limit for 2 or More Consecutive Years (% of Dry-Year limit defined above)']
waterMarketTransferCost_WetYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Wet Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
waterMarketTransferCost_AboveNormalYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Above Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
waterMarketTransferCost_BelowNormalYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Below Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
waterMarketTransferCost_DryYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
waterMarketTransferCost_CriticallyDryYears = waterMarketTransfersData[waterMarketTransfersData['Variable'] == 'Critically Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']

# Set up time series of water market transfer costs based on the hydrologic year type
waterMarketTransferCost = {'Year': historicHydrologyYears}

for contractor in contractorsList:
    contractorYearType = hydroYearType[contractor]
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
    
    waterMarketTransferCost[contractor] = contractorWaterMarketTransferCost
    
waterMarketTransferCost = pd.DataFrame(waterMarketTransferCost)
