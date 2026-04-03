import streamlit as st

# Updated imports to include the custom slider and the new distance chart
from helper.components import load_data, draw_spectral_chart, draw_mk_classification_chart, draw_avg_metrics_by_distance
from helper.custom_slider import num_slider, step_size

st.set_page_config(layout="wide") # Highly recommended for side-by-side charts
st.title("Stellar Population Statistics")

df = load_data()

# 3. UI LOGIC
options = st.radio("Select Stellar Sample:", ["Near", "Far"], horizontal=True)
st.divider()

# Metric selector for the new distance trend chart
st.subheader("Distance Trends")
selected_metric = st.selectbox(
    "Select metric to average by distance:", 
    ["Effective temperature", "Log luminosity", "Absolute magnitude"]
)
st.divider()

if options == "Near":
    # --- Custom Slider for NEAR stars (1 to 100 pc) ---
    dist_min, dist_max = 1.0, 100.0
    dist_vals = num_slider(
        label="Select distance range (pc):", 
        min_val=dist_min, 
        max_val=dist_max,
        step=step_size(dist_min, dist_max), 
        sl_key="near_dist_sl",
        default=(1.0, 50.0)
    )
    
    # Filter the dataframe using the range
    filter_df = df[(df['Distance'] >= dist_vals[0]) & (df['Distance'] <= dist_vals[1])]
    
    if filter_df.empty:
        st.warning("No stars found in this specific range. Please widen the selection.")
    else:
        # Render charts
        col1, col2 = st.columns(2)
        with col1:
            draw_spectral_chart(filter_df, f"Near Sample ({dist_vals[0]} to {dist_vals[1]} pc)")
        with col2:
            draw_mk_classification_chart(filter_df, "Luminosity Class Breakdown")
        
        # Render the new average metric chart
        draw_avg_metrics_by_distance(filter_df, metric=selected_metric, bin_size=5)
    
    st.divider()
    st.subheader("Inferences")
    st.markdown("The distribution of stars graph clearly shows us that there is a significant amount of stars of spectral class of G K M with spectral class M being its most significant contributor. This is a confirmation of the IMF theory that the universe is mostly composed of low mass, cool stars that are formed in much greater amount and usually outlast the hotter higher temperature stars.")

    st.markdown("For Luminoisity, it can be clearly understood that there are a lot of main sequence stars in each spectral class. This can be checked by accessing the dashboard and seeing the distribution of all spectral class of stars and observing a massive cluster around the Main Sequence line with very little deviation. Now for stars in the main sequence, a=3.5 so therefore Masses of 95 percentage will be ranging from 2 to 55 times the mass of the sun.")
    
    st.markdown("The near-Earth HR diagram extends to very low luminosities (log L ≈ −4) populated by M dwarfs.")
    
    st.markdown("In both panels, the main sequence is clearly visible as a diagonal band running from hot, luminous stars (upper left) to cool, faint stars (lower right).")
    
    st.markdown("It is important to note that the main sequence visible in the distant field population does not represent a same-age stellar population. Rather, stars of vastly different ages and distances converge on the main sequence simply because it is the longest lived evolutionary phase.")
    
elif options == "Far":
    # --- Custom Slider for FAR stars (100 pc to max) ---
    dist_min = 100.0
    dist_max = float(df['Distance'].max())
    
    dist_vals = num_slider(
        label="Select distance range (pc):", 
        min_val=dist_min, 
        max_val=dist_max, 
        step=step_size(dist_min, dist_max), 
        sl_key="far_dist_sl",
        default=(100.0, 500.0)
    )
    
    # Filter the dataframe using the range
    filter_df = df[(df['Distance'] >= dist_vals[0]) & (df['Distance'] <= dist_vals[1])]

    if filter_df.empty:
        st.warning("No stars found in this specific range. Please widen the selection.")
    else:
        # Render charts
        col1, col2 = st.columns(2)
        with col1:
            draw_spectral_chart(filter_df, f"Far Sample ({dist_vals[0]:.1f} to {dist_vals[1]:.1f} pc)")
        with col2:
            draw_mk_classification_chart(filter_df, "Luminosity Class Breakdown")
            
        # Render the new average metric chart
        draw_avg_metrics_by_distance(filter_df, metric=selected_metric, bin_size=50)
        
    st.divider()
    st.subheader("Inferences")
    st.markdown("You can see here that initially that there are lot of K M G F stars with K leading in proportion. But as we increase the distance the proportion of M stars keep reducing and other stars like K G and F increasing in contribution. At one point, M is gone. This does not contradict the IMT theory as")
    
    st.markdown("The distant field population peaks at a significantly lower (brighter) absolute visual magnitude of approximately 4–5, corresponding to solar-type G(stars moderate in size, temperature, brightness, similar to the sun) and subgiant stars(stars that have expanded massively after using up hydrogen in their core.).")
    
    st.markdown("The distant field HR diagram is truncated at the faint end; the lower main sequence is sparsely populated because cool red dwarf stars are undetectable at large distances. This truncation is a direct observational signature of Malmquist bias.")
    
    st.markdown("In both panels, the main sequence is clearly visible as a diagonal band running from hot, luminous stars (upper left) to cool, faint stars (lower right).")
    
    st.markdown("It is important to note that the main sequence visible in the distant field population does not represent a same-age stellar population. Rather, stars of vastly different ages and distances converge on the main sequence simply because it is the longest lived evolutionary phase.")