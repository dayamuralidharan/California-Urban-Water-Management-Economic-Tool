
import os
import pandas as pd

# Input directories and filenames
dirname = os.path.dirname(__file__)

# Read in data from CSV and create Pandas Dataframes
storageDataInput = "../inputData/systemOperationsInput_Storage.csv"
excessWaterSwitchDataInput = "../inputData/systemOperationsInput_ExcessWaterSwitch.csv"
storageHedgingStrategyInput = "../inputData/systemOperationsInput_StorageHedgingStrategy.csv"
deliveryCostInput = "../inputData/systemOperationsInput_DeliveryCosts.csv"

inputStorageDataFile = os.path.join(dirname, storageDataInput)
inputExcessWaterSwitchDataFile = os.path.join(dirname, excessWaterSwitchDataInput)
inputStorageHedgingStrategyFile = os.path.join(dirname, storageHedgingStrategyInput)
inputDeliveryCostFile = os.path.join(dirname, deliveryCostInput)

storageData = pd.read_csv(inputStorageDataFile)
excessWaterSwitchData = pd.read_csv(inputExcessWaterSwitchDataFile)
storageHedgingStrategyData = pd.read_csv(inputStorageHedgingStrategyFile)
deliveryCostData = pd.read_csv(inputDeliveryCostFile)

# Set 'Contractor' column as index
storageData.set_index('Contractor', inplace=True)
excessWaterSwitchData.set_index('Contractor', inplace=True)
storageHedgingStrategyData.set_index('Contractor', inplace=True)
deliveryCostData.set_index('Contractor', inplace=True)


groundwaterBankPutUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater bank put cost"]
groundwaterBankTakeUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater bank take cost"]
groundwaterPumpingCostSingleDryOrBetterYears = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater Pumping Cost (Base Supply, Single Dry or Better Year Types)"]
groundwaterPumpingCostMultiDryYears = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater Pumping Cost (Base Supply, Multi-Dry Year Types)"]
swpCVPDeliveryCost = deliveryCostData.loc[deliveryCostData['Variable'] == "SWP and/or CVP Delivery Cost"]
waterTreatmentCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Cost of M&I potable water treatment"]
distributionCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Cost of M&I Distribution"]
wastewaterTreatmentCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Wastewater Treatment Cost"]
wastewaterTreatmentFraction = deliveryCostData.loc[deliveryCostData['Variable'] == "Fraction of wastewater centrally treated (%)"]
energyEscalationCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Energy Escalation Cost (cents/kWh)"]
