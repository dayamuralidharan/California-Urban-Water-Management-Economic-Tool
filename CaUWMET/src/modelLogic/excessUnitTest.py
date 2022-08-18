def putExcessSupplyIntoStorage(i, excessSupplySwitch_Contractor, excessSupply_Contractor, availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor, rechargeEffectiveness_Contractor, availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor):
    putGroundwater_Contractor = 0
    putSurface_Contractor = 0
    
    if excessSupplySwitch_Contractor == "Put into Carryover and Groundwater Bank": 
        putGroundwater_Contractor = max(min(excessSupply_Contractor[i], availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor), 0)
        rechargeLoss_Contractor = putGroundwater_Contractor - putGroundwater_Contractor * rechargeEffectiveness_Contractor
        putGroundwater_Contractor = putGroundwater_Contractor - rechargeLoss_Contractor
        
        excessSupply_Contractor[i] = excessSupply_Contractor[i] - putGroundwater_Contractor - rechargeLoss_Contractor
        
        putSurface_Contractor = max(min(excessSupply_Contractor[i], availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor), 0)

    elif excessSupplySwitch_Contractor == "Put into Groundwater Bank":
        putGroundwater_Contractor = max(min(excessSupply_Contractor[i], availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor), 0)
        rechargeLoss_Contractor = putGroundwater_Contractor - putGroundwater_Contractor * rechargeEffectiveness_Contractor
        putGroundwater_Contractor = putGroundwater_Contractor - rechargeLoss_Contractor
        excessSupply_Contractor[i] = excessSupply_Contractor[i] - putGroundwater_Contractor - rechargeLoss_Contractor
        
    elif excessSupplySwitch_Contractor == "Put into Carryover Storage":
        putSurface_Contractor = max(min(excessSupply_Contractor[i], availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor), 0)

    return {'putSurface_Contractor': putSurface_Contractor, 'putGroundwater_Contractor': putGroundwater_Contractor}