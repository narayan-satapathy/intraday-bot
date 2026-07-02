Code
# Intraday AI Multi‑Timeframe Trading Bot

A lightweight intraday trading assistant that analyzes multiple timeframes (5m + 15m) using technical signals and AI‑generated reasoning.  
The dashboard is built with Streamlit and provides clean, human‑friendly summaries instead of technical jargon.

---

## 🚀 Features

- Multi‑timeframe analysis (5m + 15m)
- Clean trader‑friendly summaries (trend, momentum, volume, price)
- AI‑generated BUY / SELL / HOLD decisions
- Confidence scoring
- Support for multiple symbols
- Simple Streamlit dashboard UI
- Modular backend (market data, technicals, AI decision engine)

---

## 📂 Project Structure

Intraday-bot/
│
├── app.py                 # Streamlit dashboard (frontend)
├── main.py                # Optional CLI runner
│
├── data/
│   └── market_data.py     # Fetches candles from TwelveData
│
├── analysis/
│   ├── technicals.py      # Computes indicators
│   └── ai_decision.py     # AI scoring + clean rationale
│
└── config.py              # API keys + symbol list

Code

---

## 🖥️ Running the Dashboard

Activate your virtual environment:

source venv/bin/activate

Code

Run Streamlit:

streamlit run app.py

Code

Open the browser at:

http://localhost:8501

Code

---

## ⚙️ Configuration

Edit `config.py` to add or remove symbols:

```python
DEFAULT_SYMBOLS = [
    "AAPL", "MSFT", "TSLA",
    "NVDA", "AMZN", "META",
    "VT", "URTH"
]
Add your TwelveData API key:

python
OPENAI_API_KEY = "your-key"
🧠 AI Decision Engine
The AI rationale is intentionally simple:

No abbreviations (no EMA, MACD, RSI)

No technical jargon

Human‑friendly explanation

Focus on price action, momentum, volume, sentiment

The AI returns:

json
{
  "action": "BUY | SELL | HOLD",
  "confidence": 0.0 - 1.0,
  "rationale": "Clean human-friendly explanation",
  "timeframe_summary": {
    "5m": "Short summary",
    "15m": "Short summary"
  }
}
📦 Installation
Code
pip install -r requirements.txt
📝 Notes
Some non‑US symbols (e.g., VWCE) may not be supported by TwelveData.

For European ETFs, consider switching to Yahoo Finance.