
"""
@date: 20211011
@author: Sai Nudurupati (sai.nudurupati@jacobs.com)
@description: Code to extract CalSim II timeseries output data from the DSS file.
Reads inputs from:
- inputData/contractorInformation.csv
- inputData/calsim_hist_011221_output.dss
Writes outputs to:
- inputData/swpCVPSupplyData.csv
"""
# Import packages
import os
import numpy as np
import pyhecdss
import pandas as pd

#TODO add GUI for users to input DSS file names and locations


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
nodeMappingFileName = "../inputData/contractorInfo_calsimLinkage.csv"
nodeMappingFile = os.path.join(dirname, nodeMappingFileName)
nodeMappingDf = pd.read_csv(nodeMappingFile, encoding="ISO-8859-1")
formula = nodeMappingDf['Calsim II M&I Delivery Arc'].values
inputDSS = "../inputData/calsim_hist_011221_output.dss" # TODO change to Reclamation_2020_Benchmark_CALSIM_HIST_011221
inputDSSFile = os.path.join(dirname, inputDSS)  # Entire path to the input file (including the extension)
start_date = "31Oct1921 00:00:00"   # Start time
end_date = "30Sep2003 00:00:00"     # End time
outputFileName = "swpCVPSupplyData.csv"
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
    # Exceptions as of now. TODO: Fix these when possible.
    if (
            ("min" in item.lower()) or
            ("wy" in item.lower())
    ):
        finalExpressions.append("Invalid")
        flowData[i] = np.zeros(83)  # Fill timeseries with zeroes (temporary fix)
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
                # Resample monthly data to yearly
                dfr2 = dfr1.resample('Y').sum()
                # Keep data only for required years
                dfr3 = dfr2[(dfr2.index.year >= 1921) & (dfr2.index.year <= 2003)]
            var.append(dfr3[dfr3.columns[0]].values)
            copyExpression[j] = "var[%d]" % var_counter
            var_counter += 1
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
