import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

def dashboard(df):
    st.title("Hertzsprung-Russell Diagram Explorer")

    x_ax= st.sidebar.selectbox("X-axis:", df.columns)
    y_ax= st.sidebar.selectbox("Y-axis:", df.columns)
    clr= st.sidebar.selectbox("Colour based on:", df.columns)

    fig= px.scatter(df, x=x_ax, y=y_ax, color= clr, color_continuous_scale= "rdylbu")

    st.write(fig)
    st.write(df)

if __name__== "__main__":
    df = pd.read_csv("Near_Earth.csv")
    dashboard(df)
