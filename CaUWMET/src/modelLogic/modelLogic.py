import pandas as pd
from src.modelLogic.inputData import InputData
from src.modelLogic.readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from src.modelLogic.readDemandAssumptions import totalDemands, plannedLongTermConservation
from src.modelLogic.readSystemOperationsAssumptions import storageData,  storageHedgingStrategyData, excessWaterSwitchData, groundwaterBankPutUnitCost, groundwaterBankTakeUnitCost, swpCVPDeliveryUnitCost, groundwaterPumpingUnitCost, waterTreatmentUnitCost, distributionUnitCost, wastewaterTreatmentUnitCost, wastewaterTreatmentFraction
from src.modelLogic.readContingentWMOsAssumptions import urbanPopulation, shortageThresholdForWaterMarketTransfers, transferLimit, waterMarketTransferCost
from src.modelLogic.storageUtilities import getContractorStorageAssumptions, putExcessSupplyIntoStorage, takeFromStorage
from src.modelLogic.readLongTermWMOsAssumptions import longtermWMOSurfaceVolume, longtermWMOSurfaceUnitCost, longtermWMOGroundwaterUnitCost, longtermWMODesalinationUnitCost, longtermWMORecycledUnitCost, longtermWMOPotableReuseUnitCost, longtermWMOTransfersExchangesUnitCost, longtermWMOOtherSupplyUnitCost, longtermWMOConservationUnitCost


#TODO change all data frames with "['Contractor'] == contractor" to use Contractor column as index. See shortageThresholdForWaterMarketTransfers as example.
#TODO change availableCapacitySurface_Contractor to a list/dataframe instead of scalar
#TODO Make code faster

