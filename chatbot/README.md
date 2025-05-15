# 🤖 AI Crypto Assistant 🤖

**AI Crypto Assistant** is a Streamlit application that leverages Ollama and MongoDB technologies to provide real-time cryptocurrency market data, prices, and news from various sources.

![image](https://github.com/user-attachments/assets/crypto-assistant-main.png)

## 🧠 Features
- 💰 Real-time cryptocurrency prices and market data
- 📊 Market analysis (market cap, trading volume, etc.)
- 📰 Latest cryptocurrency news from Coindesk
- 💬 Interactive chat with AI assistant
- 📈 Top 20 cryptocurrencies by market cap tracking
- 🌐 Multi-language support

## 🛠️ Technology Stack
- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/) + LLM model (`llama3` by default)
- [MongoDB](https://www.mongodb.com/)
- APIs:
  - [CoinGecko](https://www.coingecko.com/) (market data)
  - [Binance](https://www.binance.com/) (real-time prices)
  - [Coindesk](https://www.coindesk.com/) (news)

## 🚀 Project Setup
### 1. Install dependencies
```bash
pip install -r requirements.txt
```

<details>
<summary>Example requirements.txt</summary>

```
streamlit
pymongo
requests
pandas
python-dotenv
ollama
feedparser
beautifulsoup4
```
</details>

### 2. Install and run Ollama
```bash
# Install Ollama
ollama run llama3
```

### 3. Run the Streamlit application
```bash
streamlit run main.py
```

### 4. (Optional) Configure environment variables
Create a `.env` file with the following variables:
```env
MONGO_URI=mongodb://localhost:27017
COINMARKETCAP_API_KEY=your_api_key
COINGECKO_API_KEY=your_api_key
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
OLLAMA_MODEL=llama3
```

## 📁 Project Structure
```
📦 ai-crypto-assistant/
├── main.py                # Streamlit interface
├── api_handlers.py        # API integrations
├── llm_handler.py         # LLM response generation
└── db.py                  # MongoDB operations
```

## 📝 Usage
1. **Start the application**: After following the setup instructions, navigate to the URL provided by Streamlit (typically http://localhost:8501)
2. **Ask questions**: Type your question about any cryptocurrency in the text input field
3. **View market data**: Check the sidebar for top cryptocurrencies and their rankings
4. **View news**: Latest news will be displayed in expandable sections
5. **Clear history**: Use the "Clear Chat History" button to remove all stored conversations

## 📸 Demo Screenshots

### Main Interface
![image](https://github.com/user-attachments/assets/crypto-assistant-main.png)

### Market Data Display
![image](https://github.com/user-attachments/assets/crypto-assistant-market.png)

### News Display
![image](https://github.com/user-attachments/assets/crypto-assistant-news.png)

### Chat History
![image](https://github.com/user-attachments/assets/crypto-assistant-chat.png)

## 💡 Example Questions
- "What's the current price of Bitcoin?"
- "Tell me the latest news about Ethereum"
- "How is Solana performing today?"
- "What's the market cap of Cardano?"
- "Compare Bitcoin and Ethereum prices"
- "What are the top performing coins today?"

## 📌 Notes
- Market data is cached and updated every 2 minutes
- Price data is cached and updated every 30 seconds
- News data is cached and updated every 5 minutes
- Chat history is stored in MongoDB
- The application uses Coindesk's RSS feed for news

## 🧹 Database Cleanup
To remove all chat history from the database, click the "🗑️ Clear Chat History" button in the interface.

## 🔒 Security
- The application runs locally
- All data is stored in your MongoDB
- The Ollama model runs locally, without sending data to the internet
- API keys should be kept secure in the .env file

## LICENCE
The MIT License (MIT)

Copyright (c) 2024 AI Crypto Assistant

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

