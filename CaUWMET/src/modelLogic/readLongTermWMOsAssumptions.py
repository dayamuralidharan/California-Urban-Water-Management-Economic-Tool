import os
import pandas as pd
from src.modelLogic.readGlobalAssumptions import contractorsList, futureYear

# Input directories and filenames
dirname = os.path.dirname(__file__)

# Input Assumptions
longtermWMOSupplyVolumeInputData = "src/inputData/longtermWMOsInput_supplyVolume.csv"
longtermWMOSupplyIncrementInputData = "src/inputData/longtermWMOsInput_supplyIncrements.csv"


longtermWMOSupplyVolumeData = pd.read_csv(longtermWMOSupplyVolumeInputData)
longtermWMOSupplyIncrementData = pd.read_csv(longtermWMOSupplyIncrementInputData)


# Definition of Long-term WMO Supply Volume variables
longtermWMOSurfaceVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Surface Water Supply Volume (AFY)']
longtermWMOGroundwaterVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Groundwater Supply Volume (AFY)']
longtermWMODesalinationVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Desalination Supply Volume (AFY)']
longtermWMORecycledVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Recycled Supply Volume (AFY)']
longtermWMOPotableReuseVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Potable Reuse Supply Volume (AFY)']
longtermWMOTransfersExchangesVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Transfers and Exchanges Supply Volume (AFY)']
longtermWMOOtherSupplyVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Other Supply Volume (AFY)']
longtermWMOConservationVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Additional Conservation Volume (AFY)']

longtermWMOSupplyIncrementalVolume = longtermWMOSupplyIncrementData[longtermWMOSupplyIncrementData['Variable'] == 'Supply Incremental Size (AFY)']

longtermWMOSurfaceVolume.set_index('Contractor', inplace=True)
longtermWMOGroundwaterVolume.set_index('Contractor', inplace=True)
longtermWMODesalinationVolume.set_index('Contractor', inplace=True)
longtermWMORecycledVolume.set_index('Contractor', inplace=True)
longtermWMOPotableReuseVolume.set_index('Contractor', inplace=True)
longtermWMOTransfersExchangesVolume.set_index('Contractor', inplace=True)
longtermWMOConservationVolume.set_index('Contractor', inplace=True)
longtermWMOSupplyIncrementalVolume.set_index('Contractor', inplace=True)