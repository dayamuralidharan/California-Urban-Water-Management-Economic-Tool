import os
import pandas as pd

# Input directories and filenames
dirname = os.path.dirname(__file__)

# Input Assumptions
longtermWMOSupplyVolumeInputData = "src/inputData/longtermWMOsInput_supplyVolume.csv"
longtermWMOSupplyUnitCostsInputData = "src/inputData/longtermWMOsInput_supplyCosts.csv"
#longtermWMOSupplyIncrementInputData = "src/inputData/longtermWMOsInput_supplyIncrements.csv"


longtermWMOSupplyVolumeData = pd.read_csv(longtermWMOSupplyVolumeInputData)
longtermWMOSupplyUnitCostsData = pd.read_csv(longtermWMOSupplyUnitCostsInputData)
#longtermWMOSupplyIncrementData = pd.read_csv(longtermWMOSupplyIncrementInputData)


# Definition of Long-term WMO Supply Volume variables
longtermWMOSurfaceVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Surface Water Supply Volume (AFY)']
longtermWMOGroundwaterVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Groundwater Supply Volume (AFY)']
longtermWMODesalinationVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Desalination Supply Volume (AFY)']
longtermWMORecycledVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Recycled Supply Volume (AFY)']
longtermWMOPotableReuseVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Potable Reuse Supply Volume (AFY)']
longtermWMOTransfersExchangesVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Transfers and Exchanges Supply Volume (AFY)']
longtermWMOOtherSupplyVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Other Supply Volume (AFY)']
longtermWMOConservationVolume = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Additional Conservation Volume (AFY)']

longtermWMOSurfaceUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Surface Water Supply Cost ($/AF)']
longtermWMOGroundwaterUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Groundwater Supply Cost ($/AF)']
longtermWMODesalinationUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Desalination Supply Cost ($/AF)']
longtermWMORecycledUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Recycled Supply Cost ($/AF)']
longtermWMOPotableReuseUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Potable Reuse Supply Cost ($/AF)']
longtermWMOTransfersExchangesUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Transfers and Exchanges Supply Cost ($/AF)']
longtermWMOOtherSupplyUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Other Supply Cost ($/AF)']
longtermWMOConservationUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Additional Conservation Cost ($/AF)']

#longtermWMOSupplyIncrementalVolume = longtermWMOSupplyIncrementData[longtermWMOSupplyIncrementData['Variable'] == 'Supply Incremental Size (AFY)']

longtermWMOSurfaceVolume.set_index('Contractor', inplace=True)
longtermWMOGroundwaterVolume.set_index('Contractor', inplace=True)
longtermWMODesalinationVolume.set_index('Contractor', inplace=True)
longtermWMORecycledVolume.set_index('Contractor', inplace=True)
longtermWMOPotableReuseVolume.set_index('Contractor', inplace=True)
longtermWMOTransfersExchangesVolume.set_index('Contractor', inplace=True)
longtermWMOConservationVolume.set_index('Contractor', inplace=True)

longtermWMOSurfaceUnitCost.set_index('Contractor', inplace=True)
longtermWMOGroundwaterUnitCost.set_index('Contractor', inplace=True)
longtermWMODesalinationUnitCost.set_index('Contractor', inplace=True)
longtermWMORecycledUnitCost.set_index('Contractor', inplace=True)
longtermWMOPotableReuseUnitCost.set_index('Contractor', inplace=True)
longtermWMOTransfersExchangesUnitCost.set_index('Contractor', inplace=True)
longtermWMOOtherSupplyUnitCost.set_index('Contractor', inplace=True)
longtermWMOConservationUnitCost.set_index('Contractor', inplace=True)

#longtermWMOSupplyIncrementalVolume.set_index('Contractor', inplace=True)