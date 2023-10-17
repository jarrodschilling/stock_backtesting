import yfinance as yf
from data import portfolio
import pandas as pd
from matplotlib import pyplot as plt
import calendar
from matplotlib.ticker import FuncFormatter

# Set the start and end dates
start_date = "2022-12-31"
end_date = "2023-10-16"

def historical_data(symbols, start_date, end_date):
    data = yf.download(symbols, start=start_date, end=end_date)
    return data

weights = [0.1, 0.05, 0.05, 0.2, 0.1, 0.1, 0.2, 0.1, 0.1]


portfolio_data = historical_data(portfolio, start_date, end_date)

portfolio_data = portfolio_data['Adj Close']
stock_returns = portfolio_data.pct_change()[1:]
weighted_returns = (weights * stock_returns)
portfolio_returns = weighted_returns.sum(axis=1)

print(portfolio_returns.values)


plt.plot(portfolio_returns.index, portfolio_returns.values)

plt.show()