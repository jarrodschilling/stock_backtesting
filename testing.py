import yfinance as yf
from matplotlib import pyplot as plt
import datetime


# print(plt.style.available)
plt.style.use('fivethirtyeight')

symbol1="XLE"
symbol2="OIH"
symbol3="XOP"
symbol4="SPY"

symbols = [symbol1, symbol2, symbol3, symbol4]
start_date = "2022-01-01"
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
end_date = tomorrow.strftime('%Y-%m-%d')

# Fetch historical stock data
for symbol in symbols:
    data = yf.download(symbol, start=start_date, end=end_date)
    data['Normalized'] = (data['Close'] / data['Close'].iloc[0]) * 100
    plt.plot(data['Normalized'], label=symbol)

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('NVDA Price Over Time')

plt.legend()
plt.tight_layout()
plt.show()

