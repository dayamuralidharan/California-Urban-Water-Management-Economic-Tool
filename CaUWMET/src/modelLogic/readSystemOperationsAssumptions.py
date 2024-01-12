import pandas as pd
from src.modelLogic.modelUtilities import lookupCorrespondingValue

class SystemOperationsAssumptions:
    def __init__(self, globalAssumptions, inputDataLocations):

        # Read in data from CSV and create Pandas Dataframes
        storageDataInput = inputDataLocations.storageDataInput
        storageHedgingStrategyInput = inputDataLocations.storageHedgingStrategyInput
        deliveryCostInput = inputDataLocations.deliveryCostInput

        self.storageData = pd.read_csv(storageDataInput)
        self.excessWaterSwitchData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 6, nrows = 44, usecols = 'A:E')
        self.storageHedgingStrategyData = pd.read_csv(storageHedgingStrategyInput)
        deliveryCostData = pd.read_csv(deliveryCostInput)

        # Set 'Contractor' column as index
        self.storageData.set_index('Contractor', inplace=True)
        self.excessWaterSwitchData.set_index('Contractor', inplace=True)
        self.storageHedgingStrategyData.set_index('Contractor', inplace=True)
        deliveryCostData.set_index('Contractor', inplace=True)


        self.groundwaterBankPutUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater bank put cost"]
        self.groundwaterBankTakeUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater bank take cost"]
        groundwaterPumpingUnitCostSingleDryOrBetterYears = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater Pumping Cost (Base Supply, Single Dry or Better Year Types)"]
        groundwaterPumpingUnitCostMultiDryYears = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater Pumping Cost (Base Supply, Multi-Dry Year Types)"]
        self.swpCVPDeliveryUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "SWP and/or CVP Delivery Cost"]
        self.waterTreatmentUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Cost of M&I potable water treatment"]
        self.distributionUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Cost of M&I Distribution"]
        self.wastewaterTreatmentUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Wastewater Treatment Cost"]
        self.wastewaterTreatmentFraction = deliveryCostData.loc[deliveryCostData['Variable'] == "Fraction of wastewater centrally treated (%)"]
        self.energyEscalationCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Energy Escalation Cost (cents/kWh)"]

        # Set up groundwater pumping cost time series based on hydrologic year type.
        #TODO: This can probably be abstracted to a function, duplicated in other "read..." files
        self.groundwaterPumpingUnitCost = {'Year': globalAssumptions.historicHydrologyYears}

        for contractor in globalAssumptions.contractorsList:
            contractorRegion = lookupCorrespondingValue(globalAssumptions.contractorDf, contractor, colA='Contractor', colB='Study Region')
            contractorYearType = globalAssumptions.UWMPhydrologicYearType[contractor]
            contractorGroundwaterPumpingUnitCost = []

            for i in range(len(globalAssumptions.historicHydrologyYears)):
                if contractorYearType[i] == "NB": #Normal or Better
                    contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostSingleDryOrBetterYears.loc[contractor][globalAssumptions.futureYear])
                elif contractorYearType[i] == "SD": #Single Dry
                        contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostSingleDryOrBetterYears.loc[contractor][globalAssumptions.futureYear])
                elif contractorYearType[i] == "MD": #Multi-Dry
                        contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostMultiDryYears.loc[contractor][globalAssumptions.futureYear])
            self.groundwaterPumpingUnitCost[contractor] = contractorGroundwaterPumpingUnitCost

        self.groundwaterPumpingUnitCost = pd.DataFrame(self.groundwaterPumpingUnitCost)
