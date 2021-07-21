import base64
from typing import ValuesView
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
from sklearn import datasets
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import traceback
from load_css import local_css

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

            # For some reason I need to import this again.
            import traceback

            traceback.extract_stack = self.orig_extract_stack

    with opt_echo():
        st.title('Water Management Options Assumptions')
        st.write("")
        st.write("<Description of Water Management Options Assumptions and Steps to use this page to be added.>")
        st.write("")