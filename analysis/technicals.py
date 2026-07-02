import pandas as pd
import pandas_ta as ta


def add_technicals(candles: pd.DataFrame) -> pd.DataFrame:
    if candles is None or candles.empty:
        return candles

    if "close" not in candles.columns:
        return candles

    # MACD
    macd = ta.macd(candles["close"])
    if macd is not None and not macd.empty:
        candles["macd"] = macd["MACD_12_26_9"]
        candles["macd_signal"] = macd["MACDs_12_26_9"]
        candles["macd_hist"] = macd["MACDh_12_26_9"]

    # RSI
    rsi = ta.rsi(candles["close"])
    if rsi is not None and not rsi.empty:
        candles["rsi"] = rsi

    # ATR
    if {"high", "low", "close"}.issubset(candles.columns):
        atr = ta.atr(candles["high"], candles["low"], candles["close"])
        if atr is not None and not atr.empty:
            candles["atr"] = atr

    return candles
