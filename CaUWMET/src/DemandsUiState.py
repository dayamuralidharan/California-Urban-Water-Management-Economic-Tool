import SessionState

"""
Stores and retrieves global state of UI
"""
class DemandsUiState:
    # Functions to set and get Demands Dataset Choice
    def setDemandsDatasetChoice(self, choice):
        SessionState.get().demandsDatasetChoice = choice

    def getDefaultDemandsDatasetChoice(self):
        return SessionState.get().demandsDatasetChoice

    # Functions to set and get Use By Sector Dataset Choice
    def setUseBySectorDatasetChoice(self, choice):
        SessionState.get().useBySectorDatasetChoice = choice

    def getDefaultUseBySectorDatasetChoice(self):
        return SessionState.get().useBySectorDatasetChoice

    # Functions to set and get Interior and Exterior Use By Sector Dataset Choice
    def setIntExtUseBySectorDatasetChoice(self, choice):
        SessionState.get().intExtUseBySectorDatasetChoice = choice

    def getDefaultIntExtUseBySectorDatasetChoice(self):
        return SessionState.get().intExtUseBySectorDatasetChoice
