import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from  helper.filters import *
from  helper.custom_slider import *

def dashboard(df):
    '''
    Function to generate the diagram and dashboard from data
    '''
    st.markdown("""<style>.block-container {padding-top: 2rem !important;}</style>""",unsafe_allow_html=True)
    st.set_page_config(layout="wide")

    st.markdown("<h1 style='text-align: center;'>Hertzsprung-Russell Diagram Explorer</h1>", unsafe_allow_html=True)

    df= clean_measured(df)
    filter_col, out_col= st.columns(2, gap= "medium")

    with filter_col:
        st.subheader("Data filters")
        
        subcont= st.container(height=600)
        with subcont:
            dist_vals= num_slider(label= "Distance from Earth (Parsecs):", min_val= df["Distance"].min(), max_val= df["Distance"].max(),
                                step= step_size(df["Distance"].min(), df["Distance"].max()), sl_key= "dist_sl")
            df= df[(df["Distance"]>= dist_vals[0]) & (df["Distance"]<= dist_vals[1])]
            
            spec_vals= st.multiselect(label= "Spectral classes", options= ["M", "K", "G", "F", "A", "B", "O"],
                                    default= ["M", "K", "G", "F", "A", "B", "O"], key= "spec_vals")
            df= df[df["Spectral class"].isin(spec_vals)]
            
            gmag_vals= num_slider(label= "Apparent G magnitude", min_val= df["Apparent G magnitude"].min(), max_val= df["Apparent G magnitude"].max(),
                                step= step_size(df["Apparent G magnitude"].min(), df["Apparent G magnitude"].max()), sl_key= "gmag_sl")
            df= df[(df["Apparent G magnitude"]>= gmag_vals[0]) & (df["Apparent G magnitude"]<= gmag_vals[1])]
            
            grav_vals= num_slider(label= "Surface gravity", min_val= df["Surface gravity"].min(), max_val= df["Surface gravity"].max(),
                                step= step_size(df["Surface gravity"].min(), df["Surface gravity"].max()), sl_key= "grav_sl")
            df= df[(df["Surface gravity"]>= grav_vals[0]) & (df["Surface gravity"]<= grav_vals[1])]

            # Filters
            #df= hard_filter(df, ["Apparent G magnitude", "Color index", "Effective temperature", "Log luminosity"])
            #df= del_outliers(df, ["Apparent G magnitude", "Color index", "Effective temperature", "Log luminosity"])

    # HR Diagram
    with out_col:
        st.subheader("HR Diagram")

        # Axis selection
        xcol, ycol= st.columns(2)
        with xcol:
            x_ax= st.selectbox("X-axis:", ["Color index", "Log effective temperature"])
        with ycol:
            y_ax= st.selectbox("Y-axis:", ["Absolute magnitude", "Log luminosity"])
    
    with filter_col:
        with subcont:
            # Displaying different sliders based on chosen x axis
            if x_ax== "Color index":
                temp_vals= num_slider(label= "Effective temperature", min_val= df["Effective temperature"].min(), max_val= df["Effective temperature"].max(),
                                      step= step_size(df["Effective temperature"].min(), df["Effective temperature"].max()), sl_key= "temp_sl")
                df= df[(df["Effective temperature"]>= temp_vals[0]) & (df["Effective temperature"]<= temp_vals[1])]
            else:
                clr_vals= num_slider(label= "Color index", min_val= df["Color index"].min(), max_val= df["Color index"].max(),
                                     step= step_size(df["Color index"].min(), df["Color index"].max()), sl_key= "clr_sl")
                df= df[(df["Color index"]>= clr_vals[0]) & (df["Color index"]<= clr_vals[1])]
            
            # Displaying different sliders based on chosen y axis
            if y_ax== "Absolute magnitude":
                lum_vals= num_slider(label= "Luminosity (log)", min_val= df["Log luminosity"].min(), max_val= df["Log luminosity"].max(),
                                     step= step_size(df["Log luminosity"].min(), df["Log luminosity"].max()), sl_key= "lum_sl")
                df= df[(df["Log luminosity"]>= lum_vals[0]) & (df["Log luminosity"]<= lum_vals[1])]
            else:
                abs_vals= num_slider(label= "Absolute magnitude", min_val= df["Absolute magnitude"].min(), max_val= df["Absolute magnitude"].max(),
                                     step= step_size(df["Absolute magnitude"].min(), df["Absolute magnitude"].max()), sl_key= "abs_sl")
                df= df[(df["Absolute magnitude"]>= abs_vals[0]) & (df["Absolute magnitude"]<= abs_vals[1])]
    
    with out_col:
        # Color
        clr_ax= "Color index"
        clr_scl= st.selectbox("Colour scheme:", ["Blues", "Greys", "Plasma", "RdYlBu", "Reds"], index= 3)

        # Plotting the data
        fig= px.scatter(df, x=x_ax, y=y_ax, color= clr_ax, color_continuous_scale= clr_scl+"_r", range_color=[-0.5, 2])
        fig.update_traces(marker={'size': 1})
            
        if y_ax== "Absolute magnitude":
            fig.update_yaxes(range= [16, -10])
        else:
            fig.update_yaxes(range= [-6, 6])
        
        if x_ax== "Color index":
            fig.update_xaxes(range= [-0.5, 5])
        else:
            fig.update_xaxes(range= [np.log10(30000), np.log10(1000)])

        # Displaying the plot
        st.write(fig)



# Execution
if __name__== "__main__":
    df = pd.read_csv("data/stars_clean_calc.csv")
    dashboard(df)
