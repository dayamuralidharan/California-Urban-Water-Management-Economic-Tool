from src.modelLogic.readSupplyAssumptions import totalLocalSupply, swpCVPSupply
from src.modelLogic.readContingentWMOsAssumptions import contingentConservationUseReduction, contingentConservationStorageTrigger, contingentConservationUnitCost, urbanPopulation, shortageThresholdForWaterMarketTransfers, transferLimit, waterMarketTransferCost

class InputData:
    def getTotalLocalSupply(self):
        return totalLocalSupply
    
    def getSwpCvpSupply(self):
        return swpCVPSupply
    
    def getContingentConservationUseReduction(self):
        return contingentConservationUseReduction
    
    def getContingentConservationStorageTrigger(self):
        return contingentConservationStorageTrigger