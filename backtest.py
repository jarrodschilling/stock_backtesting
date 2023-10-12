import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from data import indices, sectors, industries, sub_sectors

# -----------------------------------------------------------------------------------------------------
# ------------ INPUTS
# -----------------------------------------------------------------------------------------------------

# QQQE only backtests to 2013

comparison_portfolio = indices
comparison_portfolio_name = "Indices"
current_portfolio = "SPY"
current_portfolio_name = "SPY"
ma_period = 200
ma_type = "SMA"

# User inputs start date and auto adjust to get needed MA data
input_start_date = '2014-01-01'
start_date = (datetime.strptime(input_start_date, '%Y-%m-%d') - timedelta(days=ma_period)).strftime('%Y-%m-%d')
end_date = '2023-10-10'

# Highlighting parameters
threshold = "below"
highlight_threshold = 5

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
    above_ma = data > ma_data
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

# Plot the percentage above EMA in the first subplot
ax1.plot(percentage_above_ma.index[ma_period:], percentage_above_ma.values[ma_period:], linewidth=1.5)
ax1.set_ylabel(f'Percentage Above {ma_type}')
ax1.set_title(f'Percentage of {comparison_portfolio_name} Above {ma_period}-Day {ma_type}')

# Plot the SPY price in the second subplot
ax2.plot(current_portfolio_data.index[ma_period:], current_portfolio_data.values[ma_period:])
ax2.set_ylabel('Price')
ax2.set_title(f'{current_portfolio_name} Price')

# Customize the plot
plt.xlabel('Date')
plt.xticks(rotation=45)



# Highlight regions where the condition is met
highlighted_regions = []

if threshold == "above":
    for i in range(ma_period, len(percentage_above_ma)):
        if percentage_above_ma[i] > highlight_threshold:
            if not highlighted_regions:
                start_date = percentage_above_ma.index[i]
            highlighted_regions.append(percentage_above_ma.index[i])
        elif highlighted_regions:
            end_date = percentage_above_ma.index[i]
            highlighted_regions = []
            ax1.axvspan(start_date, end_date, facecolor='orange', alpha=0.6)
            ax2.axvspan(start_date, end_date, facecolor='orange', alpha=0.6)

elif threshold == "below":
    for i in range(ma_period, len(percentage_above_ma)):
        if percentage_above_ma[i] < highlight_threshold:
            if not highlighted_regions:
                start_date = percentage_above_ma.index[i]
            highlighted_regions.append(percentage_above_ma.index[i])
        elif highlighted_regions:
            end_date = percentage_above_ma.index[i]
            highlighted_regions = []
            ax1.axvspan(start_date, end_date, facecolor='orange', alpha=0.6)
            ax2.axvspan(start_date, end_date, facecolor='orange', alpha=0.6)

plt.tight_layout()
plt.show()