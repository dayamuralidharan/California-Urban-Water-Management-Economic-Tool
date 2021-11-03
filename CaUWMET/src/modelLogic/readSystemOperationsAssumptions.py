
import os
import pandas as pd
from readGlobalAssumptions import contractorsList, futureYear
from modelUtilities import lookupCorrespondingValue

#TODO: Set up supplies that vary by hydrological year type

# Input directories and filenames
dirname = os.path.dirname(__file__)

# SUPPLIES Inputs
carryoverStorageDataInput = "../inputData/systemOperationsInput_CarryoverStorage.csv"
excessWaterSwitchDataInput = "../inputData/systemOperationsInput_ExcessWaterSwitch.csv"

inputCarryoverStorageDataFile = os.path.join(dirname, carryoverStorageDataInput)
inputExcessWaterSwitchDataFile = os.path.join(dirname, excessWaterSwitchDataInput)

# Read in data from CSV and create Pandas Dataframes
carryoverStorageData = pd.read_csv(inputCarryoverStorageDataFile)
excessWaterSwitchData = pd.read_csv(inputExcessWaterSwitchDataFile)

# Set 'Contractor' column as index
carryoverStorageData.set_index('Contractor', inplace=True)
excessWaterSwitchData.set_index('Contractor', inplace=True)
