import streamlit as st
import traceback
from load_css import local_css
import SessionState
from appsUtilities import opt_echo

def app():
    
    with opt_echo():
        st.title('Testing page')
        testVar = st.checkbox('Test Check Box', value = True)
        st.write(testVar)
        st.write(SessionState.get().demandsDatasetChoice)


