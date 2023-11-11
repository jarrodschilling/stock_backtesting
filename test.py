import yfinance as yf

msft = yf.Ticker("MSFT")
info = msft.news
print(info)
