from src.modelLogic.readDemandAssumptions import DemandAssumptions
from src.modelLogic.readSupplyAssumptions import SupplyAssumptions
from src.modelLogic.readSystemOperationsAssumptions import SystemOperationsAssumptions
from src.modelLogic.readContingentWMOsAssumptions import contingentConservationUseReduction, contingentConservationStorageTrigger, contingentConservationUnitCost, urbanPopulation, shortageThresholdForWaterMarketTransfers, transferLimit, waterMarketTransferCost
from src.modelLogic.readLongTermWMOsAssumptions import longtermWMOSurfaceVolume, longtermWMOSurfaceUnitCost, longtermWMOGroundwaterUnitCost, longtermWMODesalinationUnitCost, longtermWMORecycledUnitCost, longtermWMOPotableReuseUnitCost, longtermWMOTransfersExchangesUnitCost, longtermWMOOtherSupplyUnitCost, longtermWMOConservationUnitCost
from src.modelLogic.readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear, contractorDf, reclassYearType, UWMPhydrologicYearType

class InputData:
    def __init__(self):
        self.demandAssumptions = DemandAssumptions(contractorsList, futureYear, contractorDf, reclassYearType, historicHydrologyYears)
        self.supplyAssumptions = SupplyAssumptions(contractorsList, futureYear, contractorDf, UWMPhydrologicYearType, historicHydrologyYears)
        self.systemOperationsAssumptions = SystemOperationsAssumptions(contractorsList, futureYear, contractorDf, UWMPhydrologicYearType, historicHydrologyYears)
        
    # Get Global Assumptions
    def getContractorsList(self):
        return contractorsList
    
    def getHistoricHydrologyYears(self):
        return historicHydrologyYears
    
    def getFutureYear(self):
        return futureYear
    
    # Get Demand Input Assumptions
    def getTotalDemands(self):
        return self.demandAssumptions.totalDemands
    
    def getPlannedLongTermConservation(self):
        return self.demandAssumptions.plannedLongTermConservation
    
    # Get Supply Input Assumptions
    def getTotalLocalSupply(self):
        return self.supplyAssumptions.totalLocalSupply
    
    def getSwpCvpSupply(self):
        return self.supplyAssumptions.swpCVPSupply
    
    # Get System Operations Input Assumptions
    def getExcessWaterSwitchData(self):
        return self.systemOperationsAssumptions.excessWaterSwitchData
    
    def getStorageData(self):
        return self.systemOperationsAssumptions.storageData
    
    def getStorageHedgingStrategyData(self):
        return self.systemOperationsAssumptions.storageHedgingStrategyData
    
    def getGroundwaterBankPutUnitCost(self):
        return self.systemOperationsAssumptions.groundwaterBankPutUnitCost
    
    def getGroundwaterBankTakeUnitCost(self):
        return self.systemOperationsAssumptions.groundwaterBankTakeUnitCost
    
    def getSwpCVPDeliveryUnitCost(self):
        return self.systemOperationsAssumptions.swpCVPDeliveryUnitCost
    
    def getGroundwaterPumpingUnitCost(self):
        return self.systemOperationsAssumptions.groundwaterPumpingUnitCost
    
    def getWaterTreatmentUnitCost(self):
        return self.systemOperationsAssumptions.waterTreatmentUnitCost
    
    def getDistributionUnitCost(self):
        return self.systemOperationsAssumptions.distributionUnitCost
    
    def getWastewaterTreatmentUnitCost(self):
        return self.systemOperationsAssumptions.wastewaterTreatmentUnitCost
    
    def getWastewaterTreatmentFraction(self):
        return self.systemOperationsAssumptions.wastewaterTreatmentFraction
    
    # Get Contingent WMOs Input Assumptions
    def getContingentConservationUseReduction(self):
        return contingentConservationUseReduction
    
    def getContingentConservationStorageTrigger(self):
        return contingentConservationStorageTrigger
    
    def getContingentConservationUnitCost(self):
        return contingentConservationUnitCost
    
    def getUrbanPopulation(self):
        return urbanPopulation
    
    def getShortageThresholdForWaterMarketTransfers(self):
        return shortageThresholdForWaterMarketTransfers
    
    def getTransferLimit(self):
        return transferLimit 
    
    def getWaterMarketTransferCost(self):
        return waterMarketTransferCost
    
    # Get Long-term WMOs Input Assumptions
    def getLongtermWMOSurfaceVolume(self):
        return longtermWMOSurfaceVolume
    
    def getLongtermWMOSurfaceUnitCost(self):
        return longtermWMOSurfaceUnitCost
    
    def getLongtermWMOGroundwaterUnitCost(self):
        return longtermWMOGroundwaterUnitCost
    
    def getLongtermWMODesalinationUnitCost(self):
        return longtermWMODesalinationUnitCost
    
    def getLongtermWMORecycledUnitCost(self):
        return longtermWMORecycledUnitCost
    
    def getLongtermWMOPotableReuseUnitCost(self):
        return longtermWMOPotableReuseUnitCost
    
    def getLongtermWMOTransfersExchangesUnitCost(self):
        return longtermWMOTransfersExchangesUnitCost
    
    def getLongtermWMOOtherSupplyUnitCost(self):
        return longtermWMOOtherSupplyUnitCost
    
    def getLongtermWMOConservationUnitCost(self):
        return longtermWMOConservationUnitCost