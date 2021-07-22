import base64
import streamlit as st
import altair as alt
from itertools import cycle
import traceback
from load_css import local_css
from demandsHelper import load_data, summary_poster
from contextlib import contextmanager
from streamlit.hashing import _CodeHasher

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