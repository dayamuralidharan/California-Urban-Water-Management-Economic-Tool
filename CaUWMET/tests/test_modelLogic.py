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
        
        # After each supply source is delivered/demand reduction is implemented, test remaining demands are as expected, along with any associated costs
        # Test implementation of planned long-term conservation
        self.assertEqual(self.modelLogic.outputHandler.appliedDemands['Metropolitan Water District of Southern California'][0], 999995)
        
        # Test delivery of local supplies
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetBySWPCVP['Metropolitan Water District of Southern California'][0], 964915)
        # Test long-term WMO costs
        self.assertEqual(self.modelLogic.surfaceLongTermWMOCost_Contractor[0], 100)
        self.assertEqual(self.modelLogic.groundwaterLongTermWMOCost_Contractor[0], 100)
        self.assertEqual(self.modelLogic.desalinationLongTermWMOCost_Contractor[0], 100)
        self.assertEqual(self.modelLogic.recycledLongTermWMOCost_Contractor[0], 100)
        self.assertEqual(self.modelLogic.potableReuseLongTermWMOCost_Contractor[0], 100)
        self.assertEqual(self.modelLogic.transfersAndExchangesLongTermWMOCost_Contractor[0], 100)
        self.assertEqual(self.modelLogic.otherSupplyLongTermWMOCost_Contractor[0], 100)
        self.assertEqual(self.modelLogic.conservationLongTermWMOCost_Contractor[0], 100)
        
        
        # Test deliveries of SWP/CVP supplies
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetByStorage['Metropolitan Water District of Southern California'][0], 959915)
        self.assertEqual(self.modelLogic.swpCVPDeliveryCost_Contractor[0], 500000)
        
        # Test deliveries from storage (groundwater bank and carryover)
        self.assertEqual(self.modelLogic.outputHandler.takeSurface['Metropolitan Water District of Southern California'][0], 516500)
        self.assertEqual(self.modelLogic.outputHandler.takeGroundwater['Metropolitan Water District of Southern California'][0], 95000)
        self.assertEqual(self.modelLogic.outputHandler.putSurface['Metropolitan Water District of Southern California'][0], 0)
        self.assertEqual(self.modelLogic.outputHandler.putGroundwater['Metropolitan Water District of Southern California'][0], 0)
        self.assertEqual(self.modelLogic.outputHandler.takeGroundwaterBankCost['Metropolitan Water District of Southern California'][0], 19506431.092)
        self.assertEqual(self.modelLogic.outputHandler.putGroundwaterBankCost['Metropolitan Water District of Southern California'][0], 0)
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetByContingentOptions['Metropolitan Water District of Southern California'][0], 348415.0)
        
        #Test implementation of Contingent Conservation Programs
        #TODO switch all variables to output handler variable like those above
        self.assertEqual(self.modelLogic.contingencyWMOs.demandsToBeMetByWaterMarketTransfers_Contractor[0], 298415.25)
        self.assertEqual(self.modelLogic.contingentConservationCost_Contractor[0], 21900500)
        
        # Test delivery of Water Market Transfers
        self.assertEqual(self.modelLogic.contingencyWMOs.totalShortage_Contractor[0], 297415.25)
        self.assertEqual(self.modelLogic.waterMarketTransferCost_Contractor[0], 468093.5324)
        
        # Test other delivery reliability costs
        self.assertEqual(self.modelLogic.totalSuppliesDelivered_Contractor[0], 652580)
        self.assertEqual(self.modelLogic.waterTreatmentCost_Contractor[0], 249294165.24617)
        self.assertEqual(self.modelLogic.distributionCost_Contractor[0], 189153045.02617002)
        self.assertEqual(self.modelLogic.wastewaterTreatmentCost_Contractor[0], 79756562.338471)
        
        # Test total reliability cost
        self.assertEqual(self.modelLogic.reliabilityManagementCost_Contractor[0], 560579597.235211)
        
        # Test remaining shortages and associated costs
        self.assertEqual(self.modelLogic.totalShortage_Contractor[0], 297415.25)
        
        
        
        

        
        
        

        # print(self.modelLogic.excessSupply_Contractor[0])
        
        #Test averaging of total cost over all timesteps
        #self.assertEqual(self.modelLogic.averageTotalAnnualCost_Contractor, 374572365.19908273)
        
        
        
        

