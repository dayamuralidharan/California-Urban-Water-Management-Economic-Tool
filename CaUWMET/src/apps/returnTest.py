import streamlit as st
import traceback
from appsUtilities import opt_echo

def app():
    
    with opt_echo():
        st.title('Testing page')

        st.write(st.session_state.totalDemandsChoice)
        st.write(st.session_state.useBySectorChoice)
        st.write(st.session_state.intExtUseBySectorChoice)


