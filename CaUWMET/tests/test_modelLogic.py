from unittest import TestCase
from src.modelLogic.inputData import InputData
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.storageUtilities import StorageUtilities
from tests.inputDataLocationsForTesting import InputDataLocationsForTesting

# See CaUWMET_Tests.xlsx for how values for assertEqual functions below were calculated
# TODO: set up test for economic loss function

class waterBalanceLogicTests(TestCase): #this class is inheriting functionality of the unittest.TestCase class
    def setUp(self):
        inputData = InputData(InputDataLocationsForTesting())
        self.modelLogic = ModelLogic(inputData, StorageUtilities())
        self.modelLogic.contractor = 'Metropolitan Water District of Southern California'
        
        
    def testModelLogic(self):
        self.x = [10, 10, 10, 10, 10, 10, 10, 10]
        self.modelLogic.executeModelLogicForContractor(self.x)
        
        # Test remaining demands are as expected after each supply source is delivered/demand reduction is implemented
        # Test implementation of planned long-term conservation
        self.assertEqual(self.modelLogic.outputHandler.appliedDemands['Metropolitan Water District of Southern California'][0], 999995)
        
        # Test delivery of local supplies
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetBySWPCVP['Metropolitan Water District of Southern California'][0], 964905)
        
        # Test deliveries of SWP/CVP supplies
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetByStorage['Metropolitan Water District of Southern California'][0], 959905)
        
        # Test deliveries from storage (groundwater bank and carryover)
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetByContingentOptions['Metropolitan Water District of Southern California'][0], 348405.0)
        
        #Test implementContingencyConservation
        self.assertEqual(self.modelLogic.contingencyWMOs.demandsToBeMetByWaterMarketTransfers_Contractor[0], 298405.25)
        
        # Test deliverWaterMarketTransfers
        self.assertEqual(self.modelLogic.contingencyWMOs.totalShortage_Contractor[0], 297405.25)
        print('adjustedShortage_Contractor:')
        print(self.modelLogic.contingencyWMOs.shortageByUseType.adjustedShortage_Contractor)
        
        #Test averaging of total cost over all timesteps
        self.assertEqual(self.modelLogic.averageTotalAnnualCost_Contractor, 374572365.19908273)
        
        
        
        

