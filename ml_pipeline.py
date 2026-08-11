"""
DSE Insight — Machine Learning Pipeline
════════════════════════════════════════════════════════════
Reads historical DSE equity CSV files, trains a Random Forest
Classifier to predict the short-term trend (Bullish, Bearish, Neutral),
and outputs predictions for the latest data.
"""

import os
import glob
import re
import warnings
from datetime import datetime

# Suppress sklearn warnings for cleaner output
warnings.filterwarnings('ignore')

try:
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
except ImportError:
    print("❌ Machine Learning dependencies not found. Run: pip install scikit-learn pandas numpy")
    pd = None


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "data", "historical", "dse_table_3_historical.csv")

def parse_change(raw) -> float:
    try:
        cleaned = re.sub(r"[▲▼⏴⏵⬆⬇+\s]", " ", str(raw)).strip()
        nums = [p for p in cleaned.split() if re.match(r"^-?\d+\.?\d*$", p)]
        if not nums: return 0.0
        val = float(nums[-1])
        if "▼" in str(raw) and val > 0: val = -val
        return val
    except:
        return 0.0

def safe_float(val) -> float:
    try: return float(str(val).replace(",", "").strip())
    except: return 0.0

def load_historical_data() -> pd.DataFrame:
    """Loads the historical equity CSV into a time-series DataFrame."""
    if not os.path.exists(HISTORICAL_DATA_PATH):
        return pd.DataFrame()

    try:
        df = pd.read_csv(HISTORICAL_DATA_PATH)
    except Exception as e:
        print(f"Error reading historical data: {e}")
        return pd.DataFrame()
            
    if df.empty:
        return pd.DataFrame()

    # Clean and standardize columns
    combined = df.rename(columns={
        'Symbol': 'symbol',
        'Close': 'close',
        'Volume': 'volume',
        'Turn over': 'turnover',
        'MCAP (TZS \'B)': 'mcap'
    })
    
    # Keep only needed columns and clean strings
    combined['symbol'] = combined['symbol'].astype(str).str.strip()
    combined = combined[combined['symbol'].str.lower() != 'nan']
    
    combined['close'] = combined['close'].apply(safe_float)
    combined['volume'] = combined['volume'].apply(safe_float)
    combined['turnover'] = combined['turnover'].apply(safe_float)
    combined['change'] = combined['Change'].apply(parse_change)
    
    # Sort by Symbol and Date to create proper time series
    combined = combined.sort_values(by=['symbol', 'Date']).reset_index(drop=True)
    
    return combined

def run_predictions(symbols_to_predict=None) -> dict:
    """
    Trains the ML model on historical data and returns predictions for the requested symbols.
    Returns a dict: { "CRDB": {"trend": "Bullish", "confidence": 85}, ... }
    """
    if pd is None:
        return _fallback_predictions(symbols_to_predict)

    df = load_historical_data()
    
    if len(df) < 50: # If we have very little historical data, the ML model will fail/overfit
        print("⚠️ Not enough historical data for deep ML training. Using heuristics fallback.")
        return _fallback_predictions(symbols_to_predict, df)

    # --- Feature Engineering ---
    # Create target variable: Did the price go up, down, or stay flat the *next* day?
    # 1: Up (Bullish), -1: Down (Bearish), 0: Flat (Neutral)
    df['next_close'] = df.groupby('symbol')['close'].shift(-1)
    
    def determine_target(row):
        if pd.isna(row['next_close']): return np.nan
        if row['next_close'] > row['close']: return 1
        elif row['next_close'] < row['close']: return -1
        else: return 0
        
    df['target'] = df.apply(determine_target, axis=1)
    
    # Drop rows where we don't have a next_close (the most recent day)
    train_df = df.dropna(subset=['target'])
    
    if len(train_df) < 20:
        return _fallback_predictions(symbols_to_predict, df)

    features = ['close', 'volume', 'turnover', 'change']
    X = train_df[features]
    y = train_df['target']
    
    # --- Train Model ---
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Random Forest is robust to outliers and works well for classification
    clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    clf.fit(X_scaled, y)
    
    # --- Predict Latest ---
    # Get the latest row for each symbol
    latest_df = df.groupby('symbol').last().reset_index()
    
    predictions = {}
    
    for _, row in latest_df.iterrows():
        sym = row['symbol']
        if symbols_to_predict and sym not in symbols_to_predict:
            continue
            
        feats = row[features].values.reshape(1, -1)
        feats_scaled = scaler.transform(feats)
        
        pred_class = clf.predict(feats_scaled)[0]
        probas = clf.predict_proba(feats_scaled)[0]
        
        # Get the probability of the predicted class
        conf = int(max(probas) * 100)
        
        if pred_class == 1: trend = "Bullish"
        elif pred_class == -1: trend = "Bearish"
        else: trend = "Neutral"
        
        predictions[sym] = {
            "trend": trend,
            "confidence": conf
        }
        
    # Fill in any missing symbols with Neutral
    if symbols_to_predict:
        for sym in symbols_to_predict:
            if sym not in predictions:
                predictions[sym] = {"trend": "Neutral", "confidence": 50}
                
    return predictions

def _fallback_predictions(symbols, df=None) -> dict:
    """Fallback heuristics if ML dependencies are missing or not enough data."""
    preds = {}
    
    if not symbols:
        return preds
        
    # If we have a tiny bit of dataframe history, use momentum heuristic
    if df is not None and not df.empty:
        latest = df.groupby('symbol').last()
        for sym in symbols:
            if sym in latest.index:
                change = latest.loc[sym, 'change']
                if change > 1.0: 
                    preds[sym] = {"trend": "Bullish", "confidence": 65}
                elif change < -1.0: 
                    preds[sym] = {"trend": "Bearish", "confidence": 65}
                else: 
                    preds[sym] = {"trend": "Neutral", "confidence": 55}
            else:
                preds[sym] = {"trend": "Neutral", "confidence": 50}
        return preds

    # Absolute fallback
    for sym in symbols:
        preds[sym] = {"trend": "Neutral", "confidence": 50}
    return preds

if __name__ == "__main__":
    print("Testing ML Pipeline...")
    res = run_predictions(["CRDB", "NMB", "PAL"])
    print(res)
