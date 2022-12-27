from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities

modelLogic = ModelLogic(InputData(), StorageUtilities())

modelLogic.execute()

# To print variables, type modelLogic.NameOfVariable