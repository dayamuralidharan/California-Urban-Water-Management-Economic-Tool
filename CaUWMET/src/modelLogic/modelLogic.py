#import pdb
import pandas as pd #TODO only import functionalities needed?
import numpy as np
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.outputHandler import OutputHandler
from src.modelLogic.contingentWMOs.contingencyWMOsHandler import ContingencyWMOs
from src.modelLogic.contingentWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput
from src.modelLogic.contingentWMOs.economicLossByUseType import EconomicLossByUseType
import warnings

#TODO change all data frames with "['Contractor'] == contractor" to use Contractor column as index. See shortageThresholdForWaterMarketTransfers as example.

# Gets the system wide average annual cost
class ModelLogic:
    def __init__(self, inputData: InputData, storageUtilities: StorageUtilities):
        self.inputData = inputData
        self.storageUtilities = storageUtilities
        self.contingencyWMOs = ContingencyWMOs(inputData)
        self.outputHandler = OutputHandler(inputData)

        warnings.filterwarnings("ignore")
        
    
    
    def execute(self, x, optimize=True):
        self.economicLossByUseType = EconomicLossByUseType(self.inputData)
        
        # Set up variables that will be used for calcs by contractor
        self.initilizeVariablesForContractorLoop()
        self.totalDemand_Contractor = self.inputData.totalDemands[self.contractor]
        
        storageInputAssumptions_Contractor = self.storageUtilities.getContractorStorageAssumptions(self.contractor, self.inputData.futureYear, self.inputData.excessWaterSwitchData, self.inputData.storageData, self.inputData.storageHedgingStrategyData)
        #TODO: Make self.excessSupplySwitch_Contractor and pass to line 3 in storageUtilies.py
        excessSupplySwitch_Contractor = self.inputData.excessWaterSwitchData['Value'].loc[[self.contractor]].values[0]
    
        self.longtermWMOConservation_Contractor = x[0]
        self.longtermWMOSurfaceSupplyIncrementalVolume_Contractor = x[1] 
        self.longtermWMOGroundwaterSupplyIncrementalVolume_Contractor = x[2]
        self.longtermWMODesalinationSupplyIncrementalVolume_Contractor = x[3]
        self.longtermWMORecycledSupplyIncrementalVolume_Contractor = x[4]
        self.longtermWMOPotableReuseSupplyIncrementalVolume_Contractor = x[5]
        self.longtermWMOTransfersAndExchangesSupplyIncrementalVolume_Contractor = x[6]
        self.longtermWMOOtherSupplyIncrementalVolume_Contractor = x[7]
        self.totalLongtermWMOSupplyIncrementalVolume_Contractor = (self.longtermWMOOtherSupplyIncrementalVolume_Contractor # Note this term does not include the long-term conservation WMO
                                                                + self.longtermWMOSurfaceSupplyIncrementalVolume_Contractor
                                                                + self.longtermWMOGroundwaterSupplyIncrementalVolume_Contractor
                                                                + self.longtermWMODesalinationSupplyIncrementalVolume_Contractor
                                                                + self.longtermWMORecycledSupplyIncrementalVolume_Contractor
                                                                + self.longtermWMOPotableReuseSupplyIncrementalVolume_Contractor
                                                                + self.longtermWMOTransfersAndExchangesSupplyIncrementalVolume_Contractor)
        
        # Iterate through the water balance and cost logic over hydrologic reference period
        #TODO: make range a user input
        for self.i in range(len(self.inputData.historicHydrologyYears)):
            self.waterBalanceAndCostLogic(storageInputAssumptions_Contractor, excessSupplySwitch_Contractor)
        self.writeToContractorOutputTimeSeriesDataframe()
        self.averageTotalAnnualCost_Contractor = sum(self.outputHandler.totalAnnualCost[self.contractor]) / len(self.outputHandler.totalAnnualCost[self.contractor])
        self.outputHandler.averageTotalAnnualCost[self.contractor] = self.averageTotalAnnualCost_Contractor

        self.outputHandler.writeToSystemwideOutputDataframes()
        
        if optimize:
            return self.averageTotalAnnualCost_Contractor
        
    
