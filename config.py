"""
CONFIGURATION & SECRETS
KEEP THIS FILE PRIVATE. DO NOT UPLOAD TO GITHUB WITH REAL KEYS.
"""

# IG MARKETS CREDENTIALS (DEMO ACCOUNT)
IG_USERNAME = "YOUR_USERNAME"
IG_PASSWORD = "YOUR_PASSWORD"
IG_API_KEY = "YOUR_API_KEY"
IG_ACC_TYPE = "DEMO" # Switch to "LIVE" only when ready

# SYSTEM SETTINGS
ZMQ_PORT = 5555
HOST = "127.0.0.1"

# WATCHLIST (Yahoo Ticker : IG Epic)
# You need the specific "EPIC" code from IG for the assets you want to trade.
# Gold (Spot) usually looks like 'CS.D.CFD.GOLD.IP' on IG.
WATCHLIST = {
    "XAUUSD": {
        "yahoo": "GC=F", 
        "ig_epic": "CS.D.CFD.GOLD.IP" 
    }
}