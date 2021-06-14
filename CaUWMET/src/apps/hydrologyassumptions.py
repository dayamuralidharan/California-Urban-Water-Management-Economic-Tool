import streamlit as st
import json
#import geopandas as gpd
#import geoviews as gv
import pyproj
import plotly.graph_objs as go
import traceback

def app():
    class opt_echo:
        def __init__(self):
            self.checkbox = st.sidebar.checkbox("Show source code", key = "1")

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
        st.title('Hydrology Assumptions')
        st.markdown('To add: Editable table with calendar year hydrologic classification indices by hydrologic region, from 1922 - 2015. Markdown text to describe table and how hydrology assumptions are incorporated into the model.')

