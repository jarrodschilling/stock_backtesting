import yfinance as yf
from matplotlib import pyplot as plt
import datetime
from functions import ma_compute_yf
from data import indices, sectors

stocks = indices
portfolio = indices

portfolio_ema20 = ma_compute_yf(stocks, "ema20", "today")
portfolio_sma50 = ma_compute_yf(stocks, "sma50", "today")
portfolio_sma200 = ma_compute_yf(stocks, "sma200", "today")

portfolio_ema20_summary = len(portfolio_ema20) / len(portfolio)
portfolio_ema20_summary = "{:.2%}".format(portfolio_ema20_summary)

portfolio_sma50_summary = len(portfolio_sma50) / len(portfolio)
portfolio_sma50_summary = "{:.2%}".format(portfolio_sma50_summary)

portfolio_sma200_summary = len(portfolio_sma200) / len(portfolio)
portfolio_sma200_summary = "{:.2%}".format(portfolio_sma200_summary)

print(portfolio_ema20)