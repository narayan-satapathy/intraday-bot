from openai import OpenAI
from config import OPENAI_API_KEY
import json
import re

client = OpenAI(api_key=OPENAI_API_KEY)

def ai_decide(snapshots: dict) -> dict:
    prompt = f"""
Return ONLY valid JSON.

We have 2 timeframe snapshots:

### 5-Minute
Price: {snapshots['5m']['price']}
EMA Fast: {snapshots['5m']['ema_fast']}
EMA Slow: {snapshots['5m']['ema_slow']}
RSI: {snapshots['5m']['rsi']}
MACD: {snapshots['5m']['macd']}
MACD Signal: {snapshots['5m']['macd_signal']}
MACD Hist: {snapshots['5m']['macd_hist']}
ATR: {snapshots['5m']['atr']}
Volume Spike: {snapshots['5m']['vol_spike']}
Momentum: {snapshots['5m']['momentum']}

### 15-Minute
Price: {snapshots['15m']['price']}
EMA Fast: {snapshots['15m']['ema_fast']}
EMA Slow: {snapshots['15m']['ema_slow']}
RSI: {snapshots['15m']['rsi']}
MACD: {snapshots['15m']['macd']}
MACD Signal: {snapshots['15m']['macd_signal']}
MACD Hist: {snapshots['15m']['macd_hist']}
ATR: {snapshots['15m']['atr']}
Volume Spike: {snapshots['15m']['vol_spike']}
Momentum: {snapshots['15m']['momentum']}

### Trend Scoring System (Improved)
For each timeframe:

EMA Trend:
- EMA Fast > EMA Slow → +2
- EMA Fast < EMA Slow → -2

MACD Trend:
- MACD > 0 → +1
- MACD < 0 → -1

RSI Trend:
- RSI > 60 → +1
- RSI < 40 → -1

Momentum:
- "up" → +1
- "down" → -1

Volume Spike:
- true → +1
- false → 0

Timeframe score range: -4 to +5  
Combined score range: -8 to +10

### Decision Logic
- Combined score ≥ +4 → BUY
- Combined score ≤ -4 → SELL
- Otherwise → HOLD

### Confidence
confidence = abs(combined_score) / 10

### Rationale Style (Important)
Write the rationale in **simple, human trader language**.
Avoid ALL abbreviations (EMA, MACD, RSI, ATR).
Avoid ALL technical jargon.
Do NOT mention indicator names.

Focus ONLY on:
- Price direction (up, down, stable)
- Strength or weakness of buyers/sellers
- Momentum (building or fading)
- Volume (strong or quiet)
- Overall sentiment (bullish, bearish, neutral)

Keep the explanation short, clear, and easy to read.

Return JSON:
{{
  "action": "BUY" | "SELL" | "HOLD",
  "confidence": number between 0 and 1,
  "rationale": string,
  "timeframe_summary": {{
      "5m": string,
      "15m": string
  }}
}}
"""

    try:
        completion = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        raw = completion.output_text

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return {
                "action": "HOLD",
                "confidence": 0.5,
                "rationale": "AI returned invalid JSON.",
                "timeframe_summary": {
                    "5m": "Invalid JSON",
                    "15m": "Invalid JSON"
                }
            }

        data = json.loads(match.group())

        return {
            "action": data.get("action", "HOLD"),
            "confidence": float(data.get("confidence", 0.5)),
            "rationale": data.get("rationale", "No rationale provided."),
            "timeframe_summary": data.get("timeframe_summary", {})
        }

    except Exception as e:
        return {
            "action": "HOLD",
            "confidence": 0.5,
            "rationale": f"AI crashed: {e}",
            "timeframe_summary": {
                "5m": "AI error",
                "15m": "AI error"
            }
        }
