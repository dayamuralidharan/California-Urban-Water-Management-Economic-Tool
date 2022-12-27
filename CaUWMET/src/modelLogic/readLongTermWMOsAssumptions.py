import os
import pandas as pd

class LongTermWMOsAssumptions:
    def __init__(self):
        # Input directories and filenames
        dirname = os.path.dirname(__file__)

        # Input Assumptions
        longtermWMOSupplyVolumeInputData = "src/inputData/longtermWMOsInput_supplyVolume.csv"
        longtermWMOSupplyUnitCostsInputData = "src/inputData/longtermWMOsInput_supplyCosts.csv"
        #longtermWMOSupplyIncrementInputData = "src/inputData/longtermWMOsInput_supplyIncrements.csv"


        longtermWMOSupplyVolumeData = pd.read_csv(longtermWMOSupplyVolumeInputData)
        longtermWMOSupplyUnitCostsData = pd.read_csv(longtermWMOSupplyUnitCostsInputData)


        # Definition of Long-term WMO Supply Volume variables
        self.longtermWMOSurfaceVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Surface Water Supply Volume (AFY)']
        self.longtermWMOGroundwaterVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Groundwater Supply Volume (AFY)']
        self.longtermWMODesalinationVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Desalination Supply Volume (AFY)']
        self.longtermWMORecycledVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Recycled Supply Volume (AFY)']
        self.longtermWMOPotableReuseVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Potable Reuse Supply Volume (AFY)']
        self.longtermWMOTransfersExchangesVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Transfers and Exchanges Supply Volume (AFY)']
        self.longtermWMOOtherSupplyVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Other Supply Volume (AFY)']
        self.longtermWMOConservationVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Additional Conservation Volume (AFY)']

        self.longtermWMOSurfaceUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Surface Water Supply Cost ($/AF)']
        self.longtermWMOGroundwaterUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Groundwater Supply Cost ($/AF)']
        self.longtermWMODesalinationUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Desalination Supply Cost ($/AF)']
        self.longtermWMORecycledUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Recycled Supply Cost ($/AF)']
        self.longtermWMOPotableReuseUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Potable Reuse Supply Cost ($/AF)']
        self.longtermWMOTransfersExchangesUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Transfers and Exchanges Supply Cost ($/AF)']
        self.longtermWMOOtherSupplyUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Other Supply Cost ($/AF)']
        self.longtermWMOConservationUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Additional Conservation Cost ($/AF)']

        self.longtermWMOSurfaceVolumeLimit.set_index('Contractor', inplace=True)
        self.longtermWMOGroundwaterVolumeLimit.set_index('Contractor', inplace=True)
        self.longtermWMODesalinationVolumeLimit.set_index('Contractor', inplace=True)
        self.longtermWMORecycledVolumeLimit.set_index('Contractor', inplace=True)
        self.longtermWMOPotableReuseVolumeLimit.set_index('Contractor', inplace=True)
        self.longtermWMOTransfersExchangesVolumeLimit.set_index('Contractor', inplace=True)
        self.longtermWMOOtherSupplyVolumeLimit.set_index('Contractor', inplace=True)
        self.longtermWMOConservationVolumeLimit.set_index('Contractor', inplace=True)

        self.longtermWMOSurfaceUnitCost.set_index('Contractor', inplace=True)
        self.longtermWMOGroundwaterUnitCost.set_index('Contractor', inplace=True)
        self.longtermWMODesalinationUnitCost.set_index('Contractor', inplace=True)
        self.longtermWMORecycledUnitCost.set_index('Contractor', inplace=True)
        self.longtermWMOPotableReuseUnitCost.set_index('Contractor', inplace=True)
        self.longtermWMOTransfersExchangesUnitCost.set_index('Contractor', inplace=True)
        self.longtermWMOOtherSupplyUnitCost.set_index('Contractor', inplace=True)
        self.longtermWMOConservationUnitCost.set_index('Contractor', inplace=True)
