import pandas as pd
from src.modelLogic.inputData import InputData

class OutputHandler:
    def __init__(self, inputData: InputData):
        
        #After variables are calculated, convert to dictionary then to panda dataframes
        self.inputData = inputData        
        self.appliedDemands = {'Year': self.inputData.historicHydrologyYears} 
        
        self.demandsToBeMetBySWPCVP = {'Year': self.inputData.historicHydrologyYears}
        self.SWPCVPSupplyDelivery = {'Year': self.inputData.historicHydrologyYears}
        self.excessSupply = {'Year': self.inputData.historicHydrologyYears}
        self.groundwaterPumpingReduction = {'Year': self.inputData.historicHydrologyYears}
        self.unallocatedSWPCVPDeliveries = {'Year': self.inputData.historicHydrologyYears}
        
        # Surface carryover and banked groundwater storage dataframes
        self.demandsToBeMetByStorage = {'Year': self.inputData.historicHydrologyYears}
        self.volumeSurfaceCarryover = {'Year': self.inputData.historicHydrologyYears}
        self.volumeGroundwaterBank = {'Year': self.inputData.historicHydrologyYears}
        self.availableCapacitySurface = {'Year': self.inputData.historicHydrologyYears}
        self.availableGroundwaterCapacity = {'Year': self.inputData.historicHydrologyYears}
        self.putGroundwater = {'Year': self.inputData.historicHydrologyYears}
        self.putSurface = {'Year': self.inputData.historicHydrologyYears}
        self.takeSurface = {'Year': self.inputData.historicHydrologyYears}
        self.takeGroundwater = {'Year': self.inputData.historicHydrologyYears}
        

        # Hedging strategy dataframes
        self.pctCapacitySurfaceCarryover = {'Year': self.inputData.historicHydrologyYears}
        self.pctStorageCalledSurfaceCarryover = {'Year': self.inputData.historicHydrologyYears}
        self.pctCapacityGroundwaterBank = {'Year': self.inputData.historicHydrologyYears}
        self.pctStorageCalledGroundwaterBank = {'Year': self.inputData.historicHydrologyYears}

        # Contingent WMOs dataframes
        self.demandsToBeMetByContingentOptions = {'Year': self.inputData.historicHydrologyYears}
        self.contingentConservationReductionVolume = {'Year': self.inputData.historicHydrologyYears}
        self.waterMarketTransferDeliveries = {'Year': self.inputData.historicHydrologyYears}

        self.totalShortage = {'Year': self.inputData.historicHydrologyYears}
        
        # System Operations Cost dataframes
        self.swpCVPDeliveryCost = {'Year': self.inputData.historicHydrologyYears}
        self.putGroundwaterBankCost = {'Year': self.inputData.historicHydrologyYears}
        self.takeGroundwaterBankCost = {'Year': self.inputData.historicHydrologyYears}
        self.groundwaterPumpingSavings = {'Year': self.inputData.historicHydrologyYears}
        self.waterTreatmentCost = {'Year': self.inputData.historicHydrologyYears}
        self.distributionCost = {'Year': self.inputData.historicHydrologyYears}
        self.wastewaterTreatmentCost = {'Year': self.inputData.historicHydrologyYears}

        # Long-term WMO costs
        self.surfaceLongTermWMOCost = {'Year': self.inputData.historicHydrologyYears}
        self.groundwaterLongTermWMOCost = {'Year': self.inputData.historicHydrologyYears}
        self.desalinationLongTermWMOCost = {'Year': self.inputData.historicHydrologyYears}
        self.recycledLongTermWMOCost = {'Year': self.inputData.historicHydrologyYears}
        self.potableReuseLongTermWMOCost = {'Year': self.inputData.historicHydrologyYears}
        self.transfersAndExchangesLongTermWMOCost = {'Year': self.inputData.historicHydrologyYears}
        self.otherSupplyLongTermWMOCost = {'Year': self.inputData.historicHydrologyYears}
        self.conservationLongTermWMOCost = {'Year': self.inputData.historicHydrologyYears}

        
        self.waterMarketTransferCost = {'Year': self.inputData.historicHydrologyYears}
        
        self.totalReliabilityMgmtCost = {'Year': self.inputData.historicHydrologyYears}
        self.totalEconomicLoss = {'Year': self.inputData.historicHydrologyYears}
        self.totalAnnualCost = {'Year': self.inputData.historicHydrologyYears}
        
        self.averageTotalAnnualCost = {'Contractor': self.inputData.contractorsList}
        
        
    def writeToSystemwideOutputDataframes(self):
        self.appliedDemands = pd.DataFrame(self.appliedDemands)
        
        self.demandsToBeMetBySWPCVP = pd.DataFrame(self.demandsToBeMetBySWPCVP)
        self.SWPCVPSupplyDelivery = pd.DataFrame(self.SWPCVPSupplyDelivery)
        self.excessSupply = pd.DataFrame(self.excessSupply)
        self.unallocatedSWPCVPDeliveries = pd.DataFrame(self.unallocatedSWPCVPDeliveries)

        self.demandsToBeMetByStorage = pd.DataFrame(self.demandsToBeMetByStorage)
        self.volumeSurfaceCarryover = pd.DataFrame(self.volumeSurfaceCarryover)
        self.volumeGroundwaterBank = pd.DataFrame(self.volumeGroundwaterBank)
        self.availableCapacitySurface = pd.DataFrame(self.availableCapacitySurface)
        self.availableGroundwaterCapacity = pd.DataFrame(self.availableGroundwaterCapacity)
        self.putGroundwater = pd.DataFrame(self.putGroundwater)
        self.putSurface = pd.DataFrame(self.putSurface)
        self.takeSurface= pd.DataFrame(self.takeSurface)
        self.takeGroundwater = pd.DataFrame(self.takeGroundwater)
        

        self.demandsToBeMetByContingentOptions = pd.DataFrame(self.demandsToBeMetByContingentOptions)
        self.contingentConservationReductionVolume = pd.DataFrame(self.contingentConservationReductionVolume)
        self.waterMarketTransferDeliveries = pd.DataFrame(self.waterMarketTransferDeliveries)
        self.totalShortage = pd.DataFrame(self.totalShortage)
        
        #Cost dataframes
        #System Operations costs
        self.swpCVPDeliveryCost = pd.DataFrame(self.swpCVPDeliveryCost)
        self.putGroundwaterBankCost = pd.DataFrame(self.putGroundwaterBankCost)
        self.takeGroundwaterBankCost = pd.DataFrame(self.takeGroundwaterBankCost)
        self.groundwaterPumpingSavings = pd.DataFrame(self.groundwaterPumpingSavings)
        self.waterTreatmentCost = pd.DataFrame(self.waterTreatmentCost)
        self.distributionCost = pd.DataFrame(self.distributionCost)
        self.wastewaterTreatmentCost = pd.DataFrame(self.wastewaterTreatmentCost)

        # WMO Costs
        self.surfaceLongTermWMOCost = pd.DataFrame(self.surfaceLongTermWMOCost)
        self.groundwaterLongTermWMOCost = pd.DataFrame(self.groundwaterLongTermWMOCost)
        self.desalinationLongTermWMOCost = pd.DataFrame(self.desalinationLongTermWMOCost)
        self.recycledLongTermWMOCost = pd.DataFrame(self.recycledLongTermWMOCost)
        self.potableReuseLongTermWMOCost = pd.DataFrame(self.potableReuseLongTermWMOCost)
        self.transfersAndExchangesLongTermWMOCost = pd.DataFrame(self.transfersAndExchangesLongTermWMOCost)
        self.otherSupplyLongTermWMOCost = pd.DataFrame(self.otherSupplyLongTermWMOCost)
        self.conservationLongTermWMOCost = pd.DataFrame(self.conservationLongTermWMOCost)

        self.waterMarketTransferCost = pd.DataFrame(self.waterMarketTransferCost)

        # Total Costs
        self.totalReliabilityMgmtCost = pd.DataFrame(self.totalReliabilityMgmtCost)
        self.totalEconomicLoss = pd.DataFrame(self.totalEconomicLoss)
        self.totalAnnualCost = pd.DataFrame(self.totalAnnualCost)
        
        self.averageTotalAnnualCost = pd.DataFrame(self.averageTotalAnnualCost)