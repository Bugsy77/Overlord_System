"""
SYSTEM: FAT BRAIN BRIAN (Phase 4: VOLUME TRUTH)
Strategy:
  1. News sets the Bias (Buy/Sell).
  2. Volume confirms the Move (Must be > 1.5x Average).
  3. Ignores Broker Price movement if Volume is weak (Anti-Fakeout).
"""

import time
import socket
import json
import yfinance as yf
import pandas as pd
import numpy as np 
from textblob import TextBlob
from colorama import Fore, Style, init

# IMPORT IG LIBRARIES (Optional)
try:
    from trading_ig import IGService
    from trading_ig.config import config as ig_config_obj
    IG_AVAILABLE = True
except ImportError:
    print(f"{Fore.RED}[SYSTEM] 'trading_ig' library not found. IG module disabled.{Style.RESET_ALL}")
    IG_AVAILABLE = False

# IMPORT SECRETS
try:
    import sys, os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import config
except ImportError:
    print(f"{Fore.RED}[SYSTEM] Critical: config.py not found!{Style.RESET_ALL}")
    exit()

init()

class FatBrainBrian:
    def __init__(self):
        print(f"{Fore.CYAN}--- FAT BRAIN BRIAN (VOLUME TRUTH EDITION) ---{Style.RESET_ALL}")
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((config.HOST, config.ZMQ_PORT))
        self.server.listen(1)
        self.conn = None
        
        self.ig = None
        if IG_AVAILABLE:
            try:
                self.ig = IGService(config.IG_USERNAME, config.IG_PASSWORD, config.IG_API_KEY, config.IG_ACC_TYPE)
                self.ig.create_session()
                print(f"{Fore.GREEN}[IG] Connected.{Style.RESET_ALL}")
            except Exception:
                print(f"{Fore.RED}[IG] Connection Failed (Check config.py){Style.RESET_ALL}")

        print(f"[NET] Waiting for cTrader on {config.ZMQ_PORT}...")
        self.conn, addr = self.server.accept()
        print(f"[NET] Connected to cTrader: {addr}")

    def execute_ig_trade(self, symbol, signal, sl, tp):
        if not self.ig: return
        epic = config.WATCHLIST[symbol]['ig_epic']
        direction = "BUY" if signal == "BUY" else "SELL"
        print(f"{Fore.MAGENTA}[IG] Attempting {direction} on {epic}...{Style.RESET_ALL}")
        try:
            self.ig.create_open_position(
                currency_code='USD', direction=direction, epic=epic, expiry='-',
                force_open=True, guaranteed_stop=False, order_type='MARKET', size=1,
                limit_level=tp, stop_level=sl
            )
        except Exception as e:
            print(f"{Fore.RED}[IG] Error: {e}{Style.RESET_ALL}")

    def send_socket_signal(self, payload):
        try:
            msg = json.dumps(payload) + "\n"
            self.conn.sendall(msg.encode('utf-8'))
            print(f"{Fore.BLUE}[SOCKET] Sent: {payload['signal']} (SL: {payload['sl']}){Style.RESET_ALL}")
        except Exception as e:
            print(f"[NET ERROR] {e}")

    def get_news_sentiment(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            if not news: return 0
            total, count = 0, 0
            for article in news[:3]:
                title = article.get('title')
                if not title and 'content' in article: title = article['content'].get('title')
                if title:
                    total += TextBlob(title).sentiment.polarity
                    count += 1
            return round(total / count, 2) if count > 0 else 0
        except: return 0

    def calculate_atr(self, data):
        if len(data) < 15: return 0 
        high = data['High']
        low = data['Low']
        close = data['Close'].shift(1)
        tr = pd.concat([high-low, abs(high-close), abs(low-close)], axis=1).max(axis=1)
        val = tr.rolling(window=14).mean().iloc[-1]
        if pd.isna(val): return 0
        return round(val, 2)

    def analyze_market_structure(self, ticker):
        try:
            # 1. FETCH DATA (Need Volume!)
            data = yf.download(ticker, period="5d", interval="15m", progress=False, auto_adjust=False)
            
            if data.empty or len(data) < 20: 
                print(f"[WARN] Not enough data for {ticker}")
                return None
            
            if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
            
            # 2. EXTRACT METRICS
            current_close = data['Close'].iloc[-1].item()
            current_vol = data['Volume'].iloc[-1].item()
            
            # SMA (Trend)
            sma_50 = data['Close'].rolling(window=50).mean().iloc[-1].item()
            trend = "BULLISH" if current_close > sma_50 else "BEARISH"
            
            # ATR (Risk)
            atr = self.calculate_atr(data)

            # 3. VOLUME ANALYSIS (The "Truth" Check)
            # Calculate Average Volume of last 20 candles
            vol_avg = data['Volume'].rolling(window=20).mean().iloc[-1].item()
            
            # Check for NaN in volume
            if pd.isna(vol_avg) or vol_avg == 0:
                rvol = 0
            else:
                # Relative Volume (RVOL) = Current / Average
                rvol = round(current_vol / vol_avg, 2)

            return {
                "price": round(current_close, 2),
                "trend": trend,
                "atr": atr,
                "rvol": rvol,          # How much stronger is volume today?
                "vol_avg": vol_avg
            }
            
        except Exception as e:
            print(f"[ERROR] Analyzing {ticker}: {e}")
            return None

    def run_surveillance(self):
        while True:
            print(f"\n{Fore.YELLOW}[SCANNING] {time.strftime('%H:%M:%S')}...{Style.RESET_ALL}")
            
            for symbol, info in config.WATCHLIST.items():
                try:
                    ticker = info['yahoo']
                    
                    # 1. Get Sentiment (The Catalyst)
                    sent = self.get_news_sentiment(ticker)
                    
                    # 2. Get Structure (The Truth)
                    tech = self.analyze_market_structure(ticker)
                    
                    if tech:
                        signal = "HOLD"
                        sl = 0
                        tp = 0
                        
                        # --- THE NEW STRATEGY ---
                        # We only trade if:
                        # A) Sentiment is Active (Not 0)
                        # B) Volume is Strong (> 1.2x Average)
                        # C) Trend aligns
                        
                        is_volume_high = tech['rvol'] > 1.2
                        
                        if tech['trend'] == "BULLISH" and sent > 0 and is_volume_high:
                            signal = "BUY"
                            sl = tech['price'] - (tech['atr'] * 2)
                            tp = tech['price'] + (tech['atr'] * 3)
                            
                        elif tech['trend'] == "BEARISH" and sent < 0 and is_volume_high:
                            signal = "SELL"
                            sl = tech['price'] + (tech['atr'] * 2)
                            tp = tech['price'] - (tech['atr'] * 3)

                        # Logic Reporting
                        vol_color = Fore.GREEN if is_volume_high else Fore.RED
                        print(f"[{symbol}] Sent:{sent:.2f} | {vol_color}Vol:{tech['rvol']}x{Style.RESET_ALL} | Trend:{tech['trend']}")

                        # Send Orders
                        payload = {"symbol": symbol, "signal": signal, "sl": round(sl, 2), "tp": round(tp, 2)}
                        self.send_socket_signal(payload)
                        
                        if signal != "HOLD":
                            print(f"{Fore.GREEN}>>> TRIGGER: High Volume + News Confirmation!{Style.RESET_ALL}")
                            self.execute_ig_trade(symbol, signal, sl, tp)
                
                except Exception as e:
                    print(f"[ERROR] Loop error: {e}")

            time.sleep(60)

if __name__ == "__main__":
    brain = FatBrainBrian()
    brain.run_surveillance()