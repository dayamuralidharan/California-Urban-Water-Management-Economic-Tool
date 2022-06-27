import os
import pandas as pd
from readGlobalAssumptions import contractorsList, futureYear
from modelUtilities import lookupCorrespondingValue

#TODO: Set up supplies that vary by hydrological year type

# Input directories and filenames
dirname = os.path.dirname(__file__)

# SUPPLIES Inputs
localSuppliesDataInput = "../inputData/supplyInput_localSupplies.csv"
swpCVPSupplyDataInput = "../inputData/supplyInput_SWPCVPCalsimII2020BenchmarkStudy.csv"
supplyPriorityInput = '../inputData/supplyInput_SupplyPriorities.csv'
inputLocalSuppliesDataFile = os.path.join(dirname, localSuppliesDataInput)
inputSWPCVPSupplyDataFile = os.path.join(dirname, swpCVPSupplyDataInput)
inputSupplyPrioritiesFile = os.path.join(dirname, supplyPriorityInput)


# Read in data from CSV
localSuppliesData = pd.read_csv(inputLocalSuppliesDataFile)
swpCVPSupplyData = pd.read_csv(inputSWPCVPSupplyDataFile)
supplyPrioritiesData = pd.read_csv(inputSupplyPrioritiesFile)

localSuppliesData.set_index('Contractor', inplace = True)

surfaceSupplyData = localSuppliesData[localSuppliesData['Variable'] == 'Surface (acre-feet/year)']
groundwaterSupplyData = localSuppliesData[localSuppliesData['Variable'] == 'Groundwater (acre-feet/year)']
recycleSupplyData = localSuppliesData[localSuppliesData['Variable'] == 'Recycle (acre-feet/year)']
potableReuseSupplyData = localSuppliesData[localSuppliesData['Variable'] == 'Potable Reuse (acre-feet/year)']
desalinationSupplyData = localSuppliesData[localSuppliesData['Variable'] == 'Desalination (acre-feet/year)']
exchangesSupplyData = localSuppliesData[localSuppliesData['Variable'] == 'Exchanges (acre-feet/year)']
otherSupplyData = localSuppliesData[localSuppliesData['Variable'] == 'Other (acre-feet/year)']

#totalLocalSupplies = 


# Create dataframe of Supplies in order of Priority
# supplyPriorities = ['Priority 1', 'Priority 2', 'Priority 3', 'Priority 4', 'Priority 5', 'Priority 6', 'Priority 7']
# suppliesByPriority = pd.DataFrame(index = [contractorsList], columns = [supplyPriorities]) 

# def setSupplyByPriority(priority):
#     for contractor in contractorsList:
#         contractorSupplyTypeByPriority = lookupCorrespondingValue(supplyPrioritiesData, contractor, colA='Contractor', colB=priority)
#         if contractorSupplyTypeByPriority == 'Recycle':
#             suppliesByPriority.loc[[contractor], [priority]] = recycleSupplyData[futureYear].loc[[contractor]].values[0]
#         if contractorSupplyTypeByPriority == 'Potable Reuse':
#             suppliesByPriority.loc[[contractor], [priority]] = potableReuseSupplyData[futureYear].loc[[contractor]].values[0]
#         if contractorSupplyTypeByPriority == 'Desalination':
#             suppliesByPriority.loc[[contractor], [priority]]  = desalinationSupplyData[futureYear].loc[[contractor]].values[0]
#         if contractorSupplyTypeByPriority == 'Exchanges':
#             suppliesByPriority.loc[[contractor], [priority]]  = exchangesSupplyData[futureYear].loc[[contractor]].values[0]
#         if contractorSupplyTypeByPriority == 'Surface':
#             suppliesByPriority.loc[[contractor], [priority]]  = surfaceSupplyData[futureYear].loc[[contractor]].values[0]
#         if contractorSupplyTypeByPriority == 'Other':
#             suppliesByPriority.loc[[contractor], [priority]]  = otherSupplyData[futureYear].loc[[contractor]].values[0]
#         if contractorSupplyTypeByPriority == 'Groundwater':
#             suppliesByPriority.loc[[contractor], [priority]]  = groundwaterSupplyData[futureYear].loc[[contractor]].values[0]

# setSupplyByPriority('Priority 1')
# setSupplyByPriority('Priority 2')
# setSupplyByPriority('Priority 3')
# setSupplyByPriority('Priority 4')
# setSupplyByPriority('Priority 5')
# setSupplyByPriority('Priority 6')
# setSupplyByPriority('Priority 7')

#print(suppliesByPriority)