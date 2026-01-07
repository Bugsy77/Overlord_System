# Overlord: Hybrid Algorithmic Trading System

**Architecture:** Python Intelligence Engine (Brain) + cTrader Execution Module (Soldier)
**Connectivity:** TCP/IP Sockets (Localhost) & REST API
**Strategy:** Volume-Confirmed Trend Following (RVOL)

## Project Overview

Overlord is a hybrid trading architecture designed to bridge the gap between **External Market Data** (Futures Volume, Sentiment) and **Retail Execution**.

It acts as a central "Intelligence Hub" that routes trades to the optimal broker based on the required execution method:

1. **Route A (IC Markets):** Uses a **cTrader Bridge** for high-frequency Spot execution (requires Soldier Bot).

2. **Route B (IG Markets):** Uses **Direct Python API** for CFD execution (bypassing trading platforms).

## System Architecture

    [ STEP 1: DATA INGEST ]           [ STEP 2: LOGIC ENGINE ]           [ STEP 3: EXECUTION ]
    +---------------------+           +----------------------+           +-------------------+
    |  Yahoo Finance API  | --------> |    PYTHON BRAIN      | --------> |  cTrader SOLDIER  |
    |  (Futures Volume)   |           |   (RVOL Calculation) |   TCP     |   (IC Markets)    |
    +---------------------+           +----------------------+           +-------------------+
                                                 |
                                                 |  (REST API)
                                                 v
                                      +----------------------+
                                      |   IG MARKETS API     |
                                      |   (Direct Python)    |
                                      +----------------------+

## Key Features

### 1. Volume "Truth" Verification

The system calculates **Relative Volume (RVOL)** using external data feeds.

* **The Logic:** If Spot Price moves but Futures Volume is low (< 1.2x average), the system identifies a "Fakeout" and holds position.

### 2. Multi-Broker Routing

The Python Brain is agnostic to the execution venue.

* **IC Markets (cTrader):** Selected for strategies requiring millisecond latency and C# hedging.
* **IG Markets (REST):** Selected for assets where Python direct execution is preferred.

### 3. Failsafe Risk Management

* **Dynamic Risk:** Stop Loss is calculated as `2.0 * ATR` (Average True Range).
* **Data Safety:** Python acts as a firewall; if data feeds fail, execution modules default to hard-coded safety stops.

## Technical Stack

* **Python 3.10+:** `pandas`, `yfinance`, `requests` (IG API), `socket`
* **C# / .NET:** `System.Net.Sockets`, `cAlgo.API` (cTrader)

---

Developed by Bugsy77 - 2026
