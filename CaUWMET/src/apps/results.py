import streamlit as st
from src.globalUtilities import opt_echo
#https://docs.streamlit.io/library/components/components-api#render-an-html-string
#https://docs.streamlit.io/library/api-reference/charts/st.bokeh_chart

def app():
    with opt_echo():      
        st.title('CaUWMET Results Page')

        st.markdown("""<div><span class='font'>
        There are ### results output by CaUWMET including:</span></div>""", unsafe_allow_html=True)
        st.write("")
