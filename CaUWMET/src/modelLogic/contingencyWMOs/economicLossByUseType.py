import math
from src.modelLogic.inputData import InputData
from src.modelLogic.contingencyWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput
from src.modelLogic.contingencyWMOs.shortageByUseType import ShortageByUseType

class ContingencyWMOs:
    def __init__(self, inputData: InputData):
        self.inputData = inputData
        self.shortageByUseType = ShortageByUseType(self.inputData)
      
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