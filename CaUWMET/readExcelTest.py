import pandas as pd

inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
inputData_X = pd.read_excel(inputDataFile, sheet_name = 'Supply Assumptions', skiprows = 984, nrows = 95, usecols = 'A:AR')
#inputData_X.set_index('Contractor', inplace = True)
#futureYear = 2045

#data = inputData_X[['Variable', futureYear]]
#data = inputData_X[['Ventura County Watershed Protection District']]


print(inputData_X)