import unittest
from src.modelLogic.excessUnitTest import putExcessSupplyIntoStorage

# Adding "unittest.testcase" in the argument allows the class WaterUserTest to inherit the unit test library's functionalities.
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
        self.verifyGroundWaterAndSurfaceForSwitch(4.5, 5, "Put into Carryover and Groundwater Bank")

    def testExcessSupplySwitchIsSetToPutIntoGroundwaterBank(self):
        self.verifyGroundWaterAndSurfaceForSwitch(4.5, 0, "Put into Groundwater Bank")
        
    def testExcessSupplySwitchIsSetToSurfaceCarryover(self):
        self.verifyGroundWaterAndSurfaceForSwitch(0, 5, "Put into Carryover Storage")
        
    def testExcessSupplySwitchIsSetToTurnbackPool(self):
        self.verifyGroundWaterAndSurfaceForSwitch(0, 0, "Turnback Pool")
        
    def verifyGroundWaterAndSurfaceForSwitch(self, groundwater, surface, switch):
        excessSupplySwitch_Contractor = switch
        putStorage = putExcessSupplyIntoStorage(self.i, excessSupplySwitch_Contractor, self.excessSupply_Contractor, self.availableGroundwaterCapacity_Contractor, self.groundwaterMaximumPutCapacity_Contractor, self.rechargeEffectiveness_Contractor, self.availableCapacitySurface_Contractor, self.surfaceMaximumPutCapacity_Contractor)
        self.assertEqual(putStorage['putGroundwater_Contractor'], groundwater)
        self.assertEqual(putStorage['putSurface_Contractor'], surface)