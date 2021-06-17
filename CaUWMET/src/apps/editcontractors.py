import base64
import numbers
import pandas as pd
import streamlit as st
from streamlit.hashing import _CodeHasher
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
import traceback
from load_css import local_css

st.set_page_config(layout="wide")

def app():

    state = get_state()        
    if state.data is None:

        col_list = ["Contractor", "Study Region", "Hydro. Region", "Type", "Key Info", "SWP or CVP"]

        state.data = pd.DataFrame(pd.read_csv("inputData/contractorInformation.csv", usecols=col_list))
    
    local_css("style.css")
    st.title("Contractor Descriptions")
    st.write("This page is where you can modify contractor names, associated study and hydrologic regions, type, etc. You can also add or remove contractors from the model here.")
    st.write('')
    st.title('Steps to use this page')
    st.write("<span class='font'>1. Review and modify contractor details in table below.</span>", unsafe_allow_html=True)
    st.write("To add a contractor, scroll to the bottom of the page and click ""Add Row."" This will create a new contractor and be sure to fill out the rest of the contractor's information in the demand, supply and system operations pages.")

    #Table 1    
    #with st.beta_expander("Contractor Information"):
    editor = TableEditor("table1", state.data)

    # Check for button interactions and updates the internal data state
    editor.interact()
    state.data = editor.data
    # st.dataframe(state.data)
    state.sync()

    #downloading the dataframe data to a .csv file
    def download_link(object_to_download, download_filename, download_link_text):

        if isinstance(object_to_download,pd.DataFrame):
            object_to_download = object_to_download.to_csv()

        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

    if st.button('Download Updated Contractor Information'):
        tmp_download_link = download_link(state.data, 'contractorInformation.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

class TableEditor:
    """Encapsulates editable tables using streamlit.

    Usage:
    >>> original_df = pd.DataFrame(...)
    >>> editor = TableEditor("editor uid", original_df)
    >>> editor.interact()
    >>> edited_df = editor.data
    """
    def __init__(self, uid, dataframe, layout=None):
        """Initialize TableEditor instance.

        Args:
            uid (str): Table unique identifier to avoid widget key conflict.
            dataframe (pandas.DataFrame): Data to be edited.
            layout (list, optional): List of column proportions. See
            https://docs.streamlit.io/en/stable/api.html#streamlit.beta_columns.
            Defaults to None.
        """
        self._uid = uid
        self._data = dataframe.copy()
        self._n_rows = dataframe.shape[0]
        self._n_cols = dataframe.shape[1]
        self._cells = {}
        self._update_button = None
        self._add_row_button = None
        self._delete_buttons = {}
        if layout is None:
            # If layout not defined the dataframe columns will be 5 times bigger
            # than Delete buttons column
            layout = st.beta_columns(7)
        self._layout = layout
        self._create_table()
        self._create_buttons()

    @property   
    def data(self):
        return self._data

    def interact(self):
        if self._update_button:
            self._update()

        if self._add_row_button:
            self._add_row()

        for key, button in self._delete_buttons.items():
            if button:
                # key[1] is always the row index
                self._delete_row(key[1])
                break

    def _create_table(self):
        # Gets only layout columns to put actual data from dataframe - indices [0:n_cols]
        data_columns = self._layout[:self._n_cols]

        for col_index, column in enumerate(data_columns):
            # Writes column names
            column.markdown(f"**{self._data.columns[col_index]}**")
            for row_index in range(self._n_rows):
                key = (self._uid, col_index, row_index)
                with column:
                    self._add_cell(key, self._data.iloc[row_index, col_index])

    def _create_buttons(self):
        # Always the last column in column layout
        button_del_column = self._layout[self._n_cols]

        # The buttons are not horizontally aligned with input widgets, so we need this little hack
        button_del_column.markdown("<div style='margin-top:4.8em;'></div>", unsafe_allow_html=True)

        for row_index in range(self._n_rows):
            key = (self._uid, row_index)
            self._delete_buttons[key] = button_del_column.button("Delete", key=str(key))
            button_del_column.markdown(
                "<div style='margin-top:2.45em;'></div>", unsafe_allow_html=True
            )

        self._add_row_button = st.button("Add Row", key=f"add_row_button_{self._uid}")
        self._update_button = st.button(label="Update Data", key=f"update_button_{self._uid}")

    def _update(self):
        for col_index in range(self._n_cols):
            for row_index in range(self._n_rows):
                new_value = self._cells[(self._uid, col_index, row_index)].value
                self._data.iloc[row_index, col_index] = new_value
        self._data = self._data.sort_values(by=self._data.columns.to_list(), ignore_index=True)

    def _add_row(self):
        columns = self._data.columns.to_list()
        values = [[""] for _ in columns]
        row = pd.DataFrame(dict(zip(columns, values)))
        self._data = self._data.append(row).reset_index(drop=True)

        for col_index in range(self._n_cols):
            row_index = self._n_rows
            key = (self._uid, col_index, row_index)
            with(self._layout[col_index]):
                self._add_cell(key, self._data.iloc[row_index, col_index])

    def _delete_row(self, row_index):
        self._data = self._data.drop([row_index]).reset_index(drop=True)
        for col_index in range(self._n_cols):
            key = (self._uid, col_index, row_index)
            self._delete_cell(key)

    def _add_cell(self, key, value):
        new_cell = _Cell(key)
        new_cell.value = value
        self._cells[key] = new_cell

    def _delete_cell(self, key):
        del self._cells[key]


class _Cell:
    def __init__(self, uid):
        self._uid = uid
        self._value = None
        self._widget = st.empty()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, numbers.Integral):
            self._value = self._widget.text_input(
                label="",
                value=value,
                # min_value=1,
                # step=1,
                key=self._uid
            )
        elif isinstance(value, float):
            self._value = self._widget.text_input(
                label="",
                value=value,
                # min_value=0.,
                # step=0.001,
                # format="%.3f",
                key=self._uid
            )
        else:
            self._value = self._widget.text_input(
                label="",
                value=value,
                key=self._uid
            )

#
# Code below is from https://gist.github.com/okld/0aba4869ba6fdc8d49132e6974e2e662.
#

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

    # def __setitem__(self, item, value):
    #     """Set state value."""
    #     self._state["data"][item] = value

    # def __setattr__(self, item, value):
    #     """Set state value."""
    #     self._state["data"][item] = value

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

def get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state

if __name__ == "__app__":
    app()