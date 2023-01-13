import math
from src.modelLogic.inputData import InputData
from src.modelLogic.contingentWMOs.contingencyWMOsHandlerInput import ContingencyWMOsHandlerInput
from src.modelLogic.contingentWMOs.shortageByUseType import ShortageByUseType


class ContingencyWMOs:
    def __init__(self, inputData: InputData):
        self.inputData = inputData
        self.shortageByUseType = ShortageByUseType(self.inputData)
        
        # self.contingentConservationUseReductionVolume_Contractor = []
        # self.waterMarketTransferDeliveries_Contractor = []
        # self.totalShortage_Contractor = []
        # self.demandsToBeMetByWaterMarketTransfers_Contractor = []
        
    def implementContingencyWMOsIfNeeded(self, input: ContingencyWMOsHandlerInput, contingentConservationUseReductionVolume_Contractor, waterMarketTransferDeliveries_Contractor, totalShortage_Contractor, demandsToBeMetByWaterMarketTransfers_Contractor):
        self.contingentWMOsinput = input
        self.contingentConservationUseReductionVolume_Contractor = contingentConservationUseReductionVolume_Contractor
        self.waterMarketTransferDeliveries_Contractor = waterMarketTransferDeliveries_Contractor
        self.totalShortage_Contractor = totalShortage_Contractor
        self.demandsToBeMetByWaterMarketTransfers_Contractor = demandsToBeMetByWaterMarketTransfers_Contractor
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
            