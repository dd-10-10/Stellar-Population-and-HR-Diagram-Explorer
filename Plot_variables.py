#This code assumes the dataframe data_var contains the columns from the gaia dataset to calculate the variable values
import numpy as np
import pandas as pd

def spectral_class(T):
    if T > 30000:
        return 'O'
    elif T > 10000:
        return 'B'
    elif T > 7500:
        return 'A'
    elif T > 6000:
        return 'F'
    elif T > 5200:
        return 'G'
    elif T > 3700:
        return 'K'
    else:
        return 'M'

# Constants
M_G_sun = 4.67

# Create new dataframe
data_plot_var = pd.DataFrame()

# --- 1. Distance ---(IMPORTANT- 'parallax' in mas)
data_plot_var['distance'] = 1000 / data_var['parallax']

# --- 2. Color Index ---
data_plot_var['bp_rp'] = data_var['phot_bp_mean_mag'] - data_var['phot_rp_mean_mag']

# --- 3. Absolute Magnitude (G) ---
data_plot_var['M_G'] = (
    data_var['phot_g_mean_mag']
    - data_var['ag_gspphot']
    + 5 * np.log10(data_var['parallax'])
    - 10
)

# --- 4. V-band magnitude ---
bp_rp = data_plot_var['bp_rp']

data_plot_var['V'] = (
    data_var['phot_g_mean_mag']
    + 0.0176
    + 0.00686 * bp_rp
    + 0.1732 * (bp_rp ** 2)
)

# --- 5. Extinction in V ---
data_plot_var['A_V'] = 1.1 * data_var['ag_gspphot']

# --- 6. Absolute Visual Magnitude ---
data_plot_var['M_V'] = (
    data_plot_var['V']
    - data_plot_var['A_V']
    + 5 * np.log10(data_var['parallax'])
    - 10
)

# --- 7. Effective Temperature (Gaia) ---
data_plot_var['T_eff'] = data_var['teff_gspphot']

# --- 8. Approx Temperature from color ---(if 'teff_gspphot' not available)
#data_plot_var['T_eff_color'] = 4600 * (
#    (1 / (0.92 * bp_rp + 1.7)) +
#    (1 / (0.92 * bp_rp + 0.62))
#)

# --- 9. Surface Gravity ---
data_plot_var['logg'] = data_var['logg_gspphot']

# --- 10. Luminosity ---
data_plot_var['L_Lsun'] = 10 ** (0.4 * (M_G_sun - data_plot_var['M_G']))
data_plot_var['log_L_Lsun'] = 0.4 * (M_G_sun - data_plot_var['M_G'])
data_plot_var['spectral_class'] = data_plot_var['T_eff'].apply(spectral_class)
