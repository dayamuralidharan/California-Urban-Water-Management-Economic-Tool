import streamlit as st
import traceback
from appsUtilities import opt_echo

def app():
    
    with opt_echo():
        st.title('Testing page')
        #st.write(SessionState.get().demandsDatasetChoice)
        #st.write(SessionState.get().useBySectorDatasetChoice)
        #st.write(SessionState.get().intExtUseBySectorDatasetChoice)

        #st.write(SessionState.get().demandsInput)
        st.write(st.session_state.totalDemandsChoice)
        st.write(st.session_state.demandsInput)


