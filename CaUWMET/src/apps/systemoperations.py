import streamlit as st
import traceback
from load_css import local_css
from appsUtilities import opt_echo

def app():
    
    with opt_echo():
        st.title('System Operations')

        st.write('This is the `System Operations` page of the dashboard.')