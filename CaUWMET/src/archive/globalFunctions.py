import pandas as pd
import pathlib

#Get current path function
currentPath = pathlib.Path.cwd()
dataPath = pathlib.Path(str(currentPath).replace('src', 'data'))
inputData = pd.read_csv(str(dataPath) + "/contractorList.csv")


# Contractors & regions in study
contractors = inputData["Contractor"]
regions = inputData["Region"]