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


        longtermWMOVolumeLimit = pd.DataFrame({'Contractor': self.inputData.contractorsList})
                                #   'Conservation': self.inputData.longtermWMOConservationVolumeLimit[self.inputData.futureYear].to_dict(),
                                #   'Surface': self.inputData.longtermWMOSurfaceVolumeLimit[self.inputData.futureYear],
                                #   'Groundwater': self.inputData.longtermWMOGroundwaterVolumeLimit[self.inputData.futureYear],
                                #   'Desalination': self.inputData.longtermWMODesalinationVolumeLimit[self.inputData.futureYear],
                                #   'Recycled': self.inputData.longtermWMORecycledVolumeLimit[self.inputData.futureYear],
                                #   'Potable Reuse': self.inputData.longtermWMORecycledVolumeLimit[self.inputData.futureYear],
                                #   'Transfers and Exchanges': self.inputData.longtermWMOTransfersExchangesVolumeLimit[self.inputData.futureYear],
                                #   'Other': self.inputData.longtermWMOOtherSupplyVolumeLimit[self.inputData.futureYear]
        longtermWMOVolumeLimit.set_index('Contractor')
        longtermWMOVolumeLimitDataFrames = [longtermWMOVolumeLimit, self.inputData.longtermWMOConservationVolumeLimit[self.inputData.futureYear], ]
        
        longtermWMOVolumeLimit2 =pd.concat(longtermWMOVolumeLimitDataFrames)
        
        print(longtermWMOVolumeLimit2)