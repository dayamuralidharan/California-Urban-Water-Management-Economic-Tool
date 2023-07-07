from unittest import TestCase
from src.modelLogic.inputData import InputData
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.storageUtilities import StorageUtilities
from tests.inputDataLocationsForTesting import InputDataLocationsForTesting

# See CaUWMET_Tests.xlsx for how values for assertEqual functions below were calculated
# See CaUWMET_CPED example for Python test.xlsx for how the values in the assertEqual functions below were calculated for the economic loss variables

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
        self.assertEqual(self.modelLogic.outputHandler.appliedDemands['Metropolitan Water District of Southern California'][0], 999985)
        
        # Test delivery of local supplies
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetBySWPCVP['Metropolitan Water District of Southern California'][0], 964905)
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
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetByStorage['Metropolitan Water District of Southern California'][0], 959905)
        self.assertEqual(self.modelLogic.swpCVPDeliveryCost_Contractor[0], 500000)
        
        # Test deliveries from storage (groundwater bank and carryover)
        self.assertEqual(self.modelLogic.outputHandler.takeSurface['Metropolitan Water District of Southern California'][0], 516500)
        self.assertEqual(self.modelLogic.outputHandler.takeGroundwater['Metropolitan Water District of Southern California'][0], 95000)
        self.assertEqual(self.modelLogic.outputHandler.putSurface['Metropolitan Water District of Southern California'][0], 0)
        self.assertEqual(self.modelLogic.outputHandler.putGroundwater['Metropolitan Water District of Southern California'][0], 0)
        self.assertEqual(self.modelLogic.outputHandler.takeGroundwaterBankCost['Metropolitan Water District of Southern California'][0], 19506431.092)
        self.assertEqual(self.modelLogic.outputHandler.putGroundwaterBankCost['Metropolitan Water District of Southern California'][0], 0)
        self.assertEqual(self.modelLogic.outputHandler.demandsToBeMetByContingentOptions['Metropolitan Water District of Southern California'][0], 348405.0)
        
        #Test implementation of Contingent Conservation Programs
        #TODO switch all variables to output handler variable like those above
        self.assertEqual(self.modelLogic.contingencyWMOs.demandsToBeMetByWaterMarketTransfers_Contractor[0], 298405.75)
        self.assertEqual(self.modelLogic.totalShortage_Contractor[0], 297405.75)
        self.assertEqual(self.modelLogic.contingentConservationCost_Contractor[0], 21900500)
        self.assertEqual(self.modelLogic.waterMarketTransferCost_Contractor[0], 468093.5324)
        
        # Test other delivery reliability costs
        self.assertEqual(self.modelLogic.totalSuppliesDelivered_Contractor[0], 652580)
        self.assertEqual(self.modelLogic.waterTreatmentCost_Contractor[0], 249294165.24617)
        self.assertEqual(self.modelLogic.distributionCost_Contractor[0], 189153045.02617002)
        self.assertEqual(self.modelLogic.wastewaterTreatmentCost_Contractor[0], 79756562.338471)
        self.assertEqual(self.modelLogic.rationingProgramCost_Contractor[0], 175204000.0)
        
        # Test total reliability cost
        self.assertEqual(self.modelLogic.reliabilityManagementCost_Contractor[0], 735783597.235211)
        
        # Test shortage by use type
        # Note most variables used to calculate the economic loss are not lists and last timestep is tested instead of i=0
        self.assertEqual(self.modelLogic.totalDemand_Contractor[93], 1500000)
        self.assertEqual(self.modelLogic.plannedLongTermConservation_Contractor, 5)
        self.assertEqual(self.modelLogic.totalShortage_Contractor[93], 773305.75)
        self.assertEqual(self.modelLogic.economicLossByUseType.shortageByUseType.baseConservationAsPercentOfDemand, 3.3333333333333333e-06)
        self.assertEqual(self.modelLogic.economicLossByUseType.shortageByUseType.demandHardeningAdjustmentFactor_Contractor, 1.0000050000111111)
        self.assertEqual(self.modelLogic.economicLossByUseType.shortageByUseType.adjustedShortage_Contractor, 0.5155397443582282)
        
        
        self.assertEqual(self.modelLogic.economicLossByUseType.shortageByUseType.singleFamilyShortagePortionOfSingleFamilyUse_Contractor, 0.39848482655708467)
        self.assertEqual(self.modelLogic.economicLossByUseType.shortageByUseType.singleFamilyShortage_Contractor, 448290.9469224215)
        self.assertEqual(self.modelLogic.economicLossByUseType.shortageByUseType.multiFamilyShortage_Contractor, 134487.28407672644)
        
        
        # Test economic loss function
        self.assertEqual(self.modelLogic.outputHandler.appliedDemands['Metropolitan Water District of Southern California'][93], 1499985)

        
        self.assertEqual(self.modelLogic.economicLossByUseType.constantOfIntegration_SF['Metropolitan Water District of Southern California'], 4108949.9456299148)
        self.assertEqual(self.modelLogic.economicLossByUseType.singleFamilyEconomicLoss_Contractor, 1213606550.9561996)
        self.assertEqual(self.modelLogic.economicLossByUseType.multiFamilyEconomicLoss_Contractor, 319933590.67021227)
        self.assertEqual(self.modelLogic.economicLossByUseType.totalEconomicLoss_Contractor[93], 1966292083.8347049)
        
        
        
        

