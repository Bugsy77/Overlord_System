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

```mermaid
graph TD
    subgraph DATA_INGEST [Step 1: Intelligence Gathering]
        A[Yahoo Finance] -->|Volume Data| B(Python Brain)
        C[News Sentiment] -->|NLP Score| B
    end

    subgraph LOGIC_ENGINE [Step 2: Decision Making]
        B -->|Calc RVOL & Trend| D{Signal Valid?}
        D -- YES --> E[Generate Trade Signal]
        D -- NO --> F[Log 'Fakeout' & Wait]
    end

    subgraph EXECUTION [Step 3: Dual Execution Routing]
        %% Route A: The Soldier Path
        E -->|TCP Socket Signal| G[cTrader Soldier]
        G -->|Execute Order| I["IC MARKETS (Spot)"]

        %% Route B: The Direct Path
        E -.->|Python REST API| J["IG MARKETS (CFD)"]
    end

    %% Professional High-Contrast Color Scheme
    style B fill:#2b2b2b,stroke:#00ff41,stroke-width:2px,color:#fff
    style G fill:#003366,stroke:#00bfff,stroke-width:2px,color:#fff
    style I fill:#003366,stroke:#fff,stroke-width:1px,color:#fff
    style J fill:#440000,stroke:#ff0000,stroke-width:2px,color:#fff

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
*Developed by Bugsy77 - 2026*