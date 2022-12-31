import math
from src.modelLogic.inputData import InputData
from src.modelLogic.contingencyWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput

class ContingencyWMOs:
    def __init__(self, inputData: InputData):
        self.inputData = inputData
        self.contingentConservationUseReductionVolume_Contractor = []
        self.waterMarketTransferDeliveries_Contractor = []
        self.totalShortage_Contractor = []
        self.demandsToBeMetByWaterMarketTransfers_Contractor = []
        
    def implementContingencyWMOsIfNeeded(self, input: ContingencyWMOsHandlerInput):
        self.input = input
        contingentConservationStorageTrigger_Contractor = self.inputData.contingentConservationStorageTrigger[self.inputData.contingentConservationStorageTrigger['Contractor'] == self.input.contractor][self.inputData.futureYear].values[0]
        self.shortageThresholdForWaterMarketTransfers_Contractor = self.inputData.shortageThresholdForWaterMarketTransfers.loc[self.input.contractor][self.inputData.futureYear] / 100
        
        if self.input.demandsToBeMetByContingentOptions_Contractor[self.input.i] > 0.0 or (self.input.volumeSurfaceCarryover_Contractor[self.input.i] + self.input.volumeGroundwaterBank_Contractor[self.input.i]) < contingentConservationStorageTrigger_Contractor:
            self.implementContingencyWMOs()
        else:
            self.doNotImplementContingencyWMOs()
        
    def implementContingencyWMOs(self):
        self.implementContingencyConservation()
        self.deliverWaterMarketTransfers()
        
        # Implement Rationing Program and calculate Loss Function
        self.calculateShortageByUseType()
        self.calculateEconomicLossByUseType()
            
            
    def doNotImplementContingencyWMOs(self):
        self.contingentConservationUseReductionVolume_Contractor.append(0)
        self.waterMarketTransferDeliveries_Contractor.append(0)
        self.totalShortage_Contractor.append(0)
        
    def implementContingencyConservation(self):
        self.contingentConservationUseReduction_Contractor = self.inputData.contingentConservationUseReduction[self.inputData.contingentConservationUseReduction['Contractor'] == self.input.contractor][self.inputData.futureYear].values[0]
        
        self.contingentConservationUseReductionVolume_Contractor.append((self.contingentConservationUseReduction_Contractor/100) * self.input.appliedDemand_Contractor[self.input.i])
        self.demandsToBeMetByWaterMarketTransfers_Contractor.append(self.input.demandsToBeMetByContingentOptions_Contractor[self.input.i] - self.contingentConservationUseReductionVolume_Contractor[self.input.i])
    
    def deliverWaterMarketTransfers(self):
        self.shortagePortionOfTotalAppliedDemand = self.input.demandsToBeMetByContingentOptions_Contractor[self.input.i] / self.input.appliedDemand_Contractor[self.input.i]
        
        ## Deliver Water Market Transfer supplies if shortage portion is above user-indicated threshold
        if  self.shortagePortionOfTotalAppliedDemand > self.shortageThresholdForWaterMarketTransfers_Contractor:
            self.waterMarketTransferDeliveries_Contractor.append(min(self.demandsToBeMetByWaterMarketTransfers_Contractor[self.input.i], self.inputData.transferLimit[self.input.contractor][self.input.i]))
            self.totalShortage_Contractor.append(max(0, self.demandsToBeMetByWaterMarketTransfers_Contractor[self.input.i] - self.waterMarketTransferDeliveries_Contractor[self.input.i]))
        else:
            self.totalShortage_Contractor.append(self.demandsToBeMetByWaterMarketTransfers_Contractor[self.input.i])
            
    
    def calculateShortageByUseType(self):
        # Calculate demand hardening adjustment factor and adjusted shortage
        self.demandHardeningFactor_Contractor = int(self.inputData.demandHardeningFactor.loc[self.input.contractor][self.inputData.futureYear]) / int(100)
        self.baseConservationAsPercentOfDemand = self.input.plannedLongTermConservation_Contractor / self.input.totalDemand_Contractor[self.input.i]
        self.longTermWMOConservationAsPercentOfDemand = self.input.longtermWMOConservationIncrementalVolume_Contractor / self.input.totalDemand_Contractor[self.input.i]
        self.demandHardeningAdjustmentFactor_Contractor = 1 + ((((1 + self.baseConservationAsPercentOfDemand) * (1 + self.longTermWMOConservationAsPercentOfDemand)) -1) * self.demandHardeningFactor_Contractor)
        self.adjustedShortage_Contractor = self.totalShortage_Contractor[self.input.i] * self.demandHardeningAdjustmentFactor_Contractor
        
        # Calculate shortage portion by type
        self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor = self.adjustedShortage_Contractor/ (self.inputData.cutRatio_singleFamily.loc[self.input.contractor] * self.inputData.singleFamilyUsePortion.loc[self.input.contractor] 
                                                                              + self.inputData.cutRatio_multiFamily.loc[self.input.contractor] * self.inputData.multiFamilyUsePortion.loc[self.input.contractor] 
                                                                              + self.inputData.cutRatio_industrial.loc[self.input.contractor] * self.inputData.industrialUsePortion.loc[self.input.contractor] 
                                                                              + self.inputData.cutRatio_commercial.loc[self.input.contractor] * self.inputData.commAndGovUsePortion.loc[self.input.contractor] 
                                                                              + self.inputData.cutRatio_landscape.loc[self.input.contractor] * self.inputData.landscapeUsePortion.loc[self.input.contractor]
                                                                                )
        self.multiFamilyShortagePortionOfMultiFamilyUse_Contractor = self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor * self.inputData.cutRatio_multiFamily.loc[self.input.contractor]
        self.industrialShortagePortionOfIndustrialUse_Contractor = self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor * self.inputData.cutRatio_industrial.loc[self.input.contractor]
        self.commercialShortagePortionOfCommerciallUse_Contractor = self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor * self.inputData.cutRatio_commercial.loc[self.input.contractor]
        self.landscapeShortagePortionOfLandscapeUse_Contractor = self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor * self.inputData.cutRatio_landscape.loc[self.input.contractor]
        
        # Calculate shortage by type
        self.singleFamilyShortage_Contractor = self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor * self.adjustedShortage_Contractor
        self.multiamilyShortage_Contractor = self.multiFamilyShortagePortionOfMultiFamilyUse_Contractor * self.adjustedShortage_Contractor
        self.industrialShortage_Contractor = self.industrialShortagePortionOfIndustrialUse_Contractor * self.adjustedShortage_Contractor
        self.commercialShortage_Contractor = self.commercialShortagePortionOfCommerciallUse_Contractor * self.adjustedShortage_Contractor
        self.landscapeShortage_Contractor = self.landscapeShortagePortionOfLandscapeUse_Contractor * self.adjustedShortage_Contractor
        #TODO add test to confirm total shortage of each use type = adjusted shortage
    
    def calculateEconomicLossByUseType(self):
        self.singleFamilyUse_Contractor = self.inputData.singleFamilyUsePortion * self.input.appliedDemand_Contractor[self.input.i]
        self.multiFamilyUse_Contractor = self.inputData.multiFamilyUsePortion * self.input.appliedDemand_Contractor[self.input.i]
        self.industrialUse_Contractor = self.inputData.industrialUsePortion * self.input.appliedDemand_Contractor[self.input.i]
        self.commAndGovUse_Contractor = self.inputData.commAndGovUsePortion * self.input.appliedDemand_Contractor[self.input.i]
        self.landscapeUse_Contractor = self.inputData.landscapeUsePortion * self.input.appliedDemand_Contractor[self.input.i]
        
        ##TODO elasticity should be by use type specifically?
        self.coefficient_SF = self.singleFamilyUse_Contractor / (float(self.inputData.retailPrice.loc[self.input.contractor]) ** float(self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor]))
        self.coefficient_MF = self.multiFamilyUse_Contractor / (float(self.inputData.retailPrice.loc[self.input.contractor]) ** float(self.inputData.elasticityOfDemand_multiFamily.loc[self.input.contractor]))
        self.coefficient_IND = self.industrialUse_Contractor / (float(self.inputData.retailPrice.loc[self.input.contractor]) ** float(self.inputData.elasticityOfDemand_indsutrial.loc[self.input.contractor]))
        self.coefficient_COM = self.commAndGovUse_Contractor / (float(self.inputData.retailPrice.loc[self.input.contractor]) ** float(self.inputData.elasticityOfDemand_commAndGov.loc[self.input.contractor]))
        self.coefficient_LAND = self.landscapeUse_Contractor / (float(self.inputData.retailPrice.loc[self.input.contractor]) ** float(self.inputData.elasticityOfDemand_landscape.loc[self.input.contractor]))
        
        if self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor <= self.inputData.lowerLossBoundary.loc[self.input.contractor]:
            self.singleFamilyEconomicLoss_Contractor = ((self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] * self.singleFamilyUse_Contractor * math.exp((math.log(self.singleFamilyUse_Contractor / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] + 1))
            - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] 
                * (self.singleFamilyUse_Contractor 
                   * (1 - self.inputData.lowerLossBoundary.loc[self.input.contractor]) 
                   * math.exp((math.log(self.singleFamilyUse_Contractor * (1 - self.inputData.lowerLossBoundary.loc[self.input.contractor]) 
                                        / self.coefficient_SF) 
                               / self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor])) 
                   / (self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] + 1))))
        elif self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor >= self.inputData.upperLossBoundary.loc[self.input.contractor]:
            ((self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] * self.singleFamilyUse_Contractor 
              * math.exp((math.log(self.singleFamilyUse_Contractor  / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] + 1))
            - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] * (self.singleFamilyUse_Contractor * (1 - self.inputData.upperLossBoundary.loc[self.input.contractor])) 
                * math.exp((math.log((self.singleFamilyUse_Contractor * (1 - self.inputData.upperLossBoundary.loc[self.input.contractor]))) / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor]))/(self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] + 1)
        else:
            ((self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] * self.singleFamilyUse_Contractor * math.exp((math.log(self.singleFamilyUse_Contractor / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor]))/(self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] + 1)) - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] * (self.singleFamilyUse_Contractor - self.singleFamilyShortage_Contractor)*math.exp((math.log((self.singleFamilyUse_Contractor - self.singleFamilyShortage_Contractor)/self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.input.contractor] + 1))