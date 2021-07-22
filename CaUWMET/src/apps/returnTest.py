import streamlit as st
import traceback
from load_css import local_css
import SessionState
from appsUtilities import opt_echo

def app():
    
    with opt_echo():
        st.title('Testing page')
        st.write(SessionState.get().demandsDatasetChoice)
        st.write(SessionState.get().useBySectorDatasetChoice)
        st.write(SessionState.get().intExtUseBySectorDatasetChoice)


