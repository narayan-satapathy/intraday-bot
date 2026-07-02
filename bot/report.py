# bot/report.py
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def explain_signal(symbol: str, signal: dict, latest_row, sentiment: dict) -> str:
    prompt = f"""
You are an intraday trading assistant.

Symbol: {symbol}
Technical snapshot:
- Price: {latest_row['close']}
- RSI: {latest_row['rsi']}
- MACD: {latest_row['macd']}
- EMA fast: {latest_row['ema_fast']}
- EMA slow: {latest_row['ema_slow']}

News sentiment:
- Sentiment: {sentiment.get('sentiment')}
- Score: {sentiment.get('score')}
- Rationale: {sentiment.get('rationale')}

System decision: {signal['action']} with confidence {signal['confidence']}.

Explain in 3–5 bullet points why this decision makes sense, and mention key risks.
    """

    completion = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    # simple text output
    return completion.output_text