class ModelLogic:
    def __init__(self, inputData: InputData):
        self.totalLocalSupply = inputData.getTotalLocalSupply()
        self.swpCVPSupply = inputData.getSwpCvpSupply()
        self.contingentConservationUseReduction = inputData.getContingentConservationUseReduction()
        self.contingentConservationStorageTrigger = inputData.getContingentConservationStorageTrigger()
        self.contingentConservationUnitCost = inputData.getContingentConservationUnitCost()
        
        self.writer = pd.ExcelWriter('Output_QAQC.xlsx', engine = 'xlsxwriter')
        # Initialize time series dataframes for each variable. These dataframes include time series for all contractors.
        self.appliedDemands = {'Year': historicHydrologyYears} #Setting these variables in the constructor method creates an instance of them in this class so we don't need to keep passing them as arguments to functions, the functions 
        self.demandsToBeMetBySWPCVP = {'Year': historicHydrologyYears}
        self.demandsToBeMetByStorage = {'Year': historicHydrologyYears}
        self.demandsToBeMetByBankedGW = {'Year': historicHydrologyYears}
        self.excessSupply = {'Year': historicHydrologyYears}
        self.groundwaterPumpingReduction = {'Year': historicHydrologyYears}

        # Surface carryover and banked groundwater storage dataframes
        self.volumeSurfaceCarryover = {'Year': historicHydrologyYears}
        self.volumeGroundwaterBank = {'Year': historicHydrologyYears}
        self.availableCapacitySurface = {'Year': historicHydrologyYears}
        self.availableGroundwaterCapacity = {'Year': historicHydrologyYears}
        self.putGroundwater = {'Year': historicHydrologyYears}
        self.putSurface = {'Year': historicHydrologyYears}
        self.takeSurface = {'Year': historicHydrologyYears}
        self.takeGroundwater = {'Year': historicHydrologyYears}
        self.putGroundwaterBankCost = {'Year': historicHydrologyYears}
        self.takeGroundwaterBankCost = {'Year': historicHydrologyYears}

        # Hedging strategy dataframes
        self.pctCapacitySurfaceCarryover = {'Year': historicHydrologyYears}
        self.pctStorageCalledSurfaceCarryover = {'Year': historicHydrologyYears}
        self.pctCapacityGroundwaterBank = {'Year': historicHydrologyYears}
        self.pctStorageCalledGroundwaterBank = {'Year': historicHydrologyYears}

        # Contingent WMOs dataframes
        self.demandsToBeMetByContingentOptions = {'Year': historicHydrologyYears}
        self.contingentConservationReductionVolume = {'Year': historicHydrologyYears}
        self.waterMarketTransferDeliveries = {'Year': historicHydrologyYears}
        self.totalShortage = {'Year': historicHydrologyYears}

    def execute(self):
        # Loop through model calculations for each contractor. All variables in this loop end with "_Contractor"
        
        for self.contractor in contractorsList:
            # Set up variables that will be used for calcs by contractor
            totalDemand_Contractor = totalDemands[self.contractor]
            self.appliedDemand_Contractor = []

            self.longtermWMOSurfaceVolume_Contractor = longtermWMOSurfaceVolume.loc[self.contractor][futureYear]
            
            demandsToBeMetBySWPCVP_Contractor = []
            demandsToBeMetByStorage_Contractor = []

            excessSupplySwitch_Contractor = excessWaterSwitchData['Switch'].loc[[self.contractor]].values[0]
            self.excessSupply_Contractor = []
            self.groundwaterPumpingReduction_Contractor = []
            
            self.volumeSurfaceCarryover_Contractor = []
            self.volumeGroundwaterBank_Contractor = []
            self.putSurface_Contractor = []
            self.putGroundwater_Contractor = []
            self.takeSurface_Contractor = []
            self.takeGroundwater_Contractor = []
            storageInputAssumptions_Contractor = getContractorStorageAssumptions(self.contractor, futureYear, excessWaterSwitchData, storageData, storageHedgingStrategyData)
            
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
            for self.i in range(len(historicHydrologyYears)):
                
                
                #### Deliver local and project supplies to meet demands:
                # Calculate Applied Demand after subtraction of Planned Long-term Conservation
                plannedLongTermConservation_Contractor = plannedLongTermConservation[plannedLongTermConservation['Contractor'] == self.contractor][futureYear].values[0]
                self.appliedDemand_Contractor.append(max(0, totalDemand_Contractor[self.i] - plannedLongTermConservation_Contractor))

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
                    putsIntoStorage_Contractor = putExcessSupplyIntoStorage(self.i, 
                                            excessSupplySwitch_Contractor, self.excessSupply_Contractor,
                                            self.availableGroundwaterCapacity_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumPutCapacity_Contractor'], storageInputAssumptions_Contractor['rechargeEffectiveness_Contractor'], # groundwater bank assumptions
                                            self.availableCapacitySurface_Contractor, storageInputAssumptions_Contractor['surfaceMaximumPutCapacity_Contractor']) # surface carryover assumptions
                
                    self.putGroundwater_Contractor.append(putsIntoStorage_Contractor['putGroundwater_Contractor'])
                    self.putSurface_Contractor.append(putsIntoStorage_Contractor['putSurface_Contractor'])
                    
                    self.volumeGroundwaterBank_Contractor[self.i] = self.volumeGroundwaterBank_Contractor[self.i] + self.putGroundwater_Contractor[self.i]
                    self.volumeSurfaceCarryover_Contractor[self.i] = self.volumeSurfaceCarryover_Contractor[self.i] + self.putSurface_Contractor[self.i]
                    
                ## If there is no excess supply, but remaining demand after local and CVP/SWP supplies are delivered, take from surface carryover storage first, then banked groundwater storage
                    takesFromStorage_Contractor = takeFromStorage(self.i, demandsToBeMetByStorage_Contractor, 
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
                self.contingentConservationUseReduction_Contractor = self.contingentConservationUseReduction[self.contingentConservationUseReduction['Contractor'] == self.contractor][futureYear].values[0]
                contingentConservationStorageTrigger_Contractor = self.contingentConservationStorageTrigger[self.contingentConservationStorageTrigger['Contractor'] == self.contractor][futureYear].values[0]
                self.shortageThresholdForWaterMarketTransfers_Contractor = shortageThresholdForWaterMarketTransfers.loc[self.contractor][futureYear] / 100
                
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
                 
            ## Calculate Reliability Management Costs
                
                self.groundwaterBankPutUnitCost_Contractor = groundwaterBankPutUnitCost.loc[self.contractor][futureYear]
                self.groundwaterBankTakeUnitCost_Contractor = groundwaterBankTakeUnitCost.loc[self.contractor][futureYear]
                self.swpCVPDeliveryUnitCost_Contractor = swpCVPDeliveryUnitCost.loc[self.contractor][futureYear]
                self.groundwaterPumpingUnitCost_Contractor = groundwaterPumpingUnitCost[self.contractor][self.i]
                self.waterTreatmentUnitCost_Contractor = waterTreatmentUnitCost.loc[self.contractor][futureYear]
                self.distributionUnitCost_Contractor = distributionUnitCost.loc[self.contractor][futureYear]
                self.wastewaterTreatmentUnitCost_Contractor = wastewaterTreatmentUnitCost.loc[self.contractor][futureYear]
                self.wastewaterTreatmentFraction_Contractor = wastewaterTreatmentFraction.loc[self.contractor][futureYear] / 100
                
                self.waterMarketTransferUnitCost_Contractor = waterMarketTransferCost[self.contractor][self.i]
                self.contingentConservationUnitCost_Contractor = self.contingentConservationUnitCost.loc[self.contractor][futureYear]
                self.urbanPopulation_Contractor = urbanPopulation.loc[self.contractor][futureYear] * 1000
                
                longtermWMOSurfaceUnitCost_Contractor = longtermWMOSurfaceUnitCost.loc[self.contractor][futureYear]
                longtermWMOGroundwaterUnitCost_Contractor = longtermWMOGroundwaterUnitCost.loc[self.contractor][futureYear]
                longtermWMODesalinationUnitCost_Contractor = longtermWMODesalinationUnitCost.loc[self.contractor][futureYear]
                longtermWMORecycledUnitCost_Contractor = longtermWMORecycledUnitCost.loc[self.contractor][futureYear]
                longtermWMOPotableReuseUnitCost_Contractor = longtermWMOPotableReuseUnitCost.loc[self.contractor][futureYear]
                longtermWMOTransfersExchangesUnitCost_Contractor = longtermWMOTransfersExchangesUnitCost.loc[self.contractor][futureYear]
                longtermWMOOtherSupplyUnitCost_Contractor = longtermWMOOtherSupplyUnitCost.loc[self.contractor][futureYear]
                longtermWMOConservationUnitCost_Contractor = longtermWMOConservationUnitCost.loc[self.contractor][futureYear]
                
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
        
    def implementContingencyWMOs(self):
        self.implementContingencyConservation()
        
        ## Deliver Water Market Transfer supplies if shortage is above user-indicated threshold
        self.shortagePortionOfTotalAppliedDemand = self.demandsToBeMetByContingentOptions_Contractor[self.i] / self.appliedDemand_Contractor[self.i]
        if  self.shortagePortionOfTotalAppliedDemand > self.shortageThresholdForWaterMarketTransfers_Contractor:
            self.deliverWaterMarketTransfers()
            
    def doNotImplementContingencyWMOs(self):
        self.contingentConservationUseReductionVolume_Contractor.append(0)
        self.waterMarketTransferDeliveries_Contractor.append(0)
        self.totalShortage_Contractor.append(0)
        
    def deliverWaterMarketTransfers(self):
        self.totalShortage_Contractor.append(max(0, self.demandsToBeMetByWaterMarketTransfers_Contractor[self.i] - transferLimit[self.contractor][self.i]))
        self.waterMarketTransferDeliveries_Contractor.append(self.demandsToBeMetByWaterMarketTransfers_Contractor[self.i] - self.totalShortage_Contractor[self.i])
        
    def implementContingencyConservation(self):
        self.contingentConservationUseReductionVolume_Contractor.append(max(0, self.contingentConservationUseReduction_Contractor * self.appliedDemand_Contractor[self.i]))
        self.demandsToBeMetByWaterMarketTransfers_Contractor.append(self.demandsToBeMetByContingentOptions_Contractor[self.i] - self.contingentConservationUseReductionVolume_Contractor[self.i])

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