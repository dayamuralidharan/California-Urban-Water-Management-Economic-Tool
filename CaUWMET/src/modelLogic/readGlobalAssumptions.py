import pandas as pd
from src.modelLogic.modelUtilities import reclassifyYearType

class GlobalAssumptions:
    def __init__(self, inputDataLocations):

        hydroYearTypeInput = inputDataLocations.hydroYearTypeInput
        contractorInformationInput = inputDataLocations.contractorInformationInput

        # Set up variables
        self.hydroYearType = pd.read_csv(hydroYearTypeInput)
        self.contractorInformation = pd.read_csv(contractorInformationInput)

        futureYearInput = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Simulation Settings', skiprows = 0, nrows = 1, usecols = 'B')
        self.futureYear = futureYearInput.columns
        self.futureYear = str(self.futureYear[0])

        # Set up time series of hydrological year type based on Sacramento and SJ CDEC data, and reclassify to UWMP data classifications of Normal or Better, Single Dry, or Multi-Dry
        self.contractorDf = self.contractorInformation[['Contractor', 'Hydro. Region']]
        self.contractorsList = list(self.contractorDf['Contractor'].values)
        self.historicHydrologyYears = self.hydroYearType['Year'].values 


        self.reclassYearType = {}
        for contractor in self.contractorsList:
            contractorYearType = self.hydroYearType[contractor].values
            self.reclassYearType[contractor] = reclassifyYearType(contractorYearType) # Reclassify hydrologic year type classifications to the categories used in the UWMP Normal or Better, Single-Dry and Multi-Dry Years
        self.UWMPhydrologicYearType = pd.DataFrame(self.reclassYearType)

        self.hydroYearTypeForSelectedContractors = self.hydroYearType.set_index('Year')
        self.hydroYearTypeForSelectedContractors = self.hydroYearTypeForSelectedContractors[self.contractorsList]
        
