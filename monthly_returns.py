import yfinance as yf
from data import portfolio
from backtest import api_historical_data
import pandas as pd
from matplotlib import pyplot as plt
import calendar
from matplotlib.ticker import FuncFormatter
# SPY - 1994, QQQ - 2000, ^GSPC
# XLC + XLRE limited data, all other sectors go back pre-GFC
# XWEB(2017), XSW(2012), XTN(2012), XAR(2012), XHS(2012), XHE(2012), XTL(2012), all others 2007



# Set the start and end dates
start_date = "2019-12-31"
end_date = "2023-10-16"

# Download SPY historical data
spy_data = yf.download("^GSPC", start=start_date, end=end_date)




# Calculate monthly returns
spy_data['Adj Close'] = spy_data['Adj Close'].ffill()  # Forward fill any missing data
monthly_returns = spy_data['Adj Close'].resample('M').ffill().pct_change()

# Calculate the average monthly return for each month of the year
average_returns_by_month = monthly_returns.groupby(monthly_returns.index.month).mean()


def percent_formatter(x, pos):
    return f'{x * 100:.1f}%'

# Create a bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# Bar chart for average returns
bars = ax.bar(calendar.month_name[1:13], average_returns_by_month)
plt.title('Average Monthly Returns for Each Month')
plt.xlabel('Month')
plt.ylabel('Average Return')
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))
plt.xticks(rotation=45)

# Display actual returns above/below bars
for bar, actual_return in zip(bars, average_returns_by_month):
    height = bar.get_height()
    label_y = height + 0.0002 if actual_return >= 0 else height - 0.004
    ax.text(bar.get_x() + bar.get_width() / 2, label_y, f'{actual_return * 100:.1f}%', ha='center')


# plt.figure(figsize=(10, 6))
# average_returns_by_month.plot(kind='bar')
# plt.title('Average Monthly Returns for Each Month')
# plt.xlabel('Month')
# plt.ylabel('Average Return')
# plt.xticks(range(1, 13), calendar.month_name[1:13])

plt.show()