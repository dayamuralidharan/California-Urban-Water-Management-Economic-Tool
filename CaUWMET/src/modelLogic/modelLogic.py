import pandas as pd
from readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from readDemandAssumptions import totalDemands, plannedLongTermConservation
from readSupplyAssumptions import totalLocalSupply, swpCVPSupply
from readSystemOperationsAssumptions import storageData,  storageHedgingStrategyData, excessWaterSwitchData
from storageUtilities import getContractorStorageAssumptions, putExcessSupplyIntoStorage


#TODO: Add water management options to local supplies

# Initialize time series dataframes for each variable. These dataframes include time series for all contractors.
appliedDemands = {'Year': historicHydrologyYears}
demandsToBeMetBySWPCVP = {'Year': historicHydrologyYears}
demandsToBeMetByStorage = {'Year': historicHydrologyYears}
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
    demandsToBeMetByStorage_Contractor = []
    demandToBeMetByContingentOptions_Contractor = []

    excessSupplySwitch_Contractor = excessWaterSwitchData['Switch'].loc[[contractor]].values[0]
    excessSupply_Contractor = []
    
    storageInputDf_Contractor = storageData.loc[[contractor]]
    volumeSurfaceCarryover_Contractor = []
    volumeGroundwaterBank_Contractor = []
    putSurface_Contractor = []
    putGroundwater_Contractor = []
    
    storageInputAssumptions_Contractor = getContractorStorageAssumptions(contractor, futureYear, excessWaterSwitchData, storageData, storageHedgingStrategyData)
    
    

    for i in range(len(historicHydrologyYears)):
        # Calculate Applied Demand after subtraction of Planned Long-term Conservation
        plannedLongTermConservation_Contractor = plannedLongTermConservation[plannedLongTermConservation['Contractor'] == contractor][futureYear].values[0]
        appliedDemand_Contractor.append(totalDemand_Contractor[i] - plannedLongTermConservation_Contractor)

        # Calculate Demand to be Met by SWP/CVP supplies after subtraction of local supplies
        demandsToBeMetBySWPCVP_Contractor.append(max(0, appliedDemand_Contractor[i] - totalLocalSupply[contractor][i]))

        # Calculate Demand to be Met by Stored supplies after delivery of SWP/CVP supplies, or calculate Excess SWP/CVP Supply.
        SWPCVPSupply_Contractor = swpCVPSupply[contractor][i]
        if demandsToBeMetBySWPCVP_Contractor[i] - SWPCVPSupply_Contractor > 0:
            demandsToBeMetByStorage_Contractor.append(demandsToBeMetBySWPCVP_Contractor[i] - SWPCVPSupply_Contractor)
            excessSupply_Contractor.append(0)
        else:
            excessSupply_Contractor.append((SWPCVPSupply_Contractor - demandsToBeMetBySWPCVP_Contractor[i]))
            demandsToBeMetByStorage_Contractor.append(0)

        # Initialize storage volumes each time step
        if i == 0: #Initial storage volumes
            volumeSurfaceCarryover_Contractor.append(storageInputAssumptions_Contractor['initialSurfaceStorageVolume_Contractor'])
            volumeGroundwaterBank_Contractor.append(storageInputAssumptions_Contractor['initialGroundwaterStorageVolume_Contractor'])
        else: # Initialize with previous time step's volumes which are updated in the putOrTakeFromStorage function
            volumeSurfaceCarryover_Contractor.append(volumeSurfaceCarryover_Contractor[i-1])
            volumeGroundwaterBank_Contractor.append(volumeGroundwaterBank_Contractor[i-1])
        
        # Check available capacity in storage systems
        availableCapacitySurface_Contractor = storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'] - volumeSurfaceCarryover_Contractor[max(0,i-1)]
        availableGroundwaterCapacity_Contractor = storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'] - volumeGroundwaterBank_Contractor[max(0,i-1)]
        
        # If there is excess supply, put into storage
        putsIntoStorage_Contractor = putExcessSupplyIntoStorage(i, 
                                excessSupplySwitch_Contractor, excessSupply_Contractor, # excess supply management assumptions
                                availableGroundwaterCapacity_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumPutCapacity_Contractor'], storageInputAssumptions_Contractor['rechargeEffectiveness_Contractor'], # groundwater bank assumptions
                                availableCapacitySurface_Contractor, storageInputAssumptions_Contractor['surfaceMaximumPutCapacity_Contractor']) # surface carryover assumptions
    
        putGroundwater_Contractor.append(putsIntoStorage_Contractor['putGroundwater_Contractor'])
        putSurface_Contractor.append(putsIntoStorage_Contractor['putSurface_Contractor'])
        
    ## If there is no excess supply, but remaining demand after local and CVP/SWP supplies are delivered, take from surface carryover storage first, then banked groundwater
        
        

# Append dataframes with updated contractor data as calculated in model logic above.
    appliedDemands[contractor] = appliedDemand_Contractor
    demandsToBeMetBySWPCVP[contractor] = demandsToBeMetBySWPCVP_Contractor
    demandsToBeMetByStorage[contractor] = demandsToBeMetByStorage_Contractor
    #demandsToBeMetByBankedGW[contractor] = demandsToBeMetByBankedGW_Contractor
    excessSupply[contractor] = excessSupply_Contractor
    
    # volumeSurfaceCarryover[contractor] = volumeSurfaceCarryover_Contractor
    #volumeGroundwaterBank[contractor] = volumeGroundwaterBank_Contractor
    # availableCapacitySurface[contractor] = availableCapacitySurface_Contractor
    # availableGroundwaterCapacity[contractor] = availableGroundwaterCapacity_Contractor
    putGroundwater[contractor] = putGroundwater_Contractor
    putSurface[contractor] = putSurface_Contractor
    # takeSurface[contractor] = takeSurface_Contractor
    # takeGroundwater[contractor] = takeGroundwater_Contractor
    # pctCapacitySurfaceCarryover[contractor] = pctCapacitySurfaceCarryover_Contractor
    # pctStorageCalledSurfaceCarryover[contractor] = pctStorageCalledSurfaceCarryover_Contractor
    # pctCapacityGroundwaterBank[contractor] = pctCapacityGroundwaterBank_Contractor
    # pctStorageCalledGroundwaterBank[contractor] = pctStorageCalledGroundwaterBank_Contractor




appliedDemands = pd.DataFrame(appliedDemands)
demandsToBeMetBySWPCVP = pd.DataFrame(demandsToBeMetBySWPCVP)
demandsToBeMetByStorage = pd.DataFrame(demandsToBeMetByStorage)
excessSupply = pd.DataFrame(excessSupply)

volumeSurfaceCarryover = pd.DataFrame(volumeSurfaceCarryover)
volumeGroundwaterBank = pd.DataFrame(volumeGroundwaterBank)
availableCapacitySurface = pd.DataFrame(availableCapacitySurface)
availableGroundwaterCapacity = pd.DataFrame(availableGroundwaterCapacity)
putGroundwater = pd.DataFrame(putGroundwater)
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