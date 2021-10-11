

import os
import numpy as np
import pandas as pd
from modelUtilities import (
    returnHydroRegion, reclassifyYearType,
)
from modelInputs import finalSuppliesDf, finalDemandsAfterBaseConservationDf

def subtractSuppliesByPriority(finalSuppliesDf, finalDemandsAfterBaseConservationDf, supplyPriorityNumber):
    suppliesPriorityNDf = finalSuppliesDf[finalSuppliesDf['Supply Priority'] == supplyPriorityNumber].copy()
    finalSuppliesPriorityNDf = suppliesPriorityNDf.reset_index()
    del finalSuppliesPriorityNDf['index']
    finaldemandsAfterPriorityNSuppliesDf = finalSuppliesPriorityNDf.copy()
    cols = finalSuppliesPriorityNDf.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
    finaldemandsAfterPriorityNSuppliesDf[cols] = finalDemandsAfterBaseConservationDf[cols] - finalSuppliesPriorityNDf[cols]
    return finaldemandsAfterPriorityNSuppliesDf

#Subtracting Supply Priority
finaldemandsAfterPriority1SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finalDemandsAfterBaseConservationDf, 1)
finaldemandsAfterPriority2SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority1SuppliesDf, 2)
finaldemandsAfterPriority3SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority2SuppliesDf, 3)
finaldemandsAfterPriority4SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority3SuppliesDf, 4)
finaldemandsAfterPriority5SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority4SuppliesDf, 5)
finaldemandsAfterPriority6SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority5SuppliesDf, 6)
finaldemandsAfterPriority7SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority6SuppliesDf, 7)
finaldemandsAfterPriority8SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority7SuppliesDf, 8)