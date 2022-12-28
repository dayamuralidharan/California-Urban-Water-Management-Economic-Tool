import os
import pandas as pd
from src.modelLogic.modelUtilities import reclassifyYearType

class GlobalAssumptions:
    def __init__(self):

        # Input directories and filenames
        dirname = os.path.dirname(__file__)

        hydroYearTypeInput = "../inputData/hydrologyAssumptions.csv"
        contractorInformationInput = "../inputData/contractorInput_contractorInfo.csv"
        inputHydroYearTypeFile = os.path.join(dirname, hydroYearTypeInput)
        inputContractorInformation = os.path.join(dirname, contractorInformationInput)


        # Set up variables
        self.hydroYearType = pd.read_csv(inputHydroYearTypeFile)
        self.contractorInformation = pd.read_csv(inputContractorInformation)

        self.futureYear = '2025'  # TODO Temporary assumption, will be input from streamlit

        # Set up time series of hydrological year type based on Sacramento and SJ CDEC data, and reclassify to UWMP data classifications of Above Normal or Better, Single Dry, or Multi-Dry
        self.contractorDf = self.contractorInformation[['Contractor', 'Hydro. Region']]
        self.contractorsList = list(self.contractorDf['Contractor'].values)
        self.historicHydrologyYears = self.hydroYearType['Year'].values  # 1922 to 2003 or 2015 depending on whether it is Calsim II or 3 input for SWP CVP deliveries
        self.reclassYearType = {}
        for contractor in self.contractorsList:
            contractorYearType = self.hydroYearType[contractor].values
            self.reclassYearType[contractor] = reclassifyYearType(contractorYearType) # Reclassify hydrologic year type classifications to the categories used in the UWMP Normal or Better, Single-Dry and Multi-Dry Years
        self.UWMPhydrologicYearType = pd.DataFrame(self.reclassYearType)
