# 🇮🇩 Indonesia Inflation Forecasting

Proyek ini bertujuan untuk membangun sistem peramalan (forecasting) inflasi di Indonesia menggunakan berbagai sumber data ekonomi makro. Sistem ini mencakup seluruh siklus data mulai dari scraping, pembersihan, rekayasa fitur (feature engineering), hingga pemodelan menggunakan metode statistik dan machine learning.

## 🚀 Fitur Utama
- **Automated Scraping**: Mengambil data dari IMF, FRED (Federal Reserve), dan TradingEconomics.
- **Economic Feature Engineering**: Transformasi data makro menjadi fitur prediktif (Lags, Rolling Stats, Seasonal Flags seperti Ramadan/Lebaran).
- **Hybrid Modelling**: Perbandingan model statistik klasik (SARIMA) dengan model Machine Learning (XGBoost/LightGBM).

## 📁 Struktur Proyek
```text
indonesia-inflation-forecast/
├── data/
│   ├── raw/               # Data mentah hasil scraping
│   ├── processed/         # Data hasil pembersihan & merge
│   └── features/          # Data siap latih (setelah engineering)
├── notebooks/
│   ├── 01_scraping.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_modelling.ipynb
├── src/
│   ├── scraper/           # Skrip pengambil data modular
│   ├── pipeline/          # Pipeline pemrosesan data
│   └── models/            # Implementasi model forecasting
├── run_all.py             # Skrip runner untuk seluruh alur
├── requirements.txt       # Dependensi proyek
└── .env                   # Konfigurasi API Keys (FRED_API_KEY)
```

## 🛠️ Instalasi

1. Clone repositori ini:
   ```bash
   git clone https://github.com/username/indonesia-inflation-forecast.git
   cd indonesia-inflation-forecast
   ```

2. Buat dan aktifkan virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate  # Windows
   ```

3. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```

4. Konfigurasi API Key:
   Buat file `.env` di root direktori dan masukkan FRED API Key Anda:
   ```text
   FRED_API_KEY=isi_dengan_api_key_fred_anda
   ```

## 📈 Cara Penggunaan

### Menjalankan Seluruh Alur
Anda dapat menjalankan pengambilan data hingga pemodelan baseline dengan satu perintah:
```bash
python run_all.py
```

### Eksplorasi via Notebook
Gunakan notebook yang tersedia untuk analisis lebih mendalam:
```bash
jupyter lab notebooks/02_eda.ipynb
```

## 📊 Metrik Baseline (SARIMA)
- **MAE**: 0.1793%
- **RMSE**: 0.2132%
- **MAPE**: 7.06%

## 📝 Catatan Penting
- **Seasonality**: Model ini secara khusus menangani siklus musiman Indonesia seperti lonjakan harga saat Ramadan dan Hari Raya Idul Fitri.
- **Data Coverage**: Data dimulai dari Januari 2010 untuk memastikan konsistensi indikator makro.

---
**Disclaimer**: Proyek ini ditujukan untuk tujuan edukasi dan analisis data. Keputusan ekonomi harus didasarkan pada sumber resmi pemerintah dan Bank Indonesia.
