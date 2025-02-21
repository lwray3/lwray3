import yfinance as yf
#import talib as ta
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime as dt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    return hist

def fetch_balance_sheet(ticker):
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet
    return balance_sheet

def fetch_income_statement(ticker):
    stock = yf.Ticker(ticker)
    income_stmt = stock.income_stmt
    return income_stmt

def analyze_sentiment(reports):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = 0
    for report in reports:
        sentiment = analyzer.polarity_scores(report)
        sentiment_score += sentiment['compound']
    return sentiment_score / len(reports) if reports else 0

def fetch_reports(ticker):
    # Placeholder function to fetch past reports
    # Replace with actual implementation to fetch reports
    return [
        "The company has shown consistent growth over the past year.",
        "Recent market trends suggest a potential downturn.",
        "Analysts are optimistic about the company's future performance."
    ]

def fetch_articles(ticker):
    # Placeholder function to fetch articles
    # Replace with actual implementation to fetch articles
    return [
        "The company has shown consistent growth over the past year.",
        "Recent market trends suggest a potential downturn.",
        "The results suggest that this company is due for a rise in shareholder value soon"
    ]

def calculate_growth_potential(ticker):
    stock_data = fetch_stock_data(ticker)
    balance_sheet = fetch_balance_sheet(ticker)
    income_stmt = fetch_income_statement(ticker)
    reports = fetch_reports(ticker)
    articles = fetch_articles(ticker)
    
    sentiment_score = analyze_sentiment(reports + articles)
    
    # Placeholder for growth potential calculation
    # Replace with actual logic to calculate growth potential
    growth_potential = (stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0] * 10

    
    # Example thresholds for balance sheet and income statement
    total_assets = balance_sheet.loc['Total Assets'].iloc[0] if 'Total Assets' in balance_sheet.index else 0
    total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'][0] if 'Total Liabilities Net Minority Interest' in balance_sheet.index else 0
    net_income = income_stmt.loc['Net Income'][0] if 'Net Income' in income_stmt.index else 0
    
    if total_assets > total_liabilities:
        growth_potential += 2  # Positive impact
    else:
        growth_potential -= 2  # Negative impact
    
    if net_income > 0:
        growth_potential += 2  # Positive impact
    else:
        growth_potential -= 2  # Negative impact
    
    weighted_growth_potential = growth_potential + sentiment_score
    
    # Scale the result to -10 to +10
    final_score = max(min(weighted_growth_potential, 10), -10)
    return final_score, balance_sheet, income_stmt

def recommend_stocks(tickers, top_n=5):
    recommendations = []
    
    for ticker in tickers:
        try:
            score, balance_sheet, income_stmt = calculate_growth_potential(ticker)
            recommendations.append((ticker, score))
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    
    # Sort the recommendations based on the score in descending order
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top N recommendations
    return recommendations[:top_n]

# Example usage
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'NFLX', 'NVDA', 'BABA', 'V']
top_recommendations = recommend_stocks(tickers, top_n=5)

print("Top stock recommendations:")
for ticker, score in top_recommendations:
    print(f"{ticker}: {score}")

# def plot_stock_data_with_sma(ticker):
###
    #stock_data = fetch_stock_data(ticker)
    #stock_data['SMA50'] = ta.SMA(stock_data['Close'], timeperiod=50)
    
   # plt.figure(figsize=(12, 6))
   # plt.plot(stock_data['Close'], label='Close Price')
   # plt.plot(stock_data['SMA50'], label='50-Day SMA', linestyle='--')
   # plt.title(f'{ticker} Stock Price and 50-Day SMA')
   # plt.xlabel('Date')
   # plt.ylabel('Price')
    #plt.legend()
  #  plt.show()
###
# Example usage
#plot_stock_data_with_sma('AAPL')


ticker = input("Enter the stock ticker symbol: ")
growth_potential_score, balance_sheet, income_stmt = calculate_growth_potential(ticker)
print(f"The growth score for {ticker} is: {growth_potential_score}")
print(f"Balance Sheet for {ticker}:\n{balance_sheet}")
print(f"Income Statement for {ticker}:\n{income_stmt}")
