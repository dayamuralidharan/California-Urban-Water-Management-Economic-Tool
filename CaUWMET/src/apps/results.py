import streamlit as st
from appsUtilities import opt_echo

def app():
    with opt_echo():      
        st.title('Results')
