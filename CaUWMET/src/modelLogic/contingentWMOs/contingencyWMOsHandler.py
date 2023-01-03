import math
from src.modelLogic.inputData import InputData
from src.modelLogic.contingentWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput
from src.modelLogic.contingentWMOs.shortageByUseType import ShortageByUseType
from src.modelLogic.contingentWMOs.economicLossByUseType import EconomicLossByUseType

class ContingencyWMOs:
    def __init__(self, inputData: InputData):
        self.inputData = inputData
        self.shortageByUseType = ShortageByUseType(self.inputData)
        self.economicLossByUseType = EconomicLossByUseType(self.inputData, self.shortageByUseType)
        self.contingentConservationUseReductionVolume_Contractor = []
        self.waterMarketTransferDeliveries_Contractor = []
        self.totalShortage_Contractor = []
        self.demandsToBeMetByWaterMarketTransfers_Contractor = []
        
    def implementContingencyWMOsIfNeeded(self, input: ContingencyWMOsHandlerInput):
        self.contingentWMOsinput = input
        contingentConservationStorageTrigger_Contractor = self.inputData.contingentConservationStorageTrigger[self.inputData.contingentConservationStorageTrigger['Contractor'] == self.contingentWMOsinput.contractor][self.inputData.futureYear].values[0]
        self.shortageThresholdForWaterMarketTransfers_Contractor = self.inputData.shortageThresholdForWaterMarketTransfers.loc[self.contingentWMOsinput.contractor][self.inputData.futureYear] / 100
        
        if self.contingentWMOsinput.demandsToBeMetByContingentOptions_Contractor[self.contingentWMOsinput.i] > 0.0 or (self.contingentWMOsinput.volumeSurfaceCarryover_Contractor[self.contingentWMOsinput.i] + self.contingentWMOsinput.volumeGroundwaterBank_Contractor[self.contingentWMOsinput.i]) < contingentConservationStorageTrigger_Contractor:
            self.implementContingencyWMOs()
        else:
            self.doNotImplementContingencyWMOs()
        
    def implementContingencyWMOs(self):
        self.implementContingencyConservation()
        self.deliverWaterMarketTransfers()
        
        # Implement Rationing Program and calculate Loss Function
        self.shortageByUseType.calculateShortageByUseType(self.contingentWMOsinput, self.totalShortage_Contractor)
        self.economicLossByUseType.calculateEconomicLossByUseType(self.contingentWMOsinput)
            
            
    def doNotImplementContingencyWMOs(self):
        self.contingentConservationUseReductionVolume_Contractor.append(0)
        self.waterMarketTransferDeliveries_Contractor.append(0)
        self.totalShortage_Contractor.append(0)
        
    def implementContingencyConservation(self):
        self.contingentConservationUseReduction_Contractor = self.inputData.contingentConservationUseReduction[self.inputData.contingentConservationUseReduction['Contractor'] == self.contingentWMOsinput.contractor][self.inputData.futureYear].values[0]
        
        self.contingentConservationUseReductionVolume_Contractor.append((self.contingentConservationUseReduction_Contractor/100) * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i])
        self.demandsToBeMetByWaterMarketTransfers_Contractor.append(self.contingentWMOsinput.demandsToBeMetByContingentOptions_Contractor[self.contingentWMOsinput.i] - self.contingentConservationUseReductionVolume_Contractor[self.contingentWMOsinput.i])
    
    def deliverWaterMarketTransfers(self):
        self.shortagePortionOfTotalAppliedDemand = self.contingentWMOsinput.demandsToBeMetByContingentOptions_Contractor[self.contingentWMOsinput.i] / self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        
        ## Deliver Water Market Transfer supplies if shortage portion is above user-indicated threshold
        if  self.shortagePortionOfTotalAppliedDemand > self.shortageThresholdForWaterMarketTransfers_Contractor:
            self.waterMarketTransferDeliveries_Contractor.append(min(self.demandsToBeMetByWaterMarketTransfers_Contractor[self.contingentWMOsinput.i], self.inputData.transferLimit[self.contingentWMOsinput.contractor][self.contingentWMOsinput.i]))
            self.totalShortage_Contractor.append(max(0, self.demandsToBeMetByWaterMarketTransfers_Contractor[self.contingentWMOsinput.i] - self.waterMarketTransferDeliveries_Contractor[self.contingentWMOsinput.i]))
        else:
            self.totalShortage_Contractor.append(self.demandsToBeMetByWaterMarketTransfers_Contractor[self.contingentWMOsinput.i])
            
    
    def calculateEconomicLossByUseType(self):
        self.singleFamilyUse_Contractor = self.inputData.singleFamilyUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.multiFamilyUse_Contractor = self.inputData.multiFamilyUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.industrialUse_Contractor = self.inputData.industrialUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.commAndGovUse_Contractor = self.inputData.commAndGovUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.landscapeUse_Contractor = self.inputData.landscapeUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        
        self.coefficient_SF = self.singleFamilyUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor]))
        self.coefficient_MF = self.multiFamilyUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_multiFamily.loc[self.contingentWMOsinput.contractor]))
        self.coefficient_IND = self.industrialUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_indsutrial.loc[self.contingentWMOsinput.contractor]))
        self.coefficient_COM = self.commAndGovUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_commAndGov.loc[self.contingentWMOsinput.contractor]))
        self.coefficient_LAND = self.landscapeUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_landscape.loc[self.contingentWMOsinput.contractor]))
        
        if self.shortageByUseType.singleFamilyShortagePortionOfSingleFamilyUse_Contractor <= self.inputData.lowerLossBoundary.loc[self.contingentWMOsinput.contractor]:
            self.singleFamilyEconomicLoss_Contractor = ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * self.singleFamilyUse_Contractor * math.exp((math.log(self.singleFamilyUse_Contractor / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))
            - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] 
                * (self.singleFamilyUse_Contractor 
                   * (1 - self.inputData.lowerLossBoundary.loc[self.contingentWMOsinput.contractor]) 
                   * math.exp((math.log(self.singleFamilyUse_Contractor * (1 - self.inputData.lowerLossBoundary.loc[self.contingentWMOsinput.contractor]) 
                                        / self.coefficient_SF) 
                               / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) 
                   / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))))
        elif self.shortageByUseType.singleFamilyShortagePortionOfSingleFamilyUse_Contractor >= self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor]:
            ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * self.singleFamilyUse_Contractor 
              * math.exp((math.log(self.singleFamilyUse_Contractor  / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))
            - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * (self.singleFamilyUse_Contractor * (1 - self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor])) 
                * math.exp((math.log((self.singleFamilyUse_Contractor * (1 - self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor]))) / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor]))/(self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1)
        else:
            ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * self.singleFamilyUse_Contractor * math.exp((math.log(self.singleFamilyUse_Contractor / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor]))/(self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1)) - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * (self.singleFamilyUse_Contractor - self.shortageByUseType.singleFamilyShortage_Contractor)*math.exp((math.log((self.singleFamilyUse_Contractor - self.shortageByUseType.singleFamilyShortage_Contractor)/self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))