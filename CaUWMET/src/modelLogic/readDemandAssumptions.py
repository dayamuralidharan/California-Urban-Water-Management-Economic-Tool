import pandas as pd

class DemandAssumptions:
    def __init__(self, globalAssumptions, inputDataLocations):
        inputETAWAdjustmentsFile = inputDataLocations.inputETAWAdjustmentsFile
        
        #TODO reconnect future year to global assumptions which we'll have to make an integer, right now its a string which doesn't work for the functions here
        futureYear = 2045 #globalAssumptions.futureYear
        futureYearTest = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Simulation Settings', skiprows = 19, nrows = 135, usecols = 'A:H')
        inputData_totalDemands = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Demand Assumptions', skiprows = 19, nrows = 135, usecols = 'A:H')
        inputData_useByType = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Demand Assumptions', skiprows = 257, nrows = 319, usecols = 'A:H')
        inputData_plannedConservation = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Demand Assumptions', skiprows = 582, nrows = 44, usecols = 'A:H')
        
        demandsData = inputData_totalDemands
        useByTypeData = inputData_useByType
        self.plannedLongTermConservation = inputData_plannedConservation
        ETAWAdjustments = pd.read_csv(inputETAWAdjustmentsFile).set_index('Year')
        
        demandsData.set_index('Contractor', inplace = True)
        useByTypeData.set_index('Contractor', inplace = True)

        # Initialize variable as a time series
        self.totalDemands = {'Year': globalAssumptions.historicHydrologyYears}
        totalDemandScenarioRadioButtonIndex = inputDataLocations.totalDemandScenarioRadioButtonIndex

        # Set up total demand time series based on hydrologic year type.
        for contractor in globalAssumptions.contractorsList:
            contractorYearType = globalAssumptions.reclassYearType[contractor]
            totalDemandsInput = demandsData.loc[contractor]
            totalDemandsInput = totalDemandsInput[['Variable', futureYear]]
            contractorDemands = []
            
            mapYearType = {
                'NB': 'Normal or Better Demands (AFY)',
                'SD': 'Single Dry-Year Demands (AFY)',
                'MD': 'Multiple Dry-Year Demands (AFY)',
            }
            if totalDemandScenarioRadioButtonIndex == 1:   # Apply ETAW Adjustments to Normal or Better Demands
                for i, Year in enumerate(globalAssumptions.historicHydrologyYears):
                    contractorDemands.append(
                        ETAWAdjustments[contractor][Year] *
                        totalDemandsInput[totalDemandsInput['Variable'] == mapYearType['NB']][futureYear].values[0]
                    )
            elif totalDemandScenarioRadioButtonIndex == 0: #Apply UWMP
                for i in range(len(globalAssumptions.historicHydrologyYears)):
                    contractorDemands.append(
                        totalDemandsInput[totalDemandsInput['Variable'] == mapYearType[contractorYearType[i]]][futureYear].values[0]
                    )
            self.totalDemands[contractor] = contractorDemands

        self.totalDemands = pd.DataFrame(self.totalDemands)
        
        # Set up Use by Type variables and Interior/Exterior Use by Type Variables
        self.singleFamilyUse = useByTypeData[useByTypeData['Variable'] == 'Single Family Residential Use (AFY)'][futureYear]
        self.multiFamilyUse = useByTypeData[useByTypeData['Variable'] == 'Multi-Family Residential Use (AFY)'][futureYear]
        self.industrialUse = useByTypeData[useByTypeData['Variable'] == 'Industrial Use (AFY)'][futureYear]
        self.commAndGovUse = useByTypeData[useByTypeData['Variable'] == 'Commercial and Governmental Use (AFY)'][futureYear]
        agUse = useByTypeData[useByTypeData['Variable'] == 'Agricultural Use (AFY)'][futureYear]
        self.landscapeUse = useByTypeData[useByTypeData['Variable'] == 'Landscape Use (AFY)'][futureYear]
        otherUse = useByTypeData[useByTypeData['Variable'] == 'Other Use (AFY)'][futureYear]

        normalYearDemands = demandsData[demandsData['Variable'] == 'Normal or Better Demands (AFY)'][futureYear]
        

        self.singleFamilyUsePortion = self.singleFamilyUse / normalYearDemands
        self.multiFamilyUsePortion = self.multiFamilyUse / normalYearDemands
        self.industrialUsePortion = self.industrialUse / normalYearDemands
        self.commAndGovUsePortion = self.commAndGovUse / normalYearDemands
        self.landscapeUsePortion = self.landscapeUse / normalYearDemands