class InputDataLocations:
    def __init__(self):
        self.futureYearInput = '2045'
        
        self.hydroYearTypeInput = "src/inputData/contractorInput_hydrologyAssumptions.csv"
        self.contractorInformationInput = "src/inputData/contractorInput_contractorInfo.csv"
        
        self.totalDemandScenarioRadioButtonIndex = 0 ##TODO - delete
        
        self.wmoSupplyVolumeIncrement = 0.1##TODO - delete
        
        self.inputDemandsFile = "src/inputData/demandsInput_totalDemands.csv"
        self.inputPlannedConservationFile = "src/inputData/demandsInput_baseLongTermConservationData.csv"
        self.inputETAWAdjustmentsFile = "src/inputData/demandsInput_ETAWAdjustments.csv"
        self.inputUseByTypeFile = "src/inputData/demandsInput_useByTypeData.csv"
        
        self.localSuppliesDataInput = "src/inputData/supplyInput_localSupplies.csv"
        self.supplyDesalinationTimeseriesInput = "src/inputData/supplyInput_desalinationTimeSeries.csv"
        self.supplyGroundwaterTimeseriesInput = "src/inputData/supplyInput_groundwaterTimeSeries.csv"
        self.supplyOtherTimeseriesInput = "src/inputData/supplyInput_otherSupplyTimeSeries.csv"
        self.supplyPotableTimeseriesInput = "src/inputData/supplyInput_potableTimeSeries.csv"
        self.supplyRecycledTimeseriesInput = "src/inputData/supplyInput_recycledTimeSeries.csv"
        self.supplySurfaceTimeseriesInput = "src/inputData/supplyInput_surfaceTimeSeries.csv"
        self.supplyExchangesTimeseriesInput = "src/inputData/supplyInput_transfersAndExchangesTimeSeries.csv"
        self.swpCVPSupplyDataInput = "src/inputData/supplyInput_SWPCVPCalsimII2020BenchmarkStudy.csv"
        
        self.storageDataInput = "src/inputData/systemOperationsInput_Storage.csv"
        self.excessWaterSwitchDataInput = "src/inputData/systemOperationsInput_ExcessWaterSwitch.csv"
        self.storageHedgingStrategyInput = "src/inputData/systemOperationsInput_StorageHedgingStrategy.csv"
        self.deliveryCostInput = "src/inputData/systemOperationsInput_DeliveryCosts.csv"
        
        self.contingentConservationInputFile = "src/inputData/contingentWMOsInput_conservation.csv"
        self.waterMarketTransfersInputFile = "src/inputData/contingentWMOsInput_WaterMarketTransfers.csv"
        self.rationingProgramInputFile = "src/inputData/contingentWMOsInput_rationingProgram.csv"
        self.cutRatioInputFile = "src/inputData/contingentWMOsInput_cutRatios.csv"
        self.elasticityOfDemandInputFile = "src/inputData/contingentWMOsInput_elasticityofDemand.csv"
        
        self.longtermWMOSupplyVolumeInputData = "src/inputData/longtermWMOsInput_supplyVolume.csv"
        self.longtermWMOSupplyUnitCostsInputData = "src/inputData/longtermWMOsInput_supplyCosts.csv"
        