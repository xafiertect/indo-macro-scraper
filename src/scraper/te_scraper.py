import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

def scrape_te_inflation() -> pd.DataFrame:
    """
    Scrape data inflasi Indonesia dari TradingEconomics.
    """
    url = "https://tradingeconomics.com/indonesia/inflation-cpi"
    
    try:
        session = requests.Session()
        response = session.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        # We try to use the historical API if possible, or parse the table
        # For simplicity in this blueprint execution, we will mock or use a public endpoint if known
        # But here we follow the blueprint's read_html suggestion
        
        # Check if table exists
        dfs = pd.read_html(response.text)
        for df in dfs:
            if "Actual" in df.columns or "Value" in df.columns:
                df.columns = [c.lower().replace(" ", "_") for c in df.columns]
                return df
        
        print("⚠️ No suitable table found on TradingEconomics page.")
        return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ TE Scraping failed: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    print("🚀 Starting TradingEconomics scraping...")
    os.makedirs("data/raw", exist_ok=True)
    
    df = scrape_te_inflation()
    if not df.empty:
        df.to_csv("data/raw/te_inflation.csv", index=False)
        print(f"✅ TradingEconomics data saved: {len(df)} rows")
    else:
        # Create a placeholder to avoid pipeline failure later
        pd.DataFrame(columns=["date", "inflation_yoy"]).to_csv("data/raw/te_inflation.csv", index=False)
        print("⚠️ Created empty placeholder for te_inflation.csv")
