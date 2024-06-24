import warnings
import pandas as pd

class SupplyAssumptions:
    def __init__(self, globalAssumptions, inputDataLocations):
        warnings.filterwarnings("ignore")
        
        #Read input data from spreadsheet
        inputData_supplyInputType = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Supply Assumptions', skiprows = 5, nrows = 1, usecols = 'A')
        baseSupplyInputAsTimeSeries = inputData_supplyInputType.columns
        baseSupplyInputAsTimeSeries = baseSupplyInputAsTimeSeries[0]
        
        swpCVPSupplyDataInput = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Supply Assumptions', skiprows = 984, nrows = 94, usecols = 'A:AR')
        self.swpCVPSupply = swpCVPSupplyDataInput


        if baseSupplyInputAsTimeSeries == "Use time series input data":
            self.totalLocalSupply = pd.DataFrame(index=range(len(globalAssumptions.historicHydrologyYears)))
            self.groundwaterLocalSupply = pd.DataFrame(index=range(len(globalAssumptions.historicHydrologyYears)))

            # Read in and set local base supplies timeseries dataframes
            sheets = ['supplyTimeSeriesInput_surface', 
                      'supplyTimeSeries_groundwater', 
                      'supplyTimeSeries_desalination', 
                      'supplyTimeSeries_recycled', 
                      'supplyTimeSeries_potableReuse', 
                      'supplyTimeSeries_potableReuse', 
                      'supplyTimeSeries_other']
            for sheet in sheets:
                 data = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = sheet, skiprows = 1, nrows = 94, usecols = 'A:AR')
                 if self.totalLocalSupply.empty:
                      self.totalLocalSupply = data
                 else:
                      self.totalLocalSupply += data
                 
                 if sheet == 'supplyTimeSeries_groundwater':
                      self.groundwaterLocalSupply = data
            
            self.totalLocalSupply['Year'] = globalAssumptions.historicHydrologyYears 

        else: # Read in data by year type

            # Initiate Total Local Supply and groundwater local supply time series variables
            self.totalLocalSupply = {'Year': globalAssumptions.historicHydrologyYears}
            self.groundwaterLocalSupply = {'Year': globalAssumptions.historicHydrologyYears}

            localSuppliesByType = pd.read_excel(inputDataLocations.inputDataFile, sheet_name = 'Supply Assumptions', skiprows = 11, nrows = 965, usecols = 'A:H')
            pd.DataFrame(localSuppliesByType.set_index('Contractor', inplace = True))
            

            # Set up local supply dataframe for Normal Year Types
            normalYearSupplies = ['Surface for Normal or Better Years (acre-feet/year)',
                                  'Groundwater for Normal or Better Years (acre-feet/year)',
                                  'Recycled for Normal or Better Years (acre-feet/year)',
                                  'Potable Reuse for Normal or Better Years (acre-feet/year)',
                                  'Desalination for Normal or Better Years (acre-feet/year)',
                                  'Long-term Contractual Transfers and Exchanges Supply for Normal or Better Years (acre-feet/year)',
                                  'Other Supply Types for Normal or Better Years (acre-feet/year)']
            
            groundwaterSupplyNormalYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Normal or Better Years (acre-feet/year)']

            filteredNormalYearSupplies = localSuppliesByType[localSuppliesByType['Variable'].isin(normalYearSupplies)]
            self.totalLocalSupplyNormalYear =  filteredNormalYearSupplies[int(globalAssumptions.futureYear)].groupby(['Contractor']).sum() #surfaceSupplyNormalYear + groundwaterSupplyNormalYear + recycleSupplyNormalYear + potableReuseSupplyNormalYear +desalinationSupplyNormalYear + exchangesSupplyNormalYear + otherSupplyNormalYear
            groundwaterSupplyNormalYear.drop('Variable', axis=1, inplace=True)

            # Set up local supply dataframe for Single Dry Year Types
            singleDryYearSupplies = ['Surface for Single Dry Years (acre-feet/year)', 
                                     'Groundwater for Single Dry Years (acre-feet/year)', 
                                     'Recycled for Single Dry Years (acre-feet/year)',
                                     'Potable Reuse for Single Dry Years (acre-feet/year)',
                                     'Desalination for Single Dry Years (acre-feet/year)',
                                     'Long-term Contractual Transfers and Exchanges Supply for Single Dry Years (acre-feet/year)',
                                     'Other Supply Types for Single Dry Years (acre-feet/year)']
            
            groundwaterSupplySingleDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Single Dry Years (acre-feet/year)']

            filteredSingleDryYearSupplies = localSuppliesByType[localSuppliesByType['Variable'].isin(singleDryYearSupplies)]
            self.totalLocalSupplySingleDryYear = filteredSingleDryYearSupplies[int(globalAssumptions.futureYear)].groupby(['Contractor']).sum()
            groundwaterSupplySingleDryYear.drop('Variable', axis=1, inplace=True)

            # Set up local supply dataframe for Multi-Dry Year Types
            multiDryYearSupplies = ['Surface for Multiple Dry Years (acre-feet/year)',
                                     'Groundwater for Multiple Dry Years (acre-feet/year)',
                                     'Recycled for Multiple Dry Years (acre-feet/year)',
                                     'Potable Reuse for Multiple Dry Years (acre-feet/year)',
                                     'Desalination for Multiple Dry Years (acre-feet/year)',
                                     'Long-term Contractual Transfers and Exchanges Supply for Multi-Dry Years (acre-feet/year)',
                                     'Other Supply Types for Multiple Dry Years (acre-feet/year)']

            groundwaterSupplyMultiDryYear = localSuppliesByType[localSuppliesByType['Variable'] == 'Groundwater for Multiple Dry Years (acre-feet/year)']

            filteredMultiDryYearSupplies = localSuppliesByType[localSuppliesByType['Variable'].isin(multiDryYearSupplies)]
            self.totalLocalSupplyMultiDryYear =  filteredMultiDryYearSupplies[int(globalAssumptions.futureYear)].groupby(['Contractor']).sum()
            groundwaterSupplyMultiDryYear.drop('Variable', axis=1, inplace=True)


            for contractor in globalAssumptions.contractorsList:
                self.contractorYearType = globalAssumptions.UWMPhydrologicYearType[contractor]
                totalLocalSupply = []
                groundwaterLocalSupply = []

                # Create time series based on local contractor hydrologic year type
                for i in range(len(globalAssumptions.historicHydrologyYears)):
                    if self.contractorYearType[i] == "NB": #Normal or Better
                        totalLocalSupply.append(self.totalLocalSupplyNormalYear.loc[contractor])
                        groundwaterLocalSupply.append(groundwaterSupplyNormalYear.loc[contractor][int(globalAssumptions.futureYear)])
                    elif self.contractorYearType[i] == "SD": #Single Dry
                            totalLocalSupply.append(self.totalLocalSupplySingleDryYear.loc[contractor])
                            groundwaterLocalSupply.append(groundwaterSupplySingleDryYear.loc[contractor][int(globalAssumptions.futureYear)])
                    elif self.contractorYearType[i] == "MD": #Multi-Dry
                            totalLocalSupply.append(self.totalLocalSupplyMultiDryYear.loc[contractor])
                            groundwaterLocalSupply.append(groundwaterSupplySingleDryYear.loc[contractor][int(globalAssumptions.futureYear)])
                self.totalLocalSupply[contractor] = totalLocalSupply
                self.groundwaterLocalSupply[contractor] = groundwaterLocalSupply

            self.totalLocalSupply = pd.DataFrame(self.totalLocalSupply)
            self.groundwaterLocalSupply = pd.DataFrame(self.groundwaterLocalSupply)
