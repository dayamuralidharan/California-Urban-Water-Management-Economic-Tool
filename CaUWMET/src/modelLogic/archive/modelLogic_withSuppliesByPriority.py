import pandas as pd
from readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from readDemandAssumptions import totalDemands, plannedLongTermConservation 
from readSupplyAssumptions import swpCVPSupply
from readSystemOperationsAssumptions import carryoverStorageData, excessWaterSwitchData
from modelUtilities import meetDemandsBySupplyPriority

#TODO: Add water management options to suppliesByPriority data

# Set up time series dataframes for each variable represented as a black box in model logic schematic
demandsAfterBaseConservation = {'Year': historicHydrologyYears}
contractorDemandsToBeMetBySWPCVP = {'Year': historicHydrologyYears}
demandsToBeMetByCarryoverStorage = {'Year': historicHydrologyYears}
demandsToBeMetByContingentOptions = {'Year': historicHydrologyYears}
excessSupply = {'Year': historicHydrologyYears}


for contractor in contractorsList:
    # Set up variables that will be used for calcs by contractor
    contractorDemandsAfterBaseConservation = []
    contractorTotalDemand = totalDemands[contractor]
    contractorDemandsToBeMetBySWPCVP = []
    contractorDemandsToBeMetBySWPCVP = []

    contractorExcessSupply = []
    contractorDemandsToBeMetByCarryover = []

    contractorExcessSupplySwitch = excessWaterSwitchData['Switch'].loc[[contractor]].values[0]


    for i in range(len(historicHydrologyYears)):
        # Calculate demands after long-term base conservation
        contractorBaseLongTermConservation = plannedLongTermConservation[plannedLongTermConservation['Contractor'] == contractor][futureYear].values[0]
        contractorDemandsAfterBaseConservation.append(contractorTotalDemand[i] - contractorBaseLongTermConservation)

        # Subtract local supplies from demands after base long-term conservation in order of priority
        # Also track for excess supplies
        # contractorSupplyPriority1 = suppliesByPriority['Priority 1'].loc[[contractor]].values[0]
        # contractorSupplyPriority2 = suppliesByPriority['Priority 2'].loc[[contractor]].values[0]
        # contractorSupplyPriority3 = suppliesByPriority['Priority 3'].loc[[contractor]].values[0]
        # contractorSupplyPriority4 = suppliesByPriority['Priority 4'].loc[[contractor]].values[0]
        # contractorSupplyPriority5 = suppliesByPriority['Priority 5'].loc[[contractor]].values[0]
        # contractorSupplyPriority6 = suppliesByPriority['Priority 6'].loc[[contractor]].values[0]
        # contractorSupplyPriority7 = suppliesByPriority['Priority 7'].loc[[contractor]].values[0]
        contractorSWPCVPSupply = swpCVPSupply[contractor][i]

        contractorDemandsToBeMetBySWPCVP = contractorDemandsAfterBaseConservation #- contractorSupplyPriority1
        
        # meetDemandsBySupplyPriorityOutput = meetDemandsBySupplyPriority(
        # i,
        # contractorDemandsToBeMetBySWPCVP,
        # # contractorSupplyPriority2, 
        # # contractorSupplyPriority3, 
        # # contractorSupplyPriority4, 
        # # contractorSupplyPriority5, 
        # # contractorSupplyPriority6, 
        # # contractorSupplyPriority7, 
        # contractorSWPCVPSupply)

        # #contractorDemandsToBeMetBySWPCVP.append(meetDemandsBySupplyPriorityOutput[0])
        # contractorExcessSupply.append(meetDemandsBySupplyPriorityOutput[1])
        # contractorDemandsToBeMetByCarryover.append(meetDemandsBySupplyPriorityOutput[2])


        # if contractorExcessSupplySwitch == 1:
        #     contractorCarryoverStorageDf = carryoverStorageData.loc[[contractor]]
        #     if i == 0:
        #         contractorSurfaceCarryoverStorage = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface initial storage (acre-feet)'][futureYear].values[0]
        #         contractorGroundwaterCarryoverStorage = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater initial storage (acre-feet)'][futureYear].values[0]
        #     ## If there are excess supplies, put into carryover storage
        #     if contractorExcessSupply > 0:
        #         contractorSurfaceMaximumCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface max storage capacity (acre-feet)'][futureYear].values[0]
        #         contractorSurfaceMaximumPutCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface max put capacity (acre-feet)'][futureYear].values[0]
        #         availableSurfaceCapacity = contractorSurfaceMaximumCapacity - contractorSurfaceCarryoverStorage
        #         inputSWStorage = min(contractorExcessSupply, min(availableSurfaceCapacity, contractorSurfaceMaximumPutCapacity))
        #         contractorExcessSupply = contractorExcessSupply - inputSWStorage
        #         contractorSurfaceCarryoverStorage = contractorSurfaceCarryoverStorage + inputSWStorage
        #         if contractorExcessSupply > 0:
        #             contractorGroundwaterMaximumCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater max storage capacity (acre-feet)'][futureYear].values[0]
        #             contractorGroundwaterMaximumPutCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater max put capacity (acre-feet)'][futureYear].values[0]
        #             availableGroundwaterCapacity = contractorGroundwaterMaximumCapacity - contractorGroundwaterCarryoverStorage
        #             inputGWStorage = min(contractorExcessSupply, min(availableGroundwaterCapacity, contractorGroundwaterMaximumPutCapacity))
        #             contractorExcessSupply = contractorExcessSupply - inputGWStorage
        #             contractorGroundwaterCarryoverStorage = contractorGroundwaterCarryoverStorage + inputGWStorage
        #     #if contractorExcessSupplies > 0 and excess supply switch = 1:
        #         # Input into SW Storage = min(excess supply, available capacity (max capacity - storage from prev timestep), surface put capacity)
        #         # Input into groundwater storage = min(excess supply - what was put into surface storage, available capacity (max capacity - storage from prev timestep), groundwater put capacity)

        #     if contractorDemandsToBeMetByCarryover > 0:
        #         if contractorSurfaceCarryoverStorage > 0:
        #             contractorSurfaceMaximumTakeCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface max take capacity (acre-feet)'][futureYear].values[0]
        #             contractorSurfaceTakeLoss = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface take loss (% of take)'][futureYear].values[0]
        #             outputSWStorage = min((1 + contractorSurfaceTakeLoss) * contractorDemandsToBeMetByCarryover, min(contractorSurfaceCarryoverStorage, contractorSurfaceMaximumTakeCapacity))
        #             contractorDemandsToBeMetByCarryover = contractorDemandsToBeMetByCarryover - ((1 - contractorSurfaceTakeLoss) * outputSWStorage)
        #             contractorSurfaceCarryoverStorage = contractorSurfaceCarryoverStorage - outputSWStorage
        #             if contractorDemandsToBeMetByCarryover > 0:
        #                 contractorGroundwaterMaximumTakeCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater max take capacity (acre-feet)'][futureYear].values[0]
        #                 contractorGroundwaterTakeLoss = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater take loss (% of take)'][futureYear].values[0]
        #                 outputGWStorage = min((1 + contractorGroundwaterTakeLoss) * contractorDemandsToBeMetByCarryover, min(contractorGroundwaterCarryoverStorage, contractorGroundwaterMaximumTakeCapacity))
        #                 contractorDemandToBeMetByContingentOptions = contractorDemandsToBeMetByCarryover - ((1 - contractorGroundwaterTakeLoss) * outputGWStorage)
        #                 contractorGroundwaterCarryoverStorage = contractorGroundwaterCarryoverStorage - outputSWStorage
        #     ## If there is remaining demand to be met by carryover storage, supply remaining demand with available carryover supply
        #     ## Start with surface carryover, then if there is still remaining demand use groundwater carryover.
        #     # if contractorDemandsToBeMetByCarryover > 0 and excess supply swith = 1:
        #     ## If there is still remaining demand after carryover storage has been allocated, return the remaining demand as a variable called contractorDemandToBeMetByContingentOptions

        
    demandsAfterBaseConservation[contractor] = contractorDemandsAfterBaseConservation
    contractorDemandsToBeMetBySWPCVP[contractor] = contractorDemandsToBeMetBySWPCVP
    demandsToBeMetByCarryoverStorage[contractor] = contractorDemandsToBeMetByCarryover
    excessSupply[contractor] = contractorExcessSupply
    



demandsAfterBaseConservation = pd.DataFrame(demandsAfterBaseConservation)
contractorDemandsToBeMetBySWPCVP = pd.DataFrame(contractorDemandsToBeMetBySWPCVP)
demandsToBeMetByCarryoverStorage = pd.DataFrame(demandsToBeMetByCarryoverStorage)

print(demandsAfterBaseConservation)
print(contractorDemandsToBeMetBySWPCVP)
print(demandsToBeMetByCarryoverStorage)