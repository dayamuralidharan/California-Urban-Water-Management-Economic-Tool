from src.modelLogic.readDemandAssumptions import DemandAssumptions
from src.modelLogic.readSupplyAssumptions import SupplyAssumptions
from src.modelLogic.readSystemOperationsAssumptions import SystemOperationsAssumptions
from src.modelLogic.readContingentWMOsAssumptions import ContingentWMOsAssumptions
from src.modelLogic.readLongTermWMOsAssumptions import LongTermWMOsAssumptions
from src.modelLogic.readGlobalAssumptions import GlobalAssumptions

class InputData:
    def __init__(self, inputDataLocations):
        self.globalAssumptions = GlobalAssumptions()
        self.demandAssumptions = DemandAssumptions(self.globalAssumptions, inputDataLocations)
        self.supplyAssumptions = SupplyAssumptions(self.globalAssumptions, inputDataLocations)
        self.systemOperationsAssumptions = SystemOperationsAssumptions(self.globalAssumptions, inputDataLocations)
        self.contingentWMOsAssumptions = ContingentWMOsAssumptions(self.globalAssumptions, inputDataLocations)
        self.longtermWMOsAssumptions = LongTermWMOsAssumptions(inputDataLocations)
        
    #### Get Global Assumptions
    def getContractorsList(self):
        return self.globalAssumptions.contractorsList
    
    def getHistoricHydrologyYears(self):
        return self.globalAssumptions.historicHydrologyYears
    
    def getFutureYear(self):
        return self.globalAssumptions.futureYear
    
    def getHydroYearType(self):
        return self.globalAssumptions.hydroYearType
    
    #### Get Demand Input Assumptions
    def getTotalDemands(self):
        return self.demandAssumptions.totalDemands
    
    def getPlannedLongTermConservation(self):
        return self.demandAssumptions.plannedLongTermConservation
    
    def getUsePortion_singleFamily(self):
        return self.demandAssumptions.singleFamilyUsePortion
    
    def getUsePortion_multiFamily(self):
        return self.demandAssumptions.multiFamilyUsePortion
    
    def getUsePortion_industrial(self):
        return self.demandAssumptions.industrialUsePortion
    
    def getUsePortion_commAndGov(self):
        return self.demandAssumptions.commAndGovUsePortion
    
    def getUsePortion_landscape(self):
        return self.demandAssumptions.landscapeUsePortion
    
    #### Get Supply Input Assumptions
    def getTotalLocalSupply(self):
        return self.supplyAssumptions.totalLocalSupply
    
    def getSwpCvpSupply(self):
        return self.supplyAssumptions.swpCVPSupply
    
    #### Get System Operations Input Assumptions
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
    
    #### Get Contingent WMOs Input Assumptions
    # Contingency Conservation Assumptions
    def getContingentConservationUseReduction(self):
        return self.contingentWMOsAssumptions.contingentConservationUseReduction
    
    def getContingentConservationStorageTrigger(self):
        return self.contingentWMOsAssumptions.contingentConservationStorageTrigger
    
    def getContingentConservationUnitCost(self):
        return self.contingentWMOsAssumptions.contingentConservationUnitCost
    
    def getUrbanPopulation(self):
        return self.contingentWMOsAssumptions.urbanPopulation
    
    # Water Market Transfers Assumptions
    def getShortageThresholdForWaterMarketTransfers(self):
        return self.contingentWMOsAssumptions.shortageThresholdForWaterMarketTransfers
    
    def getTransferLimit(self):
        return self.contingentWMOsAssumptions.transferLimit 
    
    def getWaterMarketTransferCost(self):
        return self.contingentWMOsAssumptions.waterMarketTransferCost
    
    # Get Rationing Program Assumptions
    def getDemandHardeningFactor(self):
        return self.contingentWMOsAssumptions.demandHardeningFactor
    
    def getCutRatio_singleFamily(self):
        return self.contingentWMOsAssumptions.cutRatio_singleFamily
    
    def getCutRatio_multiFamily(self):
        return self.contingentWMOsAssumptions.cutRatio_multiFamily
    
    def getCutRatio_industrial(self):
        return self.contingentWMOsAssumptions.cutRatio_industrial
    
    def getCutRatio_commercial(self):
        return self.contingentWMOsAssumptions.cutRatio_commercial
    
    def getCutRatio_landscape(self):
        return self.contingentWMOsAssumptions.cutRatio_landscape

    
    #### Get Long-term WMOs Input Assumptions
    def getLongtermWMOSurfaceVolume(self):
        return self.longtermWMOsAssumptions.longtermWMOSurfaceVolumeLimit
    
    def getLongtermWMOSurfaceUnitCost(self):
        return self.longtermWMOsAssumptions.longtermWMOSurfaceUnitCost
    
    def getLongtermWMOGroundwaterUnitCost(self):
        return self.longtermWMOsAssumptions.longtermWMOGroundwaterUnitCost
    
    def getLongtermWMODesalinationUnitCost(self):
        return self.longtermWMOsAssumptions.longtermWMODesalinationUnitCost
    
    def getLongtermWMORecycledUnitCost(self):
        return self.longtermWMOsAssumptions.longtermWMORecycledUnitCost
    
    def getLongtermWMOPotableReuseUnitCost(self):
        return self.longtermWMOsAssumptions.longtermWMOPotableReuseUnitCost
    
    def getLongtermWMOTransfersExchangesUnitCost(self):
        return self.longtermWMOsAssumptions.longtermWMOTransfersExchangesUnitCost
    
    def getLongtermWMOOtherSupplyUnitCost(self):
        return self.longtermWMOsAssumptions.longtermWMOOtherSupplyUnitCost
    
    def getLongtermWMOConservationUnitCost(self):
        return self.longtermWMOsAssumptions.longtermWMOConservationUnitCost