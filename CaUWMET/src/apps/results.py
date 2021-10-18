import streamlit as st
from globalUtilities import opt_echo

def app():
    with opt_echo():      
        st.title('Results')
