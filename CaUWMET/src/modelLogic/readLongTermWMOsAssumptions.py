import pandas as pd

class LongTermWMOsAssumptions:
    def __init__(self, inputDataLocations):
        # Input Assumptions
        longtermWMOSupplyUnitCostsInputData = inputDataLocations.longtermWMOSupplyUnitCostsInputData
        longtermWMOSupplyBaseCostsInputData = inputDataLocations.longtermWMOSupplyBaseCostsInputData

        longtermWMOSupplyVolumeData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Long-term WMOs Assumptions', skiprows = 7, nrows = 365, usecols = 'A:H')
        longtermWMOSupplyUnitCostsData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Long-term WMOs Assumptions', skiprows = 378, nrows = 733, usecols = 'A:H')
        longtermWMOSupplyBaseCostsData = pd.read_csv(longtermWMOSupplyBaseCostsInputData)


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

        self.longtermWMOSurfaceUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Surface Supply Incremental Cost ($/acre-foot)']
        self.longtermWMOGroundwaterUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Groundwater Supply Incremental Cost ($/acre-foot)']
        self.longtermWMODesalinationUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Desalination Supply Incremental Cost ($/acre-foot)']
        self.longtermWMORecycledUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Recycled Supply Incremental Cost ($/acre-foot)']
        self.longtermWMOPotableReuseUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Potable Reuse Supply Incremental Cost ($/acre-foot)']
        self.longtermWMOTransfersExchangesUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Long-term Contracts for Transfers and Exchanges Supply Incremental Cost ($/acre-foot)']
        self.longtermWMOOtherSupplyUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Other Supply Type Incremental Cost ($/acre-foot)']
        self.longtermWMOConservationUnitCost = longtermWMOSupplyUnitCostsData[longtermWMOSupplyUnitCostsData['Variable'] == 'Additional Conservation Incremental Cost ($/acre-foot)']

        self.longtermWMOSurfaceBaseCost = longtermWMOSupplyBaseCostsData[longtermWMOSupplyBaseCostsData['Variable'] == 'Surface Water Supply Cost ($)']
        self.longtermWMOGroundwaterBaseCost = longtermWMOSupplyBaseCostsData[longtermWMOSupplyBaseCostsData['Variable'] == 'Groundwater Supply Cost ($)']
        self.longtermWMODesalinationBaseCost = longtermWMOSupplyBaseCostsData[longtermWMOSupplyBaseCostsData['Variable'] == 'Desalination Supply Cost ($)']
        self.longtermWMORecycledBaseCost = longtermWMOSupplyBaseCostsData[longtermWMOSupplyBaseCostsData['Variable'] == 'Recycled Supply Cost ($)']
        self.longtermWMOPotableReuseBaseCost = longtermWMOSupplyBaseCostsData[longtermWMOSupplyBaseCostsData['Variable'] == 'Potable Reuse Supply Cost ($)']
        self.longtermWMOTransfersExchangesBaseCost = longtermWMOSupplyBaseCostsData[longtermWMOSupplyBaseCostsData['Variable'] == 'Transfers and Exchanges Supply Cost ($)']
        self.longtermWMOOtherSupplyBaseCost = longtermWMOSupplyBaseCostsData[longtermWMOSupplyBaseCostsData['Variable'] == 'Other Supply Cost ($)']
        self.longtermWMOConservationBaseCost = longtermWMOSupplyBaseCostsData[longtermWMOSupplyBaseCostsData['Variable'] == 'Additional Conservation Cost ($)']



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
        
        self.longtermWMOSurfaceBaseCost.set_index('Contractor', inplace=True)
        self.longtermWMOGroundwaterBaseCost.set_index('Contractor', inplace=True)
        self.longtermWMODesalinationBaseCost.set_index('Contractor', inplace=True)
        self.longtermWMORecycledBaseCost.set_index('Contractor', inplace=True)
        self.longtermWMOPotableReuseBaseCost.set_index('Contractor', inplace=True)
        self.longtermWMOTransfersExchangesBaseCost.set_index('Contractor', inplace=True)
        self.longtermWMOOtherSupplyBaseCost.set_index('Contractor', inplace=True)
        self.longtermWMOConservationBaseCost.set_index('Contractor', inplace=True)
        
