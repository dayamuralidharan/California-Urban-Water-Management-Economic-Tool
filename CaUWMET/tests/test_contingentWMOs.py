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

