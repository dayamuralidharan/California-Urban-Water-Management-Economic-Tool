import os
import pandas as pd
from readGlobalAssumptions import contractorsList, futureYear
from modelUtilities import lookupCorrespondingValue

#TODO: Set up supplies that vary by hydrological year type

# Input directories and filenames
dirname = os.path.dirname(__file__)

# SUPPLIES Inputs
recycledSupplyDataInput = "../inputData/supplyInput_Recycled.csv"
potableReuseSupplyDataInput = "../inputData/supplyInput_PotableReuse.csv"
desalinationSupplyDataInput = "../inputData/supplyInput_Desalination.csv"
contractualTransfersSupplyDataInput = "../inputData/supplyInput_ContractualTransfers.csv"
localSurfaceSupplyDataInput = "../inputData/supplyInput_Surface.csv"
otherImportedSupplyDataInput = "../inputData/supplyInput_OtherImported.csv"
localGroundwaterSupplyDataInput = "../inputData/supplyInput_Groundwater.csv"
swpCVPSupplyDataInput = "../inputData/supplyInput_SWPCVP.csv"
supplyPriorityInput = '../inputData/supplyInput_SupplyPriorities.csv'
inputRecycledSupplyDataFile = os.path.join(dirname, recycledSupplyDataInput)
inputPotableReuseSupplyDataFile = os.path.join(dirname, potableReuseSupplyDataInput)
inputDesalinationSupplyDataFile = os.path.join(dirname, desalinationSupplyDataInput)
inputContractualTransfersSupplyDataFile = os.path.join(dirname, contractualTransfersSupplyDataInput)
inputLocalSurfaceSupplyDataFile = os.path.join(dirname, localSurfaceSupplyDataInput)
inputOtherImportedSupplyDataFile = os.path.join(dirname, otherImportedSupplyDataInput)
inputLocalGroundwaterSupplyDataFile = os.path.join(dirname, localGroundwaterSupplyDataInput)
inputSWPCVPSupplyDataFile = os.path.join(dirname, swpCVPSupplyDataInput)
inputSupplyPrioritiesFile = os.path.join(dirname, supplyPriorityInput)


# Read in data from CSV
recycledSupplyData = pd.read_csv(inputRecycledSupplyDataFile)
potableReuseSupplyData = pd.read_csv(inputPotableReuseSupplyDataFile)
desalinationSupplyData = pd.read_csv(inputDesalinationSupplyDataFile)
contractualTransfersSupplyData = pd.read_csv(inputContractualTransfersSupplyDataFile)
surfaceSupplyData = pd.read_csv(inputLocalSurfaceSupplyDataFile)
otherImportedSupplyData = pd.read_csv(inputOtherImportedSupplyDataFile)
groundwaterSupplyData = pd.read_csv(inputLocalGroundwaterSupplyDataFile)
swpCVPSupplyData = pd.read_csv(inputSWPCVPSupplyDataFile)
supplyPrioritiesData = pd.read_csv(inputSupplyPrioritiesFile)

recycledSupplyData.set_index('Contractor', inplace = True)
potableReuseSupplyData.set_index('Contractor', inplace = True)
desalinationSupplyData.set_index('Contractor', inplace = True)
contractualTransfersSupplyData.set_index('Contractor', inplace = True)
surfaceSupplyData.set_index('Contractor', inplace = True)
otherImportedSupplyData.set_index('Contractor', inplace = True)
groundwaterSupplyData.set_index('Contractor', inplace = True)


# Create dataframe of Supplies in order of Priority
supplyPriorities = ['Priority 1', 'Priority 2', 'Priority 3', 'Priority 4', 'Priority 5', 'Priority 6', 'Priority 7']
suppliesByPriority = pd.DataFrame(index = [contractorsList], columns = [supplyPriorities]) 

def setSupplyByPriority(priority):
    for contractor in contractorsList:
        contractorSupplyTypeByPriority = lookupCorrespondingValue(supplyPrioritiesData, contractor, colA='Contractor', colB=priority)
        if contractorSupplyTypeByPriority == 'Recycled':
            suppliesByPriority.loc[[contractor], [priority]] = recycledSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Potable Reuse':
            suppliesByPriority.loc[[contractor], [priority]] = potableReuseSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Desalination':
            suppliesByPriority.loc[[contractor], [priority]]  = desalinationSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Contractual Transfers':
            suppliesByPriority.loc[[contractor], [priority]]  = contractualTransfersSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Surface':
            suppliesByPriority.loc[[contractor], [priority]]  = surfaceSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Other Imported':
            suppliesByPriority.loc[[contractor], [priority]]  = otherImportedSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Groundwater':
            suppliesByPriority.loc[[contractor], [priority]]  = groundwaterSupplyData[futureYear].loc[[contractor]].values[0]

setSupplyByPriority('Priority 1')
setSupplyByPriority('Priority 2')
setSupplyByPriority('Priority 3')
setSupplyByPriority('Priority 4')
setSupplyByPriority('Priority 5')
setSupplyByPriority('Priority 6')
setSupplyByPriority('Priority 7')

print(suppliesByPriority)