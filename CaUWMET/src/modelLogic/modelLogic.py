import pandas as pd
from src.modelLogic.readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from src.modelLogic.readDemandAssumptions import totalDemands, plannedLongTermConservation
from src.modelLogic.readSupplyAssumptions import totalLocalSupply, swpCVPSupply
from src.modelLogic.readSystemOperationsAssumptions import storageData,  storageHedgingStrategyData, excessWaterSwitchData
from src.modelLogic.readContingentWMOsAssumptions import contingentConservationUseReduction, contingentConservationStorageTrigger, shortageThresholdForWaterMarketTransfers, transferLimit, waterMarketTransferCost
from src.modelLogic.storageUtilities import getContractorStorageAssumptions, putExcessSupplyIntoStorage, takeFromStorage

#TODO change all data frames with "['Contractor'] == contractor" to use Contractor column as index. See shortageThresholdForWaterMarketTransfers as example.
#TODO change availableCapacitySurface_Contractor to a list/dataframe instead of scalar
#TODO Make code faster

class ModelLogic:
    def __init__(self):
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

        # Hedging strategy dataframes
        self.pctCapacitySurfaceCarryover = {'Year': historicHydrologyYears}
        self.pctStorageCalledSurfaceCarryover = {'Year': historicHydrologyYears}
        self.pctCapacityGroundwaterBank = {'Year': historicHydrologyYears}
        self.pctStorageCalledGroundwaterBank = {'Year': historicHydrologyYears}

        # Contingent WMOs dataframes
        self.demandsToBeMetByContingentOptions = {'Year': historicHydrologyYears}
        self.contingentConservationReduction = {'Year': historicHydrologyYears}
        self.waterMarketTransferDeliveries = {'Year': historicHydrologyYears}
        self.totalShortage = {'Year': historicHydrologyYears}

    def execute(self):
        # Loop through model calculations for each contractor. All variables in this loop start with "contractor" to indicate it is only used in this loop.
        
        for self.contractor in contractorsList:
            # Set up variables that will be used for calcs by contractor
            totalDemand_Contractor = totalDemands[self.contractor]
            self.appliedDemand_Contractor = []
            demandsToBeMetBySWPCVP_Contractor = []
            demandsToBeMetByStorage_Contractor = []
            demandToBeMetByContingentOptions_Contractor = []
            demandToBeMetByWaterMarketTransfers_Contractor = []

            excessSupplySwitch_Contractor = excessWaterSwitchData['Switch'].loc[[self.contractor]].values[0]
            excessSupply_Contractor = []
            groundwaterPumpingReduction_Contractor = []
            
            volumeSurfaceCarryover_Contractor = []
            volumeGroundwaterBank_Contractor = []
            putSurface_Contractor = []
            putGroundwater_Contractor = []
            takeSurface_Contractor = []
            takeGroundwater_Contractor = []
            
            storageInputAssumptions_Contractor = getContractorStorageAssumptions(self.contractor, futureYear, excessWaterSwitchData, storageData, storageHedgingStrategyData)
            
            self.demandsToBeMetByContingentOptions_Contractor = []
            self.contingentConservationUseReductionVolume_Contractor = []
            self.demandsToBeMetByWaterMarketTransfers_Contractor = []
            self.waterMarketTransferDeliveries_Contractor = []
            self.totalShortage_Contractor = []
            

            for self.i in range(len(historicHydrologyYears)):
                
                
                #### Deliver local and project supplies to meet demands:
                # Calculate Applied Demand after subtraction of Planned Long-term Conservation
                plannedLongTermConservation_Contractor = plannedLongTermConservation[plannedLongTermConservation['Contractor'] == self.contractor][futureYear].values[0]
                self.appliedDemand_Contractor.append(max(0, totalDemand_Contractor[self.i] - plannedLongTermConservation_Contractor))

                # Calculate Demand to be Met by SWP/CVP supplies after subtraction of local supplies
                demandsToBeMetBySWPCVP_Contractor.append(max(0, self.appliedDemand_Contractor[self.i] - totalLocalSupply[self.contractor][self.i]))

                # Calculate Demand to be Met by Stored supplies after delivery of SWP/CVP supplies, or calculate Excess SWP/CVP Supply.
                SWPCVPSupply_Contractor = swpCVPSupply[self.contractor][self.i]
                if demandsToBeMetBySWPCVP_Contractor[self.i] - SWPCVPSupply_Contractor > 0:
                    demandsToBeMetByStorage_Contractor.append(demandsToBeMetBySWPCVP_Contractor[self.i] - SWPCVPSupply_Contractor)
                    excessSupply_Contractor.append(0)
                else:
                    excessSupply_Contractor.append((SWPCVPSupply_Contractor - demandsToBeMetBySWPCVP_Contractor[self.i]))
                    demandsToBeMetByStorage_Contractor.append(0)

                excessSupplyToStorageSwitches = ["Put into Carryover and Groundwater Bank", "Put into Groundwater Bank", "Put into Carryover Storage"]

                #### Put excess into or take from storage to meet demands:
                if (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[0]) or (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[1]) or (storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == excessSupplyToStorageSwitches[2]):
                    if self.i == 0: #Initialize storage volumes
                        volumeSurfaceCarryover_Contractor.append(storageInputAssumptions_Contractor['initialSurfaceStorageVolume_Contractor'])
                        volumeGroundwaterBank_Contractor.append(storageInputAssumptions_Contractor['initialGroundwaterStorageVolume_Contractor'])
                    else: # Initialize with previous time step's volumes which are updated in the putOrTakeFromStorage function
                        volumeSurfaceCarryover_Contractor.append(volumeSurfaceCarryover_Contractor[self.i-1])
                        volumeGroundwaterBank_Contractor.append(volumeGroundwaterBank_Contractor[self.i-1])
                    
                    # Check available capacity in storage systems
                    availableCapacitySurface_Contractor = storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'] - volumeSurfaceCarryover_Contractor[max(0,self.i-1)]
                    availableGroundwaterCapacity_Contractor = storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'] - volumeGroundwaterBank_Contractor[max(0,self.i-1)]
                    
                    # If there is excess supply, calculate put into storage
                    putsIntoStorage_Contractor = putExcessSupplyIntoStorage(self.i, 
                                            excessSupplySwitch_Contractor, excessSupply_Contractor,
                                            availableGroundwaterCapacity_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumPutCapacity_Contractor'], storageInputAssumptions_Contractor['rechargeEffectiveness_Contractor'], # groundwater bank assumptions
                                            availableCapacitySurface_Contractor, storageInputAssumptions_Contractor['surfaceMaximumPutCapacity_Contractor']) # surface carryover assumptions
                
                    putGroundwater_Contractor.append(putsIntoStorage_Contractor['putGroundwater_Contractor'])
                    putSurface_Contractor.append(putsIntoStorage_Contractor['putSurface_Contractor'])
                    
                    volumeGroundwaterBank_Contractor[self.i] = volumeGroundwaterBank_Contractor[self.i] + putGroundwater_Contractor[self.i]
                    volumeSurfaceCarryover_Contractor[self.i] = volumeSurfaceCarryover_Contractor[self.i] + putSurface_Contractor[self.i]
                    
                ## If there is no excess supply, but remaining demand after local and CVP/SWP supplies are delivered, take from surface carryover storage first, then banked groundwater storage
                    takesFromStorage_Contractor = takeFromStorage(self.i, demandsToBeMetByStorage_Contractor, 
                                    volumeSurfaceCarryover_Contractor, storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'], storageInputAssumptions_Contractor['surfaceMaximumTakeCapacity_Contractor'],
                                    volumeGroundwaterBank_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'], storageInputAssumptions_Contractor['groundwaterMaximumTakeCapacity_Contractor'],
                                    storageInputAssumptions_Contractor['storageHedgingStrategySwitch_Contractor'], storageInputAssumptions_Contractor['hedgingPoint_Contractor'], storageInputAssumptions_Contractor['hedgeCallStorageFactor_Contractor'], storageInputAssumptions_Contractor['hedgingStorageCapacityFactor_Contractor'])
                    
                    takeSurface_Contractor.append(takesFromStorage_Contractor['takeSurface_Contractor'])
                    takeGroundwater_Contractor.append(takesFromStorage_Contractor['takeGroundwater_Contractor'])
                    self.demandsToBeMetByContingentOptions_Contractor.append(takesFromStorage_Contractor['demandsToBeMetByContingentOptions_Contractor'])
                elif storageInputAssumptions_Contractor['excessSupplySwitch_Contractor'] == "Reduce Groundwater Pumping":
                    groundwaterPumpingReduction_Contractor.append(excessSupply_Contractor[self.i])
                    volumeSurfaceCarryover_Contractor.append(0) ############### Clean up this duplication of code with the block below
                    volumeGroundwaterBank_Contractor.append(0)
                    availableCapacitySurface_Contractor = 0
                    availableGroundwaterCapacity_Contractor = 0
                    putSurface_Contractor.append(0)
                    putGroundwater_Contractor.append(0)
                    takeSurface_Contractor.append(0)
                    takeGroundwater_Contractor.append(0)
                    self.demandsToBeMetByContingentOptions_Contractor.append(0)
                else:
                    groundwaterPumpingReduction_Contractor.append(0)
                    volumeSurfaceCarryover_Contractor.append(0)
                    volumeGroundwaterBank_Contractor.append(0)
                    availableCapacitySurface_Contractor = 0
                    availableGroundwaterCapacity_Contractor = 0
                    putSurface_Contractor.append(0)
                    putGroundwater_Contractor.append(0)
                    takeSurface_Contractor.append(0)
                    takeGroundwater_Contractor.append(0)
                    self.demandsToBeMetByContingentOptions_Contractor.append(0)

            ## If there is remaining demand and storage is below user-defined threshold, implement contingency conservation and water market transfers assumptions:
                self.contingentConservationUseReduction_Contractor = contingentConservationUseReduction[contingentConservationUseReduction['Contractor'] == self.contractor][futureYear].values[0]
                contingentConservationStorageTrigger_Contractor = contingentConservationStorageTrigger[contingentConservationStorageTrigger['Contractor'] == self.contractor][futureYear].values[0]
                self.shortageThresholdForWaterMarketTransfers_Contractor = shortageThresholdForWaterMarketTransfers.loc[self.contractor][futureYear] / 100
                
                if self.demandsToBeMetByContingentOptions_Contractor[self.i] > 0.0:
                    self.implementContingencyWMOs()
                else:
                    self.doNotImplementContingencyWMOs()
                    
            ## Calculate Costs
            #swpCVPDeliveryCost_Contractor
            #groundwaterBankCost_Contractor
            
                    
            
            







        # Append dataframes with updated contractor data as calculated in model logic above.
            self.appliedDemands[self.contractor] = self.appliedDemand_Contractor
            self.demandsToBeMetBySWPCVP[self.contractor] = demandsToBeMetBySWPCVP_Contractor
            self.demandsToBeMetByStorage[self.contractor] = demandsToBeMetByStorage_Contractor
            self.excessSupply[self.contractor] = excessSupply_Contractor
            
            self.volumeSurfaceCarryover[self.contractor] = volumeSurfaceCarryover_Contractor
            self.volumeGroundwaterBank[self.contractor] = volumeGroundwaterBank_Contractor
            self.availableCapacitySurface[self.contractor] = availableCapacitySurface_Contractor
            self.availableGroundwaterCapacity[self.contractor] = availableGroundwaterCapacity_Contractor
            self.putGroundwater[self.contractor] = putGroundwater_Contractor
            self.putSurface[self.contractor] = putSurface_Contractor
            self.takeSurface[self.contractor] = takeSurface_Contractor
            self.takeGroundwater[self.contractor] = takeGroundwater_Contractor
            # pctCapacitySurfaceCarryover[contractor] = pctCapacitySurfaceCarryover_Contractor
            # pctStorageCalledSurfaceCarryover[contractor] = pctStorageCalledSurfaceCarryover_Contractor
            # pctCapacityGroundwaterBank[contractor] = pctCapacityGroundwaterBank_Contractor
            # pctStorageCalledGroundwaterBank[contractor] = pctStorageCalledGroundwaterBank_Contractor
            
            self.demandsToBeMetByContingentOptions[self.contractor] = self.demandsToBeMetByContingentOptions_Contractor
            self.contingentConservationReduction[self.contractor] = self.contingentConservationUseReductionVolume_Contractor
            self.waterMarketTransferDeliveries[self.contractor] = self.waterMarketTransferDeliveries_Contractor
            self.totalShortage[self.contractor] = self.totalShortage_Contractor




        self.appliedDemands = pd.DataFrame(self.appliedDemands)
        self.demandsToBeMetBySWPCVP = pd.DataFrame(self.demandsToBeMetBySWPCVP)
        self.demandsToBeMetByStorage = pd.DataFrame(self.demandsToBeMetByStorage)
        self.excessSupply = pd.DataFrame(self.excessSupply)

        self.volumeSurfaceCarryover = pd.DataFrame(self.volumeSurfaceCarryover)
        self.volumeGroundwaterBank = pd.DataFrame(self.volumeGroundwaterBank)
        self.availableCapacitySurface = pd.DataFrame(self.availableCapacitySurface)
        self.availableGroundwaterCapacity = pd.DataFrame(self.availableGroundwaterCapacity)
        self.putGroundwater = pd.DataFrame(self.putGroundwater)
        self.putSurface = pd.DataFrame(self.putSurface)
        self.takeSurface= pd.DataFrame(self.takeSurface)
        self.takeGroundwater = pd.DataFrame(self.takeGroundwater)

        # pctCapacitySurfaceCarryover = pd.DataFrame(pctCapacitySurfaceCarryover)
        # pctStorageCalledSurfaceCarryover = pd.DataFrame(pctStorageCalledSurfaceCarryover)
        # pctCapacityGroundwaterBank= pd.DataFrame(pctCapacityGroundwaterBank)
        # pctStorageCalledGroundwaterBank = pd.DataFrame(pctStorageCalledGroundwaterBank)

        self.demandsToBeMetByContingentOptions = pd.DataFrame(self.demandsToBeMetByContingentOptions)
        self.contingentConservationReduction = pd.DataFrame(self.contingentConservationReduction)
        self.waterMarketTransferDeliveries = pd.DataFrame(self.waterMarketTransferDeliveries)
        self.totalShortage = pd.DataFrame(self.totalShortage)

        workbook = self.writer.book

        self.appliedDemands.to_excel(self.writer, sheet_name = 'appliedDemands')
        self.demandsToBeMetBySWPCVP.to_excel(self.writer, sheet_name = 'demandsToBeMetBySWPCVP')
        self.demandsToBeMetByStorage.to_excel(self.writer, sheet_name = 'demandsToBeMetByStorage')
        self.volumeSurfaceCarryover.to_excel(self.writer, sheet_name = 'volumeSurfaceCarryover')
        self.volumeGroundwaterBank.to_excel(self.writer, sheet_name = 'volumeGroundwaterBank')
        self.availableCapacitySurface.to_excel(self.writer, sheet_name = 'availableCapacitySurface')
        self.availableGroundwaterCapacity.to_excel(self.writer, sheet_name = 'availableGroundwaterCapacity')
        self.putGroundwater.to_excel(self.writer, sheet_name = 'putGroundwater')
        self.putSurface.to_excel(self.writer, sheet_name = 'putSurface')
        self.takeGroundwater.to_excel(self.writer, sheet_name = 'takeGroundwater')
        self.takeSurface.to_excel(self.writer, sheet_name = 'takeSurface')

        #demandsToBeMetByContingentOptions.to_excel(writer, sheet_name = 'demandsToBeMetByContingentWMOs')


        self.writer.save()
        
    def implementContingencyWMOs(self):
        self.implementContingencyConservation()
        
        ## Deliver Water Market Transfer supplies if shortage is above user-indicated threshold
        self.shortagePortionOfTotalAppliedDemand = self.demandsToBeMetByContingentOptions_Contractor[self.i] / self.appliedDemand_Contractor[self.i]
        if  self.shortagePortionOfTotalAppliedDemand > self.shortageThresholdForWaterMarketTransfers_Contractor:
            self.deliverWaterMarketTransfers(self.contractor, self.i, self.totalShortage_Contractor, self.demandsToBeMetByWaterMarketTransfers_Contractor, self.waterMarketTransferDeliveries_Contractor)
            
    def doNotImplementContingencyWMOs(self):
        self.contingentConservationUseReductionVolume_Contractor.append(0)
        self.waterMarketTransferDeliveries_Contractor.append(0)
        self.totalShortage_Contractor.append(0)
        
    def deliverWaterMarketTransfers(self, contractor, i, totalShortage, demandsToBeMetByWaterMarketTransfers, waterMarketTransferDeliveries):
        totalShortage.append(max(0, demandsToBeMetByWaterMarketTransfers[i] - transferLimit[contractor][i]))
        waterMarketTransferDeliveries.append(demandsToBeMetByWaterMarketTransfers[i] - totalShortage[i])
        
    def implementContingencyConservation(self):
        self.contingentConservationUseReductionVolume_Contractor = max(0, self.contingentConservationUseReduction_Contractor * self.appliedDemand_Contractor[self.i])
        self.demandsToBeMetByWaterMarketTransfers_Contractor.append(self.demandsToBeMetByContingentOptions_Contractor[self.i] - self.contingentConservationUseReductionVolume_Contractor)

