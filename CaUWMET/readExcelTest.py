import pandas as pd

inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
inputData_X = pd.read_excel(inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 804, nrows = 319, usecols = 'A:I')
#inputData_X.set_index('Contractor', inplace = True)
#futureYear = 2045

#data = inputData_X[['Variable', futureYear]]
#data = inputData_X[['Ventura County Watershed Protection District']]


print(inputData_X)