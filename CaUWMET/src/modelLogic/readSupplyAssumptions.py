import pandas as pd
from src.modelLogic.modelUtilities import lookupCorrespondingValue

class SupplyAssumptions:
    def __init__(self, globalAssumptions, inputDataLocations):
        #TODO: Connect to streamlit dashboard, will either be table by year type or time series
        #TODO: Set up reading in supply data to read in time series if radio button below is set to 0
        localSupplyScenarioRadioButtonIndex = 0

        # SUPPLIES Inputs
        localSuppliesDataInput = inputDataLocations.localSuppliesDataInput
        swpCVPSupplyDataInput = inputDataLocations.swpCVPSupplyDataInput

        # Read in data from CSV
        localSuppliesByType = pd.read_csv(localSuppliesDataInput)
        self.swpCVPSupply = pd.read_csv(swpCVPSupplyDataInput)

        localSuppliesByType.set_index('Contractor', inplace = True)

        # Set up local supply dataframe for Normal Year Types
        surfaceSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Surface for Normal or Better Years (acre-feet/year)']
        groundwaterSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Normal or Better Years (acre-feet/year)']
        recycleSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Recycled for Normal or Better Years (acre-feet/year)']
        potableReuseSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Potable Reuse for Normal or Better Years (acre-feet/year)']
        desalinationSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Desalination for Normal or Better Years (acre-feet/year)']
        exchangesSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Transfers and Exchanges for Normal or Better Years (acre-feet/year)']
        otherSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Other Supply Types for Normal or Better Years (acre-feet/year)']

        totalLocalSupplyNormalYear = surfaceSupplyNormalYear + groundwaterSupplyNormalYear + recycleSupplyNormalYear + potableReuseSupplyNormalYear +desalinationSupplyNormalYear + exchangesSupplyNormalYear + otherSupplyNormalYear
        totalLocalSupplyNormalYear.drop('Variable', axis=1, inplace=True)

        # Set up local supply dataframe for Single Dry Year Types
        surfaceSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Surface for Single Dry Years (acre-feet/year)']
        groundwaterSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Single Dry Years (acre-feet/year)']
        recycleSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Recycled for Single Dry Years (acre-feet/year)']
        potableReuseSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Potable Reuse for Single Dry Years (acre-feet/year)']
        desalinationSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Desalination for Single Dry Years (acre-feet/year)']
        exchangesSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Transfers and Exchanges for Single Dry Years (acre-feet/year)']
        otherSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Other Supply Types for Single Dry Years (acre-feet/year)']

        totalLocalSupplySingleDryYear = surfaceSupplySingleDryYear + groundwaterSupplySingleDryYear + recycleSupplySingleDryYear + potableReuseSupplySingleDryYear +desalinationSupplySingleDryYear + exchangesSupplySingleDryYear + otherSupplySingleDryYear
        totalLocalSupplySingleDryYear.drop('Variable', axis=1, inplace=True)

        # Set up local supply dataframe for Multi-Dry Year Types
        surfaceSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Surface for Multiple Dry Years (acre-feet/year)']
        groundwaterSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Multiple Dry Years (acre-feet/year)']
        recycleSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Recycled for Multiple Dry Years (acre-feet/year)']
        potableReuseSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Potable Reuse for Multiple Dry Years (acre-feet/year)']
        desalinationSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Desalination for Multiple Dry Years (acre-feet/year)']
        exchangesSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Transfers and Exchanges for Multiple Dry Years (acre-feet/year)']
        otherSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Other Supply Types for Multiple Dry Years (acre-feet/year)']

        totalLocalSupplyMultiDryYear = surfaceSupplyMultiDryYear + groundwaterSupplyMultiDryYear + recycleSupplyMultiDryYear + potableReuseSupplyMultiDryYear +desalinationSupplyMultiDryYear + exchangesSupplyMultiDryYear + otherSupplyMultiDryYear
        totalLocalSupplyMultiDryYear.drop('Variable', axis=1, inplace=True)

        # Create Total Local Supply time series based on local contractor hydrologic year type
        self.totalLocalSupply = {'Year': globalAssumptions.historicHydrologyYears}

        for contractor in globalAssumptions.contractorsList:
            contractorRegion = lookupCorrespondingValue(globalAssumptions.contractorDf, contractor, colA='Contractor', colB='Hydro. Region')
            contractorYearType = globalAssumptions.UWMPhydrologicYearType[contractor]
            contractorLocalSupply = []

            if localSupplyScenarioRadioButtonIndex == 0:
                for i in range(len(globalAssumptions.historicHydrologyYears)):
                    if contractorYearType[i] == "NB": #Normal or Better
                        contractorLocalSupply.append(totalLocalSupplyNormalYear.loc[contractor][globalAssumptions.futureYear])
                    elif contractorYearType[i] == "SD": #Single Dry
                            contractorLocalSupply.append(totalLocalSupplySingleDryYear.loc[contractor][globalAssumptions.futureYear])
                    elif contractorYearType[i] == "MD": #Multi-Dry
                            contractorLocalSupply.append(totalLocalSupplyMultiDryYear.loc[contractor][globalAssumptions.futureYear])
            self.totalLocalSupply[contractor] = contractorLocalSupply

        self.totalLocalSupply = pd.DataFrame(self.totalLocalSupply)