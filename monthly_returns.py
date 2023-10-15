import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
# SPY - 1994, QQQ - 2000
# Set the start and end dates
start_date = "1994-01-01"
end_date = "2023-10-01"

# Download SPY historical data
spy_data = yf.download("SPY", start=start_date, end=end_date)

# Calculate monthly returns
spy_data['Adj Close'] = spy_data['Adj Close'].ffill()  # Forward fill any missing data
monthly_returns = spy_data['Adj Close'].resample('M').ffill().pct_change()

# Calculate the average monthly return for each month of the year
average_returns_by_month = monthly_returns.groupby(monthly_returns.index.month).mean()

# Print the monthly returns
# print(monthly_returns)
# print((monthly_returns * 100).round(1))
# print((average_returns_by_month * 100).round(1))

plt.plot(average_returns_by_month)

plt.show()