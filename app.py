import streamlit as st

from config import DEFAULT_SYMBOLS
from data.market_data import get_candles
from analysis.technicals import add_technicals, latest_snapshot
from analysis.ai_decision import ai_decide

st.set_page_config(page_title="Intraday stock analysis", layout="wide")

st.title("📈 Intraday stock analysis using market data and AI")
st.caption("Symbols: " + ", ".join(DEFAULT_SYMBOLS))


# --- Clean Summary Function ---
def clean_summary(s):
    price = s["price"]

    # Trend
    trend = "Bullish" if s["ema_fast"] > s["ema_slow"] else "Bearish"
    trend_icon = "📈" if trend == "Bullish" else "📉"

    # Momentum
    momentum = "Improving" if s["momentum"] == "up" else "Cooling"
    momentum_icon = "🔥" if s["momentum"] == "up" else "🧊"

    # Volume
    volume = "High" if s["vol_spike"] else "Normal"
    volume_icon = "📊" if s["vol_spike"] else "🔹"

    # RSI interpretation
    if s["rsi"] > 60:
        rsi = "Strong"
    elif s["rsi"] > 50:
        rsi = "Improving"
    elif s["rsi"] < 40:
        rsi = "Weak"
    else:
        rsi = "Neutral"

    return (
        f"Price: ${price:.2f} | "
        f"{trend_icon} {trend} | "
        f"{momentum_icon} Momentum {momentum} | "
        f"{volume_icon} Volume {volume} | "
        f"RSI {rsi}"
    )


# --- UI Button ---
refresh = st.button("Run Analysis")


# --- Main Logic ---
if refresh:
    for symbol in DEFAULT_SYMBOLS:
        st.header(symbol)

        # Fetch 5m + 15m data
        snapshots = {}
        for tf, interval in {"5m": "5min", "15m": "15min"}.items():
            candles = get_candles(symbol, interval)
            candles = add_technicals(candles)
            snapshots[tf] = latest_snapshot(symbol, candles)

        # AI Decision
        decision = ai_decide(snapshots)
        action = decision["action"]
        confidence = decision["confidence"]

        # Color-coded action
        if action == "BUY":
            st.success(f"BUY Signal (confidence {confidence:.2f})")
        elif action == "SELL":
            st.error(f"SELL Signal (confidence {confidence:.2f})")
        else:
            st.warning(f"HOLD (confidence {confidence:.2f})")

        # Clean summaries
        st.subheader("5m Summary")
        st.write(clean_summary(snapshots["5m"]))

        st.subheader("15m Summary")
        st.write(clean_summary(snapshots["15m"]))

        # AI rationale (clean)
        st.subheader("AI Rationale")
        st.write(decision["rationale"])

        st.divider()

else:
    st.info("Click 'Run Analysis' to fetch fresh signals.")
