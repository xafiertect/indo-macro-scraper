import subprocess
import sys
import os

def run_script(path):
    print(f"\n>>> Running {path}...")
    # Use the venv python if available
    python_exe = "venv/bin/python" if os.path.exists("venv/bin/python") else sys.executable
    result = subprocess.run([python_exe, path], capture_output=False)
    if result.returncode != 0:
        print(f"❌ {path} failed with return code {result.returncode}")
    else:
        print(f"✅ {path} completed successfully.")

if __name__ == "__main__":
    print("🌟 Indonesia Inflation Forecasting System - Master Runner 🌟")
    
    # 1. Scrape
    run_script("src/scraper/imf_scraper.py")
    run_script("src/scraper/te_scraper.py")
    # FRED needs API key, so it might skip or fail if not set, but we try anyway
    run_script("src/scraper/fred_scraper.py")
    
    # 2. Pipeline
    run_script("src/pipeline/clean.py")
    run_script("src/pipeline/features.py")
    
    # 3. Baseline Model
    run_script("src/models/baseline.py")
    
    print("\n🏁 All steps completed.")
