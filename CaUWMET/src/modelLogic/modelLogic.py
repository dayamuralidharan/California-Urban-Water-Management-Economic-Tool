import pandas as pd
from readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear
from readDemandAssumptions import totalDemands, plannedLongTermConservation
from readSupplyAssumptions import totalLocalSupply, swpCVPSupply
from readSystemOperationsAssumptions import storageData,  storageHedgingStrategyData, excessWaterSwitchData
from readContingentWMOsAssumptions import contingentConservationUseReduction, contingentConservationStorageTrigger
from storageUtilities import getContractorStorageAssumptions, putExcessSupplyIntoStorage, takeFromStorage


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

# Contingent WMOs dataframes
demandsToBeMetByContingentOptions = {'Year': historicHydrologyYears}
contingentConservationReduction = {'Year': historicHydrologyYears}

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
    
    volumeSurfaceCarryover_Contractor = []
    volumeGroundwaterBank_Contractor = []
    putSurface_Contractor = []
    putGroundwater_Contractor = []
    takeSurface_Contractor = []
    takeGroundwater_Contractor = []
    
    storageInputAssumptions_Contractor = getContractorStorageAssumptions(contractor, futureYear, excessWaterSwitchData, storageData, storageHedgingStrategyData)
    
    demandsToBeMetByContingentOptions_Contractor = []
    contingentConservationUseReduction = []
    contingentConservationStorageTrigger = []
    demandsToBeMetByWaterMarketTransfers = []
    

    for i in range(len(historicHydrologyYears)):
        
        
        #### Deliver local and project supplies to meet demands:
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




        #### Put excess into or take from storage to meet demands:
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
        
        # If there is excess supply, calculate put into storage
        putsIntoStorage_Contractor = putExcessSupplyIntoStorage(i, 
                                excessSupplySwitch_Contractor, excessSupply_Contractor,
                                availableGroundwaterCapacity_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumPutCapacity_Contractor'], storageInputAssumptions_Contractor['rechargeEffectiveness_Contractor'], # groundwater bank assumptions
                                availableCapacitySurface_Contractor, storageInputAssumptions_Contractor['surfaceMaximumPutCapacity_Contractor']) # surface carryover assumptions
    
        putGroundwater_Contractor.append(putsIntoStorage_Contractor['putGroundwater_Contractor'])
        putSurface_Contractor.append(putsIntoStorage_Contractor['putSurface_Contractor'])
        
        volumeGroundwaterBank_Contractor[i] = volumeGroundwaterBank_Contractor[i] + putGroundwater_Contractor[i]
        volumeSurfaceCarryover_Contractor[i] = volumeSurfaceCarryover_Contractor[i] + putSurface_Contractor[i]
        
    ## If there is no excess supply, but remaining demand after local and CVP/SWP supplies are delivered, take from surface carryover storage first, then banked groundwater storage
        takesFromStorage_Contractor = takeFromStorage(i, demandsToBeMetByStorage_Contractor, 
                           volumeSurfaceCarryover_Contractor, storageInputAssumptions_Contractor['surfaceMaximumCapacity_Contractor'], storageInputAssumptions_Contractor['surfaceMaximumTakeCapacity_Contractor'],
                           volumeGroundwaterBank_Contractor, storageInputAssumptions_Contractor['groundwaterMaximumCapacity_Contractor'], storageInputAssumptions_Contractor['groundwaterMaximumTakeCapacity_Contractor'],
                           storageInputAssumptions_Contractor['storageHedgingStrategySwitch_Contractor'], storageInputAssumptions_Contractor['hedgingPoint_Contractor'], storageInputAssumptions_Contractor['hedgeCallStorageFactor_Contractor'], storageInputAssumptions_Contractor['hedgingStorageCapacityFactor_Contractor'])
        
        takeSurface_Contractor.append(takesFromStorage_Contractor['takeSurface_Contractor'])
        takeGroundwater_Contractor.append(takesFromStorage_Contractor['takeGroundwater_Contractor'])
        demandsToBeMetByContingentOptions_Contractor.append(takesFromStorage_Contractor['demandsToBeMetByContingentOptions_Contractor'])


    ## If there is remaining demand and storage is below user-defined threshold, implement contingency conservation assumptions:
        contingentConservationUseReduction[contingentConservationUseReduction['Contractor'] == contractor][futureYear].values[0]
        contingentConservationStorageTrigger[contingentConservationStorageTrigger['Contractor'] == contractor][futureYear].values[0]
        
        #demandsToBeMetByWaterMarketTransfers








