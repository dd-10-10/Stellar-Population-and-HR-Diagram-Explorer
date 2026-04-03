import streamlit as st


# Define the pages
main_page = st.Page("dashboard.py", title="Diagram Explorer")
page_2 = st.Page("page_2.py", title="Statistical Perspectives")

# Set up navigation
st.sidebar.write("HR diagrams are scatter plots of stellar data, with the y-axis usually showing increasing luminosity and the x-axis showing colour, spectral class, or decreasing surface temperature. These plots (initially independently formulated by Hertzsprung and Russell) have historically helped astronomers gain a better understanding of stellar evolution.")
st.sidebar.subheader("Current Page:")
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()