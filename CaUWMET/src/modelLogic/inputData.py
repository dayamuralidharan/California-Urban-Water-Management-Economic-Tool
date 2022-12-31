from src.modelLogic.readDemandAssumptions import DemandAssumptions
from src.modelLogic.readSupplyAssumptions import SupplyAssumptions
from src.modelLogic.readSystemOperationsAssumptions import SystemOperationsAssumptions
from src.modelLogic.readContingentWMOsAssumptions import ContingentWMOsAssumptions
from src.modelLogic.readLongTermWMOsAssumptions import LongTermWMOsAssumptions
from src.modelLogic.readGlobalAssumptions import GlobalAssumptions

class InputData:
    def __init__(self, inputDataLocations):
        self.globalAssumptions = GlobalAssumptions(inputDataLocations)
        self.demandAssumptions = DemandAssumptions(self.globalAssumptions, inputDataLocations)
        self.supplyAssumptions = SupplyAssumptions(self.globalAssumptions, inputDataLocations)
        self.systemOperationsAssumptions = SystemOperationsAssumptions(self.globalAssumptions, inputDataLocations)
        self.contingentWMOsAssumptions = ContingentWMOsAssumptions(self.globalAssumptions, inputDataLocations)
        self.longtermWMOsAssumptions = LongTermWMOsAssumptions(inputDataLocations)
        
        #### Get Demand Input Assumptions
        self.totalDemands = self.demandAssumptions.totalDemands
        self.plannedLongTermConservation = self.demandAssumptions.plannedLongTermConservation
        self.singleFamilyUsePortion = self.demandAssumptions.singleFamilyUsePortion
        self.multiFamilyUsePortion = self.demandAssumptions.multiFamilyUsePortion
        self.industrialUsePortion =self.demandAssumptions.industrialUsePortion
        self.commAndGovUsePortion = self.demandAssumptions.commAndGovUsePortion
        self.landscapeUsePortion = self.demandAssumptions.landscapeUsePortion
        
        #### Get Supply Input Assumptions
        self.totalLocalSupply = self.supplyAssumptions.totalLocalSupply
        self.swpCVPSupply = self.supplyAssumptions.swpCVPSupply
        
        #### Get System Operations Input Assumptions
        self.excessWaterSwitchData = self.systemOperationsAssumptions.excessWaterSwitchData
        self.storageData = self.systemOperationsAssumptions.storageData
        self.storageHedgingStrategyData = self.systemOperationsAssumptions.storageHedgingStrategyData
        self.groundwaterBankPutUnitCost = self.systemOperationsAssumptions.groundwaterBankPutUnitCost
        self.groundwaterBankTakeUnitCost = self.systemOperationsAssumptions.groundwaterBankTakeUnitCost
        self.swpCVPDeliveryUnitCost = self.systemOperationsAssumptions.swpCVPDeliveryUnitCost
        self.groundwaterPumpingUnitCost = self.systemOperationsAssumptions.groundwaterPumpingUnitCost
        self.waterTreatmentUnitCost = self.systemOperationsAssumptions.waterTreatmentUnitCost
        self.distributionUnitCost = self.systemOperationsAssumptions.distributionUnitCost
        self.wastewaterTreatmentUnitCost = self.systemOperationsAssumptions.wastewaterTreatmentUnitCost
        self.wastewaterTreatmentFraction = self.systemOperationsAssumptions.wastewaterTreatmentFraction

    
        #### Get Contingent WMOs Input Assumptions
        # Contingency Conservation Assumptions
        self.contingentConservationUseReduction = self.contingentWMOsAssumptions.contingentConservationUseReduction
        self.contingentConservationStorageTrigger = self.contingentWMOsAssumptions.contingentConservationStorageTrigger
        self.contingentConservationUnitCost = self.contingentWMOsAssumptions.contingentConservationUnitCost
        self.urbanPopulation = self.contingentWMOsAssumptions.urbanPopulation
    
        # Water Market Transfers Assumptions
        self.shortageThresholdForWaterMarketTransfers = self.contingentWMOsAssumptions.shortageThresholdForWaterMarketTransfers
        self.transferLimit = self.contingentWMOsAssumptions.transferLimit 
        self.waterMarketTransferCost = self.contingentWMOsAssumptions.waterMarketTransferCost
    
        # Get Rationing Program Assumptions
        self.demandHardeningFactor = self.contingentWMOsAssumptions.demandHardeningFactor
        self.cutRatio_singleFamily = self.contingentWMOsAssumptions.cutRatio_singleFamily
        self.cutRatio_multiFamily = self.contingentWMOsAssumptions.cutRatio_multiFamily
        self.cutRatio_industrial = self.contingentWMOsAssumptions.cutRatio_industrial
        self.cutRatio_commercial = self.contingentWMOsAssumptions.cutRatio_commAndGov
        self.cutRatio_landscape = self.contingentWMOsAssumptions.cutRatio_landscape
        
        self.storageVolumeTriggerForRationingProgram = self.contingentWMOsAssumptions.storageVolumeTriggerForRationingProgram
        self.lowerLossBoundary = self.contingentWMOsAssumptions.lowerLossBoundary
        self.upperLossBoundary = self.contingentWMOsAssumptions.upperLossBoundary
        self.elasticityOfDemand_singleFamily = self.contingentWMOsAssumptions.elasticityOfDemand_singleFamily
        self.elasticityOfDemand_multiFamily = self.contingentWMOsAssumptions.elasticityOfDemand_multiFamily
        self.elasticityOfDemand_indsutrial = self.contingentWMOsAssumptions.elasticityOfDemand_industrial
        self.elasticityOfDemand_commAndGov = self.contingentWMOsAssumptions.elasticityOfDemand_commAndGov
        self.elasticityOfDemand_landscape = self.contingentWMOsAssumptions.elasticityOfDemand_landscape
        
        self.retailPrice = self.contingentWMOsAssumptions.retailPrice

    
        #### Get Long-term WMOs Input Assumptions
        self.longtermWMOSurfaceVolumeLimit = self.longtermWMOsAssumptions.longtermWMOSurfaceVolumeLimit
        self.longtermWMOSurfaceUnitCost = self.longtermWMOsAssumptions.longtermWMOSurfaceUnitCost
        self.longtermWMOGroundwaterUnitCost = self.longtermWMOsAssumptions.longtermWMOGroundwaterUnitCost
        self.longtermWMODesalinationUnitCost = self.longtermWMOsAssumptions.longtermWMODesalinationUnitCost
        self.longtermWMORecycledUnitCost = self.longtermWMOsAssumptions.longtermWMORecycledUnitCost
        self.longtermWMOPotableReuseUnitCost = self.longtermWMOsAssumptions.longtermWMOPotableReuseUnitCost
        self.longtermWMOTransfersExchangesUnitCost = self.longtermWMOsAssumptions.longtermWMOTransfersExchangesUnitCost
        self.longtermWMOOtherSupplyUnitCost = self.longtermWMOsAssumptions.longtermWMOOtherSupplyUnitCost
        self.longtermWMOConservationUnitCost = self.longtermWMOsAssumptions.longtermWMOConservationUnitCost
        
        #### Get Global Assumptions
        self.contractorsList = self.globalAssumptions.contractorsList
        self.historicHydrologyYears = self.globalAssumptions.historicHydrologyYears
        self.futureYear = self.globalAssumptions.futureYear