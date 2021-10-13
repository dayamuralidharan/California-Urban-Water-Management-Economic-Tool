import pandas as pd

from readModelInputs import contractorsList, historicHydrologyYears, futureYear
from readModelInputs import totalDemands, baseConservation 
#from readModelInputs import finalSuppliesDf, finalDemandsAfterBaseConservationDf
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
# finaldemandsAfterPriority1SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finalDemandsAfterBaseConservationDf, 1)
# finaldemandsAfterPriority2SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority1SuppliesDf, 2)
# finaldemandsAfterPriority3SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority2SuppliesDf, 3)
# finaldemandsAfterPriority4SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority3SuppliesDf, 4)
# finaldemandsAfterPriority5SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority4SuppliesDf, 5)
# finaldemandsAfterPriority6SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority5SuppliesDf, 6)
# finaldemandsAfterPriority7SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority6SuppliesDf, 7)
# finaldemandsAfterPriority8SuppliesDf = subtractSuppliesByPriority(finalSuppliesDf, finaldemandsAfterPriority7SuppliesDf, 8)