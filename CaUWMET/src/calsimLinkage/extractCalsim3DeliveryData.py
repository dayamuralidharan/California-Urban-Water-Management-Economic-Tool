
"""
@date: 20230326
@author: Sai Nudurupati (sai.nudurupati@jacobs.com)
@description: Code to extract CalSim 3 timeseries output data from the DSS file.
Reads inputs from:
- inputData_FullContractorList/contractorInformation.csv
- inputData_FullContractorList/DCRBL_DV_6.68.dss
Writes outputs to:
- .inputData_FullContractorList/swpCVPSupplyData_calsim3.csv
"""
# Import packages
import os
import numpy as np
import pyhecdss
import pandas as pd


# Function that checks if the last digit of a non-empty string is a digit or an alphabet. (Helper Function)
def isDigitOrAlpha(string):
    if len(string) > 0:
        if string[-1].isdigit() or string[-1].isalpha() or (string[-1] is '_'):
            return True
    return False

# Function that splits the expression string into individual parts but keeps the string intact. (Helper Function)
def splitOperators(expression):
    r=[""]
    for i in expression.replace(" ","").replace("\n", ""):
        if isDigitOrAlpha(i) and isDigitOrAlpha(r[-1]):
            r[-1]=r[-1]+i
        else:
            r.append(i)
    return r[1:]


# Inputs
dirname = os.path.dirname(os.path.dirname(__file__))
nodeMappingFileName = '../inputData/CaUWMETInputData.xlsx'
nodeMappingDf = pd.read_excel(nodeMappingFileName, sheet_name='Contractor Assumptions', skiprows=4)
formula = nodeMappingDf['Calsim 3 M&I Delivery Arc'].values

inputDSSFileName = pd.read_excel(nodeMappingFileName, sheet_name='Contractor Assumptions', usecols='H', skiprows=2, nrows=1).iloc[0, 0]
inputDSSFile = "../inputData/" + inputDSSFileName

start_date = "1921-10"   # Start time - Not used at the moment
end_date = "2015-09"     # End time - maintain the format "YYYY-MM"
switch_convertCFStoAcreFeetYear = True  # Switch to convert output supplies (originally in monthly mean cfs) to Acre Feet Year
conversion_CFStoAcreFeetYear = (365.25 * 24. * 60. * 60.) * (1 / 43560.)   # (365.24 days/year * 24 hours * 60 minutes * 60 seconds) * (1 acre / 43560 sq. ft)
outputFileName = "swpCVPSupplyData" + inputDSSFileName + ".csv"
outputFile = os.path.join(dirname, outputFileName)

# Read dss file catalog
with pyhecdss.DSSFile(inputDSSFile) as d:
    catdf = d.read_catalog()
partB = catdf['B'].values

# Code to extract timeseries data from Calsim II output dss file
flowData = {}
e = []
fData = {}
fPieces = []
flowNodes = []
finalExpressions = []
allNodes = []
nodePathnames = []

# Looping through each contractor
for i, item in enumerate(formula):
    item = str(item)
    # Exceptions as of now. TODO: Fix these when possible.
    if (
            ("min" in item.lower()) or
            ("wy" in item.lower()) or
            ("clear" in item.lower()) or
            ("not_applicable" in item.lower()) or
            ("non-project" in item.lower())
    ):
        finalExpressions.append("Invalid")
        flowData[i] = np.zeros(95)  # Fill timeseries with zeroes (temporary fix)
        fData[i] = flowData[i]
        continue
    
    flowData[i] = None
    fData[i] = []
    splitFormula = splitOperators(item)
    copyExpression = splitFormula.copy()
    fPieces.append(splitFormula)
    fNodes = []
    var = []
    var_counter = 0
    
    # Looping through individual nodes, retrieving timeseries and executing expressions
    for j, an_item in enumerate(splitFormula):
        if an_item in partB:
            fNodes.append(an_item)
            allNodes.append(an_item)
            fdf3=catdf[(catdf.B==an_item)]  # & ('FLOW' in catdf.C)]
            # Use pyhecdss to retrieve tiimeseries from dss file
            with pyhecdss.DSSFile(inputDSSFile) as d:
                plist1 = d.get_pathnames(fdf3)
                nodePathnames.append(plist1[0])
                dfr1, units1, ptype1 = d.read_rts(plist1[0])
                dfr1 = dfr1[dfr1.index <= end_date]  # Limiting data to end date
                # Resample monthly data to yearly
                dfr2 = dfr1.resample('Y').mean()
                if switch_convertCFStoAcreFeetYear:
                    dfr2 = dfr2 * conversion_CFStoAcreFeetYear  # Convert CFS to Acre Feet Year
                # Keep data only for required years
                dfr3 = dfr2[(dfr2.index.year >= 1921) & (dfr2.index.year <= 2015)]
            var.append(dfr3[dfr3.columns[0]].values)
            copyExpression[j] = "var[%d]" % var_counter
            var_counter += 1
        else:
                None
    finalExpressions.append("".join(copyExpression))
    flowData[i] = eval("".join(copyExpression))
    fData[i] = flowData[i]

# Create data frame and align contractor names to yearly timeseries data
flowDataDf = pd.DataFrame(fData, index=dfr3.index)
flowDataDf.rename(columns=dict(zip(flowDataDf.columns, nodeMappingDf['Contractor'].values)), inplace=True)

# Write data to output file
flowDataDf.to_csv(outputFile)


## Optional for QA
# pathnamesOutput = {}
# pathnamesOutput['allNodes'] = allNodes
# pathnamesOutput['nodePathnames'] = nodePathnames
# pathnamesDataframe = pd.DataFrame(pathnamesOutput)
# pathnamesDataframe.to_csv(os.path.join(dirname, "outputPathnames.csv"))