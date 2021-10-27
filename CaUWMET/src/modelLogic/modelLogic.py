import pandas as pd

from readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from readDemandAssumptions import totalDemands, baseConservation 
from readSupplyAssumptions import suppliesByPriority, swpCVPSupplyData
from modelUtilities import meetDemandsBySupplyPriority

#TODO: Add water management options to suppliesByPriority data

# Set up time series dataframes for each variable represented as a black box in model logic schematic
demandsAfterBaseConservation = {'Year': historicHydrologyYears}
demandsToBeMetBySWPCVP = {'Year': historicHydrologyYears}
demandsToBeMetByCarryoverStorage = {'Year': historicHydrologyYears}
demandsToBeMetByContingentOptions = {'Year': historicHydrologyYears}


for contractor in contractorsList:
    # Set up variables that will be used for calcs by contractor
    contractorDemandsAfterBaseConservation = []
    contractorTotalDemand = totalDemands[contractor]
    
    contractorDemandsAfterSupplyPriority1 = []
    contractorDemandsAfterSupplyPriority2 = []
    contractorDemandsAfterSupplyPriority3 = []
    contractorDemandsAfterSupplyPriority4 = []
    contractorDemandsAfterSupplyPriority5 = []
    contractorDemandsAfterSupplyPriority6 = []
    contractorDemandsAfterSupplyPriority7 = []
    
    contractorDemandsToBeMetBySWPCVP = []

    contractorExcessSupply = []
    contractorDemandsToBeMetByCarryover = []

    
    for i in range(len(historicHydrologyYears)):
        # Calculate demands after long-term base conservation
        contractorBaseLongTermConservation = baseConservation[baseConservation['Contractor'] == contractor][futureYear].values[0]
        contractorDemandsAfterBaseConservation.append(contractorTotalDemand[i] - contractorBaseLongTermConservation)

        # Subtract local supplies from demands after base long-term conservation in order of priority
        # Also track for excess supplies
        contractorSupplyPriority1 = suppliesByPriority['Priority 1'].loc[[contractor]].values[0]
        contractorSupplyPriority2 = suppliesByPriority['Priority 2'].loc[[contractor]].values[0]
        contractorSupplyPriority3 = suppliesByPriority['Priority 3'].loc[[contractor]].values[0]
        contractorSupplyPriority4 = suppliesByPriority['Priority 4'].loc[[contractor]].values[0]
        contractorSupplyPriority5 = suppliesByPriority['Priority 5'].loc[[contractor]].values[0]
        contractorSupplyPriority6 = suppliesByPriority['Priority 6'].loc[[contractor]].values[0]
        contractorSupplyPriority7 = suppliesByPriority['Priority 7'].loc[[contractor]].values[0]
        contractorSWPCVPSupply = swpCVPSupplyData[contractor][i]

        contractorDemandsAfterSupplyPriority1 = contractorDemandsAfterBaseConservation - contractorSupplyPriority1

        meetDemandsBySupplyPriorityOutput = meetDemandsBySupplyPriority(contractorDemandsAfterSupplyPriority1, contractorSupplyPriority2, contractorSupplyPriority3, contractorSupplyPriority4, contractorSupplyPriority5, contractorSupplyPriority6, contractorSupplyPriority7, contractorSWPCVPSupply)

        contractorExcessSupply = meetDemandsBySupplyPriorityOutput[0]
        contractorDemandsToBeMetByCarryover = meetDemandsBySupplyPriorityOutput[1]

        
        
        ## If there are excess supplies, put into carryover storage
        #if contractorExcessSupplies > 0 and excess supply switch = 1:
            # Input into SW Storage = min(excess supply, available capacity (max capacity - storage from prev timestep), surface put capacity)
            # Input into groundwater storage = min(excess supply - what was put into surface storage, available capacity (max capacity - storage from prev timestep), groundwater put capacity)
        
        ## If there is remaining demand to be met by carryover storage, supply remaining demand with available carryover supply
        ## Start with surface carryover, then if there is still remaining demand use groundwater carryover.
        # if contractorDemandsToBeMetByCarryover > 0 and excess supply swith = 1:

        ## If there is still remaining demand after carryover storage has been allocated, return the remaining demand as a variable called contractorDemandToBeMetByContingentOptions

        

    demandsAfterBaseConservation[contractor] = contractorDemandsAfterBaseConservation
    demandsToBeMetBySWPCVP[contractor] = contractorDemandsToBeMetBySWPCVP
    demandsToBeMetByCarryoverStorage[contractor] = contractorDemandsToBeMetByCarryover
    



demandsAfterBaseConservation = pd.DataFrame(demandsAfterBaseConservation)
demandsToBeMetBySWPCVP = pd.DataFrame(demandsToBeMetBySWPCVP)
demandsToBeMetByCarryoverStorage = pd.DataFrame(demandsToBeMetByCarryoverStorage)