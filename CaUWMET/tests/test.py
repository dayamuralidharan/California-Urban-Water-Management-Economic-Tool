import unittest

# Adding "unittest.testcase" in the argument allows the class WaterUserTest to inherit the unit test library's functionalities.
class WaterUseTest(unittest.testcase):

    def testSumOfWaterUseTypesEqualsTotalDemand(self):
        isTotalWaterUseEqualToDemand = False
        assert isTotalWaterUseEqualToDemand == True


# Read in demand and water use data
