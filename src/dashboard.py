import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from  helper.filters import *
from  helper.custom_slider import *

def dashboard(df, iso_df, iso_df2):
    '''
    Function to generate the diagram and dashboard from data
    '''
    st.markdown("""<style>.block-container {padding-top: 2rem !important;}</style>""",unsafe_allow_html=True)
    st.set_page_config(layout="wide")

    st.markdown("<h1 style='text-align: center;'>Hertzsprung-Russell Diagram Explorer</h1>", unsafe_allow_html=True)

    st.sidebar.markdown("# Diagram Explorer 🎈")

    df= clean_measured(df)
    df_old= df.copy()
    #----Data for plotting Main sequence----
    y_dwarfs= iso_df[iso_df["label"]== 1]
    o_dwarfs= iso_df2[iso_df2["label"]== 1]
    y_giants= iso_df[iso_df["label"].isin([2, 3, 4, 5, 6, 7])]
    o_giants= iso_df2[iso_df2["label"].isin([2, 3, 4, 5, 6, 7])]
    t = np.linspace(0, 1, 100)
    # Dummy Young White Dwarfs (Slightly hotter/brighter)
    y_wd = pd.DataFrame({"Color index": np.linspace(-0.2, 0.6, 100),
                         "Absolute magnitude": 10 + 5.5 * t - 1.5 * (t - t**2),
                         "Log effective temperature": np.linspace(4.8, 3.9, 100),
                         "Log luminosity": np.linspace(-0.5, -3.5, 100)})
    # Dummy Old White Dwarfs (Shifted slightly to represent an older, cooler population)
    o_wd = pd.DataFrame({"Color index": np.linspace(-0.1, 0.8, 100),
                         "Absolute magnitude": 11 + 5.0 * t - 1.0 * (t - t**2),
                         "Log effective temperature": np.linspace(4.6, 3.7, 100),
                         "Log luminosity": np.linspace(-1.0, -4.0, 100)})
    #--------

    filter_col, out_col= st.columns([0.4, 0.6], gap= "medium")

    with filter_col:
        st.subheader("Data filters")
        
        subcont= st.container(height=600)
        with subcont:
            # Quality Filters
            filt_style= st.selectbox("Select quality cut style:", ["Outlier detection-based (Univariate- IQR)", "Outlier detection-based (Multivariate- MCD)", "Physical limit-based"])
            if filt_style== "Outlier detection-based (Univariate- IQR)":
                df= del_outliers(df, ["Parallax error", "phot_g_mean_flux_over_error", "phot_bp_mean_flux_over_error", "phot_rp_mean_flux_over_error"])
            elif filt_style== "Outlier detection-based (Multivariate- MCD)":
                df= MCD_filter(df)
            else:
                df= hard_filter(df, ["Apparent G magnitude", "Color index", "Effective temperature", "Log luminosity"])
            
            # Sliders
            dist_vals= num_slider(label= "Distance from Earth (Parsecs):", min_val= df_old["Distance"].min(), max_val= df_old["Distance"].max(),
                                step= step_size(df_old["Distance"].min(), df_old["Distance"].max()), sl_key= "dist_sl")
            df= df[(df["Distance"]>= dist_vals[0]) & (df["Distance"]<= dist_vals[1])]

            if df.empty:
                st.warning("The selected range is too narrow. Please widen the selection.")
                st.stop()
            
            spec_vals= st.multiselect(label= "Spectral classes", options= ["M", "K", "G", "F", "A", "B", "O"],
                                      default= ["M", "K", "G", "F", "A", "B", "O"], key= "spec_vals")
            df= df[df["Spectral class"].isin(spec_vals)]

            if df.empty:
                st.warning("The selected range is too narrow. Please widen the selection.")
                st.stop()
            
            gmag_min, gmag_max= df_old["Apparent G magnitude"].min(), df_old["Apparent G magnitude"].max()
            gmag_vals= num_slider(label= "Apparent G magnitude", min_val= gmag_min, max_val= gmag_max,
                                  step= step_size(df_old["Apparent G magnitude"].min(), df_old["Apparent G magnitude"].max()), sl_key= "gmag_sl")
            df= df[(df["Apparent G magnitude"]>= gmag_vals[0]) & (df["Apparent G magnitude"]<= gmag_vals[1])]
            
            if df.empty:
                st.warning("The selected range is too narrow. Please widen the selection.")
                st.stop()
            if False:
                grav_min, grav_max= df_old["Surface gravity"].min(), df_old["Surface gravity"].max()
                grav_vals= num_slider(label= "Surface gravity", min_val= grav_min, max_val= grav_max,
                                    step= step_size(df_old["Surface gravity"].min(), df_old["Surface gravity"].max()), sl_key= "grav_sl")
                df= df[(df["Surface gravity"]>= grav_vals[0]) & (df["Surface gravity"]<= grav_vals[1])]
            
            if df.empty:
                st.warning("The selected range is too narrow. Please widen the selection.")
                st.stop()

    
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
                temp_min, temp_max= df_old["Effective temperature"].min(), df_old["Effective temperature"].max()
                temp_vals= num_slider(label= "Effective temperature", min_val= temp_min, max_val= temp_max,
                                      step= step_size(df_old["Effective temperature"].min(), df_old["Effective temperature"].max()), sl_key= "temp_sl")
                df= df[(df["Effective temperature"]>= temp_vals[0]) & (df["Effective temperature"]<= temp_vals[1])]

                if df.empty:
                    st.warning("The selected range is too narrow. Please widen the selection.")
                    st.stop()
            else:
                clr_min, clr_max= df_old["Color index"].min(), df_old["Color index"].max()
                clr_vals= num_slider(label= "Color index", min_val= clr_min, max_val= clr_max,
                                     step= step_size(df_old["Color index"].min(), df_old["Color index"].max()), sl_key= "clr_sl")
                df= df[(df["Color index"]>= clr_vals[0]) & (df["Color index"]<= clr_vals[1])]

                if df.empty:
                    st.warning("The selected range is too narrow. Please widen the selection.")
                    st.stop()
            
            # Displaying different sliders based on chosen y axis
            if y_ax== "Absolute magnitude":
                lum_min, lum_max= df_old["Log luminosity"].min(), df_old["Log luminosity"].max()
                lum_vals= num_slider(label= "Luminosity (log)", min_val= lum_min, max_val= lum_max,
                                     step= step_size(df_old["Log luminosity"].min(), df_old["Log luminosity"].max()), sl_key= "lum_sl")
                df= df[(df["Log luminosity"]>= lum_vals[0]) & (df["Log luminosity"]<= lum_vals[1])]

                if df.empty:
                    st.warning("The selected range is too narrow. Please widen the selection.")
                    st.stop()
            else:
                abs_min, abs_max= df_old["Absolute magnitude"].min(), df_old["Absolute magnitude"].max()
                abs_vals= num_slider(label= "Absolute magnitude", min_val= abs_min, max_val= abs_max,
                                     step= step_size(df_old["Absolute magnitude"].min(), df_old["Absolute magnitude"].max()), sl_key= "abs_sl")
                df= df[(df["Absolute magnitude"]>= abs_vals[0]) & (df["Absolute magnitude"]<= abs_vals[1])]

                if df.empty:
                    st.warning("The selected range is too narrow. Please widen the selection.")
                    st.stop()
    
    with out_col:
        # Color
        clr_ax= "Color index"
        clr_scl= st.selectbox("Colour scheme:", ["Blues", "Greys", "Plasma", "RdYlBu", "Reds"], index= 3)

        # Plotting the data
        fig= px.scatter(df, x=x_ax, y=y_ax, color= clr_ax, color_continuous_scale= clr_scl+"_r", range_color=[-0.5, 2])
        fig.update_traces(marker={'size': 1})
        
        fig.add_trace(go.Scattergl(x= y_dwarfs[x_ax], y= y_dwarfs[y_ax], mode= "lines", name= "Main Sequence (Young Dwarfs)",
                                   line=dict(color= 'purple', width= 1, dash= 'solid'), hoverinfo= 'name'))
        
        fig.add_trace(go.Scattergl(x= y_giants[x_ax], y= y_giants[y_ax], mode= "lines", name= "Supergiants",
                                   line=dict(color= 'red', width= 1, dash= 'solid'), hoverinfo= 'name'))
        
        fig.add_trace(go.Scattergl(x= y_wd[x_ax], y= y_wd[y_ax], mode= "lines", name= "White Dwarfs (Young)",
                                   line=dict(color= 'white', width= 1, dash= 'solid'), hoverinfo= 'name'))

        fig.add_trace(go.Scattergl(x= o_dwarfs[x_ax], y= o_dwarfs[y_ax], mode= "lines", name= "Main Sequence (Old Dwarfs)",
                                   line=dict(color= 'magenta', width= 1, dash= 'solid'), hoverinfo= 'name'))
        
        fig.add_trace(go.Scattergl(x= o_giants[x_ax], y= o_giants[y_ax], mode= "lines", name= "Giant Branch (Old Giants)",
                                   line=dict(color= 'gold', width= 1, dash= 'solid'), hoverinfo= 'name'))
        
        fig.add_trace(go.Scattergl(x= o_wd[x_ax], y= o_wd[y_ax], mode= "lines", name= "White Dwarfs (Old)",
                                   line=dict(color= 'grey', width= 1, dash= 'solid'), hoverinfo= 'name'))

        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                                      title=""), margin=dict(t=50))

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
    @st.cache_data
    def load_data():
        df = pd.read_csv("data/gaia_cleaned.csv")
        iso_df = pd.read_csv('data/isochrone_data.csv')
        iso_df2 = pd.read_csv('data/isochrone_data_2.csv')
        iso_df= iso_df.sort_values(by= "Mini")
        iso_df2= iso_df2.sort_values(by= "Mini")
        return df, iso_df, iso_df2
    df, iso_df, iso_df2= load_data()
    dashboard(df, iso_df, iso_df2)
