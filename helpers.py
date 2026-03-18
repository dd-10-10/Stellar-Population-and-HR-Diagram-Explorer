import numpy as np
import pandas as pd

def new_names(df):
    n_dict = {"phot_g_mean_mag" : "Apparent G magnitude",
             "phot_bp_mean_mag" : "Blue photometer magnitude",
             "phot_rp_mean_mag" : "Red photometer magnitude",
             "parallax" : "Parallax",
             "parallax_error" : "Parallax error",
             "parallax_over_error" : "Parallax over error",
             "ag_gspphot" : "Extinction in G band",
             "teff_gspphot" : "Effective temperature",
             "logg_gspphot" : "Surface gravity"}
    df.rename(columns = n_dict, inplace = True)

def distance(df):
    d = 1000/df["Parallax"]
    return d

def color(df):
    color = df["Blue photometer magnitude"] - df["Red photometer magnitude"]
    return color

def abs_vis_mag(df):
    g, p = df["Apparent G magnitude"], df["Parallax"]
    bp, rp = df["Blue photometer magnitude"], df["Red photometer magnitude"]
    g_ext = df["Extinction in G band"]
    v = g + 0.0176 + 0.00686 * (color(df)) + 0.1732 * (color(df)**2)
    mv= v - (1.1 * g_ext) + (5 * np.log10(p)) - 10
    return mv

def abs_mag(df):
    g, g_ext, p = df["Apparent G magnitude"], df["Extinction in G band"], df["Parallax"]
    mg= g - g_ext + (5 * np.log10(p)) - 10
    return mg

def log_lum(df):
    l = 0.4 * (4.66 - abs_mag(df))
    return l

def spectral_class(row):
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
    return df.apply(spectral_class, axis = 1)

if __name__ == "__main__":
    df1 = pd.read_csv("Near_earth_50k.csv")
    df1.dropna(axis = 0, inplace = True)
    new_names(df1)
    df1["Distance"] = distance(df1)
    df1["Color index"] = color(df1)
    df1["Absolute visual magnitude"] = abs_vis_mag(df1)
    df1["Absolute magnitude"] = abs_mag(df1)
    df1["Log luminosity"] = log_lum(df1)
    df1["Spectral class"] = spec(df1)
    df1.to_csv("near_earth_50k_clean_calc.csv")

    df2 = pd.read_csv("Far_earth_50k.csv")
    df2.dropna(axis = 0, inplace = True)
    new_names(df1)
    df2["Distance"] = distance(df1)
    df2["Color index"] = color(df1)
    df2["Absolute visual magnitude"] = abs_vis_mag(df1)
    df2["Absolute magnitude"] = abs_mag(df1)
    df2["Log luminosity"] = log_lum(df1)
    df2["Spectral class"] = spec(df1)
    df2.to_csv("far_earth_50k_clean_calc.csv")
