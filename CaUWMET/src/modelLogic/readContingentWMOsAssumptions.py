import pandas as pd
import warnings

class ContingentWMOsAssumptions:
    def __init__(self, globalAssumptions, inputDataLocations):
        warnings.filterwarnings("ignore")
        
        # Input directories and filenames
        contingentConservationInputData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Contingent WMOs Assumptions', skiprows = 5, nrows = 181, usecols = 'A:H')
        waterMarketTransfersInputData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Contingent WMOs Assumptions', skiprows = 192, nrows = 457, usecols = 'A:H')
        rationingProgramInputData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Contingent WMOs Assumptions', skiprows = 655, nrows = 272, usecols = 'A:H')
        cutRatioInputData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Contingent WMOs Assumptions', skiprows = 747, nrows = 44, usecols = 'A:H')
        elasticityOfDemandInputData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Contingent WMOs Assumptions', skiprows = 838, nrows = 44, usecols = 'A:H')
        
        cutRatioInputData.set_index('Contractor', inplace = True)
        rationingProgramInputData.set_index('Contractor', inplace = True)
        elasticityOfDemandInputData.set_index('Contractor', inplace = True)

        # Set Contingent Conservation Variables
        self.contingentConservationUseReduction = contingentConservationInputData[contingentConservationInputData['Variable'] == 'Use Reduction with Contingency Conservation Campaign (% of Total Applied Use)']
        self.contingentConservationStorageTrigger = contingentConservationInputData[contingentConservationInputData['Variable'] == 'Storage Volume Trigger for Contingency Conservation (AF)']
        self.contingentConservationUnitCost = contingentConservationInputData[contingentConservationInputData['Variable'] == 'Contingency Conservation Publicity Campaign Cost ($/capita)']
        self.urbanPopulation = contingentConservationInputData[contingentConservationInputData['Variable'] == 'Urban Population (thousands)']

        self.contingentConservationUnitCost.set_index('Contractor', inplace = True)
        self.urbanPopulation.set_index('Contractor', inplace = True)

        # Set Water Market Transfers Variables
        waterMarketTransfersInputData.set_index('Contractor', inplace = True)
        
        self.shortageThresholdForWaterMarketTransfers = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Shortage Threshold before Water Market Transfer Supplies are Delivered (% of Total Applied Use)']
        self.waterMarketLossFactor = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Water Market Transfer Loss Factor (%)']

        transferLimit_NormalOrBetterYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Transfer Limit for Normal or Better Years (acre-feet/year)']
        transferLimit_DryYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Transfer Limit for Dry Years (acre-feet/year)']
        transferLimitPortion_ConsecutiveDryYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Transfer Limit for 2 or More Consecutive Years (% of Dry-Year limit defined above)']

        waterMarketTransferCost_WetYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Wet Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)']
        waterMarketTransferCost_AboveNormalYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Above Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)']
        waterMarketTransferCost_BelowNormalYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Below Normal Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)']
        waterMarketTransferCost_DryYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)']
        waterMarketTransferCost_CriticallyDryYears = waterMarketTransfersInputData[waterMarketTransfersInputData['Variable'] == 'Critically Dry Year Water Market Transfers and Exchanges Supply Unit Cost ($/acre-feet)']

        transferLimit_NormalOrBetterYears.drop('Variable', axis=1, inplace=True)
        transferLimit_DryYears.drop('Variable', axis=1, inplace=True)
        transferLimitPortion_ConsecutiveDryYears.drop('Variable', axis=1, inplace=True)
        waterMarketTransferCost_WetYears.drop('Variable', axis=1, inplace=True)
        waterMarketTransferCost_AboveNormalYears.drop('Variable', axis=1, inplace=True)
        waterMarketTransferCost_BelowNormalYears.drop('Variable', axis=1, inplace=True)
        waterMarketTransferCost_DryYears.drop('Variable', axis=1, inplace=True)
        waterMarketTransferCost_CriticallyDryYears.drop('Variable', axis=1, inplace=True)

        # Set up time series of water market transfer limits and costs based on the hydrologic year type
        waterMarketTransferCost = {'Year': globalAssumptions.historicHydrologyYears}
        transferLimit = {'Year': globalAssumptions.historicHydrologyYears}

        for contractor in globalAssumptions.contractorsList:
            contractorYearType = globalAssumptions.hydroYearType[contractor] # Wet, Above Normal, Below Normal, Dry, Critically Dry
            contractorUWMPYearType = globalAssumptions.UWMPhydrologicYearType[contractor] # Normal or Better, Single Dry, Multi-Dry
            contractorTransferLimit = []
            contractorWaterMarketTransferCost = []
            
            for i in range(len(globalAssumptions.historicHydrologyYears)):
                
                if contractorYearType[i] == "W":
                    contractorWaterMarketTransferCost.append(waterMarketTransferCost_WetYears.loc[contractor][int(globalAssumptions.futureYear)])
                elif contractorYearType[i] == "AN":
                    contractorWaterMarketTransferCost.append(waterMarketTransferCost_AboveNormalYears.loc[contractor][int(globalAssumptions.futureYear)])
                elif contractorYearType[i] == "BN":
                    contractorWaterMarketTransferCost.append(waterMarketTransferCost_BelowNormalYears.loc[contractor][int(globalAssumptions.futureYear)])
                elif contractorYearType[i] == "D":
                    contractorWaterMarketTransferCost.append(waterMarketTransferCost_DryYears.loc[contractor][int(globalAssumptions.futureYear)])
                elif contractorYearType[i] == "C":
                    contractorWaterMarketTransferCost.append(waterMarketTransferCost_CriticallyDryYears.loc[contractor][int(globalAssumptions.futureYear)])
                    
                if contractorUWMPYearType[i] == 'NB':
                    contractorTransferLimit.append(transferLimit_NormalOrBetterYears.loc[contractor][int(globalAssumptions.futureYear)])
                elif contractorUWMPYearType[i] == 'SD':
                    contractorTransferLimit.append(transferLimit_DryYears.loc[contractor][int(globalAssumptions.futureYear)])  
                elif contractorUWMPYearType[i] == 'MD':
                    contractorTransferLimit.append(transferLimit_DryYears.loc[contractor][int(globalAssumptions.futureYear)] * (transferLimitPortion_ConsecutiveDryYears.loc[contractor][int(globalAssumptions.futureYear)] / 100))
            
            transferLimit[contractor] = contractorTransferLimit
            waterMarketTransferCost[contractor] = contractorWaterMarketTransferCost

        self.transferLimit = pd.DataFrame(transferLimit)    
        self.waterMarketTransferCost = pd.DataFrame(waterMarketTransferCost)


        # Set Rationing Program and Loss Function variables
        self.storageVolumeTriggerForRationingProgram = rationingProgramInputData[rationingProgramInputData['Variable'] == "Storage Volume Trigger for Rationing Programs (AF)"][int(globalAssumptions.futureYear)]
        self.costForRationingProgram = rationingProgramInputData[rationingProgramInputData['Variable'] == "Cost for Rationing Program ($/capita)"][int(globalAssumptions.futureYear)]
        self.demandHardeningFactor = rationingProgramInputData[rationingProgramInputData['Variable'] == "Demand Hardening Adjustment Factor (%)"] #TODO get just for future year here
        self.retailPrice = rationingProgramInputData[rationingProgramInputData['Variable'] == "Retail Price ($/acre-foot)"][int(globalAssumptions.futureYear)]

        self.cutRatio_singleFamily = cutRatioInputData['Single Family']
        self.cutRatio_multiFamily = cutRatioInputData['Multi-Family']
        self.cutRatio_industrial = cutRatioInputData['Industrial']
        self.cutRatio_commAndGov = cutRatioInputData['Commercial']
        self.cutRatio_landscape = cutRatioInputData['Landscape']

        self.elasticityOfDemand_singleFamily = elasticityOfDemandInputData['Elasticity']
        self.elasticityOfDemand_multiFamily = elasticityOfDemandInputData['Elasticity']
        self.elasticityOfDemand_industrial = elasticityOfDemandInputData['Elasticity']
        self.elasticityOfDemand_commAndGov = elasticityOfDemandInputData['Elasticity']
        self.elasticityOfDemand_landscape = elasticityOfDemandInputData['Elasticity']
        
        self.lowerLossBoundary = elasticityOfDemandInputData['Lower Loss Boundary']
        self.upperLossBoundary = elasticityOfDemandInputData['Upper Loss Boundary']