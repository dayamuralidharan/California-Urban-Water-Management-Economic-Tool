import pandas as pd

class LongTermWMOsAssumptions:
    def __init__(self, inputDataLocations):
        # Input Assumptions
        longtermWMOSupplyVolumeData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Long-term WMOs Assumptions', skiprows = 7, nrows = 365, usecols = 'A:H')
        longtermWMOSupplyCostsData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Long-term WMOs Assumptions', skiprows = 378, nrows = 733, usecols = 'A:H')
        longtermWMOSupplyCostsData.set_index('Contractor', inplace=True)

        # Definition of Long-term WMO Supply Volume variables
        #TODO Confirm these listed here are being used in Marks code? If not...delete or use these instead of what he is using
        self.longtermWMOSurfaceVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Surface Water Supply Volume (acre-feet/year)']
        self.longtermWMOGroundwaterVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Groundwater Supply Volume (acre-feet/year)']
        self.longtermWMODesalinationVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Desalination Supply Volume (acre-feet/year)']
        self.longtermWMORecycledVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Recycled Supply Volume (acre-feet/year)']
        self.longtermWMOPotableReuseVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Potable Reuse Supply Volume (acre-feet/year)']
        self.longtermWMOTransfersExchangesVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Transfers and Exchanges Supply Volume (acre-feet/year)']
        self.longtermWMOOtherSupplyVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Other Supply Volume (acre-feet/year)']
        self.longtermWMOConservationVolumeLimit = longtermWMOSupplyVolumeData[longtermWMOSupplyVolumeData['Variable'] == 'Additional Conservation Volume (acre-feet/year)']

        self.longtermWMOSurfaceUnitCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Surface Supply Incremental Cost ($/acre-foot)']
        self.longtermWMOGroundwaterUnitCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Groundwater Supply Incremental Cost ($/acre-foot)']
        self.longtermWMODesalinationUnitCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Desalination Supply Incremental Cost ($/acre-foot)']
        self.longtermWMORecycledUnitCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Recycled Supply Incremental Cost ($/acre-foot)']
        self.longtermWMOPotableReuseUnitCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Potable Reuse Supply Incremental Cost ($/acre-foot)']
        self.longtermWMOTransfersExchangesUnitCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Long-term Contracts for Transfers and Exchanges Supply Incremental Cost ($/acre-foot)']
        self.longtermWMOOtherSupplyUnitCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Other Supply Type Incremental Cost ($/acre-foot)']
        self.longtermWMOConservationUnitCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Additional Conservation Incremental Cost ($/acre-foot)']

        self.longtermWMOSurfaceBaseCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Surface Supply Base Cost ($/acre-foot)']
        self.longtermWMOGroundwaterBaseCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Groundwater Supply Base Cost ($/acre-foot)']
        self.longtermWMODesalinationBaseCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Desalination Supply Base Cost ($/acre-foot)']
        self.longtermWMORecycledBaseCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Recycled Supply Base Cost ($/acre-foot)']
        self.longtermWMOPotableReuseBaseCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Potable Reuse Supply Base Cost ($/acre-foot)']
        self.longtermWMOTransfersExchangesBaseCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Long-term Contracts for Transfers and Exchanges Supply Base Cost ($/acre-foot)']
        self.longtermWMOOtherSupplyBaseCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Other Supply Type Base Cost ($/acre-foot)']
        self.longtermWMOConservationBaseCost = longtermWMOSupplyCostsData[longtermWMOSupplyCostsData['Variable'] == 'Additional Conservation Base Cost ($/acre-foot)']
        
