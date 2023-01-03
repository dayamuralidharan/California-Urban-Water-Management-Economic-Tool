import math
from src.modelLogic.inputData import InputData
from src.modelLogic.contingentWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput
from src.modelLogic.contingentWMOs.shortageByUseType import ShortageByUseType

class EconomicLossByUseType:
    def __init__(self, inputData: InputData, shortageByUseType: ShortageByUseType, input: ContingencyWMOsHandlerInput):
        self.inputData = inputData
        self.shortageByUseType = shortageByUseType
        self.contingentWMOsinput = input
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
      
        self.singleFamilyEconomicLoss_Contractor = []
        self.multiFamilyEconomicLoss_Contractor = []
        self.industrialEconomicLoss_Contractor = []
        self.commAndGovEconomicLoss_Contractor = []
        self.landscapeEconomicLoss_Contractor = []
      
    def calculateEconomicLossByUseType(self, shortageByUseType, shortagePortionOfUse, lowerLossBoundary, elasticityOfDemand, volumeByUseType, coefficient, economicLossByUseType):
        if shortagePortionOfUse <= lowerLossBoundary.loc[self.contingentWMOsinput.contractor]:
            economicLoss = ((elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * volumeByUseType * math.exp((math.log(volumeByUseType / coefficient)) / elasticityOfDemand.loc[self.contingentWMOsinput.contractor])) / (elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1))
            - ((elasticityOfDemand.loc[self.contingentWMOsinput.contractor] 
                * (volumeByUseType 
                   * (1 - lowerLossBoundary.loc[self.contingentWMOsinput.contractor]) 
                   * math.exp((math.log(volumeByUseType * (1 - lowerLossBoundary.loc[self.contingentWMOsinput.contractor]) 
                                        / coefficient) 
                               / elasticityOfDemand.loc[self.contingentWMOsinput.contractor])) 
                   / (elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1))))
        elif shortagePortionOfUse >= self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor]:
            economicLoss = ((elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * volumeByUseType 
              * math.exp((math.log(volumeByUseType  / coefficient)) / elasticityOfDemand.loc[self.contingentWMOsinput.contractor])) / (elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1))
            - ((elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * (volumeByUseType * (1 - self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor])) 
                * math.exp((math.log((volumeByUseType * (1 - self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor]))) / coefficient)) / elasticityOfDemand.loc[self.contingentWMOsinput.contractor]))/(elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1)
        else:
            economicLoss = ((elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * volumeByUseType * math.exp((math.log(volumeByUseType / coefficient)) / elasticityOfDemand.loc[self.contingentWMOsinput.contractor]))/(elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1)) - ((elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * (volumeByUseType - shortageByUseType)*math.exp((math.log((volumeByUseType - shortageByUseType)/coefficient)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))
        
        
        economicLossByUseType.append(economicLoss)
        
        # if self.shortageByUseType.singleFamilyShortagePortionOfSingleFamilyUse_Contractor <= self.inputData.lowerLossBoundary.loc[self.contingentWMOsinput.contractor]:
        #     self.singleFamilyEconomicLoss_Contractor = ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * self.singleFamilyUse_Contractor * math.exp((math.log(self.singleFamilyUse_Contractor / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))
        #     - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] 
        #         * (self.singleFamilyUse_Contractor 
        #            * (1 - self.inputData.lowerLossBoundary.loc[self.contingentWMOsinput.contractor]) 
        #            * math.exp((math.log(self.singleFamilyUse_Contractor * (1 - self.inputData.lowerLossBoundary.loc[self.contingentWMOsinput.contractor]) 
        #                                 / self.coefficient_SF) 
        #                        / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) 
        #            / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))))
        # elif self.shortageByUseType.singleFamilyShortagePortionOfSingleFamilyUse_Contractor >= self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor]:
        #     ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * self.singleFamilyUse_Contractor 
        #       * math.exp((math.log(self.singleFamilyUse_Contractor  / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))
        #     - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * (self.singleFamilyUse_Contractor * (1 - self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor])) 
        #         * math.exp((math.log((self.singleFamilyUse_Contractor * (1 - self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor]))) / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor]))/(self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1)
        # else:
        #     ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * self.singleFamilyUse_Contractor * math.exp((math.log(self.singleFamilyUse_Contractor / self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor]))/(self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1)) - ((self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] * (self.singleFamilyUse_Contractor - self.shortageByUseType.singleFamilyShortage_Contractor)*math.exp((math.log((self.singleFamilyUse_Contractor - self.shortageByUseType.singleFamilyShortage_Contractor)/self.coefficient_SF)) / self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor])) / (self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor] + 1))