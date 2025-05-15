import requests
import os
from datetime import datetime
import time
from typing import Dict, List, Any
import feedparser
from bs4 import BeautifulSoup

# API Keys - should be set as environment variables
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY", "")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "")

# Cache to store data and minimize API calls
CACHE = {}
CACHE_EXPIRY = {
    "news": 5 * 60,  # 5 minutes for news
    "market": 2 * 60,  # 2 minutes for market data
    "price": 30  # 30 seconds for price data
}


def fetch_crypto_news(coin: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch news for a specific cryptocurrency from Coindesk RSS feed"""
    cache_key = f"news_{coin}"

    # Check cache first
    if cache_key in CACHE and (time.time() - CACHE[cache_key]["timestamp"]) < CACHE_EXPIRY["news"]:
        return CACHE[cache_key]["data"]

    try:
        # Get the symbol and name for the coin
        market_data = fetch_market_data(coin)
        if not market_data or "symbol" not in market_data:
            print(f"Could not get market data for {coin}")
            return []
        
        symbol = market_data["symbol"]
        name = market_data["name"]
        
        # Fetch RSS feed from Coindesk
        feed_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
        print(f"Fetching RSS feed from {feed_url}")
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            print("No entries found in RSS feed")
            return []
        
        # Process news data
        news_items = []
        keywords = [symbol.lower(), name.lower()]
        
        for entry in feed.entries:
            if len(news_items) >= limit:
                break
                
            # Check if the entry is related to our coin
            title_lower = entry.title.lower()
            description_lower = entry.description.lower()
            
            if any(keyword in title_lower or keyword in description_lower for keyword in keywords):
                # Extract clean text from HTML description
                soup = BeautifulSoup(entry.description, 'html.parser')
                description = soup.get_text()
                
                news_items.append({
                    "title": entry.title,
                    "url": entry.link,
                    "source": "Coindesk",
                    "published_at": entry.published,
                    "description": description
                })

        print(f"Found {len(news_items)} news items for {coin}")
        
        # Update cache
        CACHE[cache_key] = {
            "data": news_items,
            "timestamp": time.time()
        }

        return news_items
    except Exception as e:
        print(f"Error fetching news for {coin}: {str(e)}")
        return []


def get_coinmarketcap_id(coin: str) -> str:
    """Get CoinMarketCap ID for a given coin"""
    cache_key = f"cmc_id_{coin}"

    # Check cache first
    if cache_key in CACHE and (time.time() - CACHE[cache_key]["timestamp"]) < CACHE_EXPIRY["market"]:
        return CACHE[cache_key]["data"]

    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
        headers = {
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        coin_lower = coin.lower()
        for crypto in data.get("data", []):
            if (crypto["name"].lower() == coin_lower or
                    crypto["symbol"].lower() == coin_lower):
                # Update cache
                CACHE[cache_key] = {
                    "data": str(crypto["id"]),
                    "timestamp": time.time()
                }
                return str(crypto["id"])

        return ""
    except Exception as e:
        print(f"Error fetching CoinMarketCap ID for {coin}: {e}")
        return ""


def fetch_market_data(coin: str) -> Dict[str, Any]:
    """Fetch market data for a specific cryptocurrency from CoinGecko API"""
    cache_key = f"market_{coin}"

    # Check cache first
    if cache_key in CACHE and (time.time() - CACHE[cache_key]["timestamp"]) < CACHE_EXPIRY["market"]:
        return CACHE[cache_key]["data"]

    try:
        url = f"https://api.coingecko.com/api/v3/coins/{get_coingecko_id(coin)}"
        if COINGECKO_API_KEY:
            url += f"?x_cg_api_key={COINGECKO_API_KEY}"

        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Process market data
        market_data = {
            "name": data["name"],
            "symbol": data["symbol"].upper(),
            "market_cap_rank": data.get("market_cap_rank", "N/A"),
            "market_cap_usd": data.get("market_data", {}).get("market_cap", {}).get("usd", "N/A"),
            "volume_24h": data.get("market_data", {}).get("total_volume", {}).get("usd", "N/A"),
            "price_change_24h": data.get("market_data", {}).get("price_change_percentage_24h", "N/A"),
            "description": data.get("description", {}).get("en", "").split(".")[0] + "." if data.get("description",
                                                                                                     {}).get(
                "en") else "",
            "homepage": data.get("links", {}).get("homepage", [""])[0]
        }

        # Update cache
        CACHE[cache_key] = {
            "data": market_data,
            "timestamp": time.time()
        }

        return market_data
    except Exception as e:
        print(f"Error fetching market data for {coin}: {e}")
        return {}


def fetch_price_data(coin: str) -> Dict[str, Any]:
    """Fetch current price data for a specific cryptocurrency from Binance API"""
    cache_key = f"price_{coin}"

    # Check cache first
    if cache_key in CACHE and (time.time() - CACHE[cache_key]["timestamp"]) < CACHE_EXPIRY["price"]:
        return CACHE[cache_key]["data"]

    # Convert coin name to Binance symbol
    symbol_mapping = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "binancecoin": "BNB",
        "solana": "SOL",
        "ripple": "XRP",
        "cardano": "ADA",
        "dogecoin": "DOGE",
        "polkadot": "DOT",
        "avalanche-2": "AVAX",
        "chainlink": "LINK",
        "matic-network": "MATIC",
        "shiba-inu": "SHIB"
    }

    # Get the symbol from mapping or use the coin's symbol from market data
    symbol = symbol_mapping.get(coin.lower(), "")
    if not symbol:
        # If not in mapping, try to get from market data
        market_data = fetch_market_data(coin)
        if market_data and "symbol" in market_data:
            symbol = market_data["symbol"]
        else:
            return {}

    symbol = f"{symbol}USDT"

    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        price_data = response.json()

        url_24h = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response_24h = requests.get(url_24h)
        response_24h.raise_for_status()
        data_24h = response_24h.json()

        price_info = {
            "symbol": symbol,
            "price": float(price_data["price"]),
            "price_change_percent": float(data_24h.get("priceChangePercent", 0)),
            "high_24h": float(data_24h.get("highPrice", 0)),
            "low_24h": float(data_24h.get("lowPrice", 0)),
            "volume_24h": float(data_24h.get("volume", 0))
        }

        # Update cache
        CACHE[cache_key] = {
            "data": price_info,
            "timestamp": time.time()
        }

        return price_info
    except Exception as e:
        print(f"Error fetching price data for {symbol}: {e}")
        return {}


def get_coingecko_id(coin: str) -> str:
    """Convert common coin names/symbols to CoinGecko IDs"""
    coin = coin.lower()

    # Common mappings
    mapping = {
        "btc": "bitcoin",
        "bitcoin": "bitcoin",
        "eth": "ethereum",
        "ethereum": "ethereum",
        "bnb": "binancecoin",
        "sol": "solana",
        "solana": "solana",
        "xrp": "ripple",
        "ada": "cardano",
        "cardano": "cardano",
        "doge": "dogecoin",
        "dogecoin": "dogecoin",
        "dot": "polkadot",
        "polkadot": "polkadot",
        "avax": "avalanche-2",
        "avalanche": "avalanche-2",
        "link": "chainlink",
        "chainlink": "chainlink",
        "matic": "matic-network",
        "polygon": "matic-network",
        "shib": "shiba-inu",
        "shiba inu": "shiba-inu"
    }

    return mapping.get(coin, coin)


def get_top_coins(limit: int = 50) -> List[Dict[str, str]]:
    """Get top cryptocurrencies by market cap from CoinGecko"""
    cache_key = "top_coins"

    # Check cache first
    if cache_key in CACHE and (time.time() - CACHE[cache_key]["timestamp"]) < CACHE_EXPIRY["market"]:
        return CACHE[cache_key]["data"]

    try:
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1"
        if COINGECKO_API_KEY:
            url += f"&x_cg_api_key={COINGECKO_API_KEY}"

        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        coins = [{
            "id": coin["id"],
            "symbol": coin["symbol"],
            "name": coin["name"],
            "market_cap_rank": coin["market_cap_rank"]
        } for coin in data]

        # Update cache
        CACHE[cache_key] = {
            "data": coins,
            "timestamp": time.time()
        }

        return coins
    except Exception as e:
        print(f"Error fetching top coins: {e}")
        return []


def identify_coin(query: str) -> str:
    """Extract cryptocurrency from user query"""
    query = query.lower()

    # Get top coins
    top_coins = get_top_coins()

    # Check for coin mentions in query
    for coin in top_coins:
        if coin["id"].lower() in query or coin["symbol"].lower() in query or coin["name"].lower() in query:
            return coin["id"]

    # Check common names that might differ from official names
    common_names = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "xrp": "ripple",
        "bnb": "binancecoin"
    }

    for symbol, coin_id in common_names.items():
        if symbol in query:
            return coin_id

    return ""


def get_aggregated_data(coin: str) -> Dict[str, Any]:
    """Aggregate data from multiple sources for a specific cryptocurrency"""
    market_data = fetch_market_data(coin)
    price_data = fetch_price_data(coin)
    news_data = fetch_crypto_news(coin)

    return {
        "market_data": market_data,
        "price_data": price_data,
        "news_data": news_data
    }