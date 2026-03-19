import numpy as np
import pandas as pd

#---- Calculations and other functions; see bottom for actual setup, cleaning, and filtering ----

def new_names(df):
    '''
    Function to rename the columns to better appearing names
    '''
    n_dict = {"phot_g_mean_mag" : "Apparent G magnitude",
             "bp_rp" : "Color index",
             "parallax" : "Parallax",
             "parallax_error" : "Parallax error",
             "parallax_over_error" : "Parallax over error",
             "ag_gspphot" : "Extinction in G band",
             "teff_gspphot" : "Effective temperature",
             "logg_gspphot" : "Surface gravity"}
    df.rename(columns = n_dict, inplace = True)

def quality_cuts(df):
    # Parallax cut: Must be positive to avoid math errors
    df = df[df["Parallax"] > 0]
    # Dimness cut: Removes stars too faint for reliable sensors (till 6 are visible by naked eye)
    df = df[df["Apparent G magnitude"] < 17] 
    # Physical Color Bounds: Restricts color index to valid glowing plasma
    df = df[(df["Color index"] >= -0.5) & (df["Color index"] <= 5.5)]
    # Temperature cut: Keeps surface temperatures within realistic physical limits
    if "Effective temperature" in df.columns:
        df = df[(df["Effective temperature"] >= 2000) & (df["Effective temperature"] <= 50000)]
    
    return df

def distance(df):
    '''
    Function to calculate distance from parallax
    '''
    d = 1000/df["Parallax"]
    return d

def abs_vis_mag(df):
    '''
    Function to calculate absolute visual magnitude
    '''
    g, g_ext, p = df["Apparent G magnitude"], df["Extinction in G band"], df["Parallax"] 
    v = g + 0.0176 + 0.00686 * df["Color index"] + 0.1732 * ((df["Color index"])**2)
    mv= v - (1.1 * g_ext) + (5 * np.log10(p)) - 10
    return mv

def abs_mag(df):
    '''
    Function to calculate absolute g band magnitude
    '''
    g, g_ext, p = df["Apparent G magnitude"], df["Extinction in G band"], df["Parallax"]
    mg= g - g_ext + (5 * np.log10(p)) - 10
    return mg

def log_lum(df):
    '''
    Function to calculate luminosity (log_10)
    '''
    l = 0.4 * (4.66 - abs_mag(df))
    return l

def spectral_class(row):
    '''
    Function to identify spectral class from temperature
    '''
    if row["Effective temperature"] > 30000:
        return 'O'
    elif row["Effective temperature"] > 10000:
        return 'B'
    elif row["Effective temperature"] > 7500:
        return 'A'
    elif row["Effective temperature"] > 6000:
        return 'F'
    elif row["Effective temperature"] > 5200:
        return 'G'
    elif row["Effective temperature"] > 3700:
        return 'K'
    else:
        return 'M'

def spec(df):
    '''
    Function to vectorise the spectral class identifier
    '''
    return df.apply(spectral_class, axis = 1)

#---- Actual file setup ----

if __name__ == "__main__":
    
    #Creating one combined dataframe
    df1 = pd.read_csv("data/near_100k.csv")
    df2 = pd.read_csv("data/far_100k.csv")
    df= pd.concat((df1, df2))

    #Calculating and adding new columns
    df.dropna(axis = 0, inplace = True)
    new_names(df)
    df = quality_cuts(df)
    df["Distance"] = distance(df)
    df["Absolute visual magnitude"] = abs_vis_mag(df)
    df["Absolute magnitude"] = abs_mag(df)
    df["Log luminosity"] = log_lum(df)
    df["Log effective temperature"] = np.log10(df["Effective temperature"])
    # No need to take log of surface gravity as it is already log of surface gravity when downloaded from Gaia and it is already in range from 0 to 9. 
    df["Log surface gravity"] = np.log10(df["Surface gravity"])
    df["Spectral class"] = spec(df)

    # Post calculations Quality filters   
    df = df[df["Extinction in G band"] >= 0]
    df = df[(df["Log luminosity"] >= -6) & (df["Log luminosity"] <= 6)]
    #Saving
    df.to_csv("data/stars_clean_calc.csv", index= False)
