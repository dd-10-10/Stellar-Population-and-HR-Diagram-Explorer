import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np 
from helper.filters import *

scientific_star_colors = {
    "O": "#9bb0ff", "B": "#aabfff", "A": "#cad7ff", 
    "F": "#f8f7ff", "G": "#fff4ea", "K": "#ffd2a1", "M": "#ffcc6f"
}

pop_colors = {"Near Earth < 100pc": "#00E5FF", "Far Earth > 100pc": "#FF4466"} 
#Caching the data to load faster
@st.cache_data
def load_data():
    df = pd.read_csv("data/gaia_cleaned.csv")
    df = clean_measured(df)
    iqr_df = del_outliers(df, ["Parallax error", "phot_g_mean_flux_over_error", "phot_bp_mean_flux_over_error", "phot_rp_mean_flux_over_error"])
    mcd_df = MCD_filter(df)
    phy_df = hard_filter(df, ["Apparent G magnitude", "Color index", "Effective temperature", "Log luminosity"])
    return iqr_df, mcd_df, phy_df   


def draw_spectral_chart(filtered_data, chart_title):
    if filtered_data.empty:
        st.warning("No stars found in this range. Try adjusting the slider.")
        return

    plot_variables = filtered_data['Spectral class'].value_counts(normalize=True).reset_index()
    plot_variables.columns = ["Spectral class", "Percentage"]
    plot_variables["Percentage"] *= 100

    fig = px.bar(
        plot_variables,
        x="Spectral class",
        y="Percentage",
        title=chart_title,
        color='Spectral class',
        color_discrete_map=scientific_star_colors,
        text=plot_variables['Percentage'].apply(lambda x: f'{x:.2f}%'),
        category_orders={"Spectral class": ["O", "B", "A", "F", "G", "K", "M"]}
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_title="Percentage of Sample (%)", template="plotly_dark")
    fig.update_yaxes(range=[0, plot_variables['Percentage'].max() * 1.15])

    st.plotly_chart(fig, width="stretch")


# Morgan Keeman Classification Helper
def assign_mk_class(row):
    mag = row['Absolute magnitude']
    spec = row['Spectral class']
    
    if mag > 10 and spec in ['O', 'B', 'A', 'F']: 
        return 'White Dwarfs'
    if mag < -4: 
        return 'I - Supergiants'
    elif mag < -1: 
        return 'II - Bright Giants'
    elif mag < 2.5: 
        return 'III - Giants'
    elif mag < 4: 
        return 'IV - Subgiants'
    else: 
        return 'V - Main Sequence'

