import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

def dashboard(df1, df2):
    st.title("Hertzsprung-Russell Diagram Explorer")

    data= st.selectbox("Dataset:", ["Near-Earth", "Far-Earth"])
    if data== "Near-Earth":
        df= df1
    else:
        df= df2

    diag_type= st.sidebar.selectbox("Diagram type:", ["Observational", "Theoretical", "Spectroscopic"])
    if diag_type== "Observational":
        x_ax= "Color index"
        y_ax= "Absolute magnitude"
    elif diag_type== "Theoretical":
        x_ax= "Log effective temperature"
        y_ax= "Log luminosity"
    else:
        x_ax= "Log effective temperature"
        y_ax= "Log surface gravity"

    clr_ax= "Color index"
    clr_scl= st.sidebar.selectbox("Colour scheme:", ["Blues", "Greys", "Plasma", "RdYlBu", "Reds"])

    fig= px.scatter(df, x=x_ax, y=y_ax, color= clr_ax, color_continuous_scale= clr_scl)
    fig.update_traces(marker={'size': 1})
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(autorange="reversed")

    st.write(fig)
    st.write(df)

if __name__== "__main__":
    df1 = pd.read_csv("near_earth_50k_clean_calc.csv")
    df2 = pd.read_csv("far_earth_50k_clean_calc.csv")
    dashboard(df1, df2)
