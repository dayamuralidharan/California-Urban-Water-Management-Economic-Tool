import pandas as pd
from src.modelLogic.modelUtilities import reclassifyYearType

class GlobalAssumptions:
    def __init__(self, inputDataLocations):

        hydroYearTypeInput = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Hydrology Assumptions', skiprows = 3)
        contractorInformationInput = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Contractor Assumptions', skiprows = 4)

        # Set up variables
        self.hydroYearType = hydroYearTypeInput
        self.contractorInformation = contractorInformationInput

        futureYearInput = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Simulation Settings', skiprows = 0, nrows = 1, usecols = 'B')
        self.futureYear = futureYearInput.columns
        self.futureYear = str(self.futureYear[0])

        # Set up time series of hydrological year type based on Sacramento and SJ CDEC data, and reclassify to UWMP data classifications of Normal or Better, Single Dry, or Multi-Dry
        self.contractorDf = self.contractorInformation[['Contractor', 'Study Region']]
        self.contractorsList = list(self.contractorDf['Contractor'].values)
        self.contractorsList = [value for value in self.contractorsList if pd.notna(value)] # Remove blank values from contractor list if any
        self.historicHydrologyYears = self.hydroYearType['Year'].values 


        self.reclassYearType = {}
        for contractor in self.contractorsList:
            contractorYearType = self.hydroYearType[contractor].values
            self.reclassYearType[contractor] = reclassifyYearType(contractorYearType) # Reclassify hydrologic year type classifications to the categories used in the UWMP Normal or Better, Single-Dry and Multi-Dry Years
        self.UWMPhydrologicYearType = pd.DataFrame(self.reclassYearType)

        self.hydroYearTypeForSelectedContractors = self.hydroYearType.set_index('Year')
        self.hydroYearTypeForSelectedContractors = self.hydroYearTypeForSelectedContractors[self.contractorsList]
        
