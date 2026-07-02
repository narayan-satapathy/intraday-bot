from config import DEFAULT_SYMBOLS
from data.market_data import get_candles
from analysis.technicals import add_technicals, latest_snapshot
from analysis.ai_decision import ai_decide

def analyze_symbol(symbol: str):
    timeframes = {
        "5m": "5min",
        "15m": "15min"
    }

    snapshots = {}

    for label, interval in timeframes.items():
        candles = get_candles(symbol, interval)
        candles = add_technicals(candles)
        snapshots[label] = latest_snapshot(symbol, candles)

    decision = ai_decide(snapshots)

    return {
        "symbol": symbol,
        "decision": decision,
        "snapshots": snapshots
    }

def main():
    print("\n=== Intraday AI Multi‑Timeframe Signals (5m + 15m) ===\n")

    for symbol in DEFAULT_SYMBOLS:
        result = analyze_symbol(symbol)
        d = result["decision"]
        tf = d.get("timeframe_summary", {})

        print(f"{result['symbol']}: {d['action']} (confidence {d['confidence']:.2f})")
        print(f"Reason: {d['rationale']}\n")

        print("5m:", tf.get("5m", "N/A"))
        print("15m:", tf.get("15m", "N/A"))
        print("-" * 50)

if __name__ == "__main__":
    main()
