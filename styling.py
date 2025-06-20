import streamlit as st

def apply_custom_style():
    st.set_page_config(page_title="Origin Generator", layout="wide", initial_sidebar_state="auto")

    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .st-emotion-cache-18ni7ap {display: none;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
