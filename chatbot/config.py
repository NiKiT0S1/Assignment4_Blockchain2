import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# API Keys
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY", "")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")

# LLM Settings
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Application settings
TOP_COINS_LIMIT = int(os.getenv("TOP_COINS_LIMIT", "50"))
DATA_CACHE_TIME = int(os.getenv("DATA_CACHE_TIME", "300"))  # 5 minutes

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"