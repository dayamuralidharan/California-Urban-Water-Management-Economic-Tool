import pandas as pd

inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
inputData = pd.read_excel(inputDataFile, sheet_name = 'Demand Assumptions', skiprows = 14, nrows = 1, usecols = 'A')
inputData = inputData.columns
inputData = inputData[0]


#inputDataset_index('Contractor', inplace = True)
#futureYear = 2045

#data = inputData[['Variable', futureYear]]
#data = inputData['Ventura County Watershed Protection District']]

#vars = inputData['Variable'].unique()


print(inputData)