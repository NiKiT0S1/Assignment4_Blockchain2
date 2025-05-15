import os
import json

# Set the model name - can be changed to your preferred model
OLLAMA_MODEL = "llama3"


def generate_answer(question, data):
    """
    Generate a comprehensive answer using the LLM based on
    cryptocurrency data from different sources

    Parameters:
    - question: User's query about cryptocurrency
    - data: Dictionary containing market data, price data, and news

    Returns:
    - Generated answer from the LLM and sources information
    """
    # Extract relevant information from data
    market_data = data.get("market_data", {})
    price_data = data.get("price_data", {})
    news = data.get("news_data", [])

    # Format market data for the prompt
    market_info = ""
    if market_data:
        market_info = f"""
Name: {market_data.get('name', 'N/A')}
Symbol: {market_data.get('symbol', 'N/A')}
Market Cap Rank: #{market_data.get('market_cap_rank', 'N/A')}
Market Cap: ${format_number(market_data.get('market_cap_usd', 0))}
24h Price Change: {market_data.get('price_change_24h', 'N/A')}%
Description: {market_data.get('description', 'N/A')}
Website: {market_data.get('homepage', 'N/A')}
"""

    # Format price data for the prompt
    price_info = ""
    if price_data:
        price_info = f"""
Current Price: ${float(price_data.get('price', 0)):.2f}
24h Price Change: {price_data.get('price_change_percent', 'N/A')}%
24h High: ${price_data.get('high_24h', 'N/A')}
24h Low: ${price_data.get('low_24h', 'N/A')}
24h Volume: ${format_number(price_data.get('volume_24h', 0))}
"""

    # Format news data for the prompt
    news_info = ""
    if news:
        news_info = "Latest News:\n"
        for i, item in enumerate(news[:3], 1):  # Limit to top 3 news
            news_info += f"{i}. {item.get('title', 'N/A')} - {item.get('source', 'N/A')}\n"
            if item.get('description'):
                news_info += f"   {item.get('description')[:200]}...\n"
            news_info += f"   Published: {item.get('published_at', 'N/A')}\n"
            news_info += f"   URL: {item.get('url', 'N/A')}\n\n"
    else:
        news_info = "No recent news available.\n"

    # Create the full context
    context = f"""
## MARKET DATA
{market_info}

## PRICE DATA
{price_info}

## NEWS
{news_info}
"""

    # Create the prompt for the LLM
    prompt = f"""You are an expert cryptocurrency assistant. Answer the user's question based on the real-time data provided below.
Always respond in the same language the question was asked in. Be concise but thorough, and provide specific data when available.

DATA:
{context}

USER QUESTION: {question}

ANSWER:"""

    # Track which sources were used
    sources = []
    if market_data:
        sources.append("CoinGecko")
    if price_data:
        sources.append("Binance")
    if news:
        sources.append("Coindesk")

    sources_text = f"\n\nИсточники данных: {', '.join(sources)}" if sources else ""

    try:
        # Use Ollama for inference
        import subprocess
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )
        response = result.stdout.decode("utf-8").strip()

        # Add sources to the response
        return {
            "answer": response,
            "sources": sources
        }

    except subprocess.TimeoutExpired:
        return {
            "answer": "⚠️ Response timed out. Please try again with a simpler question.",
            "sources": []
        }
    except Exception as e:
        return {
            "answer": f"⚠️ Error generating response: {e}",
            "sources": []
        }


def format_number(num):
    """Format large numbers for better readability"""
    try:
        num = float(num)
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.2f}K"
        else:
            return f"{num:.2f}"
    except (ValueError, TypeError):
        return "N/A"