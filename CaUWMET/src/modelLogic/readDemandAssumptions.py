import os
import pandas as pd
from src.modelLogic.modelUtilities import lookupCorrespondingValue

class DemandAssumptions:
    def __init__(self, contractorsList, futureYear, contractorDf, reclassYearType, historicHydrologyYears):
        # Input directories and filenames
        dirname = os.path.dirname(__file__)

        # DEMAND Inputs
        totalDemandsInputData = "../inputData/demandsInput_totalDemands.csv"
        plannedConservationInputData = "../inputData/demandsInput_baseLongTermConservationData.csv"
        ETAWAdjustmentsInputData = "../inputData/demandsInput_ETAWAdjustments.csv"
        inputDemandsFile = os.path.join(dirname, totalDemandsInputData)
        inputPlannedConservationFile = os.path.join(dirname, plannedConservationInputData)
        inputETAWAdjustmentsFile = os.path.join(dirname, ETAWAdjustmentsInputData)

        demandsData = pd.read_csv(inputDemandsFile)
        self.plannedLongTermConservation = pd.read_csv(inputPlannedConservationFile)
        ETAWAdjustments = pd.read_csv(inputETAWAdjustmentsFile).set_index('Year')

        # Initialize variable as a time series
        self.totalDemands = {'Year': historicHydrologyYears}
        totalDemandScenarioRadioButtonIndex = 1    #TODO - connect to dashboard

        # Set up total demand time series based on hydrologic year type.
        for contractor in contractorsList:
            contractorRegion = lookupCorrespondingValue(contractorDf, contractor, colA='Contractor', colB='Hydro. Region')
            contractorYearType = reclassYearType[contractor]
            totalDemandsInput = demandsData[demandsData['Contractor'] == contractor]
            totalDemandsInput = totalDemandsInput[['Variable', 'Contractor', futureYear]]
            contractorDemands = []
            
            mapYearType = {
                'NB': 'Normal or Better Demands (acre-feet/year)',
                'SD': 'Single Dry-Year Demands (acre-feet/year)',
                'MD': 'Multiple Dry-Year Demands (acre-feet/year)',
            }
            if totalDemandScenarioRadioButtonIndex == 1:   # Apply ETAW Adjustments to Normal or Better Demands
                for i, Year in enumerate(historicHydrologyYears):
                    contractorDemands.append(
                        ETAWAdjustments[contractor][Year] *
                        totalDemandsInput[totalDemandsInput['Variable'] == mapYearType['NB']][futureYear].values[0]
                    )
            elif totalDemandScenarioRadioButtonIndex == 0:
                for i in range(len(historicHydrologyYears)):
                    contractorDemands.append(
                        totalDemandsInput[totalDemandsInput['Variable'] == mapYearType[contractorYearType[i]]][futureYear].values[0]
                    )
            self.totalDemands[contractor] = contractorDemands

        self.totalDemands = pd.DataFrame(self.totalDemands)