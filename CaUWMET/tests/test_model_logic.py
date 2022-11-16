import unittest
from src.modelLogic.modelLogic import ModelLogic

# Test puts of excess supplies into storage
class ModelLogicTests(unittest.TestCase):

    def testModelLogic(self):
        modelLogic = ModelLogic()
        modelLogic.execute()
        self.assertEqual(modelLogic.appliedDemands['San Gabriel Valley Municipal Water District'][0], 14191.36)
