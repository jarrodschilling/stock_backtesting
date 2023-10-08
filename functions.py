import yfinance as yf
from matplotlib import pyplot as plt
import datetime


# -----------------------------------------------------------------------------------------------
# ------------Moving Average Calculations w/ API Calls
# -----------------------------------------------------------------------------------------------

# Global variables for caching data
data_cache = {}

# Call the yfinance API for data needed and cache it
def api_call(symbol):
    if symbol in data_cache:
        return data_cache[symbol]
    
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date = "2022-01-01"
    end_date = today.strftime('%Y-%m-%d')

    # Fetch historical stock data
    data = yf.download(symbol, start=start_date, end=end_date)
    
    # Cache the data for future use
    data_cache[symbol] = data
    
    return data

# Get current price using API CALL data ------------------------ **THIS NEEDS UPDATING**
def current_price(data):
    data = data

    closing_price = data['Close'].iloc[-2]

    return closing_price


# Get exponential moving average using API CALL data and user inputed period
def ema(data, ema_period):
    data = data
    ema_period = ema_period
    
    data[f'EMA_{ema_period}'] = data['Close'].ewm(span=ema_period, adjust=False).mean()

    # Get the most recent day's closing 20 EMA
    most_recent_20_ema = data[f'EMA_{ema_period}'].iloc[-2]


    return most_recent_20_ema


# Get simple moving average using API CALL data and user inputed period
def sma(data, sma_period):
    data = data
    sma_period = sma_period

    data[f'SMA_{sma_period}'] = data['Close'].rolling(window=sma_period).mean()

    most_recent_50_sma = data[f'SMA_{sma_period}'].iloc[-2]

    return most_recent_50_sma


# Make batched API CALLS
def batch_api_call(symbols):
    data = {}
    for symbol in symbols:
        data[symbol] = api_call(symbol)
    return data


# Iterate list of stocks to determine if they are above trending EMAs/SMAs
def ma_compute_yf(stocks, ma_avg):
    portfolio_ma = []
    stock_name = []

    # Extract unique symbols from stocks
    symbols_to_fetch = set(stock[1] for stock in stocks)

    # Batch API call for all symbols
    data = batch_api_call(symbols_to_fetch)

    for stock in stocks:
        symbol = stock[1]
        name = stock[2]
        current = current_price(data[symbol])
        ema20 = ema(data[symbol], 20)
        sma50 = sma(data[symbol], 50)
        sma200 = sma(data[symbol], 200)
        
        if (ma_avg == "ema20") and current > ema20 and ema20 > sma50 and sma50 > sma200:
            portfolio_ma.append(symbol)
            stock_name.append(name)
        elif (ma_avg == "sma50") and current > sma50 and sma50 > sma200:
            portfolio_ma.append(symbol)
            stock_name.append(name)
        elif (ma_avg == "sma200") and current > sma200:
            portfolio_ma.append(symbol)
            stock_name.append(name)

    result = []
    for x, y in zip(portfolio_ma, stock_name):
        result.append([x, y])
    
    return result