# --- CONFIGURATION TEMPLATE ---
# RENAME THIS FILE TO: config.py
# ENTER YOUR OWN API CREDENTIALS BELOW

# 1. NETWORK SETTINGS (Localhost)
HOST = "127.0.0.1"
ZMQ_PORT = 5555

# 2. IG MARKETS CREDENTIALS (Required for Execution)
IG_USERNAME = "YOUR_USERNAME_HERE"
IG_PASSWORD = "YOUR_PASSWORD_HERE"
IG_API_KEY = "YOUR_API_KEY_HERE"
IG_ACC_TYPE = "DEMO"  # or LIVE

# 3. WATCHLIST
# "yahoo": The ticker symbol for Volume Data (Yahoo Finance)
# "ig_epic": The instrument ID for Execution (IG Markets)
WATCHLIST = {
    "GOLD": {
        "yahoo": "GC=F",    # Gold Futures (COMEX)
        "ig_epic": "CS.D.GOLD.TODAY.IP"
    },
    "BITCOIN": {
        "yahoo": "BTC-USD", # Bitcoin Spot
        "ig_epic": "CS.D.BITCOIN.TODAY.IP"
    }
}