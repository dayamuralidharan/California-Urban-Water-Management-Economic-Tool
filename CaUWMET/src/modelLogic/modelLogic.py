import pandas as pd
from readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from readDemandAssumptions import totalDemands, plannedLongTermConservation
from readSupplyAssumptions import totalLocalSupply, swpCVPSupply
from readSystemOperationsAssumptions import storageData, excessWaterSwitchData, storageHedgingStrategyData

#TODO: Add water management options to local supplies

# Set up time series dataframes for each variable. These dataframes include time series for all contractors.
appliedDemands = {'Year': historicHydrologyYears}
demandsToBeMetBySWPCVP = {'Year': historicHydrologyYears}
demandsToBeMetByCarryoverSupply = {'Year': historicHydrologyYears}
demandsToBeMetByBankedGWSupply = {'Year': historicHydrologyYears}
excessSupply = {'Year': historicHydrologyYears}

# Loop through model calculations for each contractor. All variables in this loop start with "contractor" to indicate it is only used in this loop.
for contractor in contractorsList:
    # Set up variables that will be used for calcs by contractor
    contractorTotalDemand = totalDemands[contractor]
    contractorAppliedDemand = []
    contractordemandsToBeMetBySWPCVP = []
    contractorDemandsToBeMetByCarryover = []
    contractorDemandsToBeMetByBankedGW = []

    contractorExcessSupplySwitch = excessWaterSwitchData['Switch'].loc[[contractor]].values[0]
    contractorExcessSupply = []

    for i in range(len(historicHydrologyYears)):
        # Calculate Applied Demand after subtraction of Planned Long-term Conservation
        contractorPlannedLongTermConservation = plannedLongTermConservation[plannedLongTermConservation['Contractor'] == contractor][futureYear].values[0]
        contractorAppliedDemand.append(contractorTotalDemand[i] - contractorPlannedLongTermConservation)

        # Calculate Demand to be Met by SWP/CVP supplies after subtraction of local supplies
        contractordemandsToBeMetBySWPCVP.append(max(0, contractorAppliedDemand[i] - totalLocalSupply[contractor][i]))

        # Calculate Demand to be Met by Stored supplies after subtraction of SWP/CVP supplies, or calculate Excess Supply.
        contractorSWPCVPSupply = swpCVPSupply[contractor][i]
        if contractordemandsToBeMetBySWPCVP[i] - contractorSWPCVPSupply > 0:
            contractorDemandsToBeMetByCarryover.append(contractordemandsToBeMetBySWPCVP[i] - contractorSWPCVPSupply)
            contractorExcessSupply.append(0)
        else:
            contractorExcessSupply.append(-1* (contractordemandsToBeMetBySWPCVP[i] - contractorSWPCVPSupply))
            contractorDemandsToBeMetByCarryover.append(0)

        ## contractorExcessSupplySwitch options:
        """
        "Turn Back Pool",
        "Reduce Groundwater Pumping",
        "Put into Carryover Storage",
        "Put into Groundwater Bank",
        "Put into Carryover and Groundwater Bank"
        """

        # if contractorExcessSupplySwitch == "Put into Carryover and Groundwater Bank":
        contractorCarryoverStorageDf = storageData.loc[[contractor]]
        if i == 0:
            volumeSurfaceCarryover = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface initial storage (acre-feet)'][futureYear].values[0]
            volumeGroundwaterBank = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater initial storage (acre-feet)'][futureYear].values[0]
        ## If there are excess supplies, put into groundwater bank first, then surface carryover storage
        if contractorExcessSupply[i] > 0:
            if contractorExcessSupplySwitch in ["Put into Carryover and Groundwater Bank", "Put into Groundwater Bank"]:
                contractorGroundwaterMaximumCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater max storage capacity (acre-feet)'][futureYear].values[0]
                contractorGroundwaterMaximumPutCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater max put capacity (acre-feet)'][futureYear].values[0]
                contractorRechargeEffectiveness = (contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Recharge Effectiveness (%)'][futureYear].values[0] / 100)  # Converted from % into fraction
                availableCapacity_Groundwater = contractorGroundwaterMaximumCapacity - volumeGroundwaterBank
                putGroundwater = max(min(contractorExcessSupply[i], availableCapacity_Groundwater, contractorGroundwaterMaximumPutCapacity) * contractorRechargeEffectiveness, 0)
                contractorExcessSupply[i] = contractorExcessSupply[i] - putGroundwater
                volumeGroundwaterBank = volumeGroundwaterBank + putGroundwater
            if contractorExcessSupply[i] > 0 and contractorExcessSupplySwitch in ["Put into Carryover and Groundwater Bank", "Put into Carryover Storage"]:
                contractorSurfaceMaximumCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface max storage capacity (acre-feet)'][futureYear].values[0]
                contractorSurfaceMaximumPutCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface max put capacity (acre-feet)'][futureYear].values[0]
                availableCapacity_Surface = contractorSurfaceMaximumCapacity - volumeSurfaceCarryover
                putSurface = max(min(contractorExcessSupply[i], availableCapacity_Surface, contractorSurfaceMaximumPutCapacity), 0)
                contractorExcessSupply[i] = contractorExcessSupply[i] - putSurface
                volumeSurfaceCarryover = volumeSurfaceCarryover + putSurface

        ## storageHedgingStrategySwitch:
        """
        "Surface Carryover Only",
        "Groundwater Bank Only",
        "Surface and Groundwater Storage",
        "Off"
        """
        contractorStorageHedgingStrategyDf = storageHedgingStrategyData.loc[[contractor]]
        storageHedgingStrategySwitch = contractorStorageHedgingStrategyDf[contractorStorageHedgingStrategyDf['Variable'] == 'Storage Hedging Strategy Switch']['Value'].values[0]
        contractorSurfaceStorageAnnualLoss = (contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface loss (AFY)'][futureYear].values[0])
        
        volumeSurfaceCarryover = max(volumeSurfaceCarryover - contractorSurfaceStorageAnnualLoss, 0)
        
        if contractorDemandsToBeMetByCarryover[i] > 0:
            if volumeSurfaceCarryover > 0:
                # Apply Hedging strategy if switched on 
                if storageHedgingStrategySwitch in ["Surface Carryover Only", "Surface and Groundwater Storage"]:
                    contractorSurfaceMaximumCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface max storage capacity (acre-feet)'][futureYear].values[0]
                    pctCapacity_SurfaceCarryover = (volumeSurfaceCarryover / contractorSurfaceMaximumCapacity)
                    pctStorageCalled_SurfaceCarryover = (contractorDemandsToBeMetByCarryover[i] / volumeSurfaceCarryover)
                    hedgingPoint = (contractorStorageHedgingStrategyDf[contractorStorageHedgingStrategyDf['Variable'] == 'Hedging Point (%)']['Value'].values[0] / 100.)  # Converting % into fraction
                    if pctCapacity_SurfaceCarryover <= hedgingPoint:
                        hedgeCallStorageFactor = contractorStorageHedgingStrategyDf[contractorStorageHedgingStrategyDf['Variable'] == 'Hedge Call/Storage Factor']['Value'].values[0]
                        hedgingStorageCapacityFactor = contractorStorageHedgingStrategyDf[contractorStorageHedgingStrategyDf['Variable'] == 'Hedging Storage/Capacity Factor']['Value'].values[0]
                        contractorSurfaceMaximumTakeCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Surface max take capacity (acre-feet)'][futureYear].values[0]
                        takeSurface = min(
                            (1 - hedgeCallStorageFactor * pctStorageCalled_SurfaceCarryover * (pctCapacity_SurfaceCarryover ** -hedgingStorageCapacityFactor)) * volumeSurfaceCarryover,
                            volumeSurfaceCarryover,
                            contractorDemandsToBeMetByCarryover[i],
                            contractorSurfaceMaximumTakeCapacity
                        )
                else:
                    takeSurface = min(volumeSurfaceCarryover, contractorDemandsToBeMetByCarryover[i], contractorSurfaceMaximumTakeCapacity)
        else:
            takeSurface = 0
                
        volumeSurfaceCarryover = volumeSurfaceCarryover - takeSurface
        contractorDemandsToBeMetByBankedGW[i] = contractorDemandsToBeMetByCarryover[i] - takeSurface
            
        if contractorDemandsToBeMetByBankedGW[i] > 0:
            if volumeGroundwaterBank > 0:
            # Apply Hedging strategy if switched on
                if storageHedgingStrategySwitch in ["Groundwater Bank Only", "Surface and Groundwater Storage"]:
                    hedgingPoint = (contractorStorageHedgingStrategyDf[contractorStorageHedgingStrategyDf['Variable'] == 'Hedging Point (%)']['Value'].values[0] / 100.)  # Converting % into fraction
                    hedgeCallStorageFactor = contractorStorageHedgingStrategyDf[contractorStorageHedgingStrategyDf['Variable'] == 'Hedge Call/Storage Factor']['Value'].values[0]
                    hedgingStorageCapacityFactor = contractorStorageHedgingStrategyDf[contractorStorageHedgingStrategyDf['Variable'] == 'Hedging Storage/Capacity Factor']['Value'].values[0]
                    contractorGroundwaterMaximumCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater max storage capacity (acre-feet)'][futureYear].values[0]
                    pctCapacity_GroundwaterBank = (volumeGroundwaterBank / contractorGroundwaterMaximumCapacity)
                    pctStorageCalled_GroundwaterBank = (contractorDemandsToBeMetByBankedGW[i] / volumeGroundwaterBank)
                    contractorGroundwaterMaximumTakeCapacity = contractorCarryoverStorageDf[contractorCarryoverStorageDf['Variable'] == 'Groundwater max take capacity (acre-feet)'][futureYear].values[0]
                    if pctCapacity_GroundwaterBank <= hedgingPoint and storageHedgingStrategySwitch in ["Groundwater Bank Only", "Surface and Groundwater Storage"]:
                        takeGroundwater = min(
                            (1 - hedgeCallStorageFactor * pctStorageCalled_GroundwaterBank * (pctCapacity_GroundwaterBank ** -hedgingStorageCapacityFactor)) * volumeGroundwaterBank,
                            contractorDemandsToBeMetByBankedGW[i],
                            contractorGroundwaterMaximumTakeCapacity
                        )
                else:
                    takeGroundwater = min(contractorDemandsToBeMetByBankedGW[i], contractorGroundwaterMaximumTakeCapacity)
        else:
            takeGroundwater = 0
        
        volumeGroundwaterBank = volumeGroundwaterBank - takeGroundwater
        contractorDemandToBeMetByContingentOptions = contractorDemandsToBeMetByBankedGW[i] - takeGroundwater


    appliedDemands[contractor] = contractorAppliedDemand
    demandsToBeMetBySWPCVP[contractor] = contractordemandsToBeMetBySWPCVP
#     demandsToBeMetByStoredSupply[contractor] = contractorDemandsToBeMetByCarryover
#     excessSupply[contractor] = contractorExcessSupply




appliedDemands = pd.DataFrame(appliedDemands)
demandsToBeMetBySWPCVP = pd.DataFrame(demandsToBeMetBySWPCVP)
# demandsToBeMetByStoredSupply = pd.DataFrame(demandsToBeMetByStoredSupply)

# print(appliedDemands)
# print(demandsToBeMetBySWPCVP)
# print(demandsToBeMetByStoredSupply)