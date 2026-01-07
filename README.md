# Overlord: Hybrid Algorithmic Trading System

**Architecture:** Python Intelligence Engine (Brain) + cTrader Execution Module (Soldier)
**Connectivity:** TCP/IP Sockets (Localhost)
**Strategy:** Volume-Confirmed Trend Following (RVOL)

## Project Overview
Overlord is a hybrid trading architecture designed to bridge the gap between **External Market Data** (Futures Volume, Sentiment) and **Retail Execution** (Spot Forex/CFDs).

Unlike standard bots that rely solely on broker-provided price feeds, Overlord uses a "Brain" (Python) to validate moves against the "Truth" of Exchange Volume (e.g., CME Futures) before authorizing the "Soldier" (cTrader) to execute.

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

    subgraph EXECUTION [Step 3: Execution Bridge]
        E -->|TCP Socket JSON| G[cTrader Soldier]
        G -->|Manage Risk| H[IG Markets / Spot]
        H -->|Feedback Loop| G
    end

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px