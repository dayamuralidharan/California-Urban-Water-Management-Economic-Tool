from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

import pandas as pd


class GetResults():
    def __init__(self, 
                 x, 
                 contractor):
        
        self.inputData = InputData(InputDataLocations())
        self.modelLogic = ModelLogic(self.inputData, StorageUtilities())
        self.modelLogic.contractor = contractor
        self.x = x
        
        
    def exportResults(self):
        self.modelLogic.execute(self.x, optimize=False)

        # Reconfigure dataframes that need to before exporting to Excel.
        longtermWMOVolumeLimit = pd.concat([self.inputData.longtermWMOConservationVolumeLimit[self.inputData.futureYear], 
                                          self.inputData.longtermWMOSurfaceVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMOGroundwaterVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMODesalinationVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMORecycledVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMOPotableReuseVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMOTransfersExchangesVolumeLimit[self.inputData.futureYear],
                                          self.inputData.longtermWMOOtherSupplyVolumeLimit[self.inputData.futureYear]],
                                          axis = 1)
        
        #TODO: Filter dataframe just for contractor list.
        longtermWMOVolumeLimit.columns = ['Conservation', 
                                       'Surface', 
                                       'Groundwater', 
                                       'Desalination',
                                       'Recycled', 
                                       'Potable Reuse', 
                                       'Transfers and Exchanges', 
                                      'Other']
        
        #TODO: reconfigure to handle all contractors in contractor loop and make row headers = option names
        self.x = pd.DataFrame(self.x)
        
        #Export Results to Excel
        with pd.ExcelWriter("output.xlsx") as writer:
            longtermWMOVolumeLimit.to_excel(writer, sheet_name = "Long-term WMOs Volume Limits", index_label = "Long-term WMOs Volume Limits")
            self.x.to_excel(writer, sheet_name = "Long-term WMOs Optimized Volume", index_label = "Long-term WMOs Optimized Volumes")
            
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

            self.modelLogic.inputData.hydroYearType.to_excel(writer, sheet_name = "HydroYearType", index_label = "Hydrologic Year Type")
            
        with pd.ExcelWriter("Results_QAQC.xlsx") as writer:
            self.modelLogic.outputHandler.totalAnnualCost.to_excel(writer, sheet_name = "Total Annual Cost", index_label = "Total Annual Cost")
            self.modelLogic.outputHandler.totalEconomicLoss.to_excel(writer, sheet_name = "Total Economic Loss", index_label = "Total Economic Loss")

            self.modelLogic.outputHandler.appliedDemands.to_excel(writer, sheet_name = "Applied Demands", index_label = "Applied Demands")
            self.modelLogic.outputHandler.demandsToBeMetByBankedGW.to_excel(writer, sheet_name = "GWBankDemands", index_label = "Demands to be met by GW bank")
            self.modelLogic.outputHandler.volumeGroundwaterBank.to_excel(writer, sheet_name = "GWBankVolume", index_label = "GW bank volume")
            self.modelLogic.outputHandler.takeGroundwater.to_excel(writer, sheet_name = "GWBankTake", index_label = "GW bank take volume")
            self.modelLogic.outputHandler.putGroundwater.to_excel(writer, sheet_name = "GWBankPut", index_label = "GW bank put volume")
            self.modelLogic.outputHandler.demandsToBeMetByContingentOptions.to_excel(writer, sheet_name = "ContingentDemands", index_label = "Contingent Options Demands")
            
            self.modelLogic.outputHandler.contingentConservationReductionVolume.to_excel(writer, sheet_name = "Contingent Conservation Volume", index_label = "Contingent Conservation Volume")
            self.modelLogic.outputHandler.waterMarketTransferDeliveries.to_excel(writer, sheet_name = "Market Transfers", index_label = "Water Market Transfer Deliveries")

            self.modelLogic.outputHandler.totalShortage.to_excel(writer, sheet_name = "TotalShortage", index_label = "Total Shortage")