import pandas as pd

def hard_filters(df):
    # Parallax cut: Must be positive to avoid math errors
    df = df[df["Parallax"] > 0]
    df = df[df["Parallax over error"] > 20]
    # Dimness cut: Removes stars too faint for reliable sensors (till 6 are visible by naked eye)
    df = df[df["Apparent G magnitude"] < 17] 
    # Physical Color Bounds: Restricts color index to valid glowing plasma
    df = df[(df["Color index"] >= -0.5) & (df["Color index"] <= 5.5)]
    # Temperature cut: Keeps surface temperatures within realistic physical limits
    if "Effective temperature" in df.columns:
        df = df[(df["Effective temperature"] >= 2000) & (df["Effective temperature"] <= 50000)]

    # Post calculations Quality filters   
    df = df[df["Extinction in G band"] >= 0]
    df = df[(df["Log luminosity"] >= -6) & (df["Log luminosity"] <= 6)]
    
    # Statistical filters (IQR method to remove telescope sensor noise)
    def statistical_error_cut(df, column_name):
  
    # Find the 25th percentile (Q1) and 75th percentile (Q3)
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
    
    # Calculate the size of the "normal" middle section (IQR)
        IQR = Q3 - Q1
    
    # Build the upper boundary fence (Standard formula is Q3 + 1.5 * IQR)
        upper_bound = Q3 + 1.5 * IQR
    
    # Filter the dataframe to only keep the reliable, normal errors
        df_clean = df[df[column_name] <= upper_bound]
    
        return df_clean
    if "Parallax error" in df.columns:
        df = statistical_error_cut(df, "Parallax error")
    
    return df
 """
 More error columns are needed like phot_g_mean_mag_error , bp_rp_error , teff_gspphot_error , to apply stat filters
 """


