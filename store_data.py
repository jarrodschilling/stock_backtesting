import yfinance as yf
import pandas as pd


# Set the start and end dates
start_date = "2000-01-01"
end_date = "2023-10-01"

# Download SPY historical data
spy_data = yf.download("QQQ", start=start_date, end=end_date)

# Store Data as CSV
spy_data['Adj Close'] = spy_data['Adj Close'].ffill()  # Forward fill any missing data

spy_store_data = spy_data['Adj Close']
spy_store_data.to_csv("qqq_2000_data.csv")

