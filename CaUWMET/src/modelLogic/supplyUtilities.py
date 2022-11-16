from src.modelLogic.modelUtilities import lookupCorrespondingValue

def setSupplyByPriority(priority, supplyPriorityDataframe, recycledSupplyData, potableReuseSupplyData, desalinationSupplyData, contractualTransfersSupplyData, surfaceSupplyData, otherImportedSupplyData, groundwaterSupplyData, futureYear, contractorsList):
    for contractor in contractorsList:
        contractorSupplyTypeByPriority = lookupCorrespondingValue(supplyPriorityDataframe, contractor, colA='Contractor', colB=priority)
        if contractorSupplyTypeByPriority == 'Recycled':
            supplyPriorityDataframe.loc[[contractor], [priority]] = recycledSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Potable Reuse':
            supplyPriorityDataframe.loc[[contractor], [priority]] = potableReuseSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Desalination':
            supplyPriorityDataframe.loc[[contractor], [priority]]  = desalinationSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Contractual Transfers':
            supplyPriorityDataframe.loc[[contractor], [priority]]  = contractualTransfersSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Surface':
            supplyPriorityDataframe.loc[[contractor], [priority]]  = surfaceSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Other Imported':
            supplyPriorityDataframe.loc[[contractor], [priority]]  = otherImportedSupplyData[futureYear].loc[[contractor]].values[0]
        if contractorSupplyTypeByPriority == 'Groundwater':
            supplyPriorityDataframe.loc[[contractor], [priority]]  = groundwaterSupplyData[futureYear].loc[[contractor]].values[0]