import numpy as np
import pandas as pd
from src.modelLogic.inputData import InputData
from src.modelLogic.contingentWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput
from src.modelLogic.contingentWMOs.shortageByUseType import ShortageByUseType
from src.modelLogic.contingentWMOs.contingencyWMOsHandler import ContingencyWMOs

class EconomicLossByUseType:
    def __init__(self, inputData: InputData):
        self.inputData = inputData
        
        self.singleFamilyEconomicLoss_Contractor = []
        self.multiFamilyEconomicLoss_Contractor = []
        self.industrialEconomicLoss_Contractor = []
        self.commAndGovEconomicLoss_Contractor = []
        self.landscapeEconomicLoss_Contractor = []
        self.totalEconomicLoss_Contractor = []
       

    def calculateTotalEconomicLoss(self, shortageByUseType: ShortageByUseType, input: ContingencyWMOsHandlerInput, contingencyWMOs: ContingencyWMOs, totalShortage_Contractor):
        self.shortageByUseType = shortageByUseType
        self.contingentWMOsinput = input
        self.contingencyWMOs = contingencyWMOs
        self.singleFamilyUse_Contractor = self.inputData.singleFamilyUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.multiFamilyUse_Contractor = self.inputData.multiFamilyUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.industrialUse_Contractor = self.inputData.industrialUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.commAndGovUse_Contractor = self.inputData.commAndGovUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        self.landscapeUse_Contractor = self.inputData.landscapeUsePortion * self.contingentWMOsinput.appliedDemand_Contractor[self.contingentWMOsinput.i]
        
        self.constantOfIntegration_SF = self.singleFamilyUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_singleFamily.loc[self.contingentWMOsinput.contractor]))
        self.constantOfIntegration_MF = self.multiFamilyUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_multiFamily.loc[self.contingentWMOsinput.contractor]))
        self.constantOfIntegration_IND = self.industrialUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_industrial.loc[self.contingentWMOsinput.contractor]))
        self.constantOfIntegration_COM = self.commAndGovUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_commAndGov.loc[self.contingentWMOsinput.contractor]))
        self.constantOfIntegration_LAND = self.landscapeUse_Contractor / (float(self.inputData.retailPrice.loc[self.contingentWMOsinput.contractor]) ** float(self.inputData.elasticityOfDemand_landscape.loc[self.contingentWMOsinput.contractor]))

        if totalShortage_Contractor[self.contingentWMOsinput.i] > 0:
            self.calculateEconomicLossByUseType()
            # print("singleFamilyEconomicLoss_Contractor: ", self.singleFamilyEconomicLoss_Contractor)
            # print("multiFamilyEconomicLoss_Contractor: ", self.multiFamilyEconomicLoss_Contractor)
            # print("industrialEconomicLoss_Contractor: ", self.industrialEconomicLoss_Contractor)
            # print("commAndGovEconomicLoss_Contractor: ", self.commAndGovEconomicLoss_Contractor)
            # print("landscapeEconomicLoss_Contractor: ", self.landscapeEconomicLoss_Contractor)

            self.totalEconomicLoss_Contractor.append( self.singleFamilyEconomicLoss_Contractor
                                                    + self.multiFamilyEconomicLoss_Contractor
                                                    + self.industrialEconomicLoss_Contractor
                                                    + self.commAndGovEconomicLoss_Contractor
                                                    + self.landscapeEconomicLoss_Contractor
                                                    )
        else:
            self.totalEconomicLoss_Contractor.append(0)


    def calculateEconomicLossByUseType(self):
        if self.singleFamilyUse_Contractor.loc[self.contingentWMOsinput.contractor] == 0:
            self.singleFamilyEconomicLoss_Contractor = 0
        else:
            self.singleFamilyEconomicLoss_Contractor = self.economicLossFunction(self.contingencyWMOs.shortageByUseType.singleFamilyShortage_Contractor, self.contingencyWMOs.shortageByUseType.singleFamilyShortagePortionOfSingleFamilyUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_singleFamily, self.singleFamilyUse_Contractor, self.constantOfIntegration_SF)
        
        if self.multiFamilyUse_Contractor.loc[self.contingentWMOsinput.contractor] == 0:
            self.multiFamilyEconomicLoss_Contractor = 0
        else:
            self.multiFamilyEconomicLoss_Contractor = self.economicLossFunction(self.contingencyWMOs.shortageByUseType.multiFamilyShortage_Contractor, self.contingencyWMOs.shortageByUseType.multiFamilyShortagePortionOfMultiFamilyUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_multiFamily, self.multiFamilyUse_Contractor, self.constantOfIntegration_MF)
        
        if self.industrialUse_Contractor.loc[self.contingentWMOsinput.contractor] == 0:
            self.industrialEconomicLoss_Contractor = 0
        else:
            self.industrialEconomicLoss_Contractor = self.economicLossFunction(self.contingencyWMOs.shortageByUseType.industrialShortage_Contractor, self.contingencyWMOs.shortageByUseType.industrialShortagePortionOfIndustrialUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_industrial, self.industrialUse_Contractor, self.constantOfIntegration_IND)
        
        if self.commAndGovUse_Contractor.loc[self.contingentWMOsinput.contractor] == 0:
            self.commAndGovEconomicLoss_Contractor = 0
        else:
            self.commAndGovEconomicLoss_Contractor = self.economicLossFunction(self.contingencyWMOs.shortageByUseType.commercialShortage_Contractor, self.contingencyWMOs.shortageByUseType.commercialShortagePortionOfCommercialUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_commAndGov, self.commAndGovUse_Contractor, self.constantOfIntegration_COM)
        
        if self.landscapeUse_Contractor.loc[self.contingentWMOsinput.contractor] == 0:
            self.landscapeEconomicLoss_Contractor = 0
        else:
            self.landscapeEconomicLoss_Contractor = self.economicLossFunction(self.contingencyWMOs.shortageByUseType.landscapeShortage_Contractor, self.contingencyWMOs.shortageByUseType.landscapeShortagePortionOfLandscapeUse_Contractor, self.inputData.lowerLossBoundary, self.inputData.elasticityOfDemand_landscape, self.landscapeUse_Contractor, self.constantOfIntegration_LAND)
    
    def economicLossFunction(self, shortageByUseType, shortagePortionOfUse, lowerLossBoundary, elasticityOfDemand, volumeByUseType, constantOfIntegration):
        if shortagePortionOfUse < lowerLossBoundary.loc[self.contingentWMOsinput.contractor]:

            a = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * volumeByUseType
            exponent1 = (np.log(volumeByUseType / constantOfIntegration)) / elasticityOfDemand.loc[self.contingentWMOsinput.contractor]
            b = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1
            c = (a * np.exp(exponent1)) / b
            d = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * (volumeByUseType *(1 - self.inputData.lowerLossBoundary.loc[self.contingentWMOsinput.contractor]))
            e = np.log((volumeByUseType * (1 - self.inputData.lowerLossBoundary.loc[self.contingentWMOsinput.contractor])) / constantOfIntegration)
            f = np.exp(e / elasticityOfDemand.loc[self.contingentWMOsinput.contractor]) / (elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1)
            
            economicLoss = c - (d * f)
            
        elif shortagePortionOfUse > self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor]:
            a = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * volumeByUseType
            exponent1 = (np.log(volumeByUseType / constantOfIntegration)) / elasticityOfDemand.loc[self.contingentWMOsinput.contractor]
            b = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1
            c = (a * np.exp(exponent1)) / b
            d = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * (volumeByUseType *(1 - self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor]))
            e = np.log((volumeByUseType * (1 - self.inputData.upperLossBoundary.loc[self.contingentWMOsinput.contractor])) / constantOfIntegration)
            f = np.exp(e / elasticityOfDemand.loc[self.contingentWMOsinput.contractor]) / (elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1)
            
            economicLoss = c - (d * f)

        else:
            a = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * volumeByUseType
            exponent1 = (np.log(volumeByUseType / constantOfIntegration)) / elasticityOfDemand.loc[self.contingentWMOsinput.contractor]
            b = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] + 1
            c = ((a * np.exp(exponent1)) / (b))
            d = elasticityOfDemand.loc[self.contingentWMOsinput.contractor] * (volumeByUseType - shortageByUseType)
            e = np.log((volumeByUseType - shortageByUseType)/constantOfIntegration)
            f = np.exp(e / elasticityOfDemand.loc[self.contingentWMOsinput.contractor])
            
            economicLoss = c - ((d * f) / b)
        
        return economicLoss.loc[self.contingentWMOsinput.contractor]