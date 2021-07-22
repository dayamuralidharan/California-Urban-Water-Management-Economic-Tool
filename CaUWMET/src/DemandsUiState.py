import SessionState

"""
Stores and retrieves global state of UI
"""
class DemandsUiState:  
    def setDemandsDatasetChoice(self, choice):
        SessionState.get().demandsDatasetChoice = choice

    def getDefaultDemandsDatasetChoice(self):
        return SessionState.get().demandsDatasetChoice
