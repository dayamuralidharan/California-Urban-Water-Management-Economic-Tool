import pandas as pd

from readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from readDemandAssumptions import totalDemands, baseConservation 
from readSupplyAssumptions import suppliesByPriority, swpCVPSupplyData

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

    contractorInitialSurfaceCarryoverStorage = []
    
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

        if contractorDemandsAfterSupplyPriority1 > 0:
            contractorDemandsAfterSupplyPriority2 = contractorDemandsAfterSupplyPriority1 - contractorSupplyPriority2
            
            if contractorDemandsAfterSupplyPriority2 > 0:
                contractorDemandsAfterSupplyPriority3 = contractorDemandsAfterSupplyPriority2 - contractorSupplyPriority3
            
                if contractorDemandsAfterSupplyPriority3 > 0:
                    contractorDemandsAfterSupplyPriority4 = contractorDemandsAfterSupplyPriority3 - contractorSupplyPriority4
                
                    if contractorDemandsAfterSupplyPriority4 > 0:
                        contractorDemandsAfterSupplyPriority5 = contractorDemandsAfterSupplyPriority4 - contractorSupplyPriority5

                        if contractorDemandsAfterSupplyPriority5 > 0:
                            contractorDemandsAfterSupplyPriority6 = contractorDemandsAfterSupplyPriority5 - contractorSupplyPriority6

                            if contractorDemandsAfterSupplyPriority6 > 0:
                                contractorDemandsToBeMetBySWPCVP = contractorDemandsAfterSupplyPriority6 - contractorSupplyPriority7
                                
                                if contractorDemandsToBeMetBySWPCVP > 0:
                                    contractorDemandsToBeMetByCarryover = contractorDemandsToBeMetBySWPCVP - contractorSWPCVPSupply
                                else:
                                    contractorExcessSupply = -1*contractorDemandsToBeMetBySWPCVP 
                                    contractorDemandsToBeMetByCarryover = 0
                            else:
                                contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                                contractorDemandsToBeMetBySWPCVP = 0
                                contractorDemandsToBeMetByCarryover = 0
                        else:
                            contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                            contractorDemandsToBeMetBySWPCVP = 0
                            contractorDemandsToBeMetByCarryover = 0
                    else:
                        contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority4 + contractorSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                        contractorDemandsToBeMetBySWPCVP = 0
                        contractorDemandsToBeMetByCarryover = 0
                else:
                    contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority3 + contractorSupplyPriority4 + contractorSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                    contractorDemandsToBeMetBySWPCVP = 0
                    contractorDemandsToBeMetByCarryover = 0
            else:
                contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority2 + contractorSupplyPriority3 + contractorSupplyPriority4 + contractorSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                contractorDemandsToBeMetBySWPCVP = 0
                contractorDemandsToBeMetByCarryover = 0
        else:
            contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority1 + contractorSupplyPriority2 + contractorSupplyPriority3 + contractorSupplyPriority4 + contractorSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
            contractorDemandsToBeMetBySWPCVP = 0

        
        
        # Put excess supplies into carryover storage
        #if contractorExcessSupplies > 0 and excess supply switch = 1:
            # Input into SW Storage = min(excess supply, available capacity (max capacity - storage from prev timestep), surface put capacity)
            # Input into groundwater storage = min(excess supply - what was put into surface storage, available capacity (max capacity - storage from prev timestep), groundwater put capacity)
        
        # Supply remaining demand by available carryover supply
        # Start with surface carryover, then if there is still remaining demand use groundwater carryover.
        #if contractorDemandsToBeMetByCarryover > 0 and excess supply swith = 1:

        

    demandsAfterBaseConservation[contractor] = contractorDemandsAfterBaseConservation
    demandsToBeMetBySWPCVP[contractor] = contractorDemandsToBeMetBySWPCVP
    demandsToBeMetByCarryoverStorage[contractor] = contractorDemandsToBeMetByCarryover



demandsAfterBaseConservation = pd.DataFrame(demandsAfterBaseConservation)