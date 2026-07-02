import time
import streamlit as st
import pandas as pd

from config import DEFAULT_SYMBOLS
from data.market_data import get_candles
from analysis.technicals import add_technicals

import os
st.write("Working directory:", os.getcwd())

st.set_page_config(
    page_title="Intraday Bot",
    layout="wide",
)

st.title("📈 Intraday Stock Analysis Bot")

st.sidebar.header("Settings")

interval = st.sidebar.selectbox(
    "Select interval",
    ["5min", "15min"],
)

show_raw = st.sidebar.checkbox("Show raw candle data", value=True)
show_technicals = st.sidebar.checkbox("Show technical indicators", value=True)
show_ai = st.sidebar.checkbox("Show AI decision output", value=True)


for symbol in DEFAULT_SYMBOLS:
    st.markdown(f"## 🔹 {symbol}")

    candles = get_candles(symbol, interval)

    # show row count so you see it's not 0
    st.write(f"{symbol} candle rows: {len(candles)}")

    if candles is None or candles.empty:
        st.warning(f"No candle data for {symbol} ({interval}). Skipping.")
        st.markdown("---")
        time.sleep(0.2)
        continue

    candles = add_technicals(candles)

    if show_raw:
        st.subheader("Raw Candle Data")
        st.dataframe(candles.tail(20))

    if show_technicals:
        st.subheader("Technical Indicators (Latest)")
        latest = candles.tail(1)

        cols = []
        for c in ["macd", "macd_signal", "macd_hist", "rsi", "atr"]:
            if c in candles.columns:
                cols.append(c)

        if cols:
            st.write(latest[cols])
        else:
            st.info("No technicals available for this symbol/interval.")

    if show_ai and {"macd", "macd_signal", "rsi"}.issubset(candles.columns):
        st.subheader("AI Decision")

        latest = candles.tail(1).iloc[0]
        macd = latest["macd"]
        macd_signal = latest["macd_signal"]
        rsi = latest["rsi"]

        if macd > macd_signal and rsi < 70:
            decision = "BUY"
        elif macd < macd_signal and rsi > 30:
            decision = "SELL"
        else:
            decision = "HOLD"

        st.write(f"### Decision: **{decision}**")
    elif show_ai:
        st.info("Not enough technical data to make a decision.")

    st.markdown("---")
    time.sleep(0.2)
