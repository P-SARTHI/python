import yfinance as yf
import pandas as pd
import numpy as np

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Fetch top 200 stocks on NIFTY
nifty_tickers = pd.read_csv('path/to/nifty_tickers.csv')  # Replace with the path to the CSV file containing NIFTY tickers
nifty_tickers = nifty_tickers.head(200)['Symbol']  # Assuming the CSV file contains a 'Symbol' column

# Fetch RSI for each stock
rsi_values = {}
for ticker in nifty_tickers:
    try:
        stock_data = yf.download(ticker + '.NS', start='2022-01-01', end='2024-01-01')  # Adjust start and end dates as needed
        close_prices = stock_data['Adj Close']
        rsi = calculate_rsi(close_prices)
        rsi_values[ticker] = rsi[-1]  # Taking the last RSI value
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")

# Sort RSI values
sorted_rsi = sorted(rsi_values.items(), key=lambda x: x[1], reverse=True)

# Print top 10 stocks with highest RSI
for ticker, rsi in sorted_rsi[:10]:
    print(f"{ticker}: {rsi:.2f}")