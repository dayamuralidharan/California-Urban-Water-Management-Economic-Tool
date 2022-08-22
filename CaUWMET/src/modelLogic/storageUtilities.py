import pandas as pd
#from readSystemOperationsAssumptions import storageHedgingStrategyData

def getContractorStorageAssumptions(contractor, futureYear, excessWaterSwitchData, storageData, storageHedgingStrategyData):
        excessSupplySwitch_Contractor = excessWaterSwitchData['Switch'].loc[[contractor]].values[0]
        storageInputDf_Contractor = storageData.loc[[contractor]]
        
        initialSurfaceStorageVolume_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface initial storage (acre-feet)'][futureYear].values[0]
        initialGroundwaterStorageVolume_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater initial storage (acre-feet)'][futureYear].values[0]
        
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
        return {'excessSupplySwitch_Contractor':excessSupplySwitch_Contractor, 
                'initialSurfaceStorageVolume_Contractor': initialSurfaceStorageVolume_Contractor,
                'initialGroundwaterStorageVolume_Contractor': initialGroundwaterStorageVolume_Contractor,
                'groundwaterMaximumCapacity_Contractor': groundwaterMaximumCapacity_Contractor,
                'groundwaterMaximumPutCapacity_Contractor': groundwaterMaximumPutCapacity_Contractor, 
                'groundwaterMaximumTakeCapacity_Contractor': groundwaterMaximumTakeCapacity_Contractor,
                'rechargeEffectiveness_Contractor': rechargeEffectiveness_Contractor,
                'surfaceMaximumCapacity_Contractor': surfaceMaximumCapacity_Contractor,
                'surfaceMaximumPutCapacity_Contractor': surfaceMaximumPutCapacity_Contractor,
                'surfaceMaximumTakeCapacity_Contractor': surfaceMaximumTakeCapacity_Contractor,
                'surfaceStorageAnnualLoss_Contractor': surfaceStorageAnnualLoss_Contractor,
                'storageHedgingStrategySwitch_Contractor': storageHedgingStrategySwitch_Contractor,
                'hedgeCallStorageFactor_Contractor': hedgeCallStorageFactor_Contractor,
                'hedgingStorageCapacityFactor_Contractor': hedgingStorageCapacityFactor_Contractor}
        


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
    
    
def takeSupplyFromSurfaceCarryoverStorage (i, excessSupplySwitch_Contractor, demandsToBeMetByCarryover_Contractor, 
                           volumeSurfaceCarryover_Contractor, )

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

    
    
    # if demandsToBeMetByBankedGW_Contractor > 0:
    #     if volumeGroundwaterBank_Contractor[max(0,i-1)] > 0:
    #     # Apply Hedging strategy if switched on
    #         if storageHedgingStrategySwitch_Contractor in ["Groundwater Bank Only", "Surface and Groundwater Storage"]:
    #                     pctCapacityGroundwaterBank_Contractor = (volumeGroundwaterBank_Contractor[i] / groundwaterMaximumCapacity_Contractor)
    #                     pctStorageCalledGroundwaterBank_Contractor = (demandsToBeMetByBankedGW_Contractor[i] / volumeGroundwaterBank_Contractor[i])
    #                 #else:
    #                     #pctCapacityGroundwaterBank_Contractor = 0
    #                     #pctStorageCalledGroundwaterBank_Contractor = 0
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
   
    # volumeSurfaceCarryover_Contractor[i] = max(volumeSurfaceCarryover_Contractor[max(0,i-1)] - surfaceStorageAnnualLoss_Contractor - takeSurface_Contractor + putSurface_Contractor, 0)
    # volumeGroundwaterBank_Contractor[i] = max(volumeGroundwaterBank_Contractor[max(0,i-1)] - takeGroundwater_Contractor + putGroundwater_Contractor, 0)
    
    # demandToBeMetByContingentOptions_Contractor.append(demandsToBeMetByBankedGW_Contractor - takeGroundwater_Contractor)
    
    # return {'putSurface_Contractor': putSurface_Contractor, 
    #         'takeSurface_Contractor': takeSurface_Contractor, 
    #         'putGroundwater_Contractor': putGroundwater_Contractor, 
    #         'takeGroundwater_Contractor': takeGroundwater_Contractor,
    #         'demandToBeMetByContingentOptions_Contractor': demandToBeMetByContingentOptions_Contractor}
    