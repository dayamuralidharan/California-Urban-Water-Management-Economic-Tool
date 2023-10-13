import pandas as pd

inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
inputData = pd.read_excel(inputDataFile, sheet_name = 'Long-term WMOs Assumptions', skiprows = 378, nrows = 734, usecols = 'A:I')
#inputDataset_index('Contractor', inplace = True)
#futureYear = 2045

#data = inputData[['Variable', futureYear]]
#data = inputData['Ventura County Watershed Protection District']]

vars = inputData['Variable'].unique()


print(vars)