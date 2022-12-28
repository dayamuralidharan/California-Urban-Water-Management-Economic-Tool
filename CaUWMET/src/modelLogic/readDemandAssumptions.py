import pandas as pd
from src.modelLogic.modelUtilities import lookupCorrespondingValue

class DemandAssumptions:
    def __init__(self, globalAssumptions, inputDataLocations):
        # Input directories and filenames
        inputDemandsFile = inputDataLocations.inputDemandsFile
        inputPlannedConservationFile = inputDataLocations.inputPlannedConservationFile
        inputETAWAdjustmentsFile = inputDataLocations.inputETAWAdjustmentsFile
        inputUseByTypeFile = inputDataLocations.inputUseByTypeFile
        
        demandsData = pd.read_csv(inputDemandsFile)
        self.plannedLongTermConservation = pd.read_csv(inputPlannedConservationFile)
        ETAWAdjustments = pd.read_csv(inputETAWAdjustmentsFile).set_index('Year')
        useByTypeData = pd.read_csv(inputUseByTypeFile)

        # Initialize variable as a time series
        self.totalDemands = {'Year': globalAssumptions.historicHydrologyYears}
        totalDemandScenarioRadioButtonIndex = 1    #TODO - connect to dashboard

        # Set up total demand time series based on hydrologic year type.
        for contractor in globalAssumptions.contractorsList:
            #TODO remove lookup function, not needed.
            contractorRegion = lookupCorrespondingValue(globalAssumptions.contractorDf, contractor, colA='Contractor', colB='Hydro. Region')
            contractorYearType = globalAssumptions.reclassYearType[contractor]
            totalDemandsInput = demandsData[demandsData['Contractor'] == contractor]
            totalDemandsInput = totalDemandsInput[['Variable', 'Contractor', globalAssumptions.futureYear]]
            contractorDemands = []
            
            mapYearType = {
                'NB': 'Normal or Better Demands (acre-feet/year)',
                'SD': 'Single Dry-Year Demands (acre-feet/year)',
                'MD': 'Multiple Dry-Year Demands (acre-feet/year)',
            }
            if totalDemandScenarioRadioButtonIndex == 1:   # Apply ETAW Adjustments to Normal or Better Demands
                for i, Year in enumerate(globalAssumptions.historicHydrologyYears):
                    contractorDemands.append(
                        ETAWAdjustments[contractor][Year] *
                        totalDemandsInput[totalDemandsInput['Variable'] == mapYearType['NB']][globalAssumptions.futureYear].values[0]
                    )
            elif totalDemandScenarioRadioButtonIndex == 0:
                for i in range(len(globalAssumptions.historicHydrologyYears)):
                    contractorDemands.append(
                        totalDemandsInput[totalDemandsInput['Variable'] == mapYearType[contractorYearType[i]]][globalAssumptions.futureYear].values[0]
                    )
            self.totalDemands[contractor] = contractorDemands

        self.totalDemands = pd.DataFrame(self.totalDemands)
        
        # Set up Use by Type variables and Interior/Exterior Use by Type Variables
        singleFamilyUse = useByTypeData[useByTypeData['Variable'] == 'Single Family Residential Use (acre-feet/year)']
        multiFamilyUse = useByTypeData[useByTypeData['Variable'] == 'Multi-Family Residential Use (acre-feet/year)']
        industrialUse = useByTypeData[useByTypeData['Variable'] == 'Industrial Use (acre-feet/year)']
        commAndGovUse = useByTypeData[useByTypeData['Variable'] == 'Commercial and Governmental Use (acre-feet/year)']
        agUse = useByTypeData[useByTypeData['Variable'] == 'Agricultural Use (acre-feet/year)']
        landscapeUse = useByTypeData[useByTypeData['Variable'] == 'Landscape Use (acre-feet/year)']
        otherUse = useByTypeData[useByTypeData['Variable'] == 'Other Use (acre-feet/year)']

        normalYearDemands = demandsData[demandsData['Variable'] == 'Normal or Better Demands (acre-feet/year)']

        singleFamilyUse.set_index('Contractor', inplace = True)
        multiFamilyUse.set_index('Contractor', inplace = True)
        industrialUse.set_index('Contractor', inplace = True)
        commAndGovUse.set_index('Contractor', inplace = True)
        agUse.set_index('Contractor', inplace = True)
        landscapeUse.set_index('Contractor', inplace = True)
        otherUse.set_index('Contractor', inplace = True)
        normalYearDemands.set_index('Contractor', inplace = True)

        self.singleFamilyUsePortion = singleFamilyUse[globalAssumptions.futureYear] / normalYearDemands[globalAssumptions.futureYear]
        self.multiFamilyUsePortion = multiFamilyUse[globalAssumptions.futureYear] / normalYearDemands[globalAssumptions.futureYear]
        self.industrialUsePortion = industrialUse[globalAssumptions.futureYear] / normalYearDemands[globalAssumptions.futureYear]
        self.commAndGovUsePortion = commAndGovUse[globalAssumptions.futureYear] / normalYearDemands[globalAssumptions.futureYear]
        self.landscapeUsePortion = landscapeUse[globalAssumptions.futureYear] / normalYearDemands[globalAssumptions.futureYear]