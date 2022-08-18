import pandas as pd
from readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from readDemandAssumptions import totalDemands, plannedLongTermConservation
from readSupplyAssumptions import totalLocalSupply, swpCVPSupply
from readSystemOperationsAssumptions import storageData,  storageHedgingStrategyData, excessWaterSwitchData
from storageUtilities import putOrTakeFromStorage


#TODO: Add water management options to local supplies

# Initialize time series dataframes for each variable. These dataframes include time series for all contractors.
appliedDemands = {'Year': historicHydrologyYears}
demandsToBeMetBySWPCVP = {'Year': historicHydrologyYears}
demandsToBeMetByCarryover = {'Year': historicHydrologyYears}
demandsToBeMetByBankedGW = {'Year': historicHydrologyYears}
excessSupply = {'Year': historicHydrologyYears}

# Surface carryover and banked groundwater storage dataframes
volumeSurfaceCarryover = {'Year': historicHydrologyYears}
volumeGroundwaterBank = {'Year': historicHydrologyYears}
availableCapacitySurface = {'Year': historicHydrologyYears}
availableGroundwaterCapacity = {'Year': historicHydrologyYears}
putGroundwater = {'Year': historicHydrologyYears}
putSurface = {'Year': historicHydrologyYears}
takeSurface = {'Year': historicHydrologyYears}
takeGroundwater = {'Year': historicHydrologyYears}

# Hedging strategy dataframes
pctCapacitySurfaceCarryover = {'Year': historicHydrologyYears}
pctStorageCalledSurfaceCarryover = {'Year': historicHydrologyYears}
pctCapacityGroundwaterBank = {'Year': historicHydrologyYears}
pctStorageCalledGroundwaterBank = {'Year': historicHydrologyYears}

