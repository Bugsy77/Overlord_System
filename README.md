# Overlord: Hybrid Algorithmic Trading System

**Architecture:** Python Intelligence Engine (Brain) + cTrader Execution Module (Soldier)
**Connectivity:** TCP/IP Sockets (Localhost)
**Strategy:** Volume-Confirmed Trend Following (RVOL)

## Project Overview
Overlord is a hybrid trading architecture designed to bridge the gap between **External Market Data** (Futures Volume, Sentiment) and **Retail Execution** (Spot Forex/CFDs). 

Unlike standard bots that rely solely on broker-provided price feeds, Overlord uses a "Brain" (Python) to validate moves against the "Truth" of Exchange Volume (e.g., CME Futures) before authorizing the "Soldier" (cTrader) to execute.

## System Architecture

```text
 [ DATA SOURCES ]           [ INTELLIGENCE ]            [ EXECUTION ]

 +----------------+       +------------------+       +-------------------+
 |  Yahoo Finance | ----> |   PYTHON BRAIN   | ----> |    IG MARKETS     |
 | (Futures Vol)  |       | (Fat_Brain.py)   |       |    (REST API)     |
 +----------------+       |                  |       +-------------------+
                          | 1. Vol Check(RVOL)|                ^
 +----------------+       | 2. Sentiment NLP |                 |
 |   RSS / News   | ----> | 3. Risk Engine   |                 |
 +----------------+       +--------+---------+                 |
                                   | (JSON / TCP Socket)       |
                                   v                           |
                          +------------------+                 |
                          |  CTRADER SOLDIER |                 |
                          | (C# cBot / .NET) |                 |
                          |                  |                 |
                          | 1. Thread-Safe   |                 |
                          | 2. Stop & Reverse|                 |
                          | 3. EXECUTES SPOT | ----------------+
                          +------------------+      (Hedging Logic)