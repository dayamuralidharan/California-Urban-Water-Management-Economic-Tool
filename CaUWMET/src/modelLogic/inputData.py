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
    
    def getContingentConservationUnitCost(self):
        return contingentConservationUnitCost
    
    def getUrbanPopulation(self):
        return urbanPopulation
    
    def getShortageThresholdForWaterMarketTransfers(self):
        return shortageThresholdForWaterMarketTransfers
    
    def getTransferLimit(self):
        return transferLimit 
    
    def getWaterMarketTransferCost(self):
        return waterMarketTransferCost
    
    