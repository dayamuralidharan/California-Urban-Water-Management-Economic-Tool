from src.modelLogic.readDemandAssumptions import totalDemands, plannedLongTermConservation
from src.modelLogic.readSupplyAssumptions import totalLocalSupply, swpCVPSupply
from src.modelLogic.readSystemOperationsAssumptions import storageData,  storageHedgingStrategyData, excessWaterSwitchData, groundwaterBankPutUnitCost, groundwaterBankTakeUnitCost, swpCVPDeliveryUnitCost, groundwaterPumpingUnitCost, waterTreatmentUnitCost, distributionUnitCost, wastewaterTreatmentUnitCost, wastewaterTreatmentFraction
from src.modelLogic.readContingentWMOsAssumptions import contingentConservationUseReduction, contingentConservationStorageTrigger, contingentConservationUnitCost, urbanPopulation, shortageThresholdForWaterMarketTransfers, transferLimit, waterMarketTransferCost
from src.modelLogic.readLongTermWMOsAssumptions import longtermWMOSurfaceVolume, longtermWMOSurfaceUnitCost, longtermWMOGroundwaterUnitCost, longtermWMODesalinationUnitCost, longtermWMORecycledUnitCost, longtermWMOPotableReuseUnitCost, longtermWMOTransfersExchangesUnitCost, longtermWMOOtherSupplyUnitCost, longtermWMOConservationUnitCost

class InputData:
    # Get Demand Input Assumptions
    def getTotalDemands(self):
        return totalDemands
    
    def getPlannedLongTermConservation(self):
        return plannedLongTermConservation
    
    # Get Supply Input Assumptions
    def getTotalLocalSupply(self):
        return totalLocalSupply
    
    def getSwpCvpSupply(self):
        return swpCVPSupply
    
    # Get System Operations Input Assumptions
    def getExcessWaterSwitchData(self):
        return excessWaterSwitchData
    
    def getStorageData(self):
        return storageData
    
    def getStorageHedgingStrategyData(self):
        return storageHedgingStrategyData
    
    def getGroundwaterBankPutUnitCost(self):
        return groundwaterBankPutUnitCost
    
    def getGroundwaterBankTakeUnitCost(self):
        return groundwaterBankTakeUnitCost
    
    def getSwpCVPDeliveryUnitCost(self):
        return swpCVPDeliveryUnitCost
    
    def getGroundwaterPumpingUnitCost(self):
        return groundwaterPumpingUnitCost
    
    def getWaterTreatmentUnitCost(self):
        return waterTreatmentUnitCost
    
    def getDistributionUnitCost(self):
        return distributionUnitCost
    
    def getWastewaterTreatmentUnitCost(self):
        return wastewaterTreatmentUnitCost
    
    def getWastewaterTreatmentFraction(self):
        return wastewaterTreatmentFraction
    
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