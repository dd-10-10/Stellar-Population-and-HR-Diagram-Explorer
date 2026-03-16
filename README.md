# Stellar Population and HR Diagram Explorer
Repository to store files for a program for generating and exploring HR diagrams from astronomical data.
A program for generating and exploring Hertzsprung-Russell diagrams from astronomical data.

# Data Sources and Cleaning

We are using two data files in the csv format stratified by distance from earth 

One is called Near_Earth.csv for stars near Earth and the other one is Far_Earth.csv for stars farther from Earth

We will be updating the readme for the project as it goes on

# Data Filtering
The raw data undergoes several quality cuts to ensure physical accuracy and reduce observational noise. Key filtering steps include ensuring positive distance measurements (parallax > 0)(we have parallax filtered in Near_Earth.csv), enforcing brightness limits to maintain data quality (phot_g_mean_mag < 17), and removing entries with missing color indices (bp_rp).

# Plots
The plotly python library can be used to make interactive plots, which is how the HR diagrams will be created here.

# Dashboard
The dashboard will be made using the streamlit python library, which allows for creation of a dashboard page, locally hosted or otherwise, through python code. The dashboard will allow viewers to select specific subsets of stellar data based on various criteria.
