"""
Project: The Overlord System - Master of Whispers
Author: [Your Name]
Description: 
    A multi-asset market scanner that aggregates volume data from 
    Yahoo Finance (Futures) and Binance (Crypto) to detect 
    institutional money flow anomalies.
"""

import yfinance as yf
import requests
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURATION ---
ASSETS = {
    'GOLD_FUTURES': 'GC=F',  # CME Gold
    'OIL_WTI': 'CL=F',       # Crude Oil
    'BITCOIN': 'BTCUSDT'     # Binance
}

DATA_FILE = 'market_intelligence.csv'

def get_yahoo_data(ticker):
    """Fetches daily volume and price from Yahoo Finance."""
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="20d") # Get 20 days for average calculation
        if hist.empty: return None
        
        current = hist.iloc[-1]
        avg_vol = hist['Volume'].mean()
        
        return {
            'price': current['Close'],
            'volume': current['Volume'],
            'avg_volume': avg_vol,
            'vol_ratio': current['Volume'] / avg_vol if avg_vol > 0 else 0
        }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def get_binance_data(symbol):
    """Fetches 24h volume from Binance API."""
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        res = requests.get(url).json()
        vol = float(res['volume']) # Volume in Base Asset
        return {
            'price': float(res['lastPrice']),
            'volume': vol,
            'avg_volume': vol, # Placeholder: Binance 24h is static
            'vol_ratio': 1.0   # Needs historical database for true ratio
        }
    except Exception as e:
        print(f"Error fetching Binance {symbol}: {e}")
        return None

def run_scan():
    print(f"\n--- 🦅 WHISPER SCAN: {datetime.now()} ---")
    results = []
    
    # 1. SCAN TRADITIONAL MARKETS
    for name, ticker in ASSETS.items():
        if name == 'BITCOIN':
            data = get_binance_data(ticker)
        else:
            data = get_yahoo_data(ticker)
            
        if data:
            # The "Edge" Calculation
            status = "NORMAL"
            if data['vol_ratio'] > 1.5: status = "HIGH_ACTIVITY"
            if data['vol_ratio'] > 2.5: status = "INSTITUTIONAL_BUYING"
            
            print(f"[{name}] Vol Ratio: {data['vol_ratio']:.2f}x | Status: {status}")
            
            # Save for Kaggle
            results.append({
                'timestamp': datetime.now(),
                'asset': name,
                'price': data['price'],
                'volume': data['volume'],
                'ratio': data['vol_ratio'],
                'status': status
            })

    # 2. SAVE DATA (The Memory)
    df = pd.DataFrame(results)
    header = not os.path.exists(DATA_FILE)
    df.to_csv(DATA_FILE, mode='a', header=header, index=False)
    print(f"Data saved to {DATA_FILE}")

if __name__ == "__main__":
    run_scan()