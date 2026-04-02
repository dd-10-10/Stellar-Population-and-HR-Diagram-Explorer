import streamlit as st
import plotly.express as px
import pandas as pd


scientific_star_colors = {
    "O": "#9bb0ff", "B": "#aabfff", "A": "#cad7ff", 
    "F": "#f8f7ff", "G": "#fff4ea", "K": "#ffd2a1", "M": "#ffcc6f"
}
#Caching the data to load faster
@st.cache_data
def load_data():
    df = pd.read_csv("data/gaia_cleaned.csv")
    return df


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

