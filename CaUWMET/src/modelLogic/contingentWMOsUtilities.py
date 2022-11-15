import pandas as pd

def getContractorContingentWMOsAssumptions(contractor, futureYear, contingencyConservationData, waterMarketTransfersData, rationingAndEconomicLossData):
        excessSupplySwitch_Contractor = excessWaterSwitchData['Switch'].loc[[contractor]].values[0]
        storageInputDf_Contractor = storageData.loc[[contractor]]
        
        initialSurfaceStorageVolume_Contractor = storageInputDf_Contractor[storageInputDf_Contractor['Variable'] == 'Surface initial storage (acre-feet)'][futureYear].values[0]

        return {'excessSupplySwitch_Contractor':excessSupplySwitch_Contractor}