class ContingencyWMOsHandlerInput:
    def __init__(self, 
            contractor, 
            i, 
            plannedLongTermConservation_Contractor, 
            totalDemand_Contractor, 
            longtermWMOConservationIncrementalVolume_Contractor, 
            demandsToBeMetByContingentOptions_Contractor, 
            appliedDemand_Contractor,
            volumeSurfaceCarryover_Contractor,
            volumeGroundwaterBank_Contractor,
        ):
        self.contractor = contractor
        self.i = i
        self.plannedLongTermConservation_Contractor = plannedLongTermConservation_Contractor
        self.totalDemand_Contractor = totalDemand_Contractor
        self.longtermWMOConservationIncrementalVolume_Contractor = longtermWMOConservationIncrementalVolume_Contractor
        self.demandsToBeMetByContingentOptions_Contractor = demandsToBeMetByContingentOptions_Contractor
        self.appliedDemand_Contractor = appliedDemand_Contractor
        self.volumeSurfaceCarryover_Contractor = volumeSurfaceCarryover_Contractor
        self.volumeGroundwaterBank_Contractor = volumeGroundwaterBank_Contractor