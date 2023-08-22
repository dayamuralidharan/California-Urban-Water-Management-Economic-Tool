
import pandas as pd

class SupplyAssumptions:
    def __init__(self, globalAssumptions, inputDataLocations):
        #TODO: Set up reading in supply data to read in time series if radio button below is set to 0
        baseSupplyInputAsTimeSeries = False

        # Read SWP/CVP delivery data from CSV
        swpCVPSupplyDataInput = inputDataLocations.swpCVPSupplyDataInput
        self.swpCVPSupply = pd.read_csv(swpCVPSupplyDataInput)

        if baseSupplyInputAsTimeSeries:
            # Read in and set local base supplies timeseries dataframes
            surfaceSupply = pd.read_csv(inputDataLocations.supplySurfaceTimeseriesInput)
            groundwaterSupply = pd.read_csv(inputDataLocations.supplyGroundwaterTimeseriesInput)
            recycleSupply = pd.read_csv(inputDataLocations.supplyRecycledTimeseriesInput)
            potableSupply = pd.read_csv(inputDataLocations.supplyPotableTimeseriesInput)
            desalinationSupply = pd.read_csv(inputDataLocations.supplyDesalinationTimeseriesInput)
            exchangesSupply = pd.read_csv(inputDataLocations.supplyExchangesTimeseriesInput)
            otherSupply = pd.read_csv(inputDataLocations.supplyOtherTimeseriesInput)
            self.totalLocalSupply = (
                surfaceSupply + groundwaterSupply + recycleSupply + potableSupply +
                desalinationSupply + exchangesSupply + otherSupply
            )
            #TODO: Finish setting up total local supply from time series input
            self.totalLocalSupply['Year'] = surfaceSupply['Year']
        else:
            # Read in tabular data from CSV
            localSuppliesDataInput = inputDataLocations.localSuppliesDataInput
            localSuppliesByType = pd.read_csv(localSuppliesDataInput)
            localSuppliesByType.set_index('Contractor', inplace = True)

            # Set up local supply dataframe for Normal Year Types
            surfaceSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Surface for Normal or Better Years (acre-feet/year)']
            groundwaterSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Normal or Better Years (acre-feet/year)']
            recycleSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Recycled for Normal or Better Years (acre-feet/year)']
            potableReuseSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Potable Reuse for Normal or Better Years (acre-feet/year)']
            desalinationSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Desalination for Normal or Better Years (acre-feet/year)']
            exchangesSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Transfers and Exchanges for Normal or Better Years (acre-feet/year)']
            otherSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Other Supply Types for Normal or Better Years (acre-feet/year)']

            self.totalLocalSupplyNormalYear = surfaceSupplyNormalYear + groundwaterSupplyNormalYear + recycleSupplyNormalYear + potableReuseSupplyNormalYear +desalinationSupplyNormalYear + exchangesSupplyNormalYear + otherSupplyNormalYear
            self.totalLocalSupplyNormalYear.drop('Variable', axis=1, inplace=True)
            groundwaterSupplyNormalYear.drop('Variable', axis=1, inplace=True)

            # Set up local supply dataframe for Single Dry Year Types
            surfaceSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Surface for Single Dry Years (acre-feet/year)']
            groundwaterSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Single Dry Years (acre-feet/year)']
            recycleSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Recycled for Single Dry Years (acre-feet/year)']
            potableReuseSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Potable Reuse for Single Dry Years (acre-feet/year)']
            desalinationSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Desalination for Single Dry Years (acre-feet/year)']
            exchangesSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Transfers and Exchanges for Single Dry Years (acre-feet/year)']
            otherSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Other Supply Types for Single Dry Years (acre-feet/year)']

            self.totalLocalSupplySingleDryYear = surfaceSupplySingleDryYear + groundwaterSupplySingleDryYear + recycleSupplySingleDryYear + potableReuseSupplySingleDryYear +desalinationSupplySingleDryYear + exchangesSupplySingleDryYear + otherSupplySingleDryYear
            self.totalLocalSupplySingleDryYear.drop('Variable', axis=1, inplace=True)
            groundwaterSupplySingleDryYear.drop('Variable', axis=1, inplace=True)

            # Set up local supply dataframe for Multi-Dry Year Types
            surfaceSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Surface for Multiple Dry Years (acre-feet/year)']
            groundwaterSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Multiple Dry Years (acre-feet/year)']
            recycleSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Recycled for Multiple Dry Years (acre-feet/year)']
            potableReuseSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Potable Reuse for Multiple Dry Years (acre-feet/year)']
            desalinationSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Desalination for Multiple Dry Years (acre-feet/year)']
            exchangesSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Transfers and Exchanges for Multiple Dry Years (acre-feet/year)']
            otherSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Other Supply Types for Multiple Dry Years (acre-feet/year)']

            self.totalLocalSupplyMultiDryYear = surfaceSupplyMultiDryYear + groundwaterSupplyMultiDryYear + recycleSupplyMultiDryYear + potableReuseSupplyMultiDryYear +desalinationSupplyMultiDryYear + exchangesSupplyMultiDryYear + otherSupplyMultiDryYear
            self.totalLocalSupplyMultiDryYear.drop('Variable', axis=1, inplace=True)
            groundwaterSupplyMultiDryYear.drop('Variable', axis=1, inplace=True)

            # Create Total Local Supply time series based on local contractor hydrologic year type
            self.totalLocalSupply = {'Year': globalAssumptions.historicHydrologyYears}
            # Create groundwater local supply time series to constrain groundwater pumping reduction
            self.groundwaterLocalSupply = {'Year': globalAssumptions.historicHydrologyYears}

            for contractor in globalAssumptions.contractorsList:
                self.contractorYearType = globalAssumptions.UWMPhydrologicYearType[contractor]
                totalLocalSupply = []
                groundwaterLocalSupply = []

                
                for i in range(len(globalAssumptions.historicHydrologyYears)):
                    if self.contractorYearType[i] == "NB": #Normal or Better
                        totalLocalSupply.append(self.totalLocalSupplyNormalYear.loc[contractor][globalAssumptions.futureYear])
                        groundwaterLocalSupply.append(groundwaterSupplyNormalYear.loc[contractor][globalAssumptions.futureYear])
                    elif self.contractorYearType[i] == "SD": #Single Dry
                            totalLocalSupply.append(self.totalLocalSupplySingleDryYear.loc[contractor][globalAssumptions.futureYear])
                            groundwaterLocalSupply.append(groundwaterSupplySingleDryYear.loc[contractor][globalAssumptions.futureYear])
                    elif self.contractorYearType[i] == "MD": #Multi-Dry
                            totalLocalSupply.append(self.totalLocalSupplyMultiDryYear.loc[contractor][globalAssumptions.futureYear])
                            groundwaterLocalSupply.append(groundwaterSupplySingleDryYear.loc[contractor][globalAssumptions.futureYear])
                self.totalLocalSupply[contractor] = totalLocalSupply
                self.groundwaterLocalSupply[contractor] = groundwaterLocalSupply

            self.totalLocalSupply = pd.DataFrame(self.totalLocalSupply)
            self.groundwaterLocalSupply = pd.DataFrame(self.groundwaterLocalSupply)
            print("totalLocalSupply: ", self.totalLocalSupply)
            print("groundwaterLocalSupply: ", self.groundwaterLocalSupply)