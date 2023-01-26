class InputDataLocationsForTesting:
    def __init__(self):
        self.futureYearInput = '2045'
        self.hydroYearTypeInput = "tests/inputDataForTests/contractorInput_hydrologyAssumptions.csv"
        self.contractorInformationInput = "tests/inputDataForTests/contractorInput_contractorInfo.csv"
        self.wmoSupplyVolumeIncrement = 0.1
        
        self.inputDemandsFile = "tests/inputDataForTests/demandsInput_totalDemands.csv"
        self.inputPlannedConservationFile = "tests/inputDataForTests/demandsInput_baseLongTermConservationData.csv"
        self.inputETAWAdjustmentsFile = "tests/inputDataForTests/demandsInput_ETAWAdjustments.csv"
        self.inputUseByTypeFile = "tests/inputDataForTests/demandsInput_useByTypeData.csv"
        
        self.totalDemandScenarioRadioButtonIndex = 0
        
        self.localSuppliesDataInput = "tests/inputDataForTests/supplyInput_localSupplies.csv"
        self.supplyDesalinationTimeseriesInput = "tests/inputDataForTests/supplyInput_desalinationTimeSeries.csv"
        self.supplyGroundwaterTimeseriesInput = "tests/inputDataForTests/supplyInput_groundwaterTimeSeries.csv"
        self.supplyOtherTimeseriesInput = "tests/inputDataForTests/supplyInput_otherSupplyTimeSeries.csv"
        self.supplyPotableTimeseriesInput = "tests/inputDataForTests/supplyInput_potableTimeSeries.csv"
        self.supplyRecycledTimeseriesInput = "tests/inputDataForTests/supplyInput_recycledTimeSeries.csv"
        self.supplySurfaceTimeseriesInput = "tests/inputDataForTests/supplyInput_surfaceTimeSeries.csv"
        self.supplyExchangesTimeseriesInput = "tests/inputDataForTests/supplyInput_transfersAndExchangesTimeSeries.csv"
        self.swpCVPSupplyDataInput = "tests/inputDataForTests/supplyInput_SWPCVPCalsimII2020BenchmarkStudy.csv"
        
        self.storageDataInput = "tests/inputDataForTests/systemOperationsInput_Storage.csv"
        self.excessWaterSwitchDataInput = "tests/inputDataForTests/systemOperationsInput_ExcessWaterSwitch.csv"
        self.storageHedgingStrategyInput = "tests/inputDataForTests/systemOperationsInput_StorageHedgingStrategy.csv"
        self.deliveryCostInput = "tests/inputDataForTests/systemOperationsInput_DeliveryCosts.csv"
        
        self.contingentConservationInputFile = "tests/inputDataForTests/contingentWMOsInput_conservation.csv"
        self.waterMarketTransfersInputFile = "tests/inputDataForTests/contingentWMOsInput_WaterMarketTransfers.csv"
        self.rationingProgramInputFile = "tests/inputDataForTests/contingentWMOsInput_rationingProgram.csv"
        self.cutRatioInputFile = "tests/inputDataForTests/contingentWMOsInput_cutRatios.csv"
        self.elasticityOfDemandInputFile = "tests/inputDataForTests/contingentWMOsInput_elasticityofDemand.csv"
        
        self.longtermWMOSupplyVolumeInputData = "tests/inputDataForTests/longtermWMOsInput_supplyVolume.csv"
        self.longtermWMOSupplyUnitCostsInputData = "tests/inputDataForTests/longtermWMOsInput_supplyCosts.csv"