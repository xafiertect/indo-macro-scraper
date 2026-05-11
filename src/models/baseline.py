import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

def evaluate_model(y_true, y_pred, model_name="Model"):
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    print(f"\n{'='*40}")
    print(f"  {model_name}")
    print(f"{'='*40}")
    print(f"  MAE  : {mae:.4f}%")
    print(f"  RMSE : {rmse:.4f}%")
    print(f"  MAPE : {mape:.2f}%")
    return {"mae": mae, "rmse": rmse, "mape": mape}

def run_baseline_sarima():
    """
    Run SARIMA model on inflation_yoy.
    """
    features_path = "data/features/feature_dataset.csv"
    if not os.path.exists(features_path):
        print("❌ Feature dataset not found. Run pipelines first.")
        return

    df = pd.read_csv(features_path, parse_dates=["date"])
    df.set_index("date", inplace=True)
    
    target = "inflation_yoy"
    if target not in df.columns:
        print(f"❌ Target {target} not found.")
        return
        
    y = df[target].dropna()
    
    # Train/Test Split (Chronological)
    train_size = int(len(y) * 0.8)
    train, test = y[0:train_size], y[train_size:len(y)]
    
    print(f"🚀 Training SARIMA on {len(train)} samples, testing on {len(test)}...")
    
    # Fit SARIMA (Simple parameters for baseline)
    try:
        # Simplified for resampled annual data
        model = SARIMAX(train, order=(1, 0, 0), seasonal_order=(0, 0, 0, 0))
        model_fit = model.fit(disp=False)
        predictions = model_fit.forecast(steps=len(test))
        evaluate_model(test, predictions, "Baseline SARIMA")
    except Exception as e:
        print(f"⚠️ SARIMA failed ({e}). Falling back to Naive (Lag-1)...")
        predictions = test.shift(1).fillna(train.iloc[-1])
        evaluate_model(test, predictions, "Baseline Naive")
        
    # Plot
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(train.index, train, label="Train")
        plt.plot(test.index, test, label="Test")
        plt.plot(test.index, predictions, label="Forecast", color="red")
        plt.title("Indonesia Inflation Forecast - Baseline")
        plt.legend()
        os.makedirs("data", exist_ok=True)
        plt.savefig("data/baseline_plot.png")
        print("✅ Plot saved to data/baseline_plot.png")
    except Exception as e:
        print(f"❌ Plotting failed: {e}")

if __name__ == "__main__":
    run_baseline_sarima()
