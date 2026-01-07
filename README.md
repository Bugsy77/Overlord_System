# Overlord: Hybrid Algorithmic Trading System

**Architecture:** Python Intelligence Engine (Brain) + cTrader Execution Module (Soldier)
**Connectivity:** TCP/IP Sockets (Localhost) & REST API
**Strategy:** Volume-Confirmed Trend Following (RVOL)

## Project Overview
Overlord is a hybrid trading architecture designed to bridge the gap between **External Market Data** (Futures Volume, Sentiment) and **Retail Execution**.

Unlike standard bots, Overlord acts as a central "Intelligence Hub" that can route trade instructions to different brokers based on the asset class or strategy:
1.  **cTrader (IC Markets):** For high-frequency Spot Forex/Metals execution via a custom C# Bridge.
2.  **IG Markets:** For direct execution via Python REST API (bypassing trading platforms).

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
        E -->|Route A: TCP Socket| G[cTrader Soldier]
        G -->|IC MARKETS| I[Spot Execution]
        
        E -.->|Route B: REST API| J[IG MARKETS]
        J -.->|Direct Python| K[CFD Execution]
    end

    %% Professional High-Contrast Color Scheme
    style B fill:#2b2b2b,stroke:#00ff41,stroke-width:2px,color:#fff
    style G fill:#003366,stroke:#00bfff,stroke-width:2px,color:#fff
    style J fill:#440000,stroke:#ff0000,stroke-width:2px,color:#fff