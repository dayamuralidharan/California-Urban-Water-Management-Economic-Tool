
import os
import pandas as pd
from src.modelLogic.modelUtilities import lookupCorrespondingValue
from src.modelLogic.readGlobalAssumptions import contractorsList, futureYear, contractorDf, UWMPhydrologicYearType, historicHydrologyYears

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
groundwaterPumpingUnitCostSingleDryOrBetterYears = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater Pumping Cost (Base Supply, Single Dry or Better Year Types)"]
groundwaterPumpingUnitCostMultiDryYears = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater Pumping Cost (Base Supply, Multi-Dry Year Types)"]
swpCVPDeliveryUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "SWP and/or CVP Delivery Cost"]
waterTreatmentUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Cost of M&I potable water treatment"]
distributionUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Cost of M&I Distribution"]
wastewaterTreatmentUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Wastewater Treatment Cost"]
wastewaterTreatmentFraction = deliveryCostData.loc[deliveryCostData['Variable'] == "Fraction of wastewater centrally treated (%)"]
energyEscalationCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Energy Escalation Cost (cents/kWh)"]

# Set up groundwater pumping cost time series based on hydrologic year type.
#TODO: This can probably be abstracted to a function, duplicated in other "read..." files
groundwaterPumpingUnitCost = {'Year': historicHydrologyYears}

for contractor in contractorsList:
    contractorRegion = lookupCorrespondingValue(contractorDf, contractor, colA='Contractor', colB='Hydro. Region')
    contractorYearType = UWMPhydrologicYearType[contractor]
    contractorGroundwaterPumpingUnitCost = []

    for i in range(len(historicHydrologyYears)):
        if contractorYearType[i] == "NB": #Normal or Better
            contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostSingleDryOrBetterYears.loc[contractor][futureYear])
        elif contractorYearType[i] == "SD": #Single Dry
                contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostSingleDryOrBetterYears.loc[contractor][futureYear])
        elif contractorYearType[i] == "MD": #Multi-Dry
                contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostMultiDryYears.loc[contractor][futureYear])
    groundwaterPumpingUnitCost[contractor] = contractorGroundwaterPumpingUnitCost

groundwaterPumpingUnitCost = pd.DataFrame(groundwaterPumpingUnitCost)
