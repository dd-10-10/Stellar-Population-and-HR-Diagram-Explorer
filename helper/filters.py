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
    
    return df