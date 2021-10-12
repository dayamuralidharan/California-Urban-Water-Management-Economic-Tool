
"""
@date: 20211011
@author: Sai Nudurupati (sai.nudurupati@jacobs.com)
@description: Code to extract CalSim II timeseries output data from the DSS file.
"""
# Import packages
import os
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
dirname = os.path.dirname(__file__)
nodeMappingFileName = "inputData/contractorInformation.csv"
nodeMappingFile = os.path.join(dirname, nodeMappingFileName)
nodeMappingDf = pd.read_csv(nodeMappingFile, encoding="ISO-8859-1")
formula = nodeMappingDf['calsimIIDeliveryArcs'].values
inputDSS = "inputData/calsim_hist_011221_output.dss"
inputDSSFile = os.path.join(dirname, inputDSS)  # Entire path to the input file (including the extension)
start_date = "31Oct1921 00:00:00"   # Start time
end_date = "30Sep2003 00:00:00"     # End time
outputFileName = "inputData/swpCVPSupplyData.csv"
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
for i, item in enumerate(formula):
    # Exceptions for the contractors with complicated expressions (three in total). TODO: Fix this.
    if ("south" in item.lower()) or ("min" in item.lower()) or ("wy" in item.lower()):
        continue
    flowData[i] = None
    fData[i] = []
    splitFormula = splitOperators(item)
    copyExpression = splitFormula.copy()
    fPieces.append(splitFormula)
    fNodes = []
    var = []
    var_counter = 0
    for j, an_item in enumerate(splitFormula):
        if an_item in partB:
            fNodes.append(an_item)
            fdf3=catdf[(catdf.B==an_item)]  # & ('FLOW' in catdf.C)]
            with pyhecdss.DSSFile(inputDSSFile) as d:
                plist1 = d.get_pathnames(fdf3)
                dfr1, units1, ptype1 = d.read_rts(plist1[0])
                dfr2 = dfr1.resample('Y').sum()
                dfr3 = dfr2[(dfr2.index.year >= 1921) & (dfr2.index.year <= 2003)]
            var.append(dfr3[dfr3.columns[0]].values)
            copyExpression[j] = "var[%d]" % var_counter
            var_counter += 1
    finalExpressions.append("".join(copyExpression))
    flowData[i] = eval("".join(copyExpression))
    fData[i] = flowData[i]
flowDataDf = pd.DataFrame(fData, index=dfr3.index)
flowDataDf.rename(columns=dict(zip(flowDataDf.columns, nodeMappingDf['Contractor'].values)), inplace=True)
flowDataDf.to_csv(outputFile)
