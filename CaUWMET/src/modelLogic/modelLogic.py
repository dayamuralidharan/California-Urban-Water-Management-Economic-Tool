

import os
import numpy as np
import pandas as pd
from modelUtilities import (
    returnHydroRegion, reclassifyYearType,
)
from modelInputs import finalSuppliesDf, finalDemandsAfterBaseConservationDf

#Subtracting Priority 1 Supplies
suppliesPriority1Df = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == 1]
finalSuppliesPriority1Df = suppliesPriority1Df.reset_index()
del finalSuppliesPriority1Df['index']
finaldemandsAfterPriority1SuppliesDf = finalSuppliesPriority1Df.copy()
cols = finalSuppliesPriority1Df.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
finaldemandsAfterPriority1SuppliesDf[cols] = finalDemandsAfterBaseConservationDf[cols] - finalSuppliesPriority1Df[cols]

#Subtracting Priority 2 Supplies
suppliesPriority2Df = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == 2]
finalSuppliesPriority2Df = suppliesPriority2Df.reset_index()
del finalSuppliesPriority2Df['index']
finaldemandsAfterPriority2SuppliesDf = finalSuppliesPriority2Df.copy()
cols = finalSuppliesPriority2Df.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
finaldemandsAfterPriority2SuppliesDf[cols] = finaldemandsAfterPriority1SuppliesDf[cols] - finalSuppliesPriority2Df[cols]

#Subtracting Priority 3 Supplies
suppliesPriority3Df = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == 3]
finalSuppliesPriority3Df = suppliesPriority3Df.reset_index()
del finalSuppliesPriority3Df['index']
finaldemandsAfterPriority3SuppliesDf = finalSuppliesPriority3Df.copy()
cols = finalSuppliesPriority3Df.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
finaldemandsAfterPriority3SuppliesDf[cols] = finaldemandsAfterPriority2SuppliesDf[cols] - finalSuppliesPriority3Df[cols]

#Subtracting Priority 4 Supplies
suppliesPriority4Df = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == 4]
finalSuppliesPriority4Df = suppliesPriority4Df.reset_index()
del finalSuppliesPriority4Df['index']
finaldemandsAfterPriority4SuppliesDf = finalSuppliesPriority4Df.copy()
cols = finalSuppliesPriority4Df.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
finaldemandsAfterPriority4SuppliesDf[cols] = finaldemandsAfterPriority3SuppliesDf[cols] - finalSuppliesPriority4Df[cols]

#Subtracting Priority 5 Supplies
suppliesPriority5Df = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == 5]
finalSuppliesPriority5Df = suppliesPriority5Df.reset_index()
del finalSuppliesPriority5Df['index']
finaldemandsAfterPriority5SuppliesDf = finalSuppliesPriority5Df.copy()
cols = finalSuppliesPriority5Df.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
finaldemandsAfterPriority5SuppliesDf[cols] = finaldemandsAfterPriority4SuppliesDf[cols] - finalSuppliesPriority5Df[cols]

#Subtracting Priority 6 Supplies
suppliesPriority6Df = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == 6]
finalSuppliesPriority6Df = suppliesPriority6Df.reset_index()
del finalSuppliesPriority6Df['index']
finaldemandsAfterPriority6SuppliesDf = finalSuppliesPriority6Df.copy()
cols = finalSuppliesPriority6Df.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
finaldemandsAfterPriority6SuppliesDf[cols] = finaldemandsAfterPriority5SuppliesDf[cols] - finalSuppliesPriority6Df[cols]

#Subtracting Priority 7 Supplies
suppliesPriority7Df = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == 7]
finalSuppliesPriority7Df = suppliesPriority7Df.reset_index()
del finalSuppliesPriority7Df['index']
finaldemandsAfterPriority7SuppliesDf = finalSuppliesPriority7Df.copy()
cols = finalSuppliesPriority7Df.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
finaldemandsAfterPriority7SuppliesDf[cols] = finaldemandsAfterPriority6SuppliesDf[cols] - finalSuppliesPriority7Df[cols]

#Subtracting Priority 8 Supplies
suppliesPriority8Df = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == 8]
finalSuppliesPriority8Df = suppliesPriority8Df.reset_index()
del finalSuppliesPriority8Df['index']
finaldemandsAfterPriority8SuppliesDf = finalSuppliesPriority8Df.copy()
cols = finalSuppliesPriority8Df.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
finaldemandsAfterPriority8SuppliesDf[cols] = finaldemandsAfterPriority7SuppliesDf[cols] - finalSuppliesPriority8Df[cols]