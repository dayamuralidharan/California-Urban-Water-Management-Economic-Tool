from src.modelLogic.inputData import InputData
from src.modelLogic.contingentWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput

class ShortageByUseType:
    def __init__(self, inputData: InputData):
        self.inputData = inputData
    
    def calculateShortageByUseType(self, input: ContingencyWMOsHandlerInput, totalShortage_Contractor):
        # Calculate demand hardening adjustment factor and adjusted shortage
        self.input = input
        self.totalShortage_Contractor = totalShortage_Contractor
        
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
        self.commercialShortagePortionOfCommercialUse_Contractor = self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor * self.inputData.cutRatio_commercial.loc[self.input.contractor]
        self.landscapeShortagePortionOfLandscapeUse_Contractor = self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor * self.inputData.cutRatio_landscape.loc[self.input.contractor]
        
        # Calculate shortage by type
        self.singleFamilyShortage_Contractor = self.singleFamilyShortagePortionOfSingleFamilyUse_Contractor * self.adjustedShortage_Contractor
        self.multiFamilyShortage_Contractor = self.multiFamilyShortagePortionOfMultiFamilyUse_Contractor * self.adjustedShortage_Contractor
        self.industrialShortage_Contractor = self.industrialShortagePortionOfIndustrialUse_Contractor * self.adjustedShortage_Contractor
        self.commercialShortage_Contractor = self.commercialShortagePortionOfCommercialUse_Contractor * self.adjustedShortage_Contractor
        self.landscapeShortage_Contractor = self.landscapeShortagePortionOfLandscapeUse_Contractor * self.adjustedShortage_Contractor
        #TODO add test to confirm total shortage of each use type = adjusted shortage