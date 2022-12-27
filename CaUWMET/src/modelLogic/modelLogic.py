import pandas as pd
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities


#TODO change all data frames with "['Contractor'] == contractor" to use Contractor column as index. See shortageThresholdForWaterMarketTransfers as example.
#TODO Make code faster

class ModelLogic:
    def __init__(self, inputData: InputData, storageUtilities: StorageUtilities):
        #TODO replace incremental volume with optimization algroithm variable
        self.longtermWMOConservationIncrementalVolume_Contractor = 0
        
        self.storageUtilities = storageUtilities
        
        # Get Global Assumptions
        self.contractorsList = inputData.getContractorsList()
        self.historicHydrologyYears = inputData.getHistoricHydrologyYears()
        self.futureYear = inputData.getFutureYear()
        
        # Get Demand Input Assumptions
        self.totalDemands = inputData.getTotalDemands()
        self.plannedLongTermConservation = inputData.getPlannedLongTermConservation()
        
        # Get Supply Input Assumptions
        self.totalLocalSupply = inputData.getTotalLocalSupply()
        self.swpCVPSupply = inputData.getSwpCvpSupply()
        
        # Get System Operations Input Assumptions
        self.excessWaterSwitchData = inputData.getExcessWaterSwitchData()
        self.storageData = inputData.getStorageData()
        self.storageHedgingStrategyData = inputData.getStorageHedgingStrategyData()
        self.groundwaterBankPutUnitCost = inputData.getGroundwaterBankPutUnitCost()
        self.groundwaterBankTakeUnitCost = inputData.getGroundwaterBankTakeUnitCost()
        self.swpCVPDeliveryUnitCost = inputData.getSwpCVPDeliveryUnitCost()
        self.groundwaterPumpingUnitCost = inputData.getGroundwaterPumpingUnitCost()
        self.waterTreatmentUnitCost = inputData.getWaterTreatmentUnitCost()
        self.distributionUnitCost = inputData.getDistributionUnitCost()
        self.wastewaterTreatmentUnitCost = inputData.getWastewaterTreatmentUnitCost()
        self.wastewaterTreatmentFraction = inputData.getWastewaterTreatmentFraction()
        
        # Get Contingent WMOs Input Assumptions
        self.contingentConservationUseReduction = inputData.getContingentConservationUseReduction()
        self.contingentConservationStorageTrigger = inputData.getContingentConservationStorageTrigger()
        self.contingentConservationUnitCost = inputData.getContingentConservationUnitCost()
        self.urbanPopulation = inputData.getUrbanPopulation()
        self.shortageThresholdForWaterMarketTransfers = inputData.getShortageThresholdForWaterMarketTransfers()
        self.transferLimit = inputData.getTransferLimit()
        self.waterMarketTransferCost = inputData.getWaterMarketTransferCost()
        
        self.demandHardeningFactor = inputData.getDemandHardeningFactor()
        self.cutRatio_singleFamily = inputData.getCutRatio_singleFamily()
        self.cutRatio_multiFamily = inputData.getCutRatio_multiFamily()
        self.cutRatio_industrial = inputData.getCutRatio_industrial()
        self.cutRatio_commercial = inputData.getCutRatio_commercial()
        self.cutRatio_landscape = inputData.getCutRatio_landscape()
        self.singleFamilyUsePortion = inputData.getUsePortion_singleFamily()
        self.multiFamilyUsePortion = inputData.getUsePortion_multiFamily()
        self.industrialUsePortion = inputData.getUsePortion_industrial()
        self.commAndGovUsePortion = inputData.getUsePortion_commAndGov()
        self.landscapeUsePortion = inputData.getUsePortion_landscape()
        
        
        # Get Long-term WMO Input Assumptions
        self.longtermWMOSurfaceVolume = inputData.getLongtermWMOSurfaceVolume()
        self.longtermWMOSurfaceUnitCost = inputData.getLongtermWMOSurfaceUnitCost()
        self.longtermWMOGroundwaterUnitCost = inputData.getLongtermWMOGroundwaterUnitCost()
        self.longtermWMODesalinationUnitCost = inputData.getLongtermWMODesalinationUnitCost()
        self.longtermWMORecycledUnitCost = inputData.getLongtermWMORecycledUnitCost()
        self.longtermWMOPotableReuseUnitCost = inputData.getLongtermWMOPotableReuseUnitCost()
        self.longtermWMOTransfersExchangesUnitCost = inputData.getLongtermWMOTransfersExchangesUnitCost()
        self.longtermWMOOtherSupplyUnitCost = inputData.getLongtermWMOOtherSupplyUnitCost()
        self.longtermWMOConservationUnitCost = inputData.getLongtermWMOConservationUnitCost()
        
        self.writer = pd.ExcelWriter('Output_QAQC.xlsx', engine = 'xlsxwriter')
        # Initialize time series dataframes for each variable. These dataframes include time series for all contractors.
        self.appliedDemands = {'Year': self.historicHydrologyYears} #Setting these variables in the constructor method creates an instance of them in this class so we don't need to keep passing them as arguments to functions, the functions 
        self.demandsToBeMetBySWPCVP = {'Year': self.historicHydrologyYears}
        self.demandsToBeMetByStorage = {'Year': self.historicHydrologyYears}
        self.demandsToBeMetByBankedGW = {'Year': self.historicHydrologyYears}
        self.excessSupply = {'Year': self.historicHydrologyYears}
        self.groundwaterPumpingReduction = {'Year': self.historicHydrologyYears}

        # Surface carryover and banked groundwater storage dataframes
        self.volumeSurfaceCarryover = {'Year': self.historicHydrologyYears}
        self.volumeGroundwaterBank = {'Year': self.historicHydrologyYears}
        self.availableCapacitySurface = {'Year': self.historicHydrologyYears}
        self.availableGroundwaterCapacity = {'Year': self.historicHydrologyYears}
        self.putGroundwater = {'Year': self.historicHydrologyYears}
        self.putSurface = {'Year': self.historicHydrologyYears}
        self.takeSurface = {'Year': self.historicHydrologyYears}
        self.takeGroundwater = {'Year': self.historicHydrologyYears}
        self.putGroundwaterBankCost = {'Year': self.historicHydrologyYears}
        self.takeGroundwaterBankCost = {'Year': self.historicHydrologyYears}

        # Hedging strategy dataframes
        self.pctCapacitySurfaceCarryover = {'Year': self.historicHydrologyYears}
        self.pctStorageCalledSurfaceCarryover = {'Year': self.historicHydrologyYears}
        self.pctCapacityGroundwaterBank = {'Year': self.historicHydrologyYears}
        self.pctStorageCalledGroundwaterBank = {'Year': self.historicHydrologyYears}

        # Contingent WMOs dataframes
        self.demandsToBeMetByContingentOptions = {'Year': self.historicHydrologyYears}
        self.contingentConservationReductionVolume = {'Year': self.historicHydrologyYears}
        self.waterMarketTransferDeliveries = {'Year': self.historicHydrologyYears}
        self.totalShortage = {'Year': self.historicHydrologyYears}

    def execute(self):
        # Loop through model calculations for each contractor. All variables in this loop end with "_Contractor"
        
        for self.contractor in self.contractorsList:
            # Set up variables that will be used for calcs by contractor
            self.totalDemand_Contractor = self.totalDemands[self.contractor]
            self.appliedDemand_Contractor = []

            self.longtermWMOSurfaceVolume_Contractor = self.longtermWMOSurfaceVolume.loc[self.contractor][self.futureYear]
            
            demandsToBeMetBySWPCVP_Contractor = []
            demandsToBeMetByStorage_Contractor = []

            excessSupplySwitch_Contractor = self.excessWaterSwitchData['Switch'].loc[[self.contractor]].values[0]
            self.excessSupply_Contractor = []
            self.groundwaterPumpingReduction_Contractor = []
            
            self.volumeSurfaceCarryover_Contractor = []
            self.volumeGroundwaterBank_Contractor = []
            self.putSurface_Contractor = []
            self.putGroundwater_Contractor = []
            self.takeSurface_Contractor = []
            self.takeGroundwater_Contractor = []
            storageInputAssumptions_Contractor = self.storageUtilities.getContractorStorageAssumptions(self.contractor, self.futureYear, self.excessWaterSwitchData, self.storageData, self.storageHedgingStrategyData)
            
            self.demandsToBeMetByContingentOptions_Contractor = []
            self.contingentConservationUseReductionVolume_Contractor = []
            self.demandsToBeMetByWaterMarketTransfers_Contractor = []
            self.waterMarketTransferDeliveries_Contractor = []
            self.totalShortage_Contractor = []
            
            self.totalSuppliesDelivered_Contractor = []
            
            # Cost dataframes
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
            
            # Loop through hydrologic reference period
            for self.i in range(len(self.historicHydrologyYears)):
                
                
                #### Deliver local and project supplies to meet demands:
                # Calculate Applied Demand after subtraction of Planned Long-term Conservation
                self.plannedLongTermConservation_Contractor = self.plannedLongTermConservation[self.plannedLongTermConservation['Contractor'] == self.contractor][self.futureYear].values[0]
                self.appliedDemand_Contractor.append(max(0, self.totalDemand_Contractor[self.i] - self.plannedLongTermConservation_Contractor))

                # Calculate Demand to be Met by SWP/CVP supplies after subtraction of local supplies
                demandsToBeMetBySWPCVP_Contractor.append(max(0, self.appliedDemand_Contractor[self.i] - self.totalLocalSupply[self.contractor][self.i]))

                # Calculate Demand to be Met by Stored supplies after delivery of SWP/CVP supplies, or calculate Excess SWP/CVP Supply.
                self.SWPCVPSupply_Contractor = self.swpCVPSupply[self.contractor][self.i]
                if demandsToBeMetBySWPCVP_Contractor[self.i] - self.SWPCVPSupply_Contractor > 0:
                    demandsToBeMetByStorage_Contractor.append(demandsToBeMetBySWPCVP_Contractor[self.i] - self.SWPCVPSupply_Contractor)
                    self.excessSupply_Contractor.append(0)
                else:
                    self.excessSupply_Contractor.append((self.SWPCVPSupply_Contractor - demandsToBeMetBySWPCVP_Contractor[self.i]))
                    demandsToBeMetByStorage_Contractor.append(0)

                excessSupplyToStorageSwitches = ["Put into Carryover and Groundwater Bank", "Put into Groundwater Bank", "Put into Carryover Storage"]

                #### Put excess into or take from storage to meet demands:
                if (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[0]) or (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[1]) or (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[2]):
                    if self.i == 0: #Initialize storage volumes
                        self.volumeSurfaceCarryover_Contractor.append(storageInputAssumptions_Contractor['initialSurfaceStorageVolume_Contractor'])
                        self.volumeGroundwaterBank_Contractor.append(storageInputAssumptions_Contractor['initialGroundwaterStorageVolume_Contractor'])
                    else: # Initialize with previous time step's volumes which are updated in the putOrTakeFromStorage function
                        self.volumeSurfaceCarryover_Contractor.append(self.volumeSurfaceCarryover_Contractor[self.i-1])
                        self.volumeGroundwaterBank_Contractor.append(self.volumeGroundwaterBank_Contractor[self.i-1])
                    
                    # Check available capacity in storage systems
                    self.availableCapacitySurface_Contractor = storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'] - self.volumeSurfaceCarryover_Contractor[max(0,self.i-1)]
                    self.availableGroundwaterCapacity_Contractor = storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'] - self.volumeGroundwaterBank_Contractor[max(0,self.i-1)]
                    
                    # If there is excess supply, calculate put into storage
                    putsIntoStorage_Contractor = self.storageUtilities.putExcessSupplyIntoStorage(self.i, 
                                            excessSupplySwitch_Contractor, self.excessSupply_Contractor,
                                            self.availableGroundwaterCapacity_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumPutCapacity_Contractor'], storageInputAssumptions_Contractor['rechargeEffectiveness_Contractor'], # groundwater bank assumptions
                                            self.availableCapacitySurface_Contractor, storageInputAssumptions_Contractor['surfaceMaximumPutCapacity_Contractor']) # surface carryover assumptions
                
                    self.putGroundwater_Contractor.append(putsIntoStorage_Contractor['putGroundwater_Contractor'])
                    self.putSurface_Contractor.append(putsIntoStorage_Contractor['putSurface_Contractor'])
                    
                    self.volumeGroundwaterBank_Contractor[self.i] = self.volumeGroundwaterBank_Contractor[self.i] + self.putGroundwater_Contractor[self.i]
                    self.volumeSurfaceCarryover_Contractor[self.i] = self.volumeSurfaceCarryover_Contractor[self.i] + self.putSurface_Contractor[self.i]
                    
                ## If there is no excess supply, but remaining demand after local and CVP/SWP supplies are delivered, take from surface carryover storage first, then banked groundwater storage
                    takesFromStorage_Contractor = self.storageUtilities.takeFromStorage(self.i, demandsToBeMetByStorage_Contractor, 
                                    self.volumeSurfaceCarryover_Contractor, storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'], storageInputAssumptions_Contractor['surfaceMaximumTakeCapacity_Contractor'],
                                    self.volumeGroundwaterBank_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'], storageInputAssumptions_Contractor['groundwaterMaximumTakeCapacity_Contractor'],
                                    storageInputAssumptions_Contractor['storageHedgingStrategySwitch_Contractor'], storageInputAssumptions_Contractor['hedgingPoint_Contractor'], storageInputAssumptions_Contractor['hedgeCallStorageFactor_Contractor'], storageInputAssumptions_Contractor['hedgingStorageCapacityFactor_Contractor'])
                    
                    self.takeSurface_Contractor.append(takesFromStorage_Contractor['takeSurface_Contractor'])
                    self.takeGroundwater_Contractor.append(takesFromStorage_Contractor['takeGroundwater_Contractor'])
                    self.demandsToBeMetByContingentOptions_Contractor.append(takesFromStorage_Contractor['demandsToBeMetByContingentOptions_Contractor'])
                
                elif storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == "Reduce Groundwater Pumping":
                    self.groundwaterPumpingReduction_Contractor.append(self.excessSupply_Contractor[self.i])
                    self.doNotImplementStorageOperations()
                    self.demandsToBeMetByContingentOptions_Contractor.append(0)
                
                else:
                    self.doNotImplementStorageOperations()
                    self.demandsToBeMetByContingentOptions_Contractor.append(0)

            ## If there is remaining demand and storage is below user-defined threshold, implement contingency conservation and water market transfers assumptions:
                self.contingentConservationUseReduction_Contractor = self.contingentConservationUseReduction[self.contingentConservationUseReduction['Contractor'] == self.contractor][self.futureYear].values[0]
                contingentConservationStorageTrigger_Contractor = self.contingentConservationStorageTrigger[self.contingentConservationStorageTrigger['Contractor'] == self.contractor][self.futureYear].values[0]
                self.shortageThresholdForWaterMarketTransfers_Contractor = self.shortageThresholdForWaterMarketTransfers.loc[self.contractor][self.futureYear] / 100
                
                if self.demandsToBeMetByContingentOptions_Contractor[self.i] > 0.0 or (self.volumeSurfaceCarryover_Contractor[self.i] + self.volumeGroundwaterBank_Contractor[self.i]) < contingentConservationStorageTrigger_Contractor:
                    self.implementContingencyWMOs()
                else:
                    self.doNotImplementContingencyWMOs()
                    
            ## Calculate total supplies delivered
                self.totalSuppliesDelivered_Contractor.append(self.totalLocalSupply[self.contractor][self.i]
                                                              + self.SWPCVPSupply_Contractor - self.excessSupply_Contractor[self.i]
                                                              + self.takeGroundwater_Contractor[self.i]
                                                              + self.takeSurface_Contractor[self.i]
                                                              + self.waterMarketTransferDeliveries_Contractor[self.i])
            
            
            
            
            
            
            
                 
            #### Calculate Reliability Management Costs
                
                self.groundwaterBankPutUnitCost_Contractor = self.groundwaterBankPutUnitCost.loc[self.contractor][self.futureYear]
                self.groundwaterBankTakeUnitCost_Contractor = self.groundwaterBankTakeUnitCost.loc[self.contractor][self.futureYear]
                self.swpCVPDeliveryUnitCost_Contractor = self.swpCVPDeliveryUnitCost.loc[self.contractor][self.futureYear]
                self.groundwaterPumpingUnitCost_Contractor = self.groundwaterPumpingUnitCost[self.contractor][self.i]
                self.waterTreatmentUnitCost_Contractor = self.waterTreatmentUnitCost.loc[self.contractor][self.futureYear]
                self.distributionUnitCost_Contractor = self.distributionUnitCost.loc[self.contractor][self.futureYear]
                self.wastewaterTreatmentUnitCost_Contractor = self.wastewaterTreatmentUnitCost.loc[self.contractor][self.futureYear]
                self.wastewaterTreatmentFraction_Contractor = self.wastewaterTreatmentFraction.loc[self.contractor][self.futureYear] / 100
                
                self.waterMarketTransferUnitCost_Contractor = self.waterMarketTransferCost[self.contractor][self.i]
                self.contingentConservationUnitCost_Contractor = self.contingentConservationUnitCost.loc[self.contractor][self.futureYear]
                self.urbanPopulation_Contractor = self.urbanPopulation.loc[self.contractor][self.futureYear] * 1000
                
                longtermWMOSurfaceUnitCost_Contractor = self.longtermWMOSurfaceUnitCost.loc[self.contractor][self.futureYear]
                longtermWMOGroundwaterUnitCost_Contractor = self.longtermWMOGroundwaterUnitCost.loc[self.contractor][self.futureYear]
                longtermWMODesalinationUnitCost_Contractor = self.longtermWMODesalinationUnitCost.loc[self.contractor][self.futureYear]
                longtermWMORecycledUnitCost_Contractor = self.longtermWMORecycledUnitCost.loc[self.contractor][self.futureYear]
                longtermWMOPotableReuseUnitCost_Contractor = self.longtermWMOPotableReuseUnitCost.loc[self.contractor][self.futureYear]
                longtermWMOTransfersExchangesUnitCost_Contractor = self.longtermWMOTransfersExchangesUnitCost.loc[self.contractor][self.futureYear]
                longtermWMOOtherSupplyUnitCost_Contractor = self.longtermWMOOtherSupplyUnitCost.loc[self.contractor][self.futureYear]
                longtermWMOConservationUnitCost_Contractor = self.longtermWMOConservationUnitCost.loc[self.contractor][self.futureYear]
                
                self.groundwaterBankPutCost_Contractor.append(self.putGroundwater_Contractor[self.i] * self.groundwaterBankPutUnitCost_Contractor)
                self.groundwaterBankTakeCost_Contractor.append(self.takeGroundwater_Contractor[self.i] * self.groundwaterBankTakeUnitCost_Contractor)
                self.swpCVPDeliveryCost_Contractor.append((self.SWPCVPSupply_Contractor- self.excessSupply_Contractor[self.i]) * self.swpCVPDeliveryUnitCost_Contractor)
                self.waterTreatmentCost_Contractor.append(self.totalSuppliesDelivered_Contractor[self.i] * self.waterTreatmentUnitCost_Contractor)
                self.distributionCost_Contractor.append(self.totalSuppliesDelivered_Contractor[self.i] * self.distributionUnitCost_Contractor)
                self.wastewaterTreatmentCost_Contractor.append(self.totalSuppliesDelivered_Contractor[self.i] * self.wastewaterTreatmentFraction_Contractor * self.distributionUnitCost_Contractor)
                
                self.waterMarketTransferCost_Contractor.append(self.waterMarketTransferDeliveries_Contractor[self.i] * self.waterMarketTransferUnitCost_Contractor)
                
                if self.contingentConservationUseReductionVolume_Contractor[self.i] > 0:
                    self.contingentConservationCost_Contractor.append(self.contingentConservationUnitCost_Contractor * self.urbanPopulation_Contractor)
                else:
                    self.contingentConservationCost_Contractor.append(0)
                
                if storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == "Reduce Groundwater Pumping":
                    self.groundwaterPumpingSavings_Contractor.append(self.groundwaterPumpingUnitCost_Contractor* self.groundwaterPumpingReduction_Contractor[self.i])
                else:
                    self.groundwaterPumpingSavings_Contractor.append(0)
                
                #TODO calculate rationing program cost    
                self.rationingProgramCost_Contractor.append(0)
                
                #TODO: incorporate supply volume into these calcs - replace the 1's 
                self.surfaceLongTermWMOCost_Contractor.append(1 * longtermWMOSurfaceUnitCost_Contractor)
                self.groundwaterLongTermWMOCost_Contractor.append(1 * longtermWMOGroundwaterUnitCost_Contractor)
                self.desalinationLongTermWMOCost_Contractor.append(1 * longtermWMODesalinationUnitCost_Contractor)
                self.recycledLongTermWMOCost_Contractor.append(1 * longtermWMORecycledUnitCost_Contractor)
                self.potableReuseLongTermWMOCost_Contractor.append(1 * longtermWMOPotableReuseUnitCost_Contractor)
                self.transfersAndExchangesLongTermWMOCost_Contractor.append(1 * longtermWMOTransfersExchangesUnitCost_Contractor)
                self.otherSupplyLongTermWMOCost_Contractor.append(1 * longtermWMOOtherSupplyUnitCost_Contractor)
                self.conservationLongTermWMOCost_Contractor.append(1 * longtermWMOConservationUnitCost_Contractor)
                
                
                self.reliabilityManagementCost_Contractor.append(self.groundwaterBankPutCost_Contractor[self.i]
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
                                                                 )
                






        # Append dataframes with updated contractor data as calculated in model logic above.
            self.appliedDemands[self.contractor] = self.appliedDemand_Contractor
            self.demandsToBeMetBySWPCVP[self.contractor] = demandsToBeMetBySWPCVP_Contractor
            self.demandsToBeMetByStorage[self.contractor] = demandsToBeMetByStorage_Contractor
            self.excessSupply[self.contractor] = self.excessSupply_Contractor
            
            self.volumeSurfaceCarryover[self.contractor] = self.volumeSurfaceCarryover_Contractor
            self.volumeGroundwaterBank[self.contractor] = self.volumeGroundwaterBank_Contractor
            self.availableCapacitySurface[self.contractor] = self.availableCapacitySurface_Contractor
            self.availableGroundwaterCapacity[self.contractor] = self.availableGroundwaterCapacity_Contractor
            self.putGroundwater[self.contractor] = self.putGroundwater_Contractor
            self.putSurface[self.contractor] = self.putSurface_Contractor
            self.takeSurface[self.contractor] = self.takeSurface_Contractor
            self.takeGroundwater[self.contractor] = self.takeGroundwater_Contractor
            # pctCapacitySurfaceCarryover[contractor] = pctCapacitySurfaceCarryover_Contractor
            # pctStorageCalledSurfaceCarryover[contractor] = pctStorageCalledSurfaceCarryover_Contractor
            # pctCapacityGroundwaterBank[contractor] = pctCapacityGroundwaterBank_Contractor
            # pctStorageCalledGroundwaterBank[contractor] = pctStorageCalledGroundwaterBank_Contractor
            
            self.demandsToBeMetByContingentOptions[self.contractor] = self.demandsToBeMetByContingentOptions_Contractor
            self.contingentConservationReductionVolume[self.contractor] = self.contingentConservationUseReductionVolume_Contractor
            self.waterMarketTransferDeliveries[self.contractor] = self.waterMarketTransferDeliveries_Contractor
            self.totalShortage[self.contractor] = self.totalShortage_Contractor
            
            # Cost variables
            self.putGroundwaterBankCost[self.contractor] = self.groundwaterBankPutCost_Contractor
            self.takeGroundwaterBankCost[self.contractor] = self.groundwaterBankTakeCost_Contractor



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
    
    # TODO Move to contingent WMOs utilities file    
    def implementContingencyWMOs(self):
        self.implementContingencyConservation()
        self.deliverWaterMarketTransfers()
            
            
    def doNotImplementContingencyWMOs(self):
        self.contingentConservationUseReductionVolume_Contractor.append(0)
        self.waterMarketTransferDeliveries_Contractor.append(0)
        self.totalShortage_Contractor.append(0)
        
    def deliverWaterMarketTransfers(self):
        self.shortagePortionOfTotalAppliedDemand = self.demandsToBeMetByContingentOptions_Contractor[self.i] / self.appliedDemand_Contractor[self.i]
        
        ## Deliver Water Market Transfer supplies if shortage portion is above user-indicated threshold
        if  self.shortagePortionOfTotalAppliedDemand > self.shortageThresholdForWaterMarketTransfers_Contractor:
            self.waterMarketTransferDeliveries_Contractor.append(min(self.demandsToBeMetByWaterMarketTransfers_Contractor[self.i], self.transferLimit[self.contractor][self.i]))
            self.totalShortage_Contractor.append(max(0, self.demandsToBeMetByWaterMarketTransfers_Contractor[self.i] - self.waterMarketTransferDeliveries_Contractor[self.i]))
        else:
            self.totalShortage_Contractor.append(self.demandsToBeMetByWaterMarketTransfers_Contractor[self.i])
            
    def implementContingencyConservation(self):
        self.contingentConservationUseReductionVolume_Contractor.append(self.contingentConservationUseReduction_Contractor * self.appliedDemand_Contractor[self.i])
        self.demandsToBeMetByWaterMarketTransfers_Contractor.append(self.demandsToBeMetByContingentOptions_Contractor[self.i] - self.contingentConservationUseReductionVolume_Contractor[self.i])

    def calculateShortageByUseType(self):
        # Calculate demand hardening adjustment factor and adjusted shortage
        self.demandHardeningFactor_Contractor = self.demandHardeningFactor.loc[self.contractor][self.futureYear] / 100
        self.baseConservationAsPercentOfDemand = self.plannedLongTermConservation_Contractor / self.totalDemand_Contractor[self.i]
        self.longTermWMOConservationAsPercentOfDemand = self.longtermWMOConservationIncrementalVolume_Contractor / self.totalDemand_Contractor[self.i]
        self.demandHardeningAdjustmentFactor_Contractor = 1 + ((((1 + self.baseConservationAsPercentOfDemand) * (1 + self.longTermWMOConservationAsPercentOfDemand)) -1) * self.demandHardeningFactor_Contractor)
        self.adjustedShortage_Contractor = self.totalShortage_Contractor[self.i] * self.demandHardeningAdjustmentFactor_Contractor
        
        self.singleFamilyShortagePortion = self.adjustedShortage_Contractor/ (self.cutRatio_singleFamily[self.contractor] * self.singleFamilyUsePortion[self.contractor] + self.cutRatio_multiFamily[self.contractor] * self.multiFamilyUsePortion[self.contractor] + self.cutRatio_industrial[self.contractor] * self.industrialUsePortion[self.contractor] + self.cutRatio_commercial[self.contractor] * self.commAndGovUsePortion[self.contractor] + self.cutRatio_landscape[self.contractor] * self.landscapeUsePortion[self.contractor])
        
    
    
    
    
    
    # TODO: Move to storage utilities file
    def doNotImplementStorageOperations(self):
        self.groundwaterPumpingReduction_Contractor.append(0)
        self.volumeSurfaceCarryover_Contractor.append(0)
        self.volumeGroundwaterBank_Contractor.append(0)
        self.availableCapacitySurface_Contractor = 0
        self.availableGroundwaterCapacity_Contractor = 0
        self.putSurface_Contractor.append(0)
        self.putGroundwater_Contractor.append(0)
        self.takeSurface_Contractor.append(0)
        self.takeGroundwater_Contractor.append(0)
        
    