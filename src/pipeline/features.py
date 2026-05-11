import pandas as pd
import numpy as np
import os

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tambahkan semua fitur engineered ke master dataset.
    """
    if df.empty:
        return df
        
    df = df.copy().sort_values("date").reset_index(drop=True)
    
    # Check for target column
    if "pcpipch" in df.columns and "inflation_yoy" not in df.columns:
        df["inflation_yoy"] = df["pcpipch"]
    
    target_col = "inflation_yoy"
    if target_col not in df.columns or df[target_col].isnull().all():
        # Try to find it if named differently
        potential_targets = [c for c in df.columns if "inflation" in c.lower()]
        if potential_targets:
            target_col = potential_targets[0]
            print(f"  Using {target_col} as primary inflation target.")
        else:
            print("⚠️ No inflation target column found. Lags might be empty.")
            df[target_col] = np.nan

    # 6.1 AUTOREGRESSIVE FEATURES
    df["lag_1_inflation"]  = df[target_col].shift(1)
    df["lag_2_inflation"]  = df[target_col].shift(2)
    df["lag_3_inflation"]  = df[target_col].shift(3)
    df["lag_6_inflation"]  = df[target_col].shift(6)
    df["lag_12_inflation"] = df[target_col].shift(12)
    
    if "bi_7drrr" in df.columns:
        df["lag_1_bi_rate"] = df["bi_7drrr"].shift(1)
    if "usd_idr" in df.columns:
        df["lag_1_usd_idr"] = df["usd_idr"].shift(1)
    
    # 6.2 DIFFERENTIAL FEATURES
    if "usd_idr" in df.columns:
        df["diff_usd_idr"] = df["usd_idr"].diff()
    if "oil_price_brent" in df.columns:
        df["diff_oil_price"] = df["oil_price_brent"].diff()
    if "bi_7drrr" in df.columns:
        df["diff_bi_rate"] = df["bi_7drrr"].diff()
    if "fed_fund_rate" in df.columns:
        df["diff_fed_rate"] = df["fed_fund_rate"].diff()
    
    # 6.3 ROLLING STATISTICS
    df["roll3_inflation_mean"] = df[target_col].rolling(3).mean()
    df["roll6_inflation_mean"] = df[target_col].rolling(6).mean()
    df["roll3_inflation_std"]  = df[target_col].rolling(3).std()
    if "usd_idr" in df.columns:
        df["roll3_usd_idr_mean"] = df["usd_idr"].rolling(3).mean()
    
    # 6.4 SEASONALITY FEATURES
    month_num = df["date"].dt.month
    df["month_sin"] = np.sin(2 * np.pi * month_num / 12)
    df["month_cos"] = np.cos(2 * np.pi * month_num / 12)
    
    # Binary flags
    df["is_ramadan_month"]    = month_num.isin([3, 4]).astype(int)
    df["is_lebaran_window"]   = month_num.isin([4, 5]).astype(int)
    df["is_nataru"]           = month_num.isin([12, 1]).astype(int)
    df["is_harvest_season"]   = month_num.isin([2, 3, 8, 9]).astype(int)
    
    # 6.5 INTERACTION FEATURES
    if "usd_idr" in df.columns and "oil_price_brent" in df.columns:
        df["usd_idr_x_oil"] = df["usd_idr"] * df["oil_price_brent"]
    
    # 6.6 POLICY GAP
    if "bi_7drrr" in df.columns and "fed_fund_rate" in df.columns:
        df["rate_differential"] = df["bi_7drrr"] - df["fed_fund_rate"]
    
    # 6.7 YEAR/MONTH
    df["year"]  = df["date"].dt.year
    df["month"] = df["date"].dt.month
    
    return df

if __name__ == "__main__":
    print("🚀 Starting Feature Engineering Pipeline...")
    processed_path = "data/processed/master_dataset.csv"
    features_dir = "data/features"
    os.makedirs(features_dir, exist_ok=True)
    
    if os.path.exists(processed_path):
        df = pd.read_csv(processed_path, parse_dates=["date"])
        df_feat = engineer_features(df)
        df_feat.to_csv(os.path.join(features_dir, "feature_dataset.csv"), index=False)
        print(f"✅ Feature dataset saved: {df_feat.shape}")
    else:
        print("❌ Master dataset not found. Run clean.py first.")
