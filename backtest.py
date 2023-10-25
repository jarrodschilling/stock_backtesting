import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from data import indices, sectors, industries, sub_sectors

# -----------------------------------------------------------------------------------------------------
# ------------ INPUTS
# -----------------------------------------------------------------------------------------------------

# SPY - 1994, QQQ - 2000, ^GSPC, ^IXIC
# XLC(2019) + XLRE(2016) limited data, all other sectors go back pre-GFC
# XWEB(2017), XSW(2012), XTN(2012), XAR(2012), XHS(2012), XHE(2012), XTL(2012), all others 2007
# CIBR(2016), AIQ(2019), IBUY(2017), IDRV(2020), JETS(2016), BLOK(2019), CNCR(2016), ROBO(2014), ESPO(2019), VICE(2018), , all others start of 2013 okay to run


# QQQE only backtests to 2013

comparison_portfolio = industries
comparison_portfolio_name = "Industry ETFs"
current_portfolio = "QQQ"
current_portfolio_name = "QQQ"
ma_period = 50
ma_type = "SMA"

# User inputs start date and auto adjust to get needed MA data
input_start_date = '2018-01-01'
# Adjust date for time series, so it can always capture the 200 Day SMA
start_date = (datetime.strptime(input_start_date, '%Y-%m-%d') - timedelta(days=300)).strftime('%Y-%m-%d')
end_date = '2023-10-26'

# Highlighting parameters
threshold = "below"
highlight_threshold = 1

# -----------------------------------------------------------------------------------------------------
# ------------ FUNCTIONS
# -----------------------------------------------------------------------------------------------------

# Call yfinance API for data
def api_historical_data(symbols, start_date, end_date):
    data = yf.download(symbols, start=start_date, end=end_date)
    return data['Adj Close']

# Calculate the moving average for each stock
def calculate_ma(data, ma_period, ma_type):
    if ma_type == "EMA":
        return data.ewm(span=ma_period, adjust=False).mean()
    elif ma_type == "SMA":
        return data.rolling(window=ma_period).mean()

# Backtest and calculate the percentage above MA for each date
def backtest_percentage_above_ma(data, ma_period, ma_type):
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


# API call for data
comparison_portfolio_data = api_historical_data(comparison_portfolio, start_date, end_date)
current_portfolio_data = api_historical_data(current_portfolio, start_date, end_date)


# Calculate the percentage above EMA for each date
percentage_above_ma = backtest_percentage_above_ma(comparison_portfolio_data, ma_period, ma_type)



# Create a Pandas DataFrame with the results
results = pd.DataFrame({'Date': percentage_above_ma.index, 'Percentage Above EMA': percentage_above_ma.values})



# -----------------------------------------------------------------------------------------------------
# ------------ MATPLOTLIB
# -----------------------------------------------------------------------------------------------------


plt.style.use('fivethirtyeight')

# Create a new figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Highlight regions where the condition is met
highlighted_regions = []

if threshold == "above":
    for i in range(200, len(percentage_above_ma)):
        if percentage_above_ma.iloc[i] > highlight_threshold:
            if not highlighted_regions:
                hl_start_date = percentage_above_ma.index[i]
            highlighted_regions.append(percentage_above_ma.index[i])
        elif highlighted_regions:
            hl_end_date = percentage_above_ma.index[i]
            highlighted_regions = []
            
            ax1.axvspan(hl_start_date, hl_end_date, facecolor='orange', alpha=0.6)
            ax2.axvspan(hl_start_date, hl_end_date, facecolor='orange', alpha=0.6)

elif threshold == "below":
    for i in range(200, len(percentage_above_ma)):
        if percentage_above_ma.iloc[i] < highlight_threshold:
            if not highlighted_regions:
                hl_start_date = percentage_above_ma.index[i]
                # top_start_date = percentage_above_ma.index[i]
                # bottom_start_date = percentage_above_ma.index[i]
            highlighted_regions.append(percentage_above_ma.index[i])
        elif highlighted_regions:
            hl_end_date = percentage_above_ma.index[i]
            # top_end_date = percentage_above_ma.index[i]
            # bottom_end_date = percentage_above_ma.index[i]
            highlighted_regions = []
            # ax1.axvspan(top_start_date, top_end_date, facecolor='orange', alpha=0.6)
            # ax2.axvspan(bottom_start_date, bottom_end_date, facecolor='orange', alpha=0.6)
            ax1.axvspan(hl_start_date, hl_end_date, facecolor='orange', alpha=0.6)
            ax2.axvspan(hl_start_date, hl_end_date, facecolor='orange', alpha=0.6)

# Check for a highlighted region after the loop ends
if highlighted_regions:
    hl_end_date = percentage_above_ma.index[-1]  
    # ax1.axvspan(top_start_date, top_end_date, facecolor='orange', alpha=0.6)
    # ax2.axvspan(bottom_start_date, bottom_end_date, facecolor='orange', alpha=0.6)
    ax1.axvspan(hl_start_date, hl_end_date, facecolor='orange', alpha=0.6)
    ax2.axvspan(hl_start_date, hl_end_date, facecolor='orange', alpha=0.6)


# Plot the percentage above EMA in the first subplot
ax1.plot(percentage_above_ma.index[percentage_above_ma.index >= input_start_date], percentage_above_ma.values[percentage_above_ma.index >= input_start_date], linewidth=1.5)
ax1.set_ylabel(f'Percentage Above {ma_type}')
ax1.set_title(f'Percentage of {comparison_portfolio_name} Above {ma_period}-Day {ma_type}')

# Plot the SPY price in the second subplot
ax2.plot(current_portfolio_data.index[percentage_above_ma.index >= input_start_date], current_portfolio_data.values[percentage_above_ma.index >= input_start_date], linewidth=1.7)
ax2.set_ylabel('Price')
ax2.set_title(f'{current_portfolio_name} Price')

# Customize the plot
plt.xlabel('Date')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()