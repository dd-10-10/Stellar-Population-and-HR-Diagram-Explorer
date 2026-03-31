import streamlit as st
import plotly.express as px
import pandas as pd

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/gaia_cleaned.csv")
    return df


df= load_data()

scientific_star_colors = {
    'M': '#FF4500', 'K': '#FFA500', 'G': '#FFD700', 'F': '#FFF4EA', 
    'A': '#F2F2F2', 'B': '#CCDDFF', 'O': '#9BB0FF'
}

# 2. Function to draw chart
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
        text=plot_variables['Percentage'].apply(lambda x: f'{x:.2f}%')
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_title="Percentage of Sample (%)")
    fig.update_yaxes(range=[0, plot_variables['Percentage'].max() * 1.15])

    st.plotly_chart(fig, width="stretch")


# 3. UI and Logic Flow
options = st.selectbox("Select dataset", ("Near", "Far"), index=None)

# Reacting to the selectbox cleanly:
if options is None:
    # Textbox on first loading
    st.info("👆 Please select 'Near' or 'Far' from the dropdown to begin.")

elif options == "Near":
    # Slider and logic for NEAR stars
    distance = st.slider("Select maximum distance (pc)", 0.0, 100.0, 10.0)
    filter_df = df[df['Distance'] <= distance]
    
    # Chart
    draw_spectral_chart(filter_df, f"Near Sample (< {distance} pc)")

elif options == "Far":
    # Slider and logic for FAR stars
    distance = st.slider("Select minimum distance (pc)", 100.0, df['Distance'].max(), 500.0)
    filter_df = df[df['Distance'] >= distance]
    
    # Chart
    draw_spectral_chart(filter_df, f"Far Sample (> {distance} pc)")
