import streamlit as st
import plotly.express as px
import pandas as pd

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

# 1. Load Data
@st.cache_data
def data_load():
    df = pd.read_csv("../data/gaia_cleaned.csv")
    df = df[df['Parallax'] > 0].copy()
    df['Distance_pc'] = 1000 / df['Parallax']
    
    # Create Spectral Class
    bins = [0, 3700, 5200, 6000, 7500, 10000, 30000, float('inf')] 
    labels = ['M', 'K', 'G', 'F', 'A', 'B', 'O'] 
    df['Spectral_Class'] = pd.cut(df['Effective temperature'], bins=bins, labels=labels)
    
    return df.dropna(subset=['Spectral_Class'])

df = data_load()

scientific_star_colors = {
    'M': '#FF4500', 'K': '#FFA500', 'G': '#FFD700', 'F': '#FFF4EA', 
    'A': '#F2F2F2', 'B': '#CCDDFF', 'O': '#9BB0FF'
}

# 2. HELPER FUNCTION: This makes your code 10x neater
def draw_spectral_chart(filtered_data, chart_title):
    if filtered_data.empty:
        st.warning("No stars found in this range. Try adjusting the slider.")
        return

    plot_variables = filtered_data['Spectral_Class'].value_counts(normalize=True).reset_index()
    plot_variables.columns = ["Spectral_Class", "Percentage"]
    plot_variables["Percentage"] *= 100

    fig = px.bar(
        plot_variables,
        x="Spectral_Class",
        y="Percentage",
        title=chart_title,
        color='Spectral_Class',
        color_discrete_map=scientific_star_colors,
        text=plot_variables['Percentage'].apply(lambda x: f'{x:.2f}%')
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_title="Percentage of Sample (%)")
    fig.update_yaxes(range=[0, plot_variables['Percentage'].max() * 1.15])

    st.plotly_chart(fig, use_container_width=True)


# 3. UI and Logic Flow
options = st.selectbox("Select data of preference", ("Near", "Far"), index=None)

# Reacting to the selectbox cleanly:
if options is None:
    # What to show when the page first loads
    st.info("👆 Please select 'Near' or 'Far' from the dropdown to begin.")

elif options == "Near":
    # Slider and logic for NEAR stars
    distance = st.slider("Select maximum distance (pc)", 0.0, 100.0, 10.0)
    filter_df = df[df['Distance_pc'] <= distance]
    
    # Call the helper function instead of writing 10 lines of chart code
    draw_spectral_chart(filter_df, f"Near Sample (< {distance} pc)")

elif options == "Far":
    # Slider and logic for FAR stars
    distance = st.slider("Select minimum distance (pc)", 100.0, 5000.0, 500.0)
    filter_df = df[df['Distance_pc'] >= distance]
    
    # Call the exact same helper function!
    draw_spectral_chart(filter_df, f"Far Sample (> {distance} pc)")
