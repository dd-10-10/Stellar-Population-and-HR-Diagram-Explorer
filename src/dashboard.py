import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from helper.filters import *
from helper.custom_slider import *

def dashboard(df):
    '''
    Function to generate the diagram and dashboard from data
    '''

    st.set_page_config(layout="wide")

    st.markdown("<h1 style='text-align: center;'>Hertzsprung-Russell Diagram Explorer</h1>", unsafe_allow_html=True)

    df= clean_measured(df)
    filter_col, out_col= st.columns(2, gap= "medium")

    with filter_col:
        # Filtering data in various ways

        vals= num_slider("Select range of distance from Earth:", df["Distance"].min(), df["Distance"].max(), "dist_sl")
        df= df[(df["Distance"]>= vals[0]) & (df["Distance"]<= vals[1])]
        

        # Filters
        #df= hard_filter(df, ["Apparent G magnitude", "Color index", "Effective temperature", "Log luminosity"])
        df= del_outliers(df, ["Apparent G magnitude", "Color index", "Effective temperature", "Log luminosity"])

    with out_col:
        # Tabs
        st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)
        diag_tab, data_tab= st.tabs(["Diagram", "Summary Statistics"], key= "tabs")

        # HR Diagram
        with diag_tab:
            # Axis selection
            xcol, ycol= st.columns(2)
            with xcol:
                x_ax= st.selectbox("X-axis:", ["Color index", "Log effective temperature"])
            with ycol:
                y_ax= st.selectbox("Y-axis:", ["Absolute magnitude", "Log luminosity"])

            # Color
            clr_ax= "Color index"
            clr_scl= st.selectbox("Colour scheme:", ["Blues", "Greys", "Plasma", "RdYlBu", "Reds"], index= 3)

            # Plotting the data
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

            # Displaying the plot
            st.write(fig)

# Execution
if __name__== "__main__":
    df = pd.read_csv("data/stars_clean_calc.csv")
    dashboard(df)
