import streamlit as st
import traceback
import pandas as pd

# Class with feature to show source code
# It's not thread-safe. Don't use this if you have threaded
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


def fetch_data(inputdatafile, **kwargs):
    data = pd.read_excel(io = inputdatafile, **kwargs)
    return pd.DataFrame(data)


def selectSpecifiedRows(df, selectionColumn, selectionCriteria):
    return df.loc[df[selectionColumn] == selectionCriteria]

def roundValues(value):
    try:
        if value > 1:
            value = round(float(str(value)))
        else:
            value = value
        return f"{value:,d}"
    except ValueError: 
        return str(value) 


