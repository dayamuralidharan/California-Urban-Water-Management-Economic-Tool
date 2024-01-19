import pandas as pd

inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
inputData = pd.read_excel(inputDataFile, sheet_name = 'Hydrology Assumptions', skiprows = 3) #, nrows = 97, usecols = 'A:AR'
inputData = inputData.set_index('Year', inplace = True)


#inputDataset_index('Contractor', inplace = True)
#futureYear = 2045

#data = inputData[['Variable', futureYear]]
#data = inputData['Ventura County Watershed Protection District']]

#vars = inputData['Variable'].unique()


print(inputData)