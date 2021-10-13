import os
import pandas as pd
from modelUtilities import reclassifyYearType


# Input directories and filenames
dirname = os.path.dirname(__file__)

hydroYearTypeInput = "../inputData/hydrologyAssumptions.csv"
hydroRegionInput = "../inputData/contractorInformation.csv"
inputHydroYearTypeFile = os.path.join(dirname, hydroYearTypeInput)
inputHydroRegionFile = os.path.join(dirname, hydroRegionInput)


# Set up variables
hydroYearType = pd.read_csv(inputHydroYearTypeFile)
hydroRegion = pd.read_csv(inputHydroRegionFile)

futureYear = '2030'  # TODO Temporary assumption, will be input from streamlit

# Set up time series of hydrological year type based on Sacramento and SJ CDEC data, and reclassify to UWMP data classifications of Above Normal or Better, Single Dry, or Multi-Dry
hydroRegionDf = hydroRegion[['Contractor', 'Hydro. Region']]
historicHydrologyYears = hydroYearType['Year'].values  # 1922 to 2003 or 2015 depending on whether it is Calsim II or 3 input for SWP CVP deliveries
sacYearType = hydroYearType['Sacramento Valley'].values
sjYearType = hydroYearType['San Joaquin Valley'].values
reclassSacYearType = reclassifyYearType(sacYearType) # Reclassify CDEC's classifications to the UWMP demand classifications of Normal or Better, Single-Dry and Multi-Dry Years
reclassSjYearType = reclassifyYearType(sjYearType)

contractorsList = list(hydroRegionDf['Contractor'].values) ####TODO: contractors will need to be dynamically read in from streamlit instead of read in from hydro region dataframe