# Append dataframes with updated contractor data as calculated in model logic above.
    appliedDemands[contractor] = appliedDemand_Contractor
    demandsToBeMetBySWPCVP[contractor] = demandsToBeMetBySWPCVP_Contractor
    demandsToBeMetByStorage[contractor] = demandsToBeMetByStorage_Contractor
    excessSupply[contractor] = excessSupply_Contractor
    
    volumeSurfaceCarryover[contractor] = volumeSurfaceCarryover_Contractor
    volumeGroundwaterBank[contractor] = volumeGroundwaterBank_Contractor
    availableCapacitySurface[contractor] = availableCapacitySurface_Contractor
    availableGroundwaterCapacity[contractor] = availableGroundwaterCapacity_Contractor
    putGroundwater[contractor] = putGroundwater_Contractor
    putSurface[contractor] = putSurface_Contractor
    takeSurface[contractor] = takeSurface_Contractor
    takeGroundwater[contractor] = takeGroundwater_Contractor
    # pctCapacitySurfaceCarryover[contractor] = pctCapacitySurfaceCarryover_Contractor
    # pctStorageCalledSurfaceCarryover[contractor] = pctStorageCalledSurfaceCarryover_Contractor
    # pctCapacityGroundwaterBank[contractor] = pctCapacityGroundwaterBank_Contractor
    # pctStorageCalledGroundwaterBank[contractor] = pctStorageCalledGroundwaterBank_Contractor
    
    demandsToBeMetByContingentOptions[contractor] = demandsToBeMetByContingentOptions_Contractor




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

# pctCapacitySurfaceCarryover = pd.DataFrame(pctCapacitySurfaceCarryover)
# pctStorageCalledSurfaceCarryover = pd.DataFrame(pctStorageCalledSurfaceCarryover)
# pctCapacityGroundwaterBank= pd.DataFrame(pctCapacityGroundwaterBank)
# pctStorageCalledGroundwaterBank = pd.DataFrame(pctStorageCalledGroundwaterBank)

demandsToBeMetByContingentOptions = pd.DataFrame(demandsToBeMetByContingentOptions)

writer = pd.ExcelWriter('Output_QAQC.xlsx', engine = 'xlsxwriter')
workbook = writer.book

appliedDemands.to_excel(writer, sheet_name = 'appliedDemands')
demandsToBeMetBySWPCVP.to_excel(writer, sheet_name = 'demandsToBeMetBySWPCVP')
demandsToBeMetByStorage.to_excel(writer, sheet_name = 'demandsToBeMetByStorage')
volumeSurfaceCarryover.to_excel(writer, sheet_name = 'volumeSurfaceCarryover')
volumeGroundwaterBank.to_excel(writer, sheet_name = 'volumeGroundwaterBank')
availableCapacitySurface.to_excel(writer, sheet_name = 'availableCapacitySurface')
availableGroundwaterCapacity.to_excel(writer, sheet_name = 'availableGroundwaterCapacity')
putGroundwater.to_excel(writer, sheet_name = 'putGroundwater')
putSurface.to_excel(writer, sheet_name = 'putSurface')
takeGroundwater.to_excel(writer, sheet_name = 'takeGroundwater')
takeSurface.to_excel(writer, sheet_name = 'takeSurface')

#demandsToBeMetByContingentOptions.to_excel(writer, sheet_name = 'demandsToBeMetByContingentWMOs')


writer.save()