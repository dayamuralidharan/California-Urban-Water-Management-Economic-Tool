import pandas as pd

inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
inputData_X = pd.read_excel(inputDataFile, sheet_name = 'Demand Assumptions', skiprows = 257, nrows = 319, usecols = 'A:H')
inputData_X.set_index('Contractor', inplace = True)
futureYear = 2045

data = inputData_X[['Variable', futureYear]]

print(data)