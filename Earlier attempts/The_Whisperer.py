import time
import json
import random
import os

# CONFIGURATION
# We point to the SAME folder as the C# bot (My Documents)
BRIDGE_FILE = os.path.join(os.path.expanduser("~"), "Documents", "Overlord_Bridge.txt")

WATCHLIST = ["XAUUSD", "USOIL", "AUDUSD"]

print(f"--- INITIALISING OVERLORD NATIVE BRIDGE ---")
print(f"[INIT] Targeting Bridge File: {BRIDGE_FILE}")

def run_surveillance():
    while True:
        for symbol in WATCHLIST:
            # 1. Generate Signal (Simulated)
            vol_score = random.uniform(0.5, 4.0)
            
            if vol_score > 3.0:
                # 2. Formulate Message
                message = f"SIGNAL: {symbol} | Vol: {vol_score:.2f} | Action: CHECK_ENTRY"
                
                # 3. SEND ACROSS BRIDGE (Write to File)
                try:
                    with open(BRIDGE_FILE, "w") as f:
                        f.write(message)
                    print(f"[SENT] {message}")
                except Exception as e:
                    print(f"Bridge Busy: {e}")
                
        time.sleep(2)

if __name__ == "__main__":
    try:
        run_surveillance()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Stopped.")