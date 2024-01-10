import pandas as pd

inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
inputData = pd.read_excel(inputDataFile, sheet_name = 'Simulation Settings', skiprows = 1, nrows = 1, usecols = 'B')
#inputDataset_index('Contractor', inplace = True)
#futureYear = 2045

#data = inputData[['Variable', futureYear]]
#data = inputData['Ventura County Watershed Protection District']]

vars = inputData['Variable'].unique()


print(vars)