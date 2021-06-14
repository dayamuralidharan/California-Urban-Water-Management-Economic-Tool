import base64
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
from sklearn import datasets
from multiapp import MultiApp
from apps import editcontractors
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from contextlib import contextmanager
import sys, os
from streamlit.hashing import _CodeHasher
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
import traceback

def app():
    class opt_echo:
        def __init__(self):
            self.checkbox = st.sidebar.checkbox("Show source code")

            # This is a mega-hack!
            # And it's also not thread-safe. Don't use this if you have threaded
            # code that depends on traceback.extract_stack
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
        st.title('Results')

        PAGES = {
        "Add/Delete Contractors": editcontractors,
        }

        selection = st.sidebar.radio("Go to",list(PAGES.keys()))

        # st.sidebar.title(":floppy_disk: Page states")
        # page = st.sidebar.radio("Select your page", tuple(PAGES.keys()))

        # Display the selected page with the session state
        # pages[page](state)

        # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
        # state.sync()

        #Piece of code used to execute a set of lines but suppress the putput from getting displayed
        # git checkout main
        # def suppress_stdout():
        #     with open(os.devnull, "w") as devnull:
        #         old_stdout = sys.stdout
        #         sys.stdout = devnull
        #         try:  
        #             yield
        #         finally:
        #             sys.stdout = old_stdout

        #Will load demands page on the results page but will suppress the output (i.e. displaying all the contents of the demands page)
            #with suppress_stdout():

        page = PAGES[selection]
        page.app()

        class _SessionState:

            def __init__(self, session, hash_funcs):
                """Initialize SessionState instance."""
                self.__dict__["_state"] = {
                    "data": {},
                    "hash": None,
                    "hasher": _CodeHasher(hash_funcs),
                    "is_rerun": False,
                    "session": session,
                }

            def __call__(self, **kwargs):
                """Initialize state data once."""
                for item, value in kwargs.items():
                    if item not in self._state["data"]:
                        self._state["data"][item] = value

            def __getitem__(self, item):
                """Return a saved state value, None if item is undefined."""
                return self._state["data"].get(item, None)
                
            def __getattr__(self, item):
                """Return a saved state value, None if item is undefined."""
                return self._state["data"].get(item, None)

            def __setitem__(self, item, value):
                """Set state value."""
                self._state["data"][item] = value

            def __setattr__(self, item, value):
                """Set state value."""
                self._state["data"][item] = value
            
            def clear(self):
                """Clear session state and request a rerun."""
                self._state["data"].clear()
                self._state["session"].request_rerun()
            
            def sync(self):
                """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

                # Ensure to rerun only once to avoid infinite loops
                # caused by a constantly changing state value at each run.
                #
                # Example: state.value += 1
                if self._state["is_rerun"]:
                    self._state["is_rerun"] = False
                
                elif self._state["hash"] is not None:
                    if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                        self._state["is_rerun"] = True
                        self._state["session"].request_rerun()

                self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)

        def _get_session():
            session_id = get_report_ctx().session_id
            session_info = Server.get_current()._get_session_info(session_id)

            if session_info is None:
                raise RuntimeError("Couldn't get your Streamlit Session object.")
            
            return session_info.session

        def _get_state(hash_funcs=None):
            session = _get_session()

            if not hasattr(session, "_custom_session_state"):
                session._custom_session_state = _SessionState(session, hash_funcs)

            return session._custom_session_state

        # state = _get_state()
        # sum2030 = state.sum2030
        # st.write(sum2030)
        # st.write(state)   
