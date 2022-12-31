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
        
        demandsData.set_index('Contractor', inplace = True)
        useByTypeData.set_index('Contractor', inplace = True)

        # Initialize variable as a time series
        self.totalDemands = {'Year': globalAssumptions.historicHydrologyYears}
        totalDemandScenarioRadioButtonIndex = inputDataLocations.totalDemandScenarioRadioButtonIndex

        # Set up total demand time series based on hydrologic year type.
        for contractor in globalAssumptions.contractorsList:
            #TODO remove lookup function, not needed.
            contractorRegion = lookupCorrespondingValue(globalAssumptions.contractorDf, contractor, colA='Contractor', colB='Hydro. Region')
            contractorYearType = globalAssumptions.reclassYearType[contractor]
            totalDemandsInput = demandsData.loc[contractor]
            totalDemandsInput = totalDemandsInput[['Variable', globalAssumptions.futureYear]]
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
            elif totalDemandScenarioRadioButtonIndex == 0: #Apply UWMP
                for i in range(len(globalAssumptions.historicHydrologyYears)):
                    contractorDemands.append(
                        totalDemandsInput[totalDemandsInput['Variable'] == mapYearType[contractorYearType[i]]][globalAssumptions.futureYear].values[0]
                    )
            self.totalDemands[contractor] = contractorDemands

        self.totalDemands = pd.DataFrame(self.totalDemands)
        
        # Set up Use by Type variables and Interior/Exterior Use by Type Variables
        singleFamilyUse = useByTypeData[useByTypeData['Variable'] == 'Single Family Residential Use (acre-feet/year)'][globalAssumptions.futureYear]
        multiFamilyUse = useByTypeData[useByTypeData['Variable'] == 'Multi-Family Residential Use (acre-feet/year)'][globalAssumptions.futureYear]
        industrialUse = useByTypeData[useByTypeData['Variable'] == 'Industrial Use (acre-feet/year)'][globalAssumptions.futureYear]
        commAndGovUse = useByTypeData[useByTypeData['Variable'] == 'Commercial and Governmental Use (acre-feet/year)'][globalAssumptions.futureYear]
        agUse = useByTypeData[useByTypeData['Variable'] == 'Agricultural Use (acre-feet/year)'][globalAssumptions.futureYear]
        landscapeUse = useByTypeData[useByTypeData['Variable'] == 'Landscape Use (acre-feet/year)'][globalAssumptions.futureYear]
        otherUse = useByTypeData[useByTypeData['Variable'] == 'Other Use (acre-feet/year)'][globalAssumptions.futureYear]

        normalYearDemands = demandsData[demandsData['Variable'] == 'Normal or Better Demands (acre-feet/year)'][globalAssumptions.futureYear]
        

        self.singleFamilyUsePortion = singleFamilyUse / normalYearDemands
        self.multiFamilyUsePortion = multiFamilyUse / normalYearDemands
        self.industrialUsePortion = industrialUse / normalYearDemands
        self.commAndGovUsePortion = commAndGovUse / normalYearDemands
        self.landscapeUsePortion = landscapeUse / normalYearDemands
        
        print(self.singleFamilyUsePortion)