# --- The New Stacked Bar Function ---
def draw_mk_classification_chart(filtered_data, chart_title):
    if filtered_data.empty:
        return # Warning already handled by the first chart

    # Create a copy so we don't overwrite the original dataframe
    df_plot = filtered_data.copy()
    df_plot['MK Class'] = df_plot.apply(assign_mk_class, axis=1)

    fig = px.histogram(
        df_plot, 
        x="Spectral class", 
        color="MK Class",
        category_orders={
            "Spectral class": ["O", "B", "A", "F", "G", "K", "M"],
            "MK Class": [
                "I - Supergiants", "II - Bright Giants", "III - Giants", 
                "IV - Subgiants", "V - Main Sequence", "White Dwarfs"
            ]
        }, 
        barmode='stack',
        title=chart_title,
        color_discrete_map={
            "I - Supergiants": "#FF3333", "II - Bright Giants": "#FF8833", 
            "III - Giants": "#FFCC00", "IV - Subgiants": "#FFFF66", 
            "V - Main Sequence": "#4488FF", "White Dwarfs": "#FFFFFF"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Spectral Class",
        yaxis_title="Number of Stars",
        legend_title="Luminosity Class"
    )

    st.plotly_chart(fig, width="stretch")

def draw_temperature_chart(filtered_data, chart_title):
    if filtered_data.empty:
        return # Warning already handled by the first chart

    # Create a copy so we don't overwrite the original dataframe
    df_plot = filtered_data.copy()
    df_plot['MK Class'] = df_plot.apply(assign_mk_class, axis=1)

    fig = px.histogram(
        df_plot, 
        x="Effective temperature", 
        color="MK Class",
        category_orders={"MK Class": ["I - Supergiants", "II - Bright Giants", "III - Giants", 
                                      "IV - Subgiants", "V - Main Sequence", "White Dwarfs"]}, 
        barmode='stack',
        title=chart_title,
        color_discrete_map= {"I - Supergiants": "#FF3333",
                             "II - Bright Giants": "#FF8833", 
                             "III - Giants": "#FFCC00",
                             "IV - Subgiants": "#FFFF66", 
                             "V - Main Sequence": "#4488FF",
                             "White Dwarfs": "#FFFFFF"})

    fig.update_layout(template="plotly_dark",
                      xaxis_title="Effective temperature",
                      yaxis_title="Number of Stars",
                      legend_title="Spectral Class")

    st.plotly_chart(fig, width="stretch")

def draw_distance_chart(filtered_data, chart_title):
    if filtered_data.empty:
        return # Warning already handled by the first chart

    # Create a copy so we don't overwrite the original dataframe
    df_plot = filtered_data.copy()
    df_plot['MK Class'] = df_plot.apply(assign_mk_class, axis=1)

    fig = px.histogram(
        df_plot, 
        x="Distance", 
        color="Spectral class",
        category_orders={"Spectral class": ["O", "B", "A", "F", "G", "K", "M"],}, 
        barmode='stack',
        title=chart_title,
        color_discrete_map= {"O": "#4466FF",
                             "B": "#88BBFF",
                             "A": "#FFFFFF",
                             "F": "#FFFF77",
                             "G": "#FFCC00",
                             "K": "#FF8800",
                             "M": "#FF3333"})

    fig.update_layout(template="plotly_dark",
                      xaxis_title="Distance",
                      yaxis_title="Number of Stars",
                      legend_title="Spectral Class")

    st.plotly_chart(fig, width="stretch")

def draw_extinction_chart(filtered_data, chart_title):
    if filtered_data.empty:
        return # Warning already handled by the first chart

    # Create a copy so we don't overwrite the original dataframe
    df_plot = filtered_data.copy()
    df_plot['MK Class'] = df_plot.apply(assign_mk_class, axis=1)

    fig= px.scatter(df_plot,
                    x= "Distance",
                    y= "Extinction in G band",
                    color= "Spectral class",
                    category_orders= {"Spectral class": ["O", "B", "A", "F", "G", "K", "M"],},
                    color_discrete_map= {"O": "#4466FF",
                                         "B": "#88BBFF",
                                         "A": "#FFFFFF",
                                         "F": "#FFFF77",
                                         "G": "#FFCC00",
                                         "K": "#FF8800",
                                         "M": "#FF3333"})
    
    fig.update_traces(marker={'size': 2})
    fig.update_layout(template="plotly_dark",
                      xaxis_title="Distance",
                      yaxis_title="Effect of Dust (G Band Extinction)",
                      legend_title="Spectral Class")

    st.plotly_chart(fig, width="stretch")

# --- The New Average Metric by Distance Function ---
def draw_avg_metrics_by_distance(filtered_data, metric="Effective temperature", bin_size=10):
    """
    Groups data into distance bins and plots the average of the chosen metric.
    """
    if filtered_data.empty:
        return

    df_plot = filtered_data.copy()
    
    # Create distance bins
    df_plot['Distance Bin'] = (df_plot['Distance'] // bin_size) * bin_size
    
    # Group by the bin and calculate the mean of the selected metric
    avg_df = df_plot.groupby('Distance Bin')[metric].mean().reset_index()
    
    # Sort the values just to be safe before plotting a line
    avg_df = avg_df.sort_values(by='Distance Bin')

    fig = px.line(
        avg_df, 
        x="Distance Bin", 
        y=metric,
        title=f"Average {metric} by Distance",
        markers=True,
        color_discrete_sequence=["#00ffcc"]
    )
    
    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Distance (Parsecs)",
        yaxis_title=f"Average {metric}"
    )

    st.plotly_chart(fig, width="stretch")



def draw_comparative_histograms(df):
    """
    Recreates the overall Luminosity and Temperature overlapping histograms.
    """
    df_plot = df.copy()
    
    # Create a new column to split the populations at the 100pc mark
    df_plot['Population'] = np.where(df_plot['Distance'] < 100, 'Near Earth < 100pc', 'Far Earth > 100pc')
    
    # Custom colors to match your teammate's Matplotlib charts
    

    # 1. Luminosity Function (Absolute Magnitude)
    fig_lum = px.histogram(
        df_plot, 
        x="Absolute magnitude", 
        color="Population",
        barmode="overlay", # Overlaps the bars
        histnorm='percent', # Converts raw counts to percentages
        color_discrete_map=pop_colors,
        title="Luminosity Function — Near vs Far Stars"
    )
    fig_lum.update_layout(
        template="plotly_dark", 
        yaxis_title="Percentage of Stars (%)", 
        xaxis_title="Absolute Visual Magnitude"
    )
    # Make bars slightly transparent to see the overlap
    fig_lum.update_traces(opacity=0.75)
    # 2. Effective Temperature Distribution
    fig_temp = px.histogram(
        df_plot, 
        x="Effective temperature", 
        color="Population",
        barmode="overlay", 
        histnorm='percent',
        color_discrete_map=pop_colors,
        title="Effective Temperature Distribution — Near vs Far Stars"
    )
    fig_temp.update_layout(
        template="plotly_dark", 
        yaxis_title="Percentage of Stars (%)", 
        xaxis_title="Effective Temperature (K)"
    )
    fig_temp.update_traces(opacity=0.75)

    return fig_lum, fig_temp


def draw_comparative_spectral(df):
    """
    Recreates the overall Spectral Class grouped bar chart.
    """
    df_plot = df.copy()
    df_plot = df_plot.dropna(subset=['Distance', 'Spectral class'])
    df_plot['Population'] = np.where(df_plot['Distance'] < 100, 'Near Earth < 100pc', 'Far Earth > 100pc')
    
    # Calculate percentages for each spectral class WITHIN each population
    counts = df_plot.groupby(['Population', 'Spectral class']).size().reset_index(name='Count')
    totals = df_plot.groupby('Population').size().reset_index(name='Total')
    merged = pd.merge(counts, totals, on='Population')
    merged['Percentage'] = (merged['Count'] / merged['Total']) * 100
    fig_spec = px.bar(merged, 
        x="Spectral class", 
        y="Percentage", 
        color="Population",
        barmode="group", # Places bars side-by-side
        category_orders={"Spectral class": ["O", "B", "A", "F", "G", "K", "M"]},
        color_discrete_map=pop_colors,
        title="Spectral Class Distribution — Near vs Far Stars" )
    
        
    fig_spec.update_layout(
        template="plotly_dark", 
        yaxis_title="Percentage (%)",
        xaxis_title="Spectral Class"
    )
    
    return fig_spec