# Loop through model calculations for each contractor. All variables in this loop start with "contractor" to indicate it is only used in this loop.
for contractor in contractorsList:
    # Set up variables that will be used for calcs by contractor
    totalDemand_Contractor = totalDemands[contractor]
    appliedDemand_Contractor = []
    demandsToBeMetBySWPCVP_Contractor = []
    
    demandsToBeMetByCarryover_Contractor = []
    # demandsToBeMetByBankedGW_Contractor = []

    excessSupplySwitch_Contractor = excessWaterSwitchData['Switch'].loc[[contractor]].values[0]
    excessSupply_Contractor = []
    
    volumeSurfaceCarryover_Contractor = []
    volumeGroundwaterBank_Contractor = []
    storageInputDf_Contractor = storageData.loc[[contractor]]
    
    demandToBeMetByContingentOptions_Contractor = []

    for i in range(len(historicHydrologyYears)):
        # Calculate Applied Demand after subtraction of Planned Long-term Conservation
        plannedLongTermConservation_Contractor = plannedLongTermConservation[plannedLongTermConservation['Contractor'] == contractor][futureYear].values[0]
        appliedDemand_Contractor.append(totalDemand_Contractor[i] - plannedLongTermConservation_Contractor)

        # Calculate Demand to be Met by SWP/CVP supplies after subtraction of local supplies
        demandsToBeMetBySWPCVP_Contractor.append(max(0, appliedDemand_Contractor[i] - totalLocalSupply[contractor][i]))

        # Calculate Demand to be Met by Stored supplies after subtraction of SWP/CVP supplies, or calculate Excess Supply.
        SWPCVPSupply_Contractor = swpCVPSupply[contractor][i]
        if demandsToBeMetBySWPCVP_Contractor[i] - SWPCVPSupply_Contractor > 0:
            demandsToBeMetByCarryover_Contractor.append(demandsToBeMetBySWPCVP_Contractor[i] - SWPCVPSupply_Contractor)
            excessSupply_Contractor.append(0)
        else:
            excessSupply_Contractor.append(-1* (demandsToBeMetBySWPCVP_Contractor[i] - SWPCVPSupply_Contractor))
            demandsToBeMetByCarryover_Contractor.append(0)

        # Initialize storage volumes each time step
        if i == 0: #Initial storage volumes
            volumeSurfaceCarryover_Contractor.append(storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface initial storage (acre-feet)'][futureYear].values[0])
            volumeGroundwaterBank_Contractor.append(storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater initial storage (acre-feet)'][futureYear].values[0])
        else: # Initialize with previous time step's volumes which are updated in the putOrTakeFromStorage function
            volumeSurfaceCarryover_Contractor.append(volumeSurfaceCarryover_Contractor[i-1])
            volumeGroundwaterBank_Contractor.append(volumeGroundwaterBank_Contractor[i-1])
        
        excessSupplySwitch_Contractor = excessWaterSwitchData['Switch'].loc[[contractor]].values[0]
        storageInputDf_Contractor = storageData.loc[[contractor]]
        groundwaterMaximumCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater max storage capacity (acre-feet)'][futureYear].values[0]
        groundwaterMaximumPutCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater max put capacity (acre-feet)'][futureYear].values[0]
        groundwaterMaximumTakeCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater max take capacity (acre-feet)'][futureYear].values[0]
        rechargeEffectiveness_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Recharge Effectiveness (%)'][futureYear].values[0] / 100 # Converted from % into fraction
        
        surfaceMaximumCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max storage capacity (acre-feet)'][futureYear].values[0]
        surfaceMaximumPutCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max put capacity (acre-feet)'][futureYear].values[0]
        surfaceMaximumTakeCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max take capacity (acre-feet)'][futureYear].values[0]
        surfaceStorageAnnualLoss_Contractor = (storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface loss (AFY)'][futureYear].values[0])
        
        storageHedgingStrategyDf_Contractor = storageHedgingStrategyData.loc[[contractor]]
        storageHedgingStrategySwitch_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Storage Hedging Strategy Switch']['Value'].values[0]
        hedgingPoint_Contractor = int(storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedging Point (%)']['Value'].values[0])
        hedgingPoint_Contractor = hedgingPoint_Contractor / 100  # Converting % into fraction
        hedgeCallStorageFactor_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedge Call/Storage Factor']['Value'].values[0]
        hedgingStorageCapacityFactor_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedging Storage/Capacity Factor']['Value'].values[0]
        
        putOrTakeFromStorage(i, contractor, futureYear, 
                             storageInputDf_Contractor, 
                             excessSupply_Contractor, excessSupplySwitch_Contractor, 
                             demandsToBeMetByCarryover_Contractor, 
                             volumeSurfaceCarryover_Contractor, volumeGroundwaterBank_Contractor,
                             groundwaterMaximumCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor, groundwaterMaximumTakeCapacity_Contractor, rechargeEffectiveness_Contractor,
                             surfaceMaximumCapacity_Contractor, surfaceMaximumPutCapacity_Contractor, surfaceMaximumTakeCapacity_Contractor, surfaceStorageAnnualLoss_Contractor,
                             storageHedgingStrategySwitch_Contractor, hedgingPoint_Contractor, hedgeCallStorageFactor_Contractor, hedgingStorageCapacityFactor_Contractor,
                             demandToBeMetByContingentOptions_Contractor)
        
        ## contractorExcessSupplySwitch options:
        """
        "Turn Back Pool",
        "Reduce Groundwater Pumping",
        "Put into Carryover Storage",
        "Put into Groundwater Bank",
        "Put into Carryover and Groundwater Bank"
        """

        # if contractorExcessSupplySwitch == "Put into Carryover and Groundwater Bank":
        # storageInputDf_Contractor = storageData.loc[[contractor]]
        # if i == 0:
        #     volumeSurfaceCarryover_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface initial storage (acre-feet)'][futureYear].values[0]
        #     volumeGroundwaterBank_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater initial storage (acre-feet)'][futureYear].values[0]
        
        # groundwaterMaximumCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater max storage capacity (acre-feet)'][futureYear].values[0]
        # groundwaterMaximumPutCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater max put capacity (acre-feet)'][futureYear].values[0]
        # rechargeEffectiveness_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Recharge Effectiveness (%)'][futureYear].values[0] / 100 # Converted from % into fraction
        
        # surfaceMaximumCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max storage capacity (acre-feet)'][futureYear].values[0]
        # surfaceMaximumPutCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max put capacity (acre-feet)'][futureYear].values[0]
        
        # availableCapacitySurface_Contractor = surfaceMaximumCapacity_Contractor - volumeSurfaceCarryover_Contractor
        # availableGroundwaterCapacity_Contractor = groundwaterMaximumCapacity_Contractor - volumeGroundwaterBank_Contractor
        
        
        # ## If there are excess supplies, put into groundwater bank first, then surface carryover storage
        # if excessSupply_Contractor[i] > 0:
        #     if excessSupplySwitch_Contractor in ["Put into Carryover and Groundwater Bank", "Put into Groundwater Bank"]:
        #         putGroundwater_Contractor = max(min(excessSupply_Contractor[i], availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor) * rechargeEffectiveness_Contractor, 0)
        #         excessSupply_Contractor[i] = excessSupply_Contractor[i] - putGroundwater_Contractor
        #         volumeGroundwaterBank_Contractor = volumeGroundwaterBank_Contractor + putGroundwater_Contractor
        #     if excessSupply_Contractor[i] > 0 and excessSupplySwitch_Contractor in ["Put into Carryover and Groundwater Bank", "Put into Carryover Storage"]:
        #         putSurface_Contractor = max(min(excessSupply_Contractor[i], availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor), 0)
        #         excessSupply_Contractor[i] = excessSupply_Contractor[i] - putSurface_Contractor
        #         volumeSurfaceCarryover_Contractor = volumeSurfaceCarryover_Contractor + putSurface_Contractor
        # else:
        #     putGroundwater_Contractor = 0
        #     putSurface_Contractor = 0

        # ## If there is remaining demand after local and Project supplies are delivered, take from surface carryover storage first, then banked groundwater
        # ## Apply Hedging Strategy if switched on:
        # """
        # "Surface Carryover Only",
        # "Groundwater Bank Only",
        # "Surface and Groundwater Storage",
        # "Off"
        # """
        # storageHedgingStrategyDf_Contractor = storageHedgingStrategyData.loc[[contractor]]
        # storageHedgingStrategySwitch_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Storage Hedging Strategy Switch']['Value'].values[0]
        # surfaceStorageAnnualLoss_Contractor = (storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface loss (AFY)'][futureYear].values[0])
        # surfaceMaximumTakeCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max take capacity (acre-feet)'][futureYear].values[0]
        # groundwaterMaximumTakeCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater max take capacity (acre-feet)'][futureYear].values[0]

        # volumeSurfaceCarryover_Contractor = max(volumeSurfaceCarryover_Contractor - surfaceStorageAnnualLoss_Contractor, 0)
        
        # hedgingPoint_Contractor = int(storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedging Point (%)']['Value'].values[0])
        # hedgingPoint_Contractor = hedgingPoint_Contractor / 100  # Converting % into fraction
        # hedgeCallStorageFactor_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedge Call/Storage Factor']['Value'].values[0]
        # hedgingStorageCapacityFactor_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedging Storage/Capacity Factor']['Value'].values[0]
        
        # # Set surface carryover storage hedging strategy variables
        # if volumeSurfaceCarryover_Contractor > 0:
        #     pctCapacitySurfaceCarryover_Contractor = (volumeSurfaceCarryover_Contractor / surfaceMaximumCapacity_Contractor)
        #     pctStorageCalledSurfaceCarryover_Contractor = (demandsToBeMetByCarryover_Contractor[i] / volumeSurfaceCarryover_Contractor)
            
        # else:
        #     pctCapacitySurfaceCarryover_Contractor = 0
        #     pctStorageCalledSurfaceCarryover_Contractor = 0
        
        # if demandsToBeMetByCarryover_Contractor[i] > 0:
        #     if volumeSurfaceCarryover_Contractor > 0:
        #         # Apply Hedging strategy if switched on 
        #         if storageHedgingStrategySwitch_Contractor in ["Surface Carryover Only", "Surface and Groundwater Storage"]:
        #             if pctCapacitySurfaceCarryover_Contractor <= hedgingPoint_Contractor:
        #                 takeSurface_Contractor = min(
        #                     (1 - hedgeCallStorageFactor_Contractor * pctStorageCalledSurfaceCarryover_Contractor * (pctCapacitySurfaceCarryover_Contractor ** -hedgingStorageCapacityFactor_Contractor)) * volumeSurfaceCarryover_Contractor,
        #                     volumeSurfaceCarryover_Contractor,
        #                     demandsToBeMetByCarryover_Contractor[i],
        #                     surfaceMaximumTakeCapacity_Contractor
        #                 )
        #         else:
        #             takeSurface_Contractor = min(volumeSurfaceCarryover_Contractor, demandsToBeMetByCarryover_Contractor[i], surfaceMaximumTakeCapacity_Contractor)
        # else:
        #     takeSurface_Contractor = 0
                
        # volumeSurfaceCarryover_Contractor = volumeSurfaceCarryover_Contractor - takeSurface_Contractor
        # demandsToBeMetByBankedGW_Contractor.append(demandsToBeMetByCarryover_Contractor[i] - takeSurface_Contractor)
        
        # # Set groundwater bank hedging strategy variables
        # if volumeGroundwaterBank_Contractor > 0:
        #     pctCapacityGroundwaterBank_Contractor = (volumeGroundwaterBank_Contractor / groundwaterMaximumCapacity_Contractor)
        #     pctStorageCalledGroundwaterBank_Contractor = (demandsToBeMetByBankedGW_Contractor[i] / volumeGroundwaterBank_Contractor)
        # else:
        #     pctCapacityGroundwaterBank_Contractor = 0
        #     pctStorageCalledGroundwaterBank_Contractor = 0
        
        
            
        # if demandsToBeMetByBankedGW_Contractor[i] > 0:
        #     if volumeGroundwaterBank_Contractor > 0:
        #     # Apply Hedging strategy if switched on
        #         if storageHedgingStrategySwitch_Contractor in ["Groundwater Bank Only", "Surface and Groundwater Storage"]:
        #             if pctCapacityGroundwaterBank_Contractor <= hedgingPoint_Contractor and storageHedgingStrategySwitch_Contractor in ["Groundwater Bank Only", "Surface and Groundwater Storage"]:
        #                 takeGroundwater_Contractor = min(
        #                     (1 - hedgeCallStorageFactor_Contractor * pctStorageCalledGroundwaterBank_Contractor * (pctCapacityGroundwaterBank_Contractor ** -hedgingStorageCapacityFactor_Contractor)) * volumeGroundwaterBank_Contractor,
        #                     demandsToBeMetByBankedGW_Contractor[i],
        #                     groundwaterMaximumTakeCapacity_Contractor
        #                 )
        #         else:
        #             takeGroundwater_Contractor = min(demandsToBeMetByBankedGW_Contractor[i], groundwaterMaximumTakeCapacity_Contractor)
        # else:
        #     takeGroundwater_Contractor = 0
        
        # volumeGroundwaterBank_Contractor = volumeGroundwaterBank_Contractor - takeGroundwater_Contractor
        # demandToBeMetByContingentOptions_Contractor = demandsToBeMetByBankedGW_Contractor[i] - takeGroundwater_Contractor

# Append dataframes with updated contractor data as calculated in model logic above.
    appliedDemands[contractor] = appliedDemand_Contractor
    demandsToBeMetBySWPCVP[contractor] = demandsToBeMetBySWPCVP_Contractor
    demandsToBeMetByCarryover[contractor] = demandsToBeMetByCarryover_Contractor
    demandsToBeMetByBankedGW[contractor] = demandsToBeMetByBankedGW_Contractor
    excessSupply[contractor] = excessSupply_Contractor
    
    # volumeSurfaceCarryover[contractor] = volumeSurfaceCarryover_Contractor
    # volumeGroundwaterBank[contractor] = volumeGroundwaterBank_Contractor
    # availableCapacitySurface[contractor] = availableCapacitySurface_Contractor
    # availableGroundwaterCapacity[contractor] = availableGroundwaterCapacity_Contractor
    # putGroundwater[contractor] = putGroundwater_Contractor
    # putSurface[contractor] = putSurface_Contractor
    # takeSurface[contractor] = takeSurface_Contractor
    # takeGroundwater[contractor] = takeGroundwater_Contractor
    # pctCapacitySurfaceCarryover[contractor] = pctCapacitySurfaceCarryover_Contractor
    # pctStorageCalledSurfaceCarryover[contractor] = pctStorageCalledSurfaceCarryover_Contractor
    # pctCapacityGroundwaterBank[contractor] = pctCapacityGroundwaterBank_Contractor
    # pctStorageCalledGroundwaterBank[contractor] = pctStorageCalledGroundwaterBank_Contractor




appliedDemands = pd.DataFrame(appliedDemands)
demandsToBeMetBySWPCVP = pd.DataFrame(demandsToBeMetBySWPCVP)
demandsToBeMetByCarryover = pd.DataFrame(demandsToBeMetByCarryover)
excessSupply = pd.DataFrame(excessSupply)

volumeSurfaceCarryover = pd.DataFrame(volumeSurfaceCarryover)
volumeGroundwaterBank = pd.DataFrame(volumeGroundwaterBank)
availableCapacitySurface = pd.DataFrame(availableCapacitySurface)
availableGroundwaterCapacity = pd.DataFrame(availableGroundwaterCapacity)
putGroundwater= pd.DataFrame(putGroundwater)
putSurface = pd.DataFrame(putSurface)
takeSurface= pd.DataFrame(takeSurface)
takeGroundwater = pd.DataFrame(takeGroundwater)

pctCapacitySurfaceCarryover = pd.DataFrame(pctCapacitySurfaceCarryover)
pctStorageCalledSurfaceCarryover = pd.DataFrame(pctStorageCalledSurfaceCarryover)
pctCapacityGroundwaterBank= pd.DataFrame(pctCapacityGroundwaterBank)
pctStorageCalledGroundwaterBank = pd.DataFrame(pctStorageCalledGroundwaterBank)

writer = pd.ExcelWriter('Output_QAQC.xlsx', engine = 'xlsxwriter')
workbook = writer.book

appliedDemands.to_excel(writer, sheet_name = 'appliedDemands')
demandsToBeMetBySWPCVP.to_excel(writer, sheet_name = 'demandsToBeMetBySWPCVP')


# demandsToBeMetByCarryover = pd.DataFrame(demandsToBeMetByCarryover
# excessSupply = pd.DataFrame(excessSupply

# volumeSurfaceCarryover = pd.DataFrame(volumeSurfaceCarryover
# volumeGroundwaterBank = pd.DataFrame(volumeGroundwaterBank
# availableCapacitySurface = pd.DataFrame(availableCapacitySurface
# availableGroundwaterCapacity = pd.DataFrame(availableGroundwaterCapacity
# putGroundwater= pd.DataFrame(putGroundwater
# putSurface = pd.DataFrame(putSurface
# takeSurface= pd.DataFrame(takeSurface
# takeGroundwater = pd.DataFrame(takeGroundwater

# pctCapacitySurfaceCarryover = pd.DataFrame(pctCapacitySurfaceCarryover
# pctStorageCalledSurfaceCarryover = pd.DataFrame(pctStorageCalledSurfaceCarryover
# pctCapacityGroundwaterBank= pd.DataFrame(pctCapacityGroundwaterBank
# pctStorageCalledGroundwaterBank = pd.DataFrame(pctStorageCalledGroundwaterBank

writer.save()