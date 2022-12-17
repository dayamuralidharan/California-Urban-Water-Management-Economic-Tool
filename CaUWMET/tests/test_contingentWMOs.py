import unittest
from src.modelLogic.inputData import InputData
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.storageUtilities import StorageUtilities

# Test puts of excess supplies into storage
class ContingentConservationImplementationTests(unittest.TestCase): #this class is inheriting functionality of the unittest.TestCase class
    # def setUp(self):
    #     self.modelLogic = ModelLogic() #creates an instance of the Model Logic class so it inherits the variables and methods within it, e.g. implementContingencyConservation function
    #     self.modelLogic.i = 0
        
    #     # Contingent Conservation variables
    #     self.modelLogic.appliedDemand_Contractor = [100]
    #     self.modelLogic.contingentConservationUseReduction_Contractor = 0.1
    #     self.modelLogic.demandsToBeMetByWaterMarketTransfers_Contractor = []
    #     self.modelLogic.demandsToBeMetByContingentOptions_Contractor = [10]
        
    def testModelLogic(self):
        inputData = InputData()
        storageUtilities = StorageUtilities()
        modelLogic = ModelLogic(inputData, storageUtilities)
        modelLogic.execute()
        self.assertEqual(modelLogic.appliedDemands['San Gabriel Valley Municipal Water District'][0], 14191.36)
        
        # Water Market Transfer variabels
        #contractor = ['Metropolitan Water District of Southern California']
        #totalShortage 
        #waterMarketTransferDeliveries
    
    # def testContingentConservationImplementation(self):
    #     self.modelLogic.implementContingencyConservation()
    #     self.assertEqual(self.modelLogic.contingentConservationUseReductionVolume_Contractor, 10)
    #     self.assertEqual(self.modelLogic.demandsToBeMetByWaterMarketTransfers_Contractor[0], 0)
        
    #def testWaterMarketTransfersImplementation(self):
        #self.demandsToBeMetByWaterMarketTransfers = [100]
        #self.modelLogic.deliverWaterMarketTransfers()
        

