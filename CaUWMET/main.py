
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations
from src.modelLogic.costOptimizer import CostOptimizer

inputData = InputData(InputDataLocations())
modelLogic = ModelLogic(inputData, StorageUtilities())
costOptimizer = CostOptimizer(inputData, modelLogic)
costOptimizer.optimizeWMOs()
print("Completed running main file")