import streamlit as st
from globalUtilities import opt_echo

def app():
    
    with opt_echo():
        st.title('System Operations')

        st.write('This is the `System Operations` page of the dashboard.')