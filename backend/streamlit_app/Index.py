import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Camera",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

def load_data():
    return pd.read_csv("camera_dataset.csv")

st.write("Welcome to the Home Page!")
st.write("You can perform different EDA methods from the sidebar.")

    

