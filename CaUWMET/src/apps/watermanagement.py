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
from appsUtilities import opt_echo

def app():

    with opt_echo():
        st.title('Water Management Options Assumptions')
        st.write("")
        st.write("<Description of Water Management Options Assumptions and Steps to use this page to be added.>")
        st.write("")