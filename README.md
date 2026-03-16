# Stellar Population and HR Diagram Explorer
Repository to store files for a program for generating and exploring HR diagrams from astronomical data.

# Data Sources and Cleaning

We will be using two data files in the csv format stratified by distance from earth.

One is called Near_Earth.csv for stars near Earth and the other one is Far_Earth.csv for stars farther from Earth.

We will be updating the readme for the project as it goes on.

# Data Filtering
To ensure physical accuracy and minimize observational noise, we will use quality cuts like enforcing brightness limits (phot_g_mean_mag < 17) and removing missing color indices, complementing the dataset's existing parallax filters. When we expand datasets to include metrics like luminosity or effective temperature, then we will use astrophysical cuts. These filters will restrict temperature, luminosity, standard spectral classes, and color indices strictly to realistic physical bounds.

# Data Analysis
Isochrone fitting can be used to estimate stellar ages, masses, and metallicities, while main-sequence turnoff identification helps determine the age of stellar populations.

Population classification separates stars into categories such as main sequence, giants, and white dwarfs, and density or clustering analysis identifies substructures and distinct stellar populations. Outlier detection highlights unusual stars, including binaries or blue stragglers, and population synthesis or modeling can be applied to infer the star formation history and initial mass function. 

HR diagrams can also be used together with how stars move and their chemical composition to study the structure of the Galaxy, see how stars change as they age, and look at differences in their metallicity. 
Based on the parameters chosen different analysis method may be used.

# Plots
The plotly python library can be used to make interactive plots, which is how the HR diagrams will be created here. We may switch later depending on how our vision for the plots evolves.

# Dashboard
The dashboard will be made using the streamlit python library, which allows for creation of a dashboard page, locally hosted or otherwise, through python code. The dashboard will allow viewers to select specific subsets of stellar data based on various criteria.
