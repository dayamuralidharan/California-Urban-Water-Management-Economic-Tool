import pandas as pd
from src.modelLogic.modelUtilities import lookupCorrespondingValue

class SystemOperationsAssumptions:
    def __init__(self, globalAssumptions, inputDataLocations):

        self.excessWaterSwitchData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 6, nrows = 44, usecols = 'A:E')
        self.storageData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 55, nrows = 461, usecols = 'A:I')
        self.storageHedgingStrategyData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 522, nrows = 181, usecols = 'A:F')
        storageOperationsCosts = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 709, nrows = 90, usecols = 'A:H')
        deliveryCostData = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 804, nrows = 319, usecols = 'A:I')

    
        # Set 'Contractor' column as index
        self.storageData.set_index('Contractor', inplace=True)
        self.excessWaterSwitchData.set_index('Contractor', inplace=True)
        self.storageHedgingStrategyData.set_index('Contractor', inplace=True)
        storageOperationsCosts.set_index('Contractor', inplace=True)
        deliveryCostData.set_index('Contractor', inplace=True)


        self.groundwaterBankPutUnitCost = storageOperationsCosts.loc[storageOperationsCosts['Variable'] == "Groundwater bank put cost ($/acre-feet)"]
        self.groundwaterBankTakeUnitCost = storageOperationsCosts.loc[storageOperationsCosts['Variable'] == "Groundwater bank take cost ($/acre-feet)"]
        groundwaterPumpingUnitCostSingleDryOrBetterYears = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater Pumping (Single Dry or Better Year Types, $/acre-foot)"]
        groundwaterPumpingUnitCostMultiDryYears = deliveryCostData.loc[deliveryCostData['Variable'] == "Groundwater Pumping (Multi-Dry Year Types, $/acre-foot)"]
        self.swpCVPDeliveryUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "SWP or CVP Delivery Costs ($/acre-foot)"]
        self.waterTreatmentUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Cost of M&I potable water treatment ($/acre-foot)"]
        self.distributionUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Cost of M&I Distribution ($/acre-foot)"]
        self.wastewaterTreatmentUnitCost = deliveryCostData.loc[deliveryCostData['Variable'] == "Wastewater Treatment Cost ($/acre-foot)"]
        self.wastewaterTreatmentFraction = deliveryCostData.loc[deliveryCostData['Variable'] == "Fraction of wastewater treated (%)"]

        # Set up groundwater pumping cost time series based on hydrologic year type.
        #TODO: This can probably be abstracted to a function, duplicated in other "read..." files
        self.groundwaterPumpingUnitCost = {'Year': globalAssumptions.historicHydrologyYears}

        for contractor in globalAssumptions.contractorsList:
            contractorYearType = globalAssumptions.UWMPhydrologicYearType[contractor]
            contractorGroundwaterPumpingUnitCost = []

            for i in range(len(globalAssumptions.historicHydrologyYears)):
                if contractorYearType[i] == "NB": #Normal or Better
                    contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostSingleDryOrBetterYears.loc[contractor][int(globalAssumptions.futureYear)])
                elif contractorYearType[i] == "SD": #Single Dry
                        contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostSingleDryOrBetterYears.loc[contractor][int(globalAssumptions.futureYear)])
                elif contractorYearType[i] == "MD": #Multi-Dry
                        contractorGroundwaterPumpingUnitCost.append(groundwaterPumpingUnitCostMultiDryYears.loc[contractor][int(globalAssumptions.futureYear)])
            self.groundwaterPumpingUnitCost[contractor] = contractorGroundwaterPumpingUnitCost

        self.groundwaterPumpingUnitCost = pd.DataFrame(self.groundwaterPumpingUnitCost)
