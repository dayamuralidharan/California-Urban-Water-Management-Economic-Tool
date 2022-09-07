import unittest
from src.modelLogic.storageUtilities import putExcessSupplyIntoStorage, takeFromStorage

# Test puts of excess supplies into storage
class StoragePutTests(unittest.TestCase):
    def setUp(self):
        self.i = 0
        self.excessSupply_Contractor = [10]
        self.availableGroundwaterCapacity_Contractor = 15
        self.groundwaterMaximumPutCapacity_Contractor = 5
        self.rechargeEffectiveness_Contractor = 0.9
        self.availableCapacitySurface_Contractor = 15
        self.surfaceMaximumPutCapacity_Contractor = 5

    def testExcessSupplySwitchIsSetToPutIntoCarryoverAndGroundwaterBank(self):
        self.verifyGroundWaterAndSurfacePutsForSwitch(4.5, 5, "Put into Carryover and Groundwater Bank")

    def testExcessSupplySwitchIsSetToPutIntoGroundwaterBank(self):
        self.verifyGroundWaterAndSurfacePutsForSwitch(4.5, 0, "Put into Groundwater Bank")
        
    def testExcessSupplySwitchIsSetToSurfaceCarryover(self):
        self.verifyGroundWaterAndSurfacePutsForSwitch(0, 5, "Put into Carryover Storage")
        
    def testExcessSupplySwitchIsSetToTurnbackPool(self):
        self.verifyGroundWaterAndSurfacePutsForSwitch(0, 0, "Turnback Pool")
        
    def verifyGroundWaterAndSurfacePutsForSwitch(self, groundwater, surface, switch): # arguments here are the values the results should equal for the test to pass
        excessSupplySwitch_Contractor = switch
        putStorage = putExcessSupplyIntoStorage(self.i, excessSupplySwitch_Contractor, self.excessSupply_Contractor, 
                                                self.availableGroundwaterCapacity_Contractor, self.groundwaterMaximumPutCapacity_Contractor, 
                                                self.rechargeEffectiveness_Contractor, self.availableCapacitySurface_Contractor, 
                                                self.surfaceMaximumPutCapacity_Contractor)
        self.assertEqual(putStorage['putGroundwater_Contractor'], groundwater)
        self.assertEqual(putStorage['putSurface_Contractor'], surface)
        
        
# Test puts of excess supplies into storage
class StorageTakeTests(unittest.TestCase):
    def setUp(self):
        self.i = 0
        self.demandsToBeMetByStorage_Contractor = [400000]
        self.volumeSurfaceCarryover_Contractor = [500000]
        self.surfaceMaximumCapacity_Contractor = 1000000
        self.surfaceMaximumTakeCapacity_Contractor = 600000
        #self.storageHedgingStrategySwitch_Contractor
        self.hedgingPoint_Contractor = 60
        self.hedgeCallStorageFactor_Contractor = 0.25
        self.hedgingStorageCapacityFactor_Contractor = 0.25

    def testStorageHedgingSwitchIsSetToCarryoverAndGroundwaterBank(self):
        self.verifyGroundWaterAndSurfaceTakesForSwitch(440540, "Surface  and Groundwater Storage")

#     #def testStorageHedgingSwitchIsSetToGroundwaterBank(self):
#         #self.verifyGroundWaterAndSurfaceTakesForSwitch(4.5, 0, "Groundwater Bank Only")
        
#     def testStorageHedgingSwitchIsSetToSurfaceCarryover(self):
#         self.verifyGroundWaterAndSurfaceTakesForSwitch(440540, "Surface Carryover Only")
        
#     def testStorageHedgingSwitchIsSetToOff(self):
#         self.verifyGroundWaterAndSurfaceTakesForSwitch(400000, "Off")
        
    def verifyGroundWaterAndSurfaceTakesForSwitch(self, surface, switch): #groundwater,
        storageHedgingStrategySwitch_Contractor = switch
        takeStorage = takeFromStorage(self.i, storageHedgingStrategySwitch_Contractor, self.demandsToBeMetByStorage_Contractor, 
                                                            self.volumeSurfaceCarryover_Contractor, self.surfaceMaximumCapacity_Contractor, 
                                                            self.surfaceMaximumTakeCapacity_Contractor, self.hedgingPoint_Contractor, 
                                                            self.hedgeCallStorageFactor_Contractor, self.hedgingStorageCapacityFactor_Contractor)
        #self.assertEqual(takeStorage['takeGroundwater_Contractor'], groundwater)
        self.assertEqual(takeStorage['takeSurface_Contractor'], surface)