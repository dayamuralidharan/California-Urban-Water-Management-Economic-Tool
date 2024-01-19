import pandas as pd

class StorageUtilities:
    def getContractorStorageAssumptions(self, contractor, futureYear, excessWaterSwitchData, storageData, storageHedgingStrategyData):
        excessSupplySwitch_Contractor = excessWaterSwitchData['Value'].loc[[contractor]].values[0]
        storageInputDf_Contractor = storageData.loc[[contractor]]
        
        initialSurfaceStorageVolume_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface initial storage (acre-feet)'][futureYear].values[0]
        initialGroundwaterStorageVolume_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater Initial Storage Volume (acre-feet)'][futureYear]
        
        groundwaterMaximumCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater Max Storage Capacity (acre-feet)'][futureYear]
        groundwaterMaximumPutCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater Max Put Capacity (AFY)'][futureYear]
        groundwaterMaximumTakeCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Groundwater Max Take Capacity (AFY)'][futureYear]
        rechargeEffectiveness_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Recharge Effectiveness (%)'][futureYear] / 100 # Converted from % into fraction
        
        surfaceMaximumCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max storage capacity (acre-feet)'][futureYear]
        surfaceMaximumPutCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max put capacity (AFY)'][futureYear]
        surfaceMaximumTakeCapacity_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface max take capacity (AFY)'][futureYear]
        surfaceStorageAnnualLoss_Contractor = (storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface loss (AFY)'][futureYear])
        
        storageHedgingStrategyDf_Contractor = storageHedgingStrategyData.loc[[contractor]]
        storageHedgingStrategySwitch_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Storage Hedging Strategy Switch']['Value'].values[0]
        hedgingPoint_Contractor = int(storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedging Point (%)']['Value'].values[0])
        hedgingPoint_Contractor = hedgingPoint_Contractor / 100  # Converting % into fraction
        hedgeCallStorageFactor_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedge Call/Storage Factor']['Value'].values[0]
        hedgingStorageCapacityFactor_Contractor = storageHedgingStrategyDf_Contractor[storageHedgingStrategyDf_Contractor['Variable'] == 'Hedging Storage/Capacity Factor']['Value'].values[0]
        return {'excessSupplySwitch_Contractor': excessSupplySwitch_Contractor, 
                'initialSurfaceStorageVolume_Contractor': initialSurfaceStorageVolume_Contractor,
                'initialGroundwaterStorageVolume_Contractor': initialGroundwaterStorageVolume_Contractor[contractor],
                'groundwaterMaximumCapacity_Contractor': groundwaterMaximumCapacity_Contractor[contractor],
                'groundwaterMaximumPutCapacity_Contractor': groundwaterMaximumPutCapacity_Contractor[contractor], 
                'groundwaterMaximumTakeCapacity_Contractor': groundwaterMaximumTakeCapacity_Contractor[contractor],
                'rechargeEffectiveness_Contractor': rechargeEffectiveness_Contractor[contractor],
                'surfaceMaximumCapacity_Contractor': surfaceMaximumCapacity_Contractor[contractor],
                'surfaceMaximumPutCapacity_Contractor': surfaceMaximumPutCapacity_Contractor[contractor],
                'surfaceMaximumTakeCapacity_Contractor': surfaceMaximumTakeCapacity_Contractor[contractor],
                'surfaceStorageAnnualLoss_Contractor': surfaceStorageAnnualLoss_Contractor[contractor],
                'storageHedgingStrategySwitch_Contractor': storageHedgingStrategySwitch_Contractor,
                'hedgingPoint_Contractor': hedgingPoint_Contractor,
                'hedgeCallStorageFactor_Contractor': hedgeCallStorageFactor_Contractor,
                'hedgingStorageCapacityFactor_Contractor': hedgingStorageCapacityFactor_Contractor}
    
    def putExcessSupplyIntoStorage(self, i, excessSupplySwitch_Contractor, excessSupply_Contractor, availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor, rechargeEffectiveness_Contractor, availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor):
        putGroundwater_Contractor = int('0')
        putSurface_Contractor = int('0')
        
        if excessSupplySwitch_Contractor == "Groundwater Bank and Carryover Storage":
            
            putGroundwater_Contractor = max(min(excessSupply_Contractor[i], availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor), int('0'))
            rechargeLoss_Contractor = putGroundwater_Contractor - putGroundwater_Contractor * rechargeEffectiveness_Contractor
            putGroundwater_Contractor = putGroundwater_Contractor - rechargeLoss_Contractor
            
            excessAfterGroundwaterPut_Contractor = excessSupply_Contractor[i] - putGroundwater_Contractor - rechargeLoss_Contractor
            putSurface_Contractor = max(min(excessAfterGroundwaterPut_Contractor, availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor), int('0'))


        elif excessSupplySwitch_Contractor == "Groundwater Bank":
            putGroundwater_Contractor = max(min(excessSupply_Contractor[i], availableGroundwaterCapacity_Contractor, groundwaterMaximumPutCapacity_Contractor), int('0'))
            rechargeLoss_Contractor = putGroundwater_Contractor - putGroundwater_Contractor * rechargeEffectiveness_Contractor
            putGroundwater_Contractor = putGroundwater_Contractor - rechargeLoss_Contractor
            
        elif excessSupplySwitch_Contractor == "Carryover Storage":
            putSurface_Contractor = max(min(excessSupply_Contractor[i], availableCapacitySurface_Contractor, surfaceMaximumPutCapacity_Contractor), int('0'))

        
        
        return {'putSurface_Contractor': putSurface_Contractor, 'putGroundwater_Contractor': putGroundwater_Contractor}
        
    def takeFromStorage (self, i, demandsToBeMetByStorage_Contractor, 
                            volumeSurfaceCarryover_Contractor, surfaceMaximumCapacity_Contractor, surfaceMaximumTakeCapacity_Contractor,
                            volumeGroundwaterBank_Contractor, groundwaterMaximumCapacity_Contractor, groundwaterMaximumTakeCapacity_Contractor,
                            storageHedgingStrategySwitch_Contractor, hedgingPoint_Contractor, hedgeCallStorageFactor_Contractor, hedgingStorageCapacityFactor_Contractor):
        ## Calculate Take from Surface Carryover. Apply Hedging Strategy if switched on.
        if demandsToBeMetByStorage_Contractor[i] > int('0') and volumeSurfaceCarryover_Contractor[i] > int('0'):
            # Apply Hedging strategy if switched on 
            if storageHedgingStrategySwitch_Contractor in ["Surface Carryover Only", "Surface and Groundwater Storage"]:
                # Set surface carryover storage hedging strategy variables
                pctCapacitySurfaceCarryover_Contractor = (volumeSurfaceCarryover_Contractor[i] / surfaceMaximumCapacity_Contractor)
                pctStorageCalledSurfaceCarryover_Contractor = (demandsToBeMetByStorage_Contractor[i] / surfaceMaximumCapacity_Contractor) 
                
                # Apply hedging strategy if % of Capacity is below the Hedging Point
                if pctCapacitySurfaceCarryover_Contractor <= hedgingPoint_Contractor:
                    takeSurface_Contractor = min(
                        (1 - float(hedgeCallStorageFactor_Contractor) * float(pctStorageCalledSurfaceCarryover_Contractor) * (float(pctCapacitySurfaceCarryover_Contractor) ** - float(hedgingStorageCapacityFactor_Contractor))) * float(volumeSurfaceCarryover_Contractor[i]),
                        volumeSurfaceCarryover_Contractor[i],
                        demandsToBeMetByStorage_Contractor[i],
                        surfaceMaximumTakeCapacity_Contractor
                    )
            
            else:
                takeSurface_Contractor = min(volumeSurfaceCarryover_Contractor[i], demandsToBeMetByStorage_Contractor[i], surfaceMaximumTakeCapacity_Contractor)
        else:
            takeSurface_Contractor = int('0')
        
        demandsToBeMetByBankedGW_Contractor = demandsToBeMetByStorage_Contractor[i] - takeSurface_Contractor
        
        ## Calculate Take from Groundwater Bank. Apply Hedging Strategy if switched on.
        if demandsToBeMetByBankedGW_Contractor > int('0') and volumeGroundwaterBank_Contractor[i] > int('0'):
            # Apply Hedging strategy if switched on 
            if storageHedgingStrategySwitch_Contractor in ["Groundwater Bank Only", "Surface and Groundwater Storage"]:
                # Set surface carryover storage hedging strategy variables
                pctCapacityGroundwaterBank_Contractor = (volumeGroundwaterBank_Contractor[i] / groundwaterMaximumCapacity_Contractor)
                pctStorageCalledGroundwaterBank_Contractor = (demandsToBeMetByBankedGW_Contractor / groundwaterMaximumCapacity_Contractor) 
                
                # Apply hedging strategy if % of Capacity is below the Hedging Point
                if pctCapacityGroundwaterBank_Contractor <= hedgingPoint_Contractor:
                    takeGroundwater_Contractor = min(
                        (1 - float(hedgeCallStorageFactor_Contractor) * float(pctStorageCalledGroundwaterBank_Contractor) * (float(pctCapacityGroundwaterBank_Contractor) ** - float(hedgingStorageCapacityFactor_Contractor))) * float(volumeGroundwaterBank_Contractor[i]),
                        volumeGroundwaterBank_Contractor[i],
                        demandsToBeMetByBankedGW_Contractor,
                        groundwaterMaximumTakeCapacity_Contractor
                    )
            
            else:
                takeGroundwater_Contractor = min(volumeGroundwaterBank_Contractor[i], demandsToBeMetByBankedGW_Contractor, groundwaterMaximumTakeCapacity_Contractor)
        else:
            takeGroundwater_Contractor = int('0')
        
        demandsToBeMetByContingentOptions_Contractor = demandsToBeMetByBankedGW_Contractor - takeGroundwater_Contractor
        
        return {'takeSurface_Contractor': takeSurface_Contractor, 
                'takeGroundwater_Contractor': takeGroundwater_Contractor, 
                'demandsToBeMetByContingentOptions_Contractor': demandsToBeMetByContingentOptions_Contractor}