import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

def dashboard(df):
    st.title("Hertzsprung-Russell Diagram Explorer")

    x_ax= st.sidebar.selectbox("X-axis:", df.columns)
    y_ax= st.sidebar.selectbox("Y-axis:", df.columns)
    clr_ax= st.sidebar.selectbox("Colour based on:", df.columns)
    clr_scl= st.sidebar.selectbox("Colour scheme:", ["Blues", "Greys", "Plasma", "RdYlBu", "Reds"])

    fig= px.scatter(df, x=x_ax, y=y_ax, color= clr_ax, color_continuous_scale= clr_scl)
    fig.update_traces(marker={'size': 1})

    st.write(fig)
    st.write(df)

if __name__== "__main__":
    df = pd.read_csv("Near_Earth.csv")
    dashboard(df)
