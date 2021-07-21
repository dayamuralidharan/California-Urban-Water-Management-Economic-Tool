import SessionState

"""
Stores and retrieves global state of UI
"""
class GlobalUiState:
    def __init__(self, **defaultState):
        SessionState.get(defaultState)

    def getState(self):
        return SessionState.get()

    def updateState(self, **newState):
        SessionState.get(newState)
