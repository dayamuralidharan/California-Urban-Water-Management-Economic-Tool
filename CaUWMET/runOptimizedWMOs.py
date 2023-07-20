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
        
        print(longtermWMOVolumeLimit)