
"""
@date: 20211011
@author: Sai Nudurupati (sai.nudurupati@jacobs.com)
@description: Code to extract CalSim II timeseries output data from the DSS file.
Reads inputs from:
- inputData/CaUWMETInputData.xlsx
- inputData/calsim dss file
Writes outputs to:
- inputData/swpCVPSupplyData.csv
"""
# Import packages
import os
import numpy as np
import pyhecdss
import pandas as pd
import logging
import traceback

logging.basicConfig(filename = 'logfileCalsimII.log', filemode = 'w', level = logging.INFO)

# Helper function that checks if the last digit of a non-empty string is a digit or an alphabet.
def isDigitOrAlpha(string):
    if len(string) > 0:
        if string[-1].isdigit() or string[-1].isalpha() or (string[-1] is '_'):
            return True
    return False

# Helper function that splits the expression string into individual parts but keeps the string intact.
def splitOperators(expression):
    r=[""]
    for i in expression.replace(" ","").replace("\n", ""):
        if isDigitOrAlpha(i) and isDigitOrAlpha(r[-1]):
            r[-1]=r[-1]+i
        else:
            r.append(i)
    return r[1:]




try:
    # Inputs
    dirname = os.path.dirname(os.path.dirname(__file__))
    nodeMappingFileName = '../inputData/CaUWMETInputData.xlsx'
    nodeMappingDf = pd.read_excel(nodeMappingFileName, sheet_name='Contractor Assumptions', skiprows=4)
    formula = nodeMappingDf['Calsim II M&I Delivery Arc'].values

    inputDSSFileName = pd.read_excel(nodeMappingFileName, sheet_name='Contractor Assumptions', usecols='G', skiprows=2, nrows=1).iloc[0, 0]
    inputDSSFile = "../inputData/" + inputDSSFileName

    start_date = "31Oct1921 00:00:00"   # Start time
    end_date = "30Sep2003 00:00:00"     # End time
    switch_convertCFStoAcreFeetYear = True  # Switch to convert output supplies (originally in monthly mean cfs) to Acre Feet Year
    conversion_CFStoAcreFeetYear = (365.25 * 24. * 60. * 60.) * (1 / 43560.)   # (365.24 days/year * 24 hours * 60 minutes * 60 seconds) * (1 acre / 43560 sq. ft)
    outputFileName = "swpCVPSupplyData_CalsimII.csv"

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
        logging.info("Looping through each contractor")
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
            #logging.info("j: " + str(j))
            #logging.info("an_item: " + an_item)
            if an_item in partB:
                #logging.info(an_item + " is in " + partB)
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
                    if switch_convertCFStoAcreFeetYear:
                        dfr2 = dfr2 * conversion_CFStoAcreFeetYear
                    # Keep data only for required years
                    dfr3 = dfr2[(dfr2.index.year >= 1921) & (dfr2.index.year <= 2003)]
                var.append(dfr3[dfr3.columns[0]].values)
                #logging.info("var: " + str(var_counter))
                copyExpression[j] = "var[%d]" % var_counter
                var_counter += 1
            else:
                None
                #logging.info(an_item + " is not in " + partB)

        finalExpressions.append("".join(copyExpression))
        #logging.info("Copy expression: " + "".join(copyExpression))
        flowData[i] = eval("".join(copyExpression))
        fData[i] = flowData[i]
        logging.info("Finished processing copy expression " + "".join(copyExpression))

    # Create data frame and align contractor names to yearly timeseries data
    flowDataDf = pd.DataFrame(fData, index=dfr3.index)
    flowDataDf.rename(columns=dict(zip(flowDataDf.columns, nodeMappingDf['Contractor'].values)), inplace=True)

    logging.info('Writing data to output file')
    # Write data to output file
    flowDataDf.to_csv(outputFileName)
    logging.info("Data written to output file")

except Exception as exception:
    logging.error(traceback.format_exc())
