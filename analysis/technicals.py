import pandas as pd
import pandas_ta as ta

def add_technicals(candles: pd.DataFrame) -> pd.DataFrame:
    candles = candles.copy()

    candles["ema_fast"] = ta.ema(candles["close"], length=9)
    candles["ema_slow"] = ta.ema(candles["close"], length=21)

    candles["rsi"] = ta.rsi(candles["close"], length=14)

    macd = ta.macd(candles["close"], fast=12, slow=26, signal=9)
    candles["macd"] = macd["MACD_12_26_9"]
    candles["macd_signal"] = macd["MACDs_12_26_9"]
    candles["macd_hist"] = macd["MACDh_12_26_9"]

    candles["atr"] = ta.atr(
        candles["high"], candles["low"], candles["close"], length=14
    )

    vol_ma = candles["volume"].rolling(20).mean()
    candles["vol_spike"] = candles["volume"] > (vol_ma * 1.5)

    candles["momentum"] = candles["close"].diff()
    candles["momentum_dir"] = candles["momentum"].apply(
        lambda x: "up" if x > 0 else ("down" if x < 0 else "flat")
    )

    return candles

def latest_snapshot(symbol: str, candles: pd.DataFrame) -> dict:
    row = candles.iloc[-1]

    return {
        "symbol": symbol,
        "price": row["close"],
        "ema_fast": row["ema_fast"],
        "ema_slow": row["ema_slow"],
        "rsi": row["rsi"],
        "macd": row["macd"],
        "macd_signal": row["macd_signal"],
        "macd_hist": row["macd_hist"],
        "atr": row["atr"],
        "vol_spike": bool(row["vol_spike"]),
        "momentum": row["momentum_dir"],
    }
