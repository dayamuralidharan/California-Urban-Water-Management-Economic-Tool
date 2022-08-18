import pandas as pd
#from readSystemOperationsAssumptions import storageHedgingStrategyData

def putExcessIntoStorage(i, excessSupplySwitch_Contractor, excessSupply_Contractor, availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor, rechargeEffectiveness_Contractor, availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor):
    if excessSupplySwitch_Contractor in ["Put into Carryover and Groundwater Bank", "Put into Groundwater Bank"]:
        putGroundwater_Contractor = max(min(excessSupply_Contractor[i], availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor) * rechargeEffectiveness_Contractor, 0)
        excessSupply_Contractor[i] = excessSupply_Contractor[i] - putGroundwater_Contractor
        putSurface_Contractor = 0
        
    if excessSupply_Contractor[i] > 0 and excessSupplySwitch_Contractor in ["Put into Carryover and Groundwater Bank", "Put into Carryover Storage"]:
        putSurface_Contractor = max(min(excessSupply_Contractor[i], availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor), 0)
    return {'putGroundwater_Contractor': putGroundwater_Contractor, 'putSurface_Contractor': putSurface_Contractor}


def putOrTakeFromStorage(i, 
                         contractor, 
                         futureYear,
                         storageInputDf_Contractor, 
                         excessSupply_Contractor,
                         excessSupplySwitch_Contractor, 
                         demandsToBeMetByCarryover_Contractor, 
                         volumeSurfaceCarryover_Contractor, 
                         volumeGroundwaterBank_Contractor,
                         groundwaterMaximumCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor, groundwaterMaximumTakeCapacity_Contractor, rechargeEffectiveness_Contractor,
                         surfaceMaximumCapacity_Contractor, surfaceMaximumPutCapacity_Contractor, surfaceMaximumTakeCapacity_Contractor, surfaceStorageAnnualLoss_Contractor,
                         storageHedgingStrategySwitch_Contractor, hedgingPoint_Contractor, hedgeCallStorageFactor_Contractor, hedgingStorageCapacityFactor_Contractor,
                         demandToBeMetByContingentOptions_Contractor):
    
    
    availableCapacitySurface_Contractor = surfaceMaximumCapacity_Contractor - volumeSurfaceCarryover_Contractor[max(0,i-1)]
    availableGroundwaterCapacity_Contractor = groundwaterMaximumCapacity_Contractor - volumeGroundwaterBank_Contractor[max(0,i-1)]
    
    
    ## If there are excess supplies, put into groundwater bank first, then surface carryover storage
    if excessSupply_Contractor[i] > 0:
        if excessSupplySwitch_Contractor in ["Put into Carryover and Groundwater Bank", "Put into Groundwater Bank"]:
            putGroundwater_Contractor = max(min(excessSupply_Contractor[i], availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor) * rechargeEffectiveness_Contractor, 0)
            excessSupply_Contractor[i] = excessSupply_Contractor[i] - putGroundwater_Contractor
            #volumeGroundwaterBank_Contractor[i] = volumeGroundwaterBank_Contractor[i] + putGroundwater_Contractor
        if excessSupply_Contractor[i] > 0 and excessSupplySwitch_Contractor in ["Put into Carryover and Groundwater Bank", "Put into Carryover Storage"]:
            putSurface_Contractor = max(min(excessSupply_Contractor[i], availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor), 0)
            # excessSupply_Contractor[i] = excessSupply_Contractor[i] - putSurface_Contractor
            #volumeSurfaceCarryover_Contractor[i] = max(volumeSurfaceCarryover_Contractor[max(0,i-1)] - surfaceStorageAnnualLoss_Contractor, 0) + putSurface_Contractor
    else:
        putGroundwater_Contractor = 0
        putSurface_Contractor = 0
        # volumeSurfaceCarryover_Contractor[i] = max(volumeSurfaceCarryover_Contractor[max(0,i-1)] - surfaceStorageAnnualLoss_Contractor, 0)

    ## If there is remaining demand after local and Project supplies are delivered, take from surface carryover storage first, then banked groundwater
    
    """
    "Surface Carryover Only",
    "Groundwater Bank Only",
    "Surface and Groundwater Storage",
    "Off"
    """

    #volumeSurfaceCarryover_Contractor[i] = max(volumeSurfaceCarryover_Contractor[i] - surfaceStorageAnnualLoss_Contractor, 0)
    

    ## Calculate Take from Surface Carryover. Apply Hedging Strategy if switched on.
    if demandsToBeMetByCarryover_Contractor[i] > 0:
        if volumeSurfaceCarryover_Contractor[[max(0,i-1)]] > 0:
            # Apply Hedging strategy if switched on 
            if storageHedgingStrategySwitch_Contractor in ["Surface Carryover Only", "Surface and Groundwater Storage"]:
                # Set surface carryover storage hedging strategy variables
                #if volumeSurfaceCarryover_Contractor[i] > 0:
                pctCapacitySurfaceCarryover_Contractor = (volumeSurfaceCarryover_Contractor[max(0,i-1)] / surfaceMaximumCapacity_Contractor)
                pctStorageCalledSurfaceCarryover_Contractor = (demandsToBeMetByCarryover_Contractor[i] / volumeSurfaceCarryover_Contractor[max(0,i-1)]) 
                #else:
                    #pctCapacitySurfaceCarryover_Contractor = 0
                    #pctStorageCalledSurfaceCarryover_Contractor = 0
                
                # Apply hedging strategy if % of Capacity is below the Hedging Point
                if pctCapacitySurfaceCarryover_Contractor <= hedgingPoint_Contractor:
                    takeSurface_Contractor = min(
                        (1 - hedgeCallStorageFactor_Contractor * pctStorageCalledSurfaceCarryover_Contractor * (pctCapacitySurfaceCarryover_Contractor ** -hedgingStorageCapacityFactor_Contractor)) * volumeSurfaceCarryover_Contractor,
                        volumeSurfaceCarryover_Contractor[i],
                        demandsToBeMetByCarryover_Contractor[i],
                        surfaceMaximumTakeCapacity_Contractor
                    )
            else:
                takeSurface_Contractor = min(volumeSurfaceCarryover_Contractor[max(0,i-1)], demandsToBeMetByCarryover_Contractor[i], surfaceMaximumTakeCapacity_Contractor)
    else:
        takeSurface_Contractor = 0
            
    
    demandsToBeMetByBankedGW_Contractor = demandsToBeMetByCarryover_Contractor[i] - takeSurface_Contractor
    
    # Set groundwater bank hedging strategy variables
    # if volumeGroundwaterBank_Contractor[i] > 0:

    
    
    if demandsToBeMetByBankedGW_Contractor > 0:
        if volumeGroundwaterBank_Contractor[max(0,i-1)] > 0:
        # Apply Hedging strategy if switched on
            if storageHedgingStrategySwitch_Contractor in ["Groundwater Bank Only", "Surface and Groundwater Storage"]:
                        pctCapacityGroundwaterBank_Contractor = (volumeGroundwaterBank_Contractor[i] / groundwaterMaximumCapacity_Contractor)
                        pctStorageCalledGroundwaterBank_Contractor = (demandsToBeMetByBankedGW_Contractor[i] / volumeGroundwaterBank_Contractor[i])
                    #else:
                        #pctCapacityGroundwaterBank_Contractor = 0
                        #pctStorageCalledGroundwaterBank_Contractor = 0
                if pctCapacityGroundwaterBank_Contractor <= hedgingPoint_Contractor and storageHedgingStrategySwitch_Contractor in ["Groundwater Bank Only", "Surface and Groundwater Storage"]:
                    takeGroundwater_Contractor = min(
                        (1 - hedgeCallStorageFactor_Contractor * pctStorageCalledGroundwaterBank_Contractor * (pctCapacityGroundwaterBank_Contractor ** -hedgingStorageCapacityFactor_Contractor)) * volumeGroundwaterBank_Contractor,
                        demandsToBeMetByBankedGW_Contractor[i],
                        groundwaterMaximumTakeCapacity_Contractor
                    )
            else:
                takeGroundwater_Contractor = min(demandsToBeMetByBankedGW_Contractor[i], groundwaterMaximumTakeCapacity_Contractor)
    else:
        takeGroundwater_Contractor = 0
   
    volumeSurfaceCarryover_Contractor[i] = max(volumeSurfaceCarryover_Contractor[max(0,i-1)] - surfaceStorageAnnualLoss_Contractor - takeSurface_Contractor + putSurface_Contractor, 0)
    volumeGroundwaterBank_Contractor[i] = max(volumeGroundwaterBank_Contractor[max(0,i-1)] - takeGroundwater_Contractor + putGroundwater_Contractor, 0)
    
    demandToBeMetByContingentOptions_Contractor.append(demandsToBeMetByBankedGW_Contractor - takeGroundwater_Contractor)
    
    return {'putSurface_Contractor': putSurface_Contractor, 
            'takeSurface_Contractor': takeSurface_Contractor, 
            'putGroundwater_Contractor': putGroundwater_Contractor, 
            'takeGroundwater_Contractor': takeGroundwater_Contractor,
            'demandToBeMetByContingentOptions_Contractor': demandToBeMetByContingentOptions_Contractor}
    