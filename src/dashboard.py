import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from helper.filters import hard_filters

def dashboard(df):
    '''
    Function to generate the diagram and dashboard from data
    '''
    st.title("Hertzsprung-Russell Diagram Explorer")

    #Filters
    df= hard_filters(df)

    #Selecting data based on distance from Earth
    vals= st.slider("Select range of distance from Earth:", df["Distance"].min(), df["Distance"].max(), (1.0, 100.0))
    
    #Selecting type of diagram; MAY REMOVE IN FUTURE (Theoretical HR diagram cannot be made with only observational data)

    #diag_type= st.sidebar.selectbox("Diagram type:", ["Observational", "Theoretical"])
    y_ax, x_ax= st.selectbox("Y-axis:", ["Absolute magnitude", "Log luminosity"]), st.selectbox("X-axis:", ["Color index", "Log effective temperature"])

    #Color
    clr_ax= "Color index"
    clr_scl= st.selectbox("Colour scheme:", ["Blues", "Greys", "Plasma", "RdYlBu", "Reds"])

    #Plotting the data
    fig= px.scatter(df[(df["Distance"]>= vals[0]) & (df["Distance"]<= vals[1])], x=x_ax, y=y_ax, color= clr_ax, color_continuous_scale= clr_scl+"_r", range_color=[-0.5, 2])
    fig.update_traces(marker={'size': 1})
    
    if y_ax== "Absolute magnitude":
        fig.update_yaxes(range= [15, -10])
    else:
        fig.update_yaxes(range= [-5, 6])
    
    if x_ax== "Color index":
        fig.update_xaxes(range= [-0.5, 2])
    elif x_ax== "Log effective temperature":
        fig.update_xaxes(range= [np.log10(30000), np.log10(1000)])

    #Displaying the plot (and, for now, the data)
    st.write(fig)
    st.write(df)

#Execution
if __name__== "__main__":
    df = pd.read_csv("data/stars_clean_calc.csv")
    dashboard(df)
