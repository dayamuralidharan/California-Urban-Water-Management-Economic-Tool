import pandas as pd
from src.modelLogic.inputData import InputData

class OutputHandler:
    def __init__(self, inputData: InputData):
        self.inputData = inputData        
        self.appliedDemands = {'Year': self.inputData.historicHydrologyYears} 
        self.demandsToBeMetBySWPCVP = {'Year': self.inputData.historicHydrologyYears}
        self.demandsToBeMetByStorage = {'Year': self.inputData.historicHydrologyYears}
        self.demandsToBeMetByBankedGW = {'Year': self.inputData.historicHydrologyYears}
        self.excessSupply = {'Year': self.inputData.historicHydrologyYears}
        self.groundwaterPumpingReduction = {'Year': self.inputData.historicHydrologyYears}

        # Surface carryover and banked groundwater storage dataframes
        self.volumeSurfaceCarryover = {'Year': self.inputData.historicHydrologyYears}
        self.volumeGroundwaterBank = {'Year': self.inputData.historicHydrologyYears}
        self.availableCapacitySurface = {'Year': self.inputData.historicHydrologyYears}
        self.availableGroundwaterCapacity = {'Year': self.inputData.historicHydrologyYears}
        self.putGroundwater = {'Year': self.inputData.historicHydrologyYears}
        self.putSurface = {'Year': self.inputData.historicHydrologyYears}
        self.takeSurface = {'Year': self.inputData.historicHydrologyYears}
        self.takeGroundwater = {'Year': self.inputData.historicHydrologyYears}
        self.putGroundwaterBankCost = {'Year': self.inputData.historicHydrologyYears}
        self.takeGroundwaterBankCost = {'Year': self.inputData.historicHydrologyYears}

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
        
        self.totalReliabilityMgmtCost = {'Year': self.inputData.historicHydrologyYears}
        self.totalEconomicLoss = {'Year': self.inputData.historicHydrologyYears}
        self.totalAnnualCost = {'Year': self.inputData.historicHydrologyYears}
        
    def saveToOutputDataframes(self):
        self.appliedDemands = pd.DataFrame(self.appliedDemands)
        self.demandsToBeMetBySWPCVP = pd.DataFrame(self.demandsToBeMetBySWPCVP)
        
        self.excessSupply = pd.DataFrame(self.excessSupply)
        self.demandsToBeMetByStorage = pd.DataFrame(self.demandsToBeMetByStorage)
        self.volumeSurfaceCarryover = pd.DataFrame(self.volumeSurfaceCarryover)
        self.volumeGroundwaterBank = pd.DataFrame(self.volumeGroundwaterBank)
        self.availableCapacitySurface = pd.DataFrame(self.availableCapacitySurface)
        self.availableGroundwaterCapacity = pd.DataFrame(self.availableGroundwaterCapacity)
        self.putGroundwater = pd.DataFrame(self.putGroundwater)
        self.putSurface = pd.DataFrame(self.putSurface)
        self.takeSurface= pd.DataFrame(self.takeSurface)
        self.takeGroundwater = pd.DataFrame(self.takeGroundwater)
        self.putGroundwaterBankCost = pd.DataFrame(self.putGroundwaterBankCost)
        self.takeGroundwaterBankCost = pd.DataFrame(self.takeGroundwaterBankCost)

        self.demandsToBeMetByContingentOptions = pd.DataFrame(self.demandsToBeMetByContingentOptions)
        self.contingentConservationReductionVolume = pd.DataFrame(self.contingentConservationReductionVolume)
        self.waterMarketTransferDeliveries = pd.DataFrame(self.waterMarketTransferDeliveries)
        self.totalShortage = pd.DataFrame(self.totalShortage)
        
        self.totalReliabilityMgmtCost = pd.DataFrame(self.totalReliabilityMgmtCost)
        self.totalEconomicLoss = pd.DataFrame(self.totalEconomicLoss)
        self.totalAnnualCost = pd.DataFrame(self.totalAnnualCost)
        
        
        
        
        
        
        # self.appliedDemands.to_excel(self.writer, sheet_name = 'appliedDemands')
        # self.demandsToBeMetBySWPCVP.to_excel(self.writer, sheet_name = 'demandsToBeMetBySWPCVP')
        # self.demandsToBeMetByStorage.to_excel(self.writer, sheet_name = 'demandsToBeMetByStorage')
        # self.volumeSurfaceCarryover.to_excel(self.writer, sheet_name = 'volumeSurfaceCarryover')
        # self.volumeGroundwaterBank.to_excel(self.writer, sheet_name = 'volumeGroundwaterBank')
        # self.availableCapacitySurface.to_excel(self.writer, sheet_name = 'availableCapacitySurface')
        # self.availableGroundwaterCapacity.to_excel(self.writer, sheet_name = 'availableGroundwaterCapacity')
        # self.putGroundwater.to_excel(self.writer, sheet_name = 'putGroundwater')
        # self.putSurface.to_excel(self.writer, sheet_name = 'putSurface')
        # self.takeGroundwater.to_excel(self.writer, sheet_name = 'takeGroundwater')
        # self.takeSurface.to_excel(self.writer, sheet_name = 'takeSurface')

        # workbook = self.writer.book
        # #demandsToBeMetByContingentOptions.to_excel(writer, sheet_name = 'demandsToBeMetByContingentWMOs')
        # self.writer.save()