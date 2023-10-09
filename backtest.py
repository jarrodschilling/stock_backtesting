import yfinance as yf
from matplotlib import pyplot as plt
import datetime

symbol1="XLE"
symbol2="OIH"
symbol3="XOP"
symbol4="SPY"

symbols = [symbol1, symbol2, symbol3, symbol4]

    
ma_avg = 20
days = 100
# days variable created by asking user how far back in time they want to go, so must make negative
days = -1 * days

def price_backtest(data, days):
    price_list = []
    for i in range(days, -1):
        closing_price = data['Close'].iloc[i]
        price_list.append(closing_price)

    return price_list

def ema_20_backtest(data, ema_period, i):
    data[f'EMA_{ema_period}'] = data['Close'].ewm(span=ema_period, adjust=False).mean()
    most_recent_20_ema = data[f'EMA_{ema_period}'].iloc[i]
    return most_recent_20_ema


# portfolio_ema20 = ma_compute_yf(stocks, "ema20", "today")
# portfolio_ema20_summary = len(portfolio_ema20) / len(portfolio)


def summary_backtest(symbols, period, days):
    ema_20_dict = {}
    start_date = "2022-01-01"
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    end_date = tomorrow.strftime('%Y-%m-%d')

    for symbol in symbols:
        data = yf.download(symbol, start=start_date, end=end_date)
        for i in range(days, 0):
            price = data['Close'].iloc[i]
            ema_20 = ema_20_backtest(data, period, i)
            if price > ema_20:
                ema_20_dict[i] = symbol
            else:
                ema_20_dict[i] = None
    

    # special_list = []
    # counter = 0
    # days = days * -1
    # for i in range(0, 80):
    #     for j in range(0, 2):
    #         if ema_20_dict[j][i] == True:
    #             print(ema_20_dict[j][i])
    #             counter += 1
    #     list_add = counter/len(symbols)
    #     special_list.append(list_add)
    
    return ema_20_dict

print(summary_backtest(symbols, 20, days))


# result = []
# for x, y in zip(date, ema20):
#     result.append([x, y])
# print(result)