import streamlit as st
from src.globalUtilities import opt_echo

def app():
    
    with opt_echo():
        st.title('Testing page')

        st.write(st.session_state.totalDemandsChoice)
        st.write(st.session_state.baseLongTermConservationChoice)
        st.dataframe(st.session_state.totalDemandsdf)
        st.dataframe(st.session_state.useByTypedf)
        st.dataframe(st.session_state.intExtUseByTypedf)
        st.dataframe(st.session_state.baseLongTermConservationdf)