#TODO Move to its own class        
    def waterBalanceAndCostLogic(self, storageInputAssumptions_Contractor, excessSupplySwitch_Contractor):
        # Deliver local and imported supplies, and implement base long-term conservation to meet demands:
        self.deliverLocalSuppliesAndImplementPlannedConservation()

        # Deliver SWP/CVP supplies
        self.deliverSwpCvpSupplies()
        
        # Check if there is remaining demand to be met by stored supplies, or calculate excess SWP/CVP supply
        self.checkIfThereIsExcessSupplyOrRemainingDemand()

        # If excess supply switch includes storage operations, put excess into or take from storage to meet demands
        # If excess supply switch is set to reduce groundwater pumping, take excess supply and reduce groundwater
        self.manageExcessSuppliesAndStorageOperations(storageInputAssumptions_Contractor, excessSupplySwitch_Contractor)
    
        # If there is still remaining demand and/or storage is below user-defined threshold to retrieve water market transfers, implement contingent WMOs (contingency conservation, and/or water market transfers, and/or rationing program):
        contingencyWMOsInput = ContingencyWMOsHandlerInput(self.contractor, self.i, self.plannedLongTermConservation_Contractor, self.totalDemand_Contractor, self.longtermWMOConservation_Contractor, self.demandsToBeMetByContingentOptions_Contractor, self.appliedDemand_Contractor, self.volumeSurfaceCarryover_Contractor, self.volumeGroundwaterBank_Contractor)
        self.contingencyWMOs.implementContingencyWMOsIfNeeded(contingencyWMOsInput, self.contingentConservationUseReductionVolume_Contractor, self.waterMarketTransferDeliveries_Contractor, self.totalShortage_Contractor, self.demandsToBeMetByWaterMarketTransfers_Contractor)
        
        # Calculate Costs
        self.calculateReliabilityManagementCosts(storageInputAssumptions_Contractor)
        
        self.economicLossByUseType.calculateTotalEconomicLoss(self.contingencyWMOs.shortageByUseType, contingencyWMOsInput, self.contingencyWMOs, self.totalShortage_Contractor)
        self.totalAnnualCost_Contractor.append(self.reliabilityManagementCost_Contractor[self.i] + self.economicLossByUseType.totalEconomicLoss_Contractor[self.i])
    
    #TODO move to separate file
    def writeToContractorOutputTimeSeriesDataframe(self):
        # Append contractor results to output dataframes.
        self.outputHandler.appliedDemands[self.contractor] = self.appliedDemand_Contractor
        self.outputHandler.demandsToBeMetBySWPCVP[self.contractor] = self.demandsToBeMetBySWPCVP_Contractor
        
        self.outputHandler.SWPCVPSupplyDelivery[self.contractor] = self.SWPCVPSupplyDelivery_Contractor
        
        self.outputHandler.excessSupply[self.contractor] = self.excessSupply_Contractor
        self.outputHandler.unallocatedSWPCVPDeliveries[self.contractor] = self.unallocatedSWPCVPDeliveries_Contractor
        
        self.outputHandler.demandsToBeMetByStorage[self.contractor] = self.demandsToBeMetByStorage_Contractor
        self.outputHandler.volumeSurfaceCarryover[self.contractor] = self.volumeSurfaceCarryover_Contractor
        self.outputHandler.volumeGroundwaterBank[self.contractor] = self.volumeGroundwaterBank_Contractor
        self.outputHandler.availableCapacitySurface[self.contractor] = self.availableCapacitySurface_Contractor
        self.outputHandler.availableGroundwaterCapacity[self.contractor] = self.availableGroundwaterCapacity_Contractor
        self.outputHandler.putGroundwater[self.contractor] = self.putGroundwater_Contractor
        self.outputHandler.putSurface[self.contractor] = self.putSurface_Contractor
        self.outputHandler.takeSurface[self.contractor] = self.takeSurface_Contractor
        self.outputHandler.takeGroundwater[self.contractor] = self.takeGroundwater_Contractor
        
        self.outputHandler.demandsToBeMetByContingentOptions[self.contractor] = self.demandsToBeMetByContingentOptions_Contractor
        self.outputHandler.contingentConservationReductionVolume[self.contractor] = self.contingencyWMOs.contingentConservationUseReductionVolume_Contractor
        self.outputHandler.waterMarketTransferDeliveries[self.contractor] = self.contingencyWMOs.waterMarketTransferDeliveries_Contractor
        self.outputHandler.totalShortage[self.contractor] = self.contingencyWMOs.totalShortage_Contractor
        
        # Cost variables
        # System Operations Costs
        self.outputHandler.swpCVPDeliveryCost[self.contractor] = self.swpCVPDeliveryCost_Contractor
        self.outputHandler.putGroundwaterBankCost[self.contractor] = self.groundwaterBankPutCost_Contractor
        self.outputHandler.takeGroundwaterBankCost[self.contractor] = self.groundwaterBankTakeCost_Contractor
        self.outputHandler.groundwaterPumpingSavings[self.contractor] = self.groundwaterPumpingSavings_Contractor
        self.outputHandler.waterTreatmentCost[self.contractor] = self.waterTreatmentCost_Contractor
        self.outputHandler.distributionCost[self.contractor] = self.distributionCost_Contractor
        self.outputHandler.wastewaterTreatmentCost[self.contractor] = self.wastewaterTreatmentCost_Contractor
        
        # WMO Costs
        self.outputHandler.waterMarketTransferCost[self.contractor] = self.waterMarketTransferCost_Contractor
        
        self.outputHandler.surfaceLongTermWMOCost[self.contractor] = self.surfaceLongTermWMOCost_Contractor
        self.outputHandler.groundwaterLongTermWMOCost[self.contractor] = self.groundwaterLongTermWMOCost_Contractor
        self.outputHandler.desalinationLongTermWMOCost[self.contractor] = self.desalinationLongTermWMOCost_Contractor
        self.outputHandler.recycledLongTermWMOCost[self.contractor] = self.recycledLongTermWMOCost_Contractor
        self.outputHandler.potableReuseLongTermWMOCost[self.contractor] = self.potableReuseLongTermWMOCost_Contractor
        self.outputHandler.transfersAndExchangesLongTermWMOCost[self.contractor] = self.transfersAndExchangesLongTermWMOCost_Contractor
        self.outputHandler.otherSupplyLongTermWMOCost[self.contractor] = self.otherSupplyLongTermWMOCost_Contractor
        self.outputHandler.conservationLongTermWMOCost[self.contractor] = self.conservationLongTermWMOCost_Contractor
        
        # Total Costs
        self.outputHandler.totalReliabilityMgmtCost[self.contractor] = self.reliabilityManagementCost_Contractor
        self.outputHandler.totalEconomicLoss[self.contractor] = self.economicLossByUseType.totalEconomicLoss_Contractor
        self.outputHandler.totalAnnualCost[self.contractor] = self.totalAnnualCost_Contractor
                
        
    def deliverLocalSuppliesAndImplementPlannedConservation(self):
        self.plannedLongTermConservation_Contractor = self.inputData.plannedLongTermConservation[self.inputData.plannedLongTermConservation['Contractor'] == self.contractor][int(self.inputData.futureYear)].values[0]
        self.appliedDemand_Contractor.append(max(0, self.totalDemand_Contractor[self.i] - self.plannedLongTermConservation_Contractor - self.longtermWMOConservation_Contractor))
        self.demandsToBeMetBySWPCVP_Contractor.append(max(0, self.appliedDemand_Contractor[self.i] - self.inputData.totalLocalSupply[self.contractor][self.i] - self.totalLongtermWMOSupplyIncrementalVolume_Contractor))

    def deliverSwpCvpSupplies(self):
        self.SWPCVPSupply_Contractor = self.inputData.swpCVPSupply[self.contractor][self.i]
        self.remainingDemandAfterDeliveryOfSwpCVPSupplies = max(0, self.demandsToBeMetBySWPCVP_Contractor[self.i] - self.SWPCVPSupply_Contractor)
        self.SWPCVPSupplyDelivery_Contractor.append(max(0, self.demandsToBeMetBySWPCVP_Contractor[self.i] - self.remainingDemandAfterDeliveryOfSwpCVPSupplies))

    def checkIfThereIsExcessSupplyOrRemainingDemand(self):
        if self.remainingDemandAfterDeliveryOfSwpCVPSupplies > 0:
            self.demandsToBeMetByStorage_Contractor.append(self.remainingDemandAfterDeliveryOfSwpCVPSupplies)
            self.excessSupply_Contractor.append(0)
        else:
            self.excessSupply_Contractor.append((max(0, self.SWPCVPSupply_Contractor - self.demandsToBeMetBySWPCVP_Contractor[self.i])))
            self.demandsToBeMetByStorage_Contractor.append(0)


    # Put/take from storage, reduce groundwater pumping, or send to turn back pool    
    def manageExcessSuppliesAndStorageOperations(self, storageInputAssumptions_Contractor, excessSupplySwitch_Contractor):
        # First initialize storage volumes
        if self.i == 0:
            self.volumeSurfaceCarryover_Contractor.append(storageInputAssumptions_Contractor['initialSurfaceStorageVolume_Contractor'])
            self.volumeGroundwaterBank_Contractor.append(storageInputAssumptions_Contractor['initialGroundwaterStorageVolume_Contractor'])
        else:
            self.volumeGroundwaterBank_Contractor.append(self.volumeGroundwaterBank_Contractor[self.i-1])
            self.volumeSurfaceCarryover_Contractor.append(self.volumeSurfaceCarryover_Contractor[self.i-1])

        # Set available capacity for put in storage systems
        if self.i == 0:
            self.availableCapacitySurface_Contractor = storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'] - storageInputAssumptions_Contractor['initialSurfaceStorageVolume_Contractor']
            self.availableGroundwaterCapacity_Contractor = storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'] - storageInputAssumptions_Contractor['initialGroundwaterStorageVolume_Contractor']
        else:
            self.availableCapacitySurface_Contractor = storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'] - self.volumeSurfaceCarryover_Contractor[self.i - 1]
            self.availableGroundwaterCapacity_Contractor = storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'] - self.volumeGroundwaterBank_Contractor[self.i-1]


        # If there is a surface or groundwater storage system, and if there is excess supply to put into or demand to take from storage, 
        # then implement storage operations
        excessSupplyToStorageSwitches = ["Groundwater Bank and Carryover Storage", "Groundwater Bank", "Carryover Storage"]
    
        if (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[0]) or (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[1]) or (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[2]):
            self.implementStorageOperations(excessSupplySwitch_Contractor, storageInputAssumptions_Contractor)
            self.groundwaterPumpingReduction_Contractor.append(0)

        # If switch is set to reduce groundwater pumping and there is excess supply, reduce groundwater pumping and do not implement storage operations
        elif storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == "Reduce Groundwater Pumping":
            
            self.doNotImplementStorageOperations(storageInputAssumptions_Contractor)
            self.groundwaterPumpingReduction_Contractor.append(min(self.excessSupply_Contractor[self.i], self.inputData.groundwaterLocalSupply[self.contractor][self.i]))
            self.demandsToBeMetByContingentOptions_Contractor.append(self.demandsToBeMetByStorage_Contractor[self.i])
        
        # If switch is set to turn back pool and there is excess supply, send to turn back pool and do not implement any storage operations
        else:
            self.doNotImplementStorageOperations(storageInputAssumptions_Contractor)
            self.groundwaterPumpingReduction_Contractor.append(0)
            self.demandsToBeMetByContingentOptions_Contractor.append(self.demandsToBeMetByStorage_Contractor[self.i])
        
        self.unallocatedSWPCVPDeliveries_Contractor.append(max(0, self.excessSupply_Contractor[self.i] - self.putGroundwater_Contractor[self.i] - self.putSurface_Contractor[self.i] - self.groundwaterPumpingReduction_Contractor[self.i]))
             
    def implementStorageOperations(self, excessSupplySwitch_Contractor, storageInputAssumptions_Contractor):
        # If there is excess supply, calculate put into storage
        putsIntoStorage_Contractor = self.storageUtilities.putExcessSupplyIntoStorage(self.i, 
                                excessSupplySwitch_Contractor, self.excessSupply_Contractor,
                                self.availableGroundwaterCapacity_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumPutCapacity_Contractor'], storageInputAssumptions_Contractor['rechargeEffectiveness_Contractor'], # groundwater bank assumptions
                                self.availableCapacitySurface_Contractor, storageInputAssumptions_Contractor['surfaceMaximumPutCapacity_Contractor']) # surface carryover assumptions
    
        self.putGroundwater_Contractor.append(putsIntoStorage_Contractor['putGroundwater_Contractor'])
        self.putSurface_Contractor.append(putsIntoStorage_Contractor['putSurface_Contractor'])
        
    ## If there is no excess supply, but remaining demand after local and CVP/SWP supplies are delivered, take from surface carryover storage first, then banked groundwater storage
        takesFromStorage_Contractor = self.storageUtilities.takeFromStorage(self.i, self.demandsToBeMetByStorage_Contractor,
                        self.volumeSurfaceCarryover_Contractor, storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'], storageInputAssumptions_Contractor['surfaceMaximumTakeCapacity_Contractor'],
                        self.volumeGroundwaterBank_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'], storageInputAssumptions_Contractor['groundwaterMaximumTakeCapacity_Contractor'],
                        storageInputAssumptions_Contractor['storageHedgingStrategySwitch_Contractor'], storageInputAssumptions_Contractor['hedgingPoint_Contractor'], storageInputAssumptions_Contractor['hedgeCallStorageFactor_Contractor'], storageInputAssumptions_Contractor['hedgingStorageCapacityFactor_Contractor'])
        
        self.takeSurface_Contractor.append(takesFromStorage_Contractor['takeSurface_Contractor'])
        self.takeGroundwater_Contractor.append(takesFromStorage_Contractor['takeGroundwater_Contractor'])
        self.demandsToBeMetByContingentOptions_Contractor.append(takesFromStorage_Contractor['demandsToBeMetByContingentOptions_Contractor'])

        # Update storage volumes after puts and takes
        # Initialize storage volumes
        self.volumeGroundwaterBank_Contractor[self.i] = self.volumeGroundwaterBank_Contractor[self.i] + self.putGroundwater_Contractor[self.i] - self.takeGroundwater_Contractor[self.i]
        self.volumeSurfaceCarryover_Contractor[self.i] = self.volumeSurfaceCarryover_Contractor[self.i] + self.putSurface_Contractor[self.i] - self.takeSurface_Contractor[self.i]
        

    def doNotImplementStorageOperations(self, storageInputAssumptions_Contractor):
        if self.i == 0:
            self.volumeSurfaceCarryover_Contractor[self.i] = storageInputAssumptions_Contractor['initialSurfaceStorageVolume_Contractor']
            self.volumeGroundwaterBank_Contractor[self.i] = storageInputAssumptions_Contractor['initialGroundwaterStorageVolume_Contractor']
        else:
            self.volumeGroundwaterBank_Contractor[self.i] = self.volumeGroundwaterBank_Contractor[self.i-1]
            self.volumeSurfaceCarryover_Contractor[self.i] = self.volumeSurfaceCarryover_Contractor[self.i-1]
        self.putSurface_Contractor.append(0)
        self.putGroundwater_Contractor.append(0)
        self.takeSurface_Contractor.append(0)
        self.takeGroundwater_Contractor.append(0)

    def calculateReliabilityManagementCosts(self, storageInputAssumptions_Contractor):
        self.totalSuppliesDelivered_Contractor.append(min(self.inputData.totalLocalSupply[self.contractor][self.i] + self.totalLongtermWMOSupplyIncrementalVolume_Contractor, self.appliedDemand_Contractor[self.i])
                                                        + max(0, self.SWPCVPSupply_Contractor - self.excessSupply_Contractor[self.i])
                                                        + self.takeGroundwater_Contractor[self.i]
                                                        + self.takeSurface_Contractor[self.i]
                                                        + self.contingencyWMOs.waterMarketTransferDeliveries_Contractor[self.i])
        
        #Get unit cost input data
        self.swpCVPDeliveryUnitCost_Contractor = self.inputData.swpCVPDeliveryUnitCost.loc[self.contractor][self.inputData.futureYear]
        self.groundwaterBankPutUnitCost_Contractor = self.inputData.groundwaterBankPutUnitCost.loc[self.contractor][self.inputData.futureYear]
        self.groundwaterBankTakeUnitCost_Contractor = self.inputData.groundwaterBankTakeUnitCost.loc[self.contractor][self.inputData.futureYear]
        self.groundwaterPumpingUnitCost_Contractor = self.inputData.groundwaterPumpingUnitCost[self.contractor][self.i]
        self.waterTreatmentUnitCost_Contractor = self.inputData.waterTreatmentUnitCost.loc[self.contractor][self.inputData.futureYear]
        self.distributionUnitCost_Contractor = self.inputData.distributionUnitCost.loc[self.contractor][self.inputData.futureYear]
        self.wastewaterTreatmentUnitCost_Contractor = self.inputData.wastewaterTreatmentUnitCost.loc[self.contractor][self.inputData.futureYear]
        self.wastewaterTreatmentFraction_Contractor = self.inputData.wastewaterTreatmentFraction.loc[self.contractor][self.inputData.futureYear] / 100
        
        self.waterMarketTransferUnitCost_Contractor = self.inputData.waterMarketTransferCost[self.contractor][self.i]
        self.waterMarketLossFactor_Contractor = 1 + (self.inputData.waterMarketLossFactor.loc[self.contractor][self.inputData.futureYear] / 100)
        self.contingentConservationUnitCost_Contractor = self.inputData.contingentConservationUnitCost.loc[self.contractor][self.inputData.futureYear]
        self.costForRationingProgram_Contractor = float(self.inputData.costForRationingProgram.loc[self.contractor])
        self.urbanPopulation_Contractor = self.inputData.urbanPopulation.loc[self.contractor][self.inputData.futureYear] * 1000
        
        longtermWMOSurfaceUnitCost_Contractor = self.inputData.longtermWMOSurfaceUnitCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOGroundwaterUnitCost_Contractor = self.inputData.longtermWMOGroundwaterUnitCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMODesalinationUnitCost_Contractor = self.inputData.longtermWMODesalinationUnitCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMORecycledUnitCost_Contractor = self.inputData.longtermWMORecycledUnitCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOPotableReuseUnitCost_Contractor = self.inputData.longtermWMOPotableReuseUnitCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOTransfersExchangesUnitCost_Contractor = self.inputData.longtermWMOTransfersExchangesUnitCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOOtherSupplyUnitCost_Contractor = self.inputData.longtermWMOOtherSupplyUnitCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOConservationUnitCost_Contractor = self.inputData.longtermWMOConservationUnitCost.loc[self.contractor][self.inputData.futureYear]
        
        longtermWMOSurfaceBaseCost_Contractor = self.inputData.longtermWMOSurfaceBaseCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOGroundwaterBaseCost_Contractor = self.inputData.longtermWMOGroundwaterBaseCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMODesalinationBaseCost_Contractor = self.inputData.longtermWMODesalinationBaseCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMORecycledBaseCost_Contractor = self.inputData.longtermWMORecycledBaseCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOPotableReuseBaseCost_Contractor = self.inputData.longtermWMOPotableReuseBaseCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOTransfersExchangesBaseCost_Contractor = self.inputData.longtermWMOTransfersExchangesBaseCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOOtherSupplyBaseCost_Contractor = self.inputData.longtermWMOOtherSupplyBaseCost.loc[self.contractor][self.inputData.futureYear]
        longtermWMOConservationBaseCost_Contractor = self.inputData.longtermWMOConservationBaseCost.loc[self.contractor][self.inputData.futureYear]
        
        #Get reliability management costs based on delivered volumes
        self.swpCVPDeliveryCost_Contractor.append((max(0, self.SWPCVPSupply_Contractor - self.excessSupply_Contractor[self.i])) * self.swpCVPDeliveryUnitCost_Contractor)
        
        self.groundwaterBankPutCost_Contractor.append(self.putGroundwater_Contractor[self.i] * self.groundwaterBankPutUnitCost_Contractor)
        self.groundwaterBankTakeCost_Contractor.append(self.takeGroundwater_Contractor[self.i] * self.groundwaterBankTakeUnitCost_Contractor)
        
        self.waterTreatmentCost_Contractor.append(self.totalSuppliesDelivered_Contractor[self.i] * self.waterTreatmentUnitCost_Contractor)
        self.distributionCost_Contractor.append(self.totalSuppliesDelivered_Contractor[self.i] * self.distributionUnitCost_Contractor)
        self.wastewaterTreatmentCost_Contractor.append(self.totalSuppliesDelivered_Contractor[self.i] * self.wastewaterTreatmentFraction_Contractor * self.wastewaterTreatmentUnitCost_Contractor)
        
        self.waterMarketTransferCost_Contractor.append((self.contingencyWMOs.waterMarketTransferDeliveries_Contractor[self.i] * self.waterMarketLossFactor_Contractor) * (self.waterMarketTransferUnitCost_Contractor + self.swpCVPDeliveryUnitCost_Contractor))
        
        if self.contingencyWMOs.contingentConservationUseReductionVolume_Contractor[self.i] > 0:
            self.contingentConservationCost_Contractor.append(self.contingentConservationUnitCost_Contractor * self.urbanPopulation_Contractor)
        else:
            self.contingentConservationCost_Contractor.append(0)
        
        if storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == "Reduce Groundwater Pumping":
            self.groundwaterPumpingSavings_Contractor.append(self.groundwaterPumpingUnitCost_Contractor* self.groundwaterPumpingReduction_Contractor[self.i])
        else:
            self.groundwaterPumpingSavings_Contractor.append(0)
        
        if self.totalShortage_Contractor[self.i] > 0:    
            self.rationingProgramCost_Contractor.append(self.costForRationingProgram_Contractor* self.urbanPopulation_Contractor)
        else:
            self.rationingProgramCost_Contractor.append(0)
        
        self.surfaceLongTermWMOCost_Contractor.append((self.longtermWMOSurfaceSupplyIncrementalVolume_Contractor * longtermWMOSurfaceUnitCost_Contractor + longtermWMOSurfaceBaseCost_Contractor) * self.longtermWMOSurfaceSupplyIncrementalVolume_Contractor)
        self.groundwaterLongTermWMOCost_Contractor.append((self.longtermWMOGroundwaterSupplyIncrementalVolume_Contractor * longtermWMOGroundwaterUnitCost_Contractor + longtermWMOGroundwaterBaseCost_Contractor) * self.longtermWMOGroundwaterSupplyIncrementalVolume_Contractor)
        self.desalinationLongTermWMOCost_Contractor.append((self.longtermWMODesalinationSupplyIncrementalVolume_Contractor * longtermWMODesalinationUnitCost_Contractor + longtermWMODesalinationBaseCost_Contractor) * self.longtermWMODesalinationSupplyIncrementalVolume_Contractor)
        self.recycledLongTermWMOCost_Contractor.append((self.longtermWMORecycledSupplyIncrementalVolume_Contractor * longtermWMORecycledUnitCost_Contractor + longtermWMORecycledBaseCost_Contractor) * self.longtermWMORecycledSupplyIncrementalVolume_Contractor)
        self.potableReuseLongTermWMOCost_Contractor.append((self.longtermWMOPotableReuseSupplyIncrementalVolume_Contractor * longtermWMOPotableReuseUnitCost_Contractor + longtermWMOPotableReuseBaseCost_Contractor) * self.longtermWMOPotableReuseSupplyIncrementalVolume_Contractor)
        self.transfersAndExchangesLongTermWMOCost_Contractor.append((self.longtermWMOTransfersAndExchangesSupplyIncrementalVolume_Contractor * longtermWMOTransfersExchangesUnitCost_Contractor + longtermWMOTransfersExchangesBaseCost_Contractor))
        self.otherSupplyLongTermWMOCost_Contractor.append((self.longtermWMOOtherSupplyIncrementalVolume_Contractor * longtermWMOOtherSupplyUnitCost_Contractor + longtermWMOOtherSupplyBaseCost_Contractor) * self.longtermWMOOtherSupplyIncrementalVolume_Contractor)
        self.conservationLongTermWMOCost_Contractor.append((self.longtermWMOConservation_Contractor * longtermWMOConservationUnitCost_Contractor + longtermWMOConservationBaseCost_Contractor) * self.longtermWMOConservation_Contractor)


        self.reliabilityManagementCost_Contractor.append(
            self.groundwaterBankPutCost_Contractor[self.i]
            + self.groundwaterBankTakeCost_Contractor[self.i]
            + self.swpCVPDeliveryCost_Contractor[self.i]
            
            + self.waterMarketTransferCost_Contractor[self.i]
            + self.contingentConservationCost_Contractor[self.i]
            
            + self.waterTreatmentCost_Contractor[self.i]
            + self.distributionCost_Contractor[self.i]
            + self.wastewaterTreatmentCost_Contractor[self.i]
            
            + self.rationingProgramCost_Contractor[self.i]
            
            + self.surfaceLongTermWMOCost_Contractor[self.i]
            + self.groundwaterLongTermWMOCost_Contractor[self.i]
            + self.desalinationLongTermWMOCost_Contractor[self.i]
            + self.recycledLongTermWMOCost_Contractor[self.i]
            + self.potableReuseLongTermWMOCost_Contractor[self.i]
            + self.transfersAndExchangesLongTermWMOCost_Contractor[self.i]
            + self.otherSupplyLongTermWMOCost_Contractor[self.i]
            + self.conservationLongTermWMOCost_Contractor[self.i]

            - self.groundwaterPumpingSavings_Contractor[self.i]
        )


    def initilizeVariablesForContractorLoop(self):
        self.appliedDemand_Contractor = []
        self.demandsToBeMetBySWPCVP_Contractor = []
        self.SWPCVPSupplyDelivery_Contractor = []
        self.demandsToBeMetByStorage_Contractor = []

        # Water balance variables
        self.excessSupply_Contractor = []
        self.unallocatedSWPCVPDeliveries_Contractor = []
        self.groundwaterPumpingReduction_Contractor = []
        
        self.volumeSurfaceCarryover_Contractor = []
        self.volumeGroundwaterBank_Contractor = []
        self.putSurface_Contractor = []
        self.putGroundwater_Contractor = []
        self.takeSurface_Contractor = []
        self.takeGroundwater_Contractor = []
        
        self.demandsToBeMetByContingentOptions_Contractor = []
        self.contingentConservationUseReductionVolume_Contractor = []
        self.waterMarketTransferDeliveries_Contractor = []
        self.totalShortage_Contractor = []
        self.demandsToBeMetByWaterMarketTransfers_Contractor = []
        
        self.totalSuppliesDelivered_Contractor = []
        
        # Cost variables
        self.groundwaterBankTakeCost_Contractor = []
        self.groundwaterBankPutCost_Contractor = []
        self.swpCVPDeliveryCost_Contractor = []
        self.groundwaterPumpingSavings_Contractor = []
        self.waterTreatmentCost_Contractor = []
        self.distributionCost_Contractor = []
        self.wastewaterTreatmentCost_Contractor = []
        self.contingentConservationCost_Contractor = []
        self.waterMarketTransferCost_Contractor = []
        
        self.surfaceLongTermWMOCost_Contractor = []
        self.groundwaterLongTermWMOCost_Contractor = []
        self.desalinationLongTermWMOCost_Contractor = []
        self.recycledLongTermWMOCost_Contractor = []
        self.potableReuseLongTermWMOCost_Contractor = []
        self.transfersAndExchangesLongTermWMOCost_Contractor = []
        self.otherSupplyLongTermWMOCost_Contractor = []
        self.conservationLongTermWMOCost_Contractor = []
        self.rationingProgramCost_Contractor = []
        
        self.reliabilityManagementCost_Contractor = []
        self.totalAnnualCost_Contractor = []
        
