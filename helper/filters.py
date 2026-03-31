import pandas as pd
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
# TODO: Figure out a better method for multivariate outlier removal

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
"""
teff_gspphot_error colum is not added yet
"""
def MCD_filter(df):
    '''
    Uses the Minimum Covariance Determinant (MCD) method to remove
    multivariate statistical outliers based on telescope measurement errors.
    '''
    error_columns = ["Parallax error", "phot_g_mean_flux_over_error", "phot_bp_mean_flux_over_error", "phot_rp_mean_flux_over_error", "teff_gspphot_error"]

    available_cols = [col for col in error_columns if col in df.columns]

    if len(available_cols) > 0:
        data_to_check = df[available_cols]

        mcd_model = EllipticEnvelope(contamination=0.05, random_state=42)

        labels = mcd_model.fit_predict(data_to_check)

        df = df[labels == 1]
    return df
