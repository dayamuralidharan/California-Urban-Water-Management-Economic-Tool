class ContingentWmosUtilities:
        
    def implementContingencyConservation(self, demandsToBeMetByWaterMarketTransfers_Contractor, demandsToBeMetByContingentOptions_Contractor, i, contingentConservationUseReductionVolume_Contractor):
        # Set variables
        self.demandsToBeMetByWaterMarketTransfers_Contractor = demandsToBeMetByWaterMarketTransfers_Contractor
        self.demandsToBeMetByContingentOptions_Contractor = demandsToBeMetByContingentOptions_Contractor
        self.i = i
        self.contingentConservationUseReductionVolume_Contractor = contingentConservationUseReductionVolume_Contractor