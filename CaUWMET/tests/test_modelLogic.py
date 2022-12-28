import unittest
from src.modelLogic.inputData import InputData
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.storageUtilities import StorageUtilities
from tests.inputDataLocationsForTesting import InputDataLocationsForTesting

# Test puts of excess supplies into storage
class ContingentConservationImplementationTests(unittest.TestCase): #this class is inheriting functionality of the unittest.TestCase class
    def setUp(self):
        inputData = InputData(InputDataLocationsForTesting())
        self.modelLogic = ModelLogic(inputData, StorageUtilities()) #creates an instance of the Model Logic class so it inherits the variables and methods within it, e.g. implementContingencyConservation function
        
        #self.inputData.plannedLongTermConservation[self.inputData.plannedLongTermConservation['Contractor'] == self.contractor][self.inputData.futureYear].values[0]
        
    def testModelLogic(self):
        self.modelLogic.execute()
        #print(self.modelLogic.inputData.totalDemands['Metropolitan Water District of Southern California'][0])
        #self.assertEqual(self.modelLogic.inputData.plannedLongTermConservation['Contractor'] == 'Metropolitan Water District of Southern California', 5)
        #self.assertEqual(self.modelLogic.inputData.totalDemands['Metropolitan Water District of Southern California'][0], 1000000)
        
        self.assertEqual(self.modelLogic.appliedDemands['Metropolitan Water District of Southern California'][0], 999995)

        

