import unittest
from src.modelLogic.inputData import InputData
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.storageUtilities import StorageUtilities
from tests.inputDataLocationsForTesting import InputDataLocationsForTesting

# See CaUWMET_Tests.xlsx for how values for assertEqual functions below were calculated


class waterBalanceLogicTests(unittest.TestCase): #this class is inheriting functionality of the unittest.TestCase class
    def setUp(self):
        inputData = InputData(InputDataLocationsForTesting())
        self.modelLogic = ModelLogic(inputData, StorageUtilities()) #creates an instance of the Model Logic class so it inherits the variables and methods within it, e.g. implementContingencyConservation function
        
        #self.inputData.plannedLongTermConservation[self.inputData.plannedLongTermConservation['Contractor'] == self.contractor][self.inputData.futureYear].values[0]
        
    def testModelLogic(self):
        self.modelLogic.executeModelLogic()
        #print(self.modelLogic.inputData.totalDemands['Metropolitan Water District of Southern California'][0])
        #self.assertEqual(self.modelLogic.inputData.plannedLongTermConservation['Contractor'] == 'Metropolitan Water District of Southern California', 5)
        #self.assertEqual(self.modelLogic.inputData.totalDemands['Metropolitan Water District of Southern California'][0], 1000000)
        
        # Test remaining demands are as expected after each supply source is delivered/demand reduction is implemented
        # Test implementation of planned long-term conservation
        self.assertEqual(self.modelLogic.outputHandler.appliedDemands['Metropolitan Water District of Southern California'][0], 999995)
        
        # Test delivery of local supplies
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetBySWPCVP['Metropolitan Water District of Southern California'][0], 964995)
        
        # Test deliveries of SWP/CVP supplies
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetByStorage['Metropolitan Water District of Southern California'][0], 959995)
        
        # Test deliveries from storage (groundwater bank and carryover)
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetByContingentOptions['Metropolitan Water District of Southern California'][0], 348495)
        
        #Test implementContingencyConservation
        self.assertEqual(self.modelLogic.contingencyWMOs.demandsToBeMetByWaterMarketTransfers_Contractor[0], 298495.25)
        
        # Test deliverWaterMarketTransfers
        self.assertEqual(self.modelLogic.contingencyWMOs.totalShortage_Contractor[0], 297495.25)
        
        
        

