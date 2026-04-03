# Stellar Population and HR Diagram Explorer

A program for generating and exploring Hertzsprung-Russell (HR) diagrams from astronomical data.

---

## Table of Contents

- [Installation and Usage](#installation-and-usage)
- [Hertzsprung-Russell Diagrams](#hertzsprung-russell-diagrams)
- [Data Sources and Cleaning](#data-sources-and-cleaning)
- [Data Filtering](#data-filtering)
- [Data Analysis](#data-analysis)
- [Plots](#plots)
- [Dashboard](#dashboard)
- [Acknowledgements](#acknowledgements)

---

## Installation and Usage

### Prerequisites

Ensure you have **Python 3.8+** installed.

### Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes the following core libraries:

```
streamlit
plotly
pandas
```

### Run the Dashboard

```bash
streamlit run src/app.py
```

This will launch the dashboard in your default browser. From there you can explore the HR Diagram Plotter and Summary Statistics pages using the sidebar navigation.

---

## Folder Structure

```
PROJECT_FOLDER/
│
├── data/                        # Raw and processed stellar datasets
│
├── helper/                      # Utility scripts for the dashboard
│   ├── components.py            # Reusable UI components
│   ├── custom_slider.py         # Custom slider widget
│   ├── file_setup.py            # File loading and setup utilities
│   └── filters.py               # Data filtering logic
│
├── report/                      # Project reports
│   ├── analysis_report.pdf
│   └── DSP_mini_report.pdf
│
├── src/                         # Main application source code
│   ├── app.py                   # Streamlit app entry point
│   ├── dashboard.py             # HR Diagram Plotter page
│   └── page_2.py                # Summary Statistics page
│
├── venv/                        # Virtual environment (not tracked by Git)
├── .gitignore
├── LICENSE.md
├── README.md
├── requirements.txt
└── Sample.png                   # Sample HR diagram output
```

---

## Hertzsprung-Russell Diagrams

HR diagrams are scatter plots of stellar data, with the y-axis showing increasing luminosity and the x-axis showing colour, spectral class, or decreasing surface temperature. These plots — initially and independently formulated by Hertzsprung and Russell — helped astronomers gain a better understanding of stellar evolution.

---

## Data Sources and Cleaning

The stellar data is stratified based on distance and obtained from the Gaia mission. For further details, refer to the [Acknowledgements](#acknowledgements) section.

---

## Data Filtering

To ensure physical accuracy and minimise observational noise, quality cuts are applied, including:

- Enforcing brightness limits (`phot_g_mean_mag < 17`)
- Removing entries with missing colour indices
- Complementing the dataset's existing parallax filters

When the dataset is expanded to include metrics like luminosity or effective temperature, astrophysical cuts are also applied. These restrict temperature, luminosity, standard spectral classes, and colour indices strictly to realistic physical bounds.

---

## Data Analysis

Since the data consists of field stars spanning multiple distances and ages, isochrone fitting is not applicable. Instead, a comparative study between near and far field star populations is carried out.

The analysis involves constructing multiple statistical representations of the data, including:

- Luminosity functions
- Effective temperature distributions
- Hertzsprung-Russell (HR) diagrams
- Spectral class distributions

These visualisations are used to systematically compare the properties of the two populations and infer the reasons behind their similarities and differences.

---

## Plots

Interactive HR diagrams are created using the [Plotly](https://plotly.com/python/) Python library, which supports rich, interactive scatter plots suitable for exploring stellar data.

---

## Dashboard

The dashboard is built using the [Streamlit](https://streamlit.io/) Python library, which enables creation of a locally or remotely hosted dashboard through Python code. It allows viewers to select specific subsets of stellar data based on various criteria.

The dashboard consists of two pages:

1. **HR Diagram Plotter** (`dashboard.py`) — Displays the distribution of stars with various adjustable parameters, providing insight into stellar evolution through the HR diagram.
2. **Summary Statistics** (`page_2.py`) — Provides detailed statistical information about the stellar population, including the distribution of stars across spectral classes and other properties.

---

## Acknowledgements

This work has made use of data from the European Space Agency (ESA) mission **[Gaia](https://www.cosmos.esa.int/gaia)**, processed by the Gaia Data Processing and Analysis Consortium (**[DPAC](https://www.cosmos.esa.int/web/gaia/dpac/consortium)**).

Funding for the DPAC has been provided by national institutions, in particular the institutions participating in the Gaia Multilateral Agreement.
