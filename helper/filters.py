import pandas as pd
import numpy as np
from sklearn.covariance import EllipticEnvelope

def clean_measured(df):
    # Parallax cut: Must be positive to avoid math errors
    df = df[df["Parallax"] > 0]
    df = df[df["Parallax over error"] > 20]
    
    # Extinction must also always be positive
    df = df[df["Extinction in G band"] >= 0]

    return df

def hard_filter(df, names):
    # Dimness cut: Removes stars too faint for reliable sensors (till 6 are visible by naked eye)
    if "Apparent G magnitude" in names:
        df = df[df["Apparent G magnitude"] < 17] 

    # Physical Color Bounds: Restricts color index to valid glowing plasma
    if "Color index" in names:
        df = df[(df["Color index"] >= -0.5) & (df["Color index"] <= 5.5)]
    
    # Temperature cut: Keeps surface temperatures within realistic physical limits
    if "Effective temperature" in names:
        df = df[(df["Effective temperature"] >= 2000) & (df["Effective temperature"] <= 50000)]

    # Luminosity
    if "Log luminosity" in names:
        df = df[(df["Log luminosity"] >= -6) & (df["Log luminosity"] <= 6)]
    
    return df

# Statistical filter

def del_outliers(df, names):
    df_clean = df.copy()
    for name in names:
        if name in df.columns:
            Q1 = df[name].quantile(0.25)
            Q3 = df[name].quantile(0.75)
            IQR = Q3 - Q1
            upper_bound = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[name] <= upper_bound)]
    return df_clean


def MCD_filter(df):
    '''
    Uses the Minimum Covariance Determinant (MCD) method to remove
    multivariate statistical outliers based on telescope measurement errors.
    '''
    # 1. Calculate the Temperature Error
    df = df.copy()
    if 'teff_gspphot_upper' in df.columns and 'teff_gspphot_lower' in df.columns:
        df['teff_gspphot_error'] = (df['teff_gspphot_upper'] - df['teff_gspphot_lower']) / 2

    # 2. Calculate the Magnitude and Color Errors from Flux Over Error (SNR)
    MAG_CONSTANT = 1.0857 # 2.5 / ln(10)
    
    if 'phot_g_mean_flux_over_error' in df.columns:
        df['phot_g_mean_mag_error'] = MAG_CONSTANT / df['phot_g_mean_flux_over_error']
        
    if 'phot_bp_mean_flux_over_error' in df.columns and 'phot_rp_mean_flux_over_error' in df.columns:
        sigma_bp = MAG_CONSTANT / df['phot_bp_mean_flux_over_error']
        sigma_rp = MAG_CONSTANT / df['phot_rp_mean_flux_over_error']
        # Remember the double-asterisk to square the numbers!
        df['bp_rp_error'] = np.sqrt(sigma_bp*2 + sigma_rp*2)

    # 3. Define the actual mathematical error columns for the model
    error_columns = [
        "Parallax error", 
        "phot_g_mean_mag_error", 
        "bp_rp_error", 
        "teff_gspphot_error"
    ]

    # 4. Check which columns actually exist to prevent crashes
    available_cols = [col for col in error_columns if col in df.columns]

    if len(available_cols) > 0:
        data_to_check = df[available_cols]
        mcd_model = EllipticEnvelope(contamination=0.05, random_state=42)
        labels = mcd_model.fit_predict(data_to_check)
        df = df[labels == 1]
        
    return df
