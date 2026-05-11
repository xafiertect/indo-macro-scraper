import os
import requests
import pandas as pd
from dotenv import load_dotenv
from functools import reduce

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")

def scrape_fred(series_id: str, start_date: str = "2010-01-01") -> pd.DataFrame:
    """
    Scrape satu series dari FRED API.
    """
    if not FRED_API_KEY or FRED_API_KEY == "your_fred_api_key_here":
        print(f"⚠️ FRED_API_KEY not set. Skipping {series_id}")
        return pd.DataFrame()

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "frequency": "m",
        "aggregation_method": "avg"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()["observations"]
        df = pd.DataFrame(data)[["date", "value"]]
        df.rename(columns={"value": series_id.lower()}, inplace=True)
        df["date"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp()
        df[series_id.lower()] = pd.to_numeric(df[series_id.lower()], errors="coerce")
        
        return df
    except Exception as e:
        print(f"❌ Error scraping {series_id}: {e}")
        return pd.DataFrame()

# Mapping FRED series yang dibutuhkan
FRED_SERIES = {
    "DEXINUS": "usd_idr",           # Kurs USD/IDR
    "FEDFUNDS": "fed_fund_rate",    # Fed Funds Rate
    "DCOILBRENTEU": "oil_price_brent", # Harga Minyak Brent
    "IDNCPIALLMINMEI": "inflation_yoy" # Consumer Price Index for Indonesia (Total, All Items)
}

if __name__ == "__main__":
    print("🚀 Starting FRED scraping...")
    all_fred = []
    for series_id, col_name in FRED_SERIES.items():
        print(f"  Scraping {series_id} -> {col_name}...")
        df = scrape_fred(series_id)
        if not df.empty:
            df.rename(columns={series_id.lower(): col_name}, inplace=True)
            all_fred.append(df)

    if all_fred:
        fred_combined = reduce(lambda l, r: pd.merge(l, r, on="date", how="outer"), all_fred)
        fred_combined.sort_values("date", inplace=True)
        os.makedirs("data/raw", exist_ok=True)
        fred_combined.to_csv("data/raw/fred_data.csv", index=False)
        print(f"✅ FRED data saved: {fred_combined.shape}")
    else:
        print("❌ No FRED data collected (Check API Key).")
