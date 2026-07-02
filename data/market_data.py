import requests
import pandas as pd
from config import TWELVEDATA_API_KEY, DEFAULT_INTERVAL

BASE_URL = "https://api.twelvedata.com/time_series"

def get_candles(symbol: str, interval: str):
    params = {
        "symbol": symbol,
        "interval": interval,
        "apikey": TWELVEDATA_API_KEY,
        "outputsize": 100
    }

    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json()

    candles = pd.DataFrame(data["values"])
    candles["datetime"] = pd.to_datetime(candles["datetime"])
    candles = candles.sort_values("datetime")
    candles = candles.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    })

    return candles
