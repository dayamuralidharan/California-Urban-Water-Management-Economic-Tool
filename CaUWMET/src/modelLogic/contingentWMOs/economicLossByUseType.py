import math
from src.modelLogic.inputData import InputData
from src.modelLogic.contingentWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput
from src.modelLogic.contingentWMOs.shortageByUseType import ShortageByUseType
from src.modelLogic.contingentWMOs.contingencyWMOsHandler import ContingencyWMOs

class EconomicLossByUseType:
    def __init__(self, inputData: InputData, shortageByUseType: ShortageByUseType, input: ContingencyWMOsHandlerInput, contingencyWMOs: ContingencyWMOs):
        self.inputData = inputData
        self.shortageByUseType = shortageByUseType
        self.contingentWMOsinput = input
        self.contingencyWMOs = contingencyWMOs
        self.singleFamilyUse_Contractor = self.inputData.singleFamilyUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.multiFamilyUse_Contractor = self.inputData.multiFamilyUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.industrialUse_Contractor = self.inputData.industrialUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.commAndGovUse_Contractor = self.inputData.commAndGovUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.landscapeUse_Contractor = self.inputData.landscapeUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        
        self.coefficient_SF = self.singleFamilyUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor]))
        self.coefficient_MF = self.multiFamilyUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_multiFamily.loc[self.contingentWMOsinput.contractor]))
        self.coefficient_IND = self.industrialUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_industrial.loc[self.contingentWMOsinput.contractor]))
        self.coefficient_COM = self.commAndGovUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_commAndGov.loc[self.contingentWMOsinput.contractor]))
        self.coefficient_LAND = self.landscapeUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_landscape.loc[self.contingentWMOsinput.contractor]))
      
        self.singleFamilyEconomicLoss_Contractor = []
        self.multiFamilyEconomicLoss_Contractor = []
        self.industrialEconomicLoss_Contractor = []
        self.commAndGovEconomicLoss_Contractor = []
        self.landscapeEconomicLoss_Contractor = []
        
        self.totalEconomicLoss_Contractor = []
        
    def calculateTotalEconomicLoss(self):
        self.calculateEconomicLossByUseType()
        self.totalEconomicLoss_Contractor.append( self.singleFamilyEconomicLoss_Contractor
                                                 + self.multiFamilyEconomicLoss_Contractor
                                                 + self.industrialEconomicLoss_Contractor
                                                 + self.industrialEconomicLoss_Contractor
                                                 + self.commAndGovEconomicLoss_Contractor
                                                 + self.landscapeEconomicLoss_Contractor
                                                 )
        
    def calculateEconomicLossByUseType(self):
        self.singleFamilyEconomicLoss_Contractor.append(self.economicLossFunction(self.contingencyWMOs.shortageByUseType.singleFamilyShortage_Contractor, self.contingencyWMOs.shortageByUseType.singleFamilyShortagePortionOfSingleFamilyUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_singleFamily, self.singleFamilyUse_Contractor, self.coefficient_SF))
        self.multiFamilyEconomicLoss_Contractor.append(self.economicLossFunction(self.contingencyWMOs.shortageByUseType.multiFamilyShortage_Contractor, self.contingencyWMOs.shortageByUseType.multiFamilyShortagePortionOfMultiFamilyUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_multiFamily, self.multiFamilyUse_Contractor, self.coefficient_MF))
        self.industrialEconomicLoss_Contractor.append(self.economicLossFunction(self.contingencyWMOs.shortageByUseType.industrialShortage_Contractor, self.contingencyWMOs.shortageByUseType.industrialShortagePortionOfIndustrialUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_industrial, self.industrialUse_Contractor, self.coefficient_IND))
        self.commAndGovEconomicLoss_Contractor.append(self.economicLossFunction(self.contingencyWMOs.shortageByUseType.commercialShortage_Contractor, self.contingencyWMOs.shortageByUseType.commercialShortagePortionOfCommercialUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_commAndGov, self.commAndGovUse_Contractor, self.coefficient_COM))
        self.landscapeEconomicLoss_Contractor.append(self.economicLossFunction(self.contingencyWMOs.shortageByUseType.landscapeShortage_Contractor, self.contingencyWMOs.shortageByUseType.landscapeShortagePortionOfLandscapeUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_landscape, self.landscapeUse_Contractor, self.coefficient_LAND))

    def economicLossFunction(self, shortageByUseType, shortagePortionOfUse, lowerLossBoundary, elasticityOfDemand, volumeByUseType, coefficient):
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
        
        
        return economicLoss