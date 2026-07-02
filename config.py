import os
from dotenv import load_dotenv

# Load .env from project root
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")

DEFAULT_INTERVAL = "5min"
DEFAULT_SYMBOLS = ["INTC","TSLA","NVDA", "ORCL", "SPCX","AMZN", "NKE","AVGO","GIB","NDAQ"]
