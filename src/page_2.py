import streamlit as st

from helper.components import load_data, draw_spectral_chart, draw_mk_classification_chart

st.set_page_config(layout="wide") # Highly recommended for side-by-side charts
st.title("Stellar Population Statistics")


df = load_data()

# 3. UI LOGIC
options = st.radio("Select Stellar Sample:", ["Near", "Far"], horizontal=True)
st.divider()

if options == "Near":
    # Slider for NEAR stars (1 to 100 pc)
    distance = st.slider("Select maximum distance (pc)", min_value=1.0, max_value=100.0, value=50.0)
    
    # Filter the dataframe
    filter_df = df[df['Distance'] <= distance]
    
    # Render both charts simultaneously
    col1, col2 = st.columns(2)
    with col1:
        draw_spectral_chart(filter_df, f"Near Sample (<= {distance} pc)")
    with col2:
        draw_mk_classification_chart(filter_df, "Luminosity Class Breakdown")

elif options == "Far":
    max_dist = float(df['Distance'].max())
    distance = st.slider("Select minimum distance (pc)", min_value=100.0, max_value=max_dist, value=500.0)
    
    
    filter_df = df[df['Distance'] >= distance]

    col1, col2 = st.columns(2)
    with col1:
        draw_spectral_chart(filter_df, f"Far Sample (>= {distance} pc)")
    with col2:
        draw_mk_classification_chart(filter_df, "Luminosity Class Breakdown")