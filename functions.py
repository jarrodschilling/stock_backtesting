import yfinance as yf
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import pandas as pd


# -----------------------------------------------------------------------------------------------
# ------------Fetch Data
# -----------------------------------------------------------------------------------------------

# Adjust data start date to always be able to capture the 200SMA
def adjust_start(start_date):
    adjusted_start_date = (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=300)).strftime('%Y-%m-%d')
    return adjusted_start_date

# Call yfinance API for portfolio data
def api_historical_data(symbols, start_date, end_date):
    data = yf.download(symbols, start=start_date, end=end_date)
    return data['Adj Close']


# -----------------------------------------------------------------------------------------------
# ------------Moving Average Calculations
# -----------------------------------------------------------------------------------------------

# Calculate the moving average for each stock
def calculate_ma(data, ma_period, ma_type):
    if ma_type == "EMA":
        return data.ewm(span=ma_period, adjust=False).mean()
    elif ma_type == "SMA":
        return data.rolling(window=ma_period).mean()
    
# Backtest and calculate the percentage above MA for each date
def backtest_percentage_above_ma(data, ma_period, ma_type, comparison_portfolio):
    ma_data = calculate_ma(data, ma_period, ma_type)
    ema_20 = calculate_ma(data, 20, "EMA")
    sma_50 = calculate_ma(data, 50, "SMA")
    sma_200 = calculate_ma(data, 200, "SMA")
    
    if ma_period == 20:
        above_ma = (data > ema_20) & (ema_20 > sma_50) & (sma_50 > sma_200)
    elif ma_period == 50:
        above_ma = (data > sma_50) & (sma_50 > sma_200)
    elif ma_period == 200:
        above_ma = data > sma_200


    percentage_above_ma = (above_ma.sum(axis=1) / len(comparison_portfolio)) * 100
    return percentage_above_ma


# -----------------------------------------------------------------------------------------------
# ------------Matplotlib Highlighting Functions
# -----------------------------------------------------------------------------------------------

