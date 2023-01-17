from unittest import TestCase
from src.modelLogic.inputData import InputData
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.storageUtilities import StorageUtilities
from tests.inputDataLocationsForTesting import InputDataLocationsForTesting
from src.modelLogic.costOptimizer import CostOptimizer

class CostOptimizationTests(TestCase):
    
    def testPolynomialFunctionWasRetrieved(self):
        inputData = InputData(InputDataLocationsForTesting())
        self.modelLogic = ModelLogic(inputData, StorageUtilities())
        self.costOptimizer = CostOptimizer(inputData, self.modelLogic)
        self.costOptimizer.loopThroughWmoIncrementalVolumes()
        
        self.assertIsNotNone(self.costOptimizer.polyCoefficients)