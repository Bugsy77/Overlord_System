using System;
using System.Linq;
using cAlgo.API;
using cAlgo.API.Internals;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Globalization;

namespace cAlgo.Robots
{
    [Robot(TimeZone = TimeZones.UTC, AccessRights = AccessRights.FullAccess)]
    public class Overlord_Sergeant : Robot
    {
        private bool _isRunning = true;
        private TcpClient _client;
        private NetworkStream _stream;

        private readonly object _stateLock = new object();
        private string _signal = "HOLD";
        private double _slPrice = 0;
        private double _tpPrice = 0;

        protected override void OnStart()
        {
            Print("--- OVERLORD SERGEANT (REVERSAL MODE) ONLINE ---");
            var thread = new Thread(StartListening);
            thread.IsBackground = true;
            thread.Start();
        }

        protected override void OnTick()
        {
            // 1. SAFELY READ SIGNAL
            string localSignal;
            double localSl;
            double localTp;

            lock (_stateLock)
            {
                localSignal = _signal;
                localSl = _slPrice;
                localTp = _tpPrice;
            }

            if (localSignal == "HOLD") return;

            // 2. CHECK CURRENT POSITIONS
            var longPosition = Positions.Find("Overlord", SymbolName, TradeType.Buy);
            var shortPosition = Positions.Find("Overlord", SymbolName, TradeType.Sell);

            // 3. LOGIC: STOP & REVERSE
            // If we are told to BUY...
            if (localSignal == "BUY")
            {
                // ...and we hold a SELL, close it first!
                if (shortPosition != null)
                {
                    Print("[REVERSAL] Closing Short to go Long!");
                    ClosePosition(shortPosition);
                }

                // Only open if we don't already have a Buy
                if (longPosition == null)
                {
                    double slPips = CalculatePips(localSl, TradeType.Buy);
                    double tpPips = CalculatePips(localTp, TradeType.Buy);
                    ExecuteMarketOrder(TradeType.Buy, SymbolName, Symbol.VolumeInUnitsMin, "Overlord", slPips, tpPips);
                }
            }
            // If we are told to SELL...
            else if (localSignal == "SELL")
            {
                // ...and we hold a BUY, close it first!
                if (longPosition != null)
                {
                    Print("[REVERSAL] Closing Long to go Short!");
                    ClosePosition(longPosition);
                }

                // Only open if we don't already have a Sell
                if (shortPosition == null)
                {
                    double slPips = CalculatePips(localSl, TradeType.Sell);
                    double tpPips = CalculatePips(localTp, TradeType.Sell);
                    ExecuteMarketOrder(TradeType.Sell, SymbolName, Symbol.VolumeInUnitsMin, "Overlord", slPips, tpPips);
                }
            }

            // 4. RESET SIGNAL
            lock (_stateLock)
            {
                _signal = "HOLD"; 
            }
        }

        // Helper to calculate Pips safely
        private double CalculatePips(double priceLevel, TradeType type)
        {
            if (priceLevel <= 0 || double.IsNaN(priceLevel)) return 20; // Default

            double pips = 0;
            if (type == TradeType.Buy)
                pips = Math.Abs(Symbol.Ask - priceLevel) / Symbol.PipSize;
            else
                pips = Math.Abs(Symbol.Bid - priceLevel) / Symbol.PipSize;

            if (pips <= 0.1 || pips > 5000) return 20; // Failsafe
            return Math.Round(pips, 1);
        }

        private void StartListening()
        {
            while (_isRunning)
            {
                try
                {
                    if (_client == null || !_client.Connected)
                    {
                        Print("[NET] Connecting...");
                        _client = new TcpClient("127.0.0.1", 5555);
                        _stream = _client.GetStream();
                        Print("[NET] Connected!");
                    }

                    if (_stream.DataAvailable)
                    {
                        byte[] data = new byte[1024];
                        int bytes = _stream.Read(data, 0, data.Length);
                        string json = Encoding.UTF8.GetString(data, 0, bytes);

                        string newSignal = ExtractValue(json, "signal");
                        string slStr = ExtractValue(json, "sl");
                        string tpStr = ExtractValue(json, "tp");

                        double sl = ParseDouble(slStr);
                        double tp = ParseDouble(tpStr);

                        if (newSignal == "BUY" || newSignal == "SELL")
                        {
                            lock (_stateLock)
                            {
                                _slPrice = sl;
                                _tpPrice = tp;
                                _signal = newSignal;
                            }
                            Print($"[INTEL] Signal: {newSignal}");
                        }
                    }
                }
                catch { Thread.Sleep(3000); }
                Thread.Sleep(100); 
            }
        }

        private string ExtractValue(string json, string key)
        {
            try 
            {
                string searchKey = $"\"{key}\":"; 
                int startIndex = json.IndexOf(searchKey);
                if (startIndex == -1) return "0";
                startIndex += searchKey.Length;
                int endIndex = json.IndexOf(",", startIndex);
                if (endIndex == -1) endIndex = json.IndexOf("}", startIndex);
                if (endIndex == -1) return "0";
                return json.Substring(startIndex, endIndex - startIndex).Replace("\"", "").Trim(); 
            }
            catch { return "0"; }
        }

        private double ParseDouble(string value)
        {
             double result;
             if (double.TryParse(value, NumberStyles.Any, CultureInfo.InvariantCulture, out result)) return result;
             return 0;
        }

        protected override void OnStop()
        {
            _isRunning = false;
            if (_client != null) _client.Close();
        }
    }
}