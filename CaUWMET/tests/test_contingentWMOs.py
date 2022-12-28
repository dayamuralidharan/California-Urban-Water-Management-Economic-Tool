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
        
    def testModelLogic(self):
        self.modelLogic.execute()
        self.assertEqual(self.modelLogic.appliedDemands['San Gabriel Valley Municipal Water District'][0], 14191.36)

        

