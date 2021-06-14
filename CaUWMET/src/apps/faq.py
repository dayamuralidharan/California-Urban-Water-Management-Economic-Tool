import streamlit as st
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

            # This needs to be imported again.
            import traceback

            traceback.extract_stack = self.orig_extract_stack

    with opt_echo():
        st.title('Further Information and Support')

        st.write('TO ADD: DWR contact information, model documentation, how to modify source code, etc.')