import requests
import pandas as pd
import os

IMF_BASE = "https://www.imf.org/external/datamapper/api/v1"

def scrape_imf(indicator_code: str, country_code: str = "IDN") -> pd.DataFrame:
    """
    Scrape data dari IMF DataMapper API.
    """
    url = f"{IMF_BASE}/{indicator_code}/{country_code}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        raw = data.get("values", {}).get(indicator_code, {}).get(country_code, {})
        
        if not raw:
            print(f"⚠️ No data found for {indicator_code}/{country_code}")
            return pd.DataFrame()
        
        df = pd.DataFrame(list(raw.items()), columns=["year", indicator_code.lower()])
        df["date"] = pd.to_datetime(df["year"].astype(str) + "-01-01")
        df[indicator_code.lower()] = pd.to_numeric(df[indicator_code.lower()], errors="coerce")
        
        # IMF data annual -> resample ke bulanan (forward-fill)
        df = df.set_index("date")[[indicator_code.lower()]]
        df_monthly = df.resample("MS").ffill()
        df_monthly.reset_index(inplace=True)
        
        print(f"✅ IMF {indicator_code} ({country_code}): {len(df_monthly)} rows")
        return df_monthly
        
    except Exception as e:
        print(f"❌ IMF API failed for {indicator_code}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    print("🚀 Starting IMF scraping...")
    os.makedirs("data/raw", exist_ok=True)
    
    # Scrape indicators
    imf_indicators = {
        "PCPIPCH": "imf_inflation.csv",  # Inflation CPI YoY
        "RA": "imf_reserves.csv",       # Foreign Reserves
        "FM": "imf_m2.csv"              # Money Supply M2
    }
    
    for code, filename in imf_indicators.items():
        df = scrape_imf(code)
        if not df.empty:
            df.to_csv(f"data/raw/{filename}", index=False)
            print(f"  Saved {filename}")
