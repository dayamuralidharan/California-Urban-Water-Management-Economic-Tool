import streamlit as st
from src.globalUtilities import opt_echo

def app():
    with opt_echo():      
        st.title('Results')
