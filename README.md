# 🇮🇩 Indonesia Inflation Forecasting — Macroeconomic Scraper & Predictor

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Statsmodels](https://img.shields.io/badge/Forecasting-SARIMA-green.svg)](https://www.statsmodels.org/)
[![Framework: XGBoost](https://img.shields.io/badge/ML-XGBoost-orange.svg)](https://xgboost.readthedocs.io/)

Proyek ini adalah sistem end-to-end untuk mengambil, memproses, dan memprediksi tingkat inflasi di Indonesia menggunakan data ekonomi makro global dan domestik.

---

## 🏛️ Arsitektur Proyek
Sesuai dengan blueprint desain, proyek ini dibagi menjadi beberapa lapisan modular:

### 1. Lapisan Data (`/data`)
- **Raw**: Data mentah dari API FRED, IMF, dan TradingEconomics.
- **Processed**: Hasil penggabungan (outer join) dan normalisasi deret waktu.
- **Features**: Dataset akhir dengan fitur teknis (Lags, Differencing, Seasonal Flags).

### 2. Lapisan Logika (`/src`)
- **Scraper**: Implementasi REST API dan Web Scraping modular.
- **Pipeline**: Automasi pembersihan data dan rekayasa fitur otomatis.
- **Models**: Implementasi model SARIMA sebagai baseline dan XGBoost sebagai model tingkat lanjut.

### 3. Lapisan Eksplorasi (`/notebooks`)
- Alur kerja langkah-demi-langkah dari ekstraksi data hingga evaluasi model.

---

## 🛠️ Persiapan & Instalasi

### 1. Lingkungan Virtual
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi API
Buat file `.env` dan masukkan API Key dari [FRED](https://fred.stlouisfed.org/docs/api/api_key.html):
```env
FRED_API_KEY=your_actual_key_here
```

---

## 🚀 Cara Menjalankan

### **Opsi A: Alur Otomatis**
Jalankan seluruh pipeline dari awal hingga akhir (Scrape -> Clean -> Feature -> Model):
```bash
python run_all.py
```

### **Opsi B: Eksplorasi Manual**
Buka Jupyter Lab untuk melihat analisis data secara interaktif:
```bash
jupyter lab
```
Urutan pengerjaan:
1. `01_scraping.ipynb`
2. `02_eda.ipynb`
3. `03_feature_engineering.ipynb`
4. `04_modelling.ipynb`

---

## 📊 Analisis & Metrik
Sistem ini menggunakan fitur khusus ekonomi Indonesia:
- **Ramadan Effect**: Menangkap lonjakan musiman saat bulan puasa.
- **Imported Inflation**: Melacak pengaruh kurs USD/IDR terhadap harga domestik.
- **Commodity Link**: Menghubungkan harga minyak dunia (Brent) dengan inflasi transportasi.

**Metrik Performa (Baseline):**
- **MAE**: 0.1793%
- **RMSE**: 0.2132%
- **MAPE**: 7.06%

---

## 🛡️ Keamanan & Privasi
Proyek ini menggunakan `.gitignore` yang ketat untuk mengabaikan:
- Data sensitif di `.env`
- Lingkungan virtual (`venv/`)
- Log internal agen coding (`.agents/`)
- Data mentah CSV yang besar.

---
**Author**: xafiertect | **Repo**: [indo-macro-scraper](https://github.com/xafiertect/indo-macro-scraper)
