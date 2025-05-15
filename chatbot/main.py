import streamlit as st
from api_handlers import identify_coin, get_aggregated_data, get_top_coins
from llm_handler import generate_answer
from db import save_qa_to_db, get_chat_history, clear_database
import time
import pandas as pd

st.set_page_config(page_title="AI Crypto Assistant", layout="wide")

# App title and description
st.title("""
🚀 **AI Crypto Assistant** 🚀
### _Your expert guide to cryptocurrency markets_ 💰
""")
st.write("Ask any question about the top 50 cryptocurrencies by market cap.")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "clear_triggered" not in st.session_state:
    st.session_state.clear_triggered = False

# Sidebar with top coins info
with st.sidebar:
    st.header("Top Cryptocurrencies")
    # Add refresh button
    if st.button("🔄 Refresh Market Data"):
        st.cache_data.clear()

    # Display top coins table
    try:
        top_coins = get_top_coins(20)  # Get top 20 coins
        if top_coins:
            # Get price data for display
            df = pd.DataFrame([{
                "Rank": coin["market_cap_rank"],
                "Symbol": coin["symbol"].upper(),
                "Name": coin["name"]
            } for coin in top_coins])

            st.dataframe(df, hide_index=True)
    except Exception as e:
        st.error(f"Error loading top coins: {e}")

    # Display system status
    st.subheader("System Status")
    st.write("✅ CoinGecko API: Connected")
    st.write("✅ Binance API: Connected")
    st.write("✅ CoinMarketCap API: Connected")
    st.write("✅ Coindesk RSS: Connected")

    # Clear database button
    if st.button("🗑️ Clear Chat History"):
        clear_database()
        st.session_state.chat_history = []
        st.success("Chat history cleared.")
        st.session_state.clear_triggered = True

# Function to process user query
def process_query(query):
    if query and not st.session_state.clear_triggered:
        # Show spinner while processing
        with st.spinner("Processing your query..."):
            # Identify coin in the query (if any)
            coin = identify_coin(query)
            
            # Get data from APIs if a coin was identified
            data = {}
            if coin:
                data = get_aggregated_data(coin)
            
            # Generate answer
            response = generate_answer(query, data)
            answer = response["answer"]
            sources = response["sources"]

            # Display answer
            st.markdown(f"**AI Assistant:** {answer}")

            # Display sources if available
            if sources:
                source_text = ", ".join(sources)
                st.markdown(f"**Источники данных:** {source_text}")

            # Save to database
            save_qa_to_db(query, answer)

            # Add to session history
            st.session_state.chat_history.append((query, answer, sources))

# Main chat area
col1, col2 = st.columns([3, 1])

with col1:
    # User query input
    user_query = st.text_input("Ask about any cryptocurrency:",
                               placeholder="Example: What's the latest news about Ethereum?")

    # Process the user query
    if user_query:
        process_query(user_query)
        
        # Display news separately if available
        coin = identify_coin(user_query)
        if coin:
            data = get_aggregated_data(coin)
            news_data = data.get("news_data", [])
            if news_data:
                st.subheader("📰 Latest News")
                for news in news_data:
                    with st.expander(news["title"]):
                        st.write(news["description"])
                        st.write(f"Source: {news['source']}")
                        st.write(f"Published: {news['published_at']}")
                        st.markdown(f"[Read more]({news['url']})")

    # Chat history
    if st.session_state.chat_history:
        st.subheader("Recent Conversations")
        for history_item in st.session_state.chat_history[::-1]:
            st.markdown(f"**You:** {history_item[0]}")
            st.markdown(f"**AI Assistant:** {history_item[1]}")

            # Display sources for this history item if available
            if len(history_item) > 2 and history_item[2]:
                sources_text = ", ".join(history_item[2])
                st.markdown(f"**Источники данных:** {sources_text}")

            st.markdown("---")

    if st.session_state.clear_triggered:
        st.session_state.clear_triggered = False

with col2:
    # Examples of queries
    st.subheader("Example Questions")
    examples = [
        "What's the current price of Bitcoin?",
        "Tell me the latest news about Ethereum",
        "How is Solana performing today?",
        "What's the market cap of Cardano?",
        "Compare Bitcoin and Ethereum prices",
        "What are the top performing coins today?"
    ]

    for example in examples:
        if st.button(example):
            # Process the example query directly
            process_query(example)