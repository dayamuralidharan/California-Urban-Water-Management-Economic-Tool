import base64
import streamlit as st
import altair as alt
from itertools import cycle
import traceback
from load_css import local_css
from demandsHelper import load_data, summary_poster
from contextlib import contextmanager
from streamlit.hashing import _CodeHasher
import pandas as pd

# Class with feature to show source code
# This is a mega-hack!
# And it's also not thread-safe. Don't use this if you have threaded
# code that depends on traceback.extract_stack
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

        import traceback

        traceback.extract_stack = self.orig_extract_stack






def fetch_data(inputDataLocation):
    data = pd.read_csv(inputDataLocation)
    return pd.DataFrame(data)




#downloading the dataframe data to a .csv file
def download_link(object_to_download, download_filename, download_link_text):
    # Generates a link to download the given object_to_download.

    # object_to_download (str, pd.DataFrame):  The object to be downloaded.
    # download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    # download_link_text (str): Text to display for download link.

    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

