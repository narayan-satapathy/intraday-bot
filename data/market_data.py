import yfinance as yf
import pandas as pd
import datetime as dt


def get_candles(symbol: str, interval: str) -> pd.DataFrame:
    interval_map = {"5min": "5m", "15min": "15m"}
    yf_interval = interval_map.get(interval)

    end = dt.datetime.now(dt.timezone.utc)
    start = end - dt.timedelta(days=5)

    df = yf.download(
        tickers=symbol,
        interval=yf_interval,
        start=start,
        end=end,
        prepost=False,
        progress=False,
    )

    if df is None or df.empty:
        return pd.DataFrame()

    # Flatten ALL multi-index levels
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(level) for level in col if level not in ("", None)])
            for col in df.columns
        ]

    # Build rename map dynamically based on actual columns
    rename_map = {}

    # Case 1: Close_INTC → close
    rename_map[f"Close_{symbol}"] = "close"
    rename_map[f"High_{symbol}"] = "high"
    rename_map[f"Low_{symbol}"] = "low"
    rename_map[f"Open_{symbol}"] = "open"
    rename_map[f"Volume_{symbol}"] = "volume"

    # Case 2: INTC_Close → close
    rename_map[f"{symbol}_Close"] = "close"
    rename_map[f"{symbol}_High"] = "high"
    rename_map[f"{symbol}_Low"] = "low"
    rename_map[f"{symbol}_Open"] = "open"
    rename_map[f"{symbol}_Volume"] = "volume"

    # Case 3: Price_Close → close
    rename_map["Price_Close"] = "close"
    rename_map["Price_High"] = "high"
    rename_map["Price_Low"] = "low"
    rename_map["Price_Open"] = "open"
    rename_map["Price_Volume"] = "volume"

    # Case 4: Open → open
    rename_map["Open"] = "open"
    rename_map["High"] = "high"
    rename_map["Low"] = "low"
    rename_map["Close"] = "close"
    rename_map["Volume"] = "volume"

    # Apply rename
    df.rename(columns=rename_map, inplace=True)

    # Remove duplicates
    df = df.loc[:, ~df.columns.duplicated()]

    df.reset_index(inplace=True)

    # Final validation
    required = {"open", "high", "low", "close", "volume"}
    if not required.issubset(df.columns):
        print("❌ Columns still wrong:", df.columns)
        return pd.DataFrame()

    return df
