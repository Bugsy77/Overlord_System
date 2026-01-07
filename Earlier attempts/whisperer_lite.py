"""
Project: The Overlord System - Master of Whispers (Lite Architecture)
Author: [Your Name]
Description: Lightweight market scanner using Standard Libraries only.
"""

import json
import urllib.request
import csv
import time
import random
from datetime import datetime
import os

# --- CONFIGURATION ---
DATA_FILE = 'market_intelligence.csv'

def get_binance_price(symbol="BTCUSDT"):
    """Fetches Live Price from Binance using standard URL tools."""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return float(data['price'])
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def run_scan():
    print(f"\n--- 🦅 WHISPER SCAN: {datetime.now().strftime('%H:%M:%S')} ---")
    
    # 1. GET REAL DATA (Bitcoin)
    btc_price = get_binance_price()
    
    # 2. SIMULATE GOLD DATA (Since we skipped the heavy library install)
    # In the Pro version, this comes from Yahoo. For now, we simulate the feed.
    gold_price = 2035.50 + random.uniform(-10, 10) 
    gold_vol_ratio = random.uniform(0.8, 2.1)
    
    status = "NORMAL"
    if gold_vol_ratio > 1.5: status = "INSTITUTIONAL_ACTIVITY"
    
    # 3. PRINT REPORT
    if btc_price:
        print(f"[BITCOIN] Live Price: ${btc_price:,.2f}")
    print(f"[GOLD]    Vol Ratio:  {gold_vol_ratio:.2f}x | Status: {status}")

    # 4. SAVE TO CSV (The Memory)
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Asset', 'Price', 'Status']) # Header
        
        writer.writerow([datetime.now(), 'BTC', btc_price, 'LIVE'])
        writer.writerow([datetime.now(), 'GOLD', gold_price, status])
        
    print(f"Data saved to {DATA_FILE}")

if __name__ == "__main__":
    run_scan()