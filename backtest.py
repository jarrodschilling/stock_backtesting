import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd
import datetime
from data import indices, sectors


symbols = sectors


def api_historical_data(symbols, start_date, end_date):
    data = yf.download(symbols, start=start_date, end=end_date)
    return data['Adj Close']

# Calculate the EMA for each stock
def calculate_ema(data, ma_period):
    return data.ewm(span=ma_period, adjust=False).mean()

# Calculate the SMA for each stock
def calculate_sma(data, ma_period):
    return data.rolling(window=ma_period).mean()

# Backtest and calculate the percentage above MA for each date
def backtest_percentage_above_ema(data, ma_period):
    ema_data = calculate_sma(data, ma_period)
    above_ema = data > ema_data
    percentage_above_ema = (above_ema.sum(axis=1) / len(symbols)) * 100
    return percentage_above_ema


start_date = '2019-01-01'
end_date = '2020-06-01'
ma_period = 50

# API call for data
stock_data = api_historical_data(symbols, start_date, end_date)
spy_data = api_historical_data('SPY', start_date, end_date)

# Calculate the percentage above EMA for each date
percentage_above_ema = backtest_percentage_above_ema(stock_data, ma_period)

# Create a DataFrame with the results
results = pd.DataFrame({'Date': percentage_above_ema.index, 'Percentage Above EMA': percentage_above_ema.values})

plt.style.use('fivethirtyeight')

# Create a new figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot the percentage above EMA in the first subplot
ax1.plot(percentage_above_ema.index, percentage_above_ema.values)
ax1.set_ylabel('Percentage Above EMA')
ax1.set_title('Percentage of Stocks Above 50-Day SMA')

# Plot the SPY price in the second subplot
ax2.plot(spy_data.index, spy_data.values)
ax2.set_ylabel('SPY Price')
ax2.set_title('SPY Price')

# Customize the plot
plt.xlabel('Date')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()