# tools/yahoo_finance_news.py

from langchain.tools import tool
import yfinance as yf
from datetime import datetime
import logging

@tool("yahoo_finance_news", return_direct=False)
def yahoo_finance_news(ticker: str) -> str:
    """Fetches the last 4 news articles about a company from Yahoo Finance.
    
    Args:
        ticker: The stock ticker symbol (e.g., "AAPL", "GOOGL", "TSLA")
    
    Returns a formatted list of news articles with titles, publishers, and links
    that can be summarized by the AI.
    
    Example queries:
    - "What's the latest news about Apple?"
    - "Get me news about TSLA"
    - "Show me recent articles about Microsoft"
    """             
    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        # Get news articles
        news = stock.get_news(4)

        if not news:
            return f"No news articles found for {ticker}."
        
        # Get the last 4 articles
        articles = news[:4]
        
        # Format the results
        result = f"Latest news for {ticker}:\n\n"
        
        for i, article in enumerate(articles, 1):
            article = article.get('content', article)
            title = article.get('title', 'No title')
            summary = article.get('summary', 'No summary available')
            
            result += f"{i}. {title}\n"
            result += f"   summary: {summary}\n"
        
        return result
        
    except Exception as e:
        return f"Error fetching news for {ticker}: {str(e)}"
