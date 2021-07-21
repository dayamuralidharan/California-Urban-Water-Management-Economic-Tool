import streamlit as st
import traceback
from load_css import local_css
from demandsHelper import getTestValue
import GlobalUiState

def app():
    
    class opt_echo:
        def __init__(self):
            self.checkbox = st.sidebar.checkbox("Show source code")
            self.orig_extract_stack = traceback.extract_stack

            if self.checkbox:
                traceback.extract_stack = lambda: self.orig_extract_stack()[:-2]
                self.echo = st.echo()

        def __enter__(self):
            if self.checkbox:
                return self.echo.__enter__()

        def __exit__(self, type, value, traceback):
            if self.checkbox:
                self.echo.__exit__(type, value, traceback)

            # This needs to be imported again.
            import traceback

            traceback.extract_stack = self.orig_extract_stack

    with opt_echo():
        st.title('Testing page')
        globalUiState = GlobalUiState()
        globalUiState.updateState(checkBoxReturn = True)
        defaultState = globalUiState.getState()
        testVar = st.checkbox('Test Check Box', value = defaultState.checkBoxReturn)
        st.write(testVar)
        st.write(getTestValue() + 1)
