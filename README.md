# Stellar Population and HR Diagram Explorer
A program for generating and exploring Hertzsprung-Russell (HR) diagrams from astronomical data.

## Hertzsprung-Russell diagrams
HR diagrams are scatter plots of stellar data, with the y-axis usually showing increasing luminosity and the x-axis showing colour, spectral class, or decreasing surface temperature. These plots (initially independently formulated by by Hertzsprung and Russell) helped astronomers gain a better understanding of stellar evolution.

## Data Sources and Cleaning

The files used here are based on the strategy that the stars are stratified based on distance. The data is obtained from Gaia. For more detalis, check the Acknowledgements part.


## Data Filtering
To ensure physical accuracy and minimize observational noise, we will use quality cuts like enforcing brightness limits (phot_g_mean_mag < 17) and removing missing color indices, complementing the dataset's existing parallax filters. When we expand datasets to include metrics like luminosity or effective temperature, then we will use astrophysical cuts. These filters will restrict temperature, luminosity, standard spectral classes, and color indices strictly to realistic physical bounds.

## Data Analysis
Isochrone fitting can be used to estimate stellar ages, masses, and metallicities, while main-sequence turnoff identification helps determine the age of stellar populations. 

HR diagrams can also be used together with how stars move and their chemical composition to study the structure of the Galaxy, see how stars change as they age, and look at differences in their metallicity. 
Based on the parameters chosen different analysis method may be used.

## Plots
The plotly python library can be used to make interactive plots, which is how the HR diagrams will be created here. 

## Dashboard
The dashboard will be made using the streamlit python library, which allows for creation of a dashboard page, locally hosted or otherwise, through python code. The dashboard will allow viewers to select specific subsets of stellar data based on various criteria. 

There are two pages to the dashboard, one of them being the HR Diagram plotter itself, consisting of various parameters to see the distribution of stars and get an idea of stellar evolution is through this diagram. The second page is basically calculating the summary statistics, wherein much more detail can be found about the stars in general like, distribution of stars in the spectral class etc.

## Acknowledgments

This work has made use of data from the European Space Agency (ESA) mission **[Gaia](https://www.cosmos.esa.int/gaia)**, processed by the Gaia Data Processing and Analysis Consortium (**[DPAC](https://www.cosmos.esa.int/web/gaia/dpac/consortium)**). 

Funding for the DPAC has been provided by national institutions, in particular the institutions participating in the Gaia Multilateral Agreement.
