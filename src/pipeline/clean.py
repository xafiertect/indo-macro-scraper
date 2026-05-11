import pandas as pd
import numpy as np
import os
from functools import reduce

def normalize_date(df):
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp()
    elif "Date" in df.columns:
        df["date"] = pd.to_datetime(df["Date"]).dt.to_period("M").dt.to_timestamp()
        df.drop(columns=["Date"], inplace=True)
    return df

def clean_and_merge_all() -> pd.DataFrame:
    """
    Master pipeline: load semua raw data, bersihkan, merge ke satu DataFrame.
    """
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    # Files to load
    files = {
        "fred": "fred_data.csv",
        "imf_inf": "imf_inflation.csv",
        "imf_res": "imf_reserves.csv",
        "imf_m2": "imf_m2.csv",
        "te_inf": "te_inflation.csv"
    }
    
    loaded_dfs = []
    for key, filename in files.items():
        path = os.path.join(raw_dir, filename)
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                if not df.empty:
                    df = normalize_date(df)
                    loaded_dfs.append(df)
                    print(f"  Loaded {filename}: {len(df)} rows")
            except Exception as e:
                print(f"  Error loading {filename}: {e}")

    if not loaded_dfs:
        print("❌ No data found to merge.")
        return pd.DataFrame()

    # Merge all
    print("  Merging datasets...")
    master = reduce(lambda l, r: pd.merge(l, r, on="date", how="outer"), loaded_dfs)
    master.sort_values("date", inplace=True)
    master.reset_index(drop=True, inplace=True)
    
    # Handle Missing Values (adapted from blueprint)
    slow_cols = ["bi_7drrr", "fed_fund_rate", "foreign_reserves", "m2_supply"]
    for col in slow_cols:
        if col in master.columns:
            master[col] = master[col].fillna(method="ffill", limit=3)
    
    commodity_cols = ["oil_price_brent", "cpo_price", "usd_idr"]
    for col in commodity_cols:
        if col in master.columns:
            master[col] = master[col].interpolate(method="linear", limit_direction="both")
    
    # Filter range
    master = master[(master["date"] >= "2010-01-01")]
    
    master.to_csv(os.path.join(processed_dir, "master_dataset.csv"), index=False)
    print(f"✅ Master dataset saved: {master.shape}")
    return master

if __name__ == "__main__":
    print("🚀 Starting Cleaning Pipeline...")
    clean_and_merge_all()
