# Find water management portfolio option that has the least cost

# Loop through incremental volumes of supply/demand options input by user for each contractor - j
# Calculate average annual cost for each contractor - k
# Total average annual cost for all contractors - j
# Fit a curve to total annual average cost from each incremental volume loop
# Calculate global minimum on curve
# Return supply volume increments that correspond to that global min

class CostOptimizer:
    
    def __init__(self, modelLogic):
        self.modelLogic = modelLogic
        self.minimumCost = 0
        
        self.longtermWMOConservationIncrementalVolume_Contractor = 10
        self.longtermWMOSurfaceSupplyIncrementalVolume_Contractor = 10
        self.longtermWMOGroundwaterSupplyIncrementalVolume_Contractor = 10
        self.longtermWMODesalinationSupplyIncrementalVolume_Contractor = 10
        self.longtermWMORecycledSupplyIncrementalVolume_Contractor = 10
        self.longtermWMOPotableReuseSupplyIncrementalVolume_Contractor = 10
        self.longtermWMOTransfersAndExchangesSupplyIncrementalVolume_Contractor = 10
        self.longtermWMOOtherSupplyIncrementalVolume_Contractor = 10
        
    #def optimize(self):
        #for volume in waterManagementVolumes:
            #self.modelLogic.executeModelLogic(volume)