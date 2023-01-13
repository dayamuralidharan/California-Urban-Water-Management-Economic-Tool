from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

inputData = InputData(InputDataLocations())
modelLogic = ModelLogic(inputData, StorageUtilities())

modelLogic.loopThroughWmoIncrementalVolumes()
