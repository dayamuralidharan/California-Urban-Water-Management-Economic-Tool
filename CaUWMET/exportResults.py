from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

import pandas as pd


class RunOptimizedWMOs():
    def __init__(self, 
                 x, 
                 contractor):
        
        self.inputData = InputData(InputDataLocations())
        self.modelLogic = ModelLogic(self.inputData, StorageUtilities())
        self.modelLogic.contractor = contractor
        self.x = x
        
        
    def runOptimizedWMOs(self):
        self.modelLogic.execute(self.x, optimize=False)

        # Configure long-term WMO available supply dataframe for output
        longtermWMOVolumeLimit = pd.concat([self.inputData.longtermWMOConservationVolumeLimit[self.inputData.futureYear], 
                                          self.inputData.longtermWMOSurfaceVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMOGroundwaterVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMODesalinationVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMORecycledVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMOPotableReuseVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMOTransfersExchangesVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMOOtherSupplyVolumeLimit[self.inputData.futureYear]],
                                          axis = 1)
        
        longtermWMOVolumeLimit.columns = ['Conservation', 
                                       'Surface', 
                                       'Groundwater', 
                                       'Desalination',
                                       'Recycled', 
                                       'Potable Reuse', 
                                       'Transfers and Exchanges', 
                                      'Other']
        
        #Export to Excel
        with pd.ExcelWriter("output.xlsx") as writer:
            self.modelLogic.outputHandler.totalAnnualCost.to_excel(writer, sheet_name = "Total Annual Cost", index_label = "Total Annual Cost")
            self.modelLogic.outputHandler.totalEconomicLoss.to_excel(writer, sheet_name = "Total Economic Loss", index_label = "Total Economic Loss")
            
            self.modelLogic.outputHandler.surfaceLongTermWMOCost.to_excel(writer, sheet_name = "LT WMO Cost SW", index_label = "Long-term WMO Cost: Surface")
            self.modelLogic.outputHandler.groundwaterLongTermWMOCost.to_excel(writer, sheet_name = "LT WMO Cost GW", index_label = "Long-term WMO Cost: Groundwater")
            self.modelLogic.outputHandler.desalinationLongTermWMOCost.to_excel(writer, sheet_name = "LT WMO Cost Desal", index_label = "Long-term WMO Cost: Desalination")
            self.modelLogic.outputHandler.recycledLongTermWMOCost.to_excel(writer, sheet_name = "LT WMO Cost Recyc", index_label = "Long-term WMO Cost: Recycled")
            self.modelLogic.outputHandler.potableReuseLongTermWMOCost.to_excel(writer, sheet_name = "LT WMO Cost PR", index_label = "Long-term WMO Cost: Potable Reuse")
            self.modelLogic.outputHandler.transfersAndExchangesLongTermWMOCost.to_excel(writer, sheet_name = "LT WMO Cost TransExch", index_label = "Long-term WMO Cost: Transfers and Exchanges")
            self.modelLogic.outputHandler.otherSupplyLongTermWMOCost.to_excel(writer, sheet_name = "LT WMO Cost Other", index_label = "Long-term WMO Cost: Other")
            self.modelLogic.outputHandler.conservationLongTermWMOCost.to_excel(writer, sheet_name = "LT WMO Cost Conserv", index_label = "Long-term WMO Cost: Conservation")

            self.modelLogic.outputHandler.swpCVPDeliveryCost.to_excel(writer, sheet_name = "SWP CVP Cost", index_label = "SWP/CVP operations cost")

            self.modelLogic.outputHandler.totalReliabilityMgmtCost.to_excel(writer, sheet_name = "Reliability Mgmt Cost", index_label = "Reliability Management costs")

            self.modelLogic.outputHandler.waterMarketTransferDeliveries.to_excel(writer, sheet_name = "WM Transfers", index_label = "Water Market Transfer Deliveries")
            self.modelLogic.outputHandler.waterMarketTransferCost.to_excel(writer, sheet_name = "WM Transfer Costs", index_label = "Water Market Transfer Costs")
        print(self.x)