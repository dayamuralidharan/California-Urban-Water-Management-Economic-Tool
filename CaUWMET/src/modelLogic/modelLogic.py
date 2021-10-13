import pandas as pd

from readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from readDemandAssumptions import totalDemands, baseConservation 
from readSupplyAssumptions import finalSuppliesDf, finalDemandsAfterBaseConservationDf
from modelUtilities import subtractSuppliesByPriority

demandsAfterBaseConservation = {'Year': historicHydrologyYears}

for contractor in contractorsList:
    # Calculate demands after long-term base conservation
    contractorDemandsAfterBaseConservation = []
    contractorTotalDemand = totalDemands[contractor]
    for i in range(len(historicHydrologyYears)):
        contractorBaseLongTermConservation = baseConservation[baseConservation['Contractor'] == contractor][futureYear].values[0]
        contractorDemandsAfterBaseConservation.append(contractorTotalDemand[i] - contractorBaseLongTermConservation)
    demandsAfterBaseConservation[contractor] = contractorDemandsAfterBaseConservation

demandsAfterBaseConservation = pd.DataFrame(demandsAfterBaseConservation)

#Subtracting Supply Priority TODO: turn into for loop

# demandsAfterBaseConservationDfIndexSet = demandsAfterBaseConservation.set_index('Year')
# demandsAfterBaseConservationDfTransposed = demandsAfterBaseConservationDfIndexSet.T
# demandsAfterBaseConservationDfTransposedStacked = demandsAfterBaseConservationDfTransposed.stack()
# demandsAfterBaseConservationDfTransposedStacked = demandsAfterBaseConservationDfTransposedStacked.to_frame()
# demandsAfterBaseConservationDfTransposedStackedReset = demandsAfterBaseConservationDfTransposedStacked.reset_index()
# demandsAfterBaseConservationDfTransposedStackedReset.columns = ['Contractor', 'Year', 'Supply Volume']
# finalDemandsAfterBaseConservationDf = demandsAfterBaseConservationDfTransposedStackedReset

# finaldemandsAfterPriority1SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finalDemandsAfterBaseConservationDf, 1)
# finaldemandsAfterPriority2SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority1SuppliesDf, 2)
# finaldemandsAfterPriority3SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority2SuppliesDf, 3)
# finaldemandsAfterPriority4SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority3SuppliesDf, 4)
# finaldemandsAfterPriority5SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority4SuppliesDf, 5)
# finaldemandsAfterPriority6SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority5SuppliesDf, 6)
# finaldemandsAfterPriority7SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority6SuppliesDf, 7)
# finaldemandsAfterPriority8SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority7SuppliesDf, 8)