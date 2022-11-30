
import os
import pandas as pd

# Input directories and filenames
dirname = os.path.dirname(__file__)

# Read in data from CSV and create Pandas Dataframes
storageDataInput = "../inputData/systemOperationsInput_Storage.csv"
excessWaterSwitchDataInput = "../inputData/systemOperationsInput_ExcessWaterSwitch.csv"
storageHedgingStrategyInput = "../inputData/systemOperationsInput_StorageHedgingStrategy.csv"

inputStorageDataFile = os.path.join(dirname, storageDataInput)
inputExcessWaterSwitchDataFile = os.path.join(dirname, excessWaterSwitchDataInput)
inputStorageHedgingStrategyFile = os.path.join(dirname, storageHedgingStrategyInput)

storageData = pd.read_csv(inputStorageDataFile)
excessWaterSwitchData = pd.read_csv(inputExcessWaterSwitchDataFile)
storageHedgingStrategyData = pd.read_csv(inputStorageHedgingStrategyFile)

# Set 'Contractor' column as index
storageData.set_index('Contractor', inplace=True)
excessWaterSwitchData.set_index('Contractor', inplace=True)
storageHedgingStrategyData.set_index('Contractor', inplace=True)
