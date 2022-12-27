import os
import pandas as pd

class ContingentWMOsAssumptions:
    def __init__(self, contractorsList, historicHydrologyYears, hydroYearType, UWMPhydrologicYearType, futureYear):
        # Input directories and filenames
        dirname = os.path.dirname(__file__)

        # Input Assumptions
        contingentConservationInputFile = "src/inputData/contingentWMOsInput_conservation.csv"
        waterMarketTransfersInputFile = "src/inputData/contingentWMOsInput_WaterMarketTransfers.csv"
        rationingProgramInputFile = "src/inputData/contingentWMOsInput_rationingProgram.csv"
        cutRatioInputFile = "src/inputData/contingentWMOsInput_cutRatios.csv"
        elasticityOfDemandInputFile = "src/inputData/contingentWMOsInput_elasticityofDemand.csv"

        # contingentConservationData = pd.read_csv(inputContingentConservationFile)
        contingentConservationInputData = pd.read_csv(contingentConservationInputFile)
        waterMarketTransfersInputData = pd.read_csv(waterMarketTransfersInputFile)
        rationingProgramInputData = pd.read_csv(rationingProgramInputFile)
        cutRatioInputData = pd.read_csv(cutRatioInputFile)
        elasticityOfDemandInputData = pd.read_csv(elasticityOfDemandInputFile)

        # Definition of Contingent Conservation Variables
        self.contingentConservationUseReduction = contingentConservationInputData[contingentConservationInputData['Variable'] == 'Use Reduction with Contingency Conservation Campaign (% of Total Applied Use)']
        self.contingentConservationStorageTrigger = contingentConservationInputData[contingentConservationInputData['Variable'] == 'Storage Volume Trigger for Contingency Conservation (AF)']
        self.contingentConservationUnitCost = contingentConservationInputData[contingentConservationInputData['Variable'] == 'Contingency Conservation Publicity Campaign Cost ($/capita)']
        self.urbanPopulation = contingentConservationInputData[contingentConservationInputData['Variable'] == 'Urban Population (thousands)']

        self.contingentConservationUnitCost.set_index('Contractor', inplace = True)
        self.urbanPopulation.set_index('Contractor', inplace = True)

        # Definition of Water Market Transfers Variables
        waterMarketTransfersInputData.set_index('Contractor', inplace = True)
        
        self.shortageThresholdForWaterMarketTransfers = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Shortage Threshold before Water Market Transfer Supplies are Delivered (% of Total Applied Use)']
        waterMarketLossFactor = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Water Market Transfer Loss Factor (%)']

        transferLimit_NormalOrBetterYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Transfer Limit for Normal or Better Years (AFY)']
        transferLimit_DryYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Transfer Limit for Dry Years (AFY)']
        transferLimit_ConsecutiveDryYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Transfer Limit for 2 or More Consecutive Years (% of Dry-Year limit defined above)']

        waterMarketTransferCost_WetYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Wet Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
        waterMarketTransferCost_AboveNormalYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Above Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
        waterMarketTransferCost_BelowNormalYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Below Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
        waterMarketTransferCost_DryYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']
        waterMarketTransferCost_CriticallyDryYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Critically Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/AF)']


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

        self.transferLimit = pd.DataFrame(transferLimit)    
        self.waterMarketTransferCost = pd.DataFrame(waterMarketTransferCost)


        # Definition of Rationing Program and Loss Function variables
        storageVolumeTriggerForRationingProgram = rationingProgramInputData[rationingProgramInputData['Variable'] == "Storage Volume Trigger for Rationing Programs (AF)"]
        costForRationingProgram = rationingProgramInputData[rationingProgramInputData['Variable'] == "Cost for Rationing Program ($/capita)"]
        consecutiveYearLossAdjustment = rationingProgramInputData[rationingProgramInputData['Variable'] == "Consecutive Year Loss Adjustment (%)"]
        demandHardeningAdjustmentFactor = rationingProgramInputData[rationingProgramInputData['Variable'] == "Demand Hardening Adjustment Factor (%)"]
        retailPrice = rationingProgramInputData[rationingProgramInputData['Variable'] == "Retail Price ($/AF)"]

        cutRatio_singleFamily = cutRatioInputData[cutRatioInputData['Variable'] == 'Single Family']
        cutRatio_multiFamily = cutRatioInputData[cutRatioInputData['Variable'] == 'Multi-Family']
        cutRatio_industrial = cutRatioInputData[cutRatioInputData['Variable'] == 'Industrial']
        cutRatio_commercial = cutRatioInputData[cutRatioInputData['Variable'] == 'Commercial']
        cutRatio_landscape = cutRatioInputData[cutRatioInputData['Variable'] == 'Landscape']

        elasticityOfDemand = elasticityOfDemandInputData[elasticityOfDemandInputData['Variable'] == 'Elasticity']
        lowerLossBoundary = elasticityOfDemandInputData[elasticityOfDemandInputData['Variable'] == 'Lower Loss Boundary']
        upperLossBoundary = elasticityOfDemandInputData[elasticityOfDemandInputData['Variable'] == 'Upper Loss Boundary']

        storageVolumeTriggerForRationingProgram.set_index('Contractor', inplace = True)
        costForRationingProgram.set_index('Contractor', inplace = True)
        consecutiveYearLossAdjustment.set_index('Contractor', inplace = True)
        demandHardeningAdjustmentFactor.set_index('Contractor', inplace = True)
        retailPrice.set_index('Contractor', inplace = True)

        cutRatio_singleFamily.set_index('Contractor', inplace = True)
        cutRatio_multiFamily.set_index('Contractor', inplace = True)
        cutRatio_industrial.set_index('Contractor', inplace = True)
        cutRatio_commercial.set_index('Contractor', inplace = True)
        cutRatio_landscape.set_index('Contractor', inplace = True)

        elasticityOfDemand.set_index('Contractor', inplace = True)
        lowerLossBoundary.set_index('Contractor', inplace = True)
        upperLossBoundary.set_index('Contractor', inplace = True)