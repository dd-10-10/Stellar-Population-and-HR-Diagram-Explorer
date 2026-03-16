# Stellar Population and HR Diagram Explorer
Repository to store files for a program for generating and exploring HR diagrams from astronomical data.

# Data Sources and Cleaning

We will be using two data files in the csv format stratified by distance from earth.

One is called Near_Earth.csv for stars near Earth and the other one is Far_Earth.csv for stars farther from Earth.

We will be updating the readme for the project as it goes on.

# Data Filtering
To ensure physical accuracy and minimize observational noise, we will use quality cuts like enforcing brightness limits (phot_g_mean_mag < 17) and removing missing color indices, complementing the dataset's existing parallax filters. When we expand datasets to include metrics like luminosity or effective temperature, then we will use astrophysical cuts. These filters will restrict temperature, luminosity, standard spectral classes, and color indices strictly to realistic physical bounds.

# Plots
The plotly python library can be used to make interactive plots, which is how the HR diagrams will be created here. We may switch later depending on how our vision for the plots evolves.

# Dashboard
The dashboard will be made using the streamlit python library, which allows for creation of a dashboard page, locally hosted or otherwise, through python code. The dashboard will allow viewers to select specific subsets of stellar data based on various criteria.
