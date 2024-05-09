import requests
import pandas as pd
import bs4 as bs
import datetime as dt
import pandas_datareader as pdr
"""
The dataset in pandas_datareader library 
The S&P 100 Index is a stock market index of United States stocks maintained by Standard & Poor's
"""

def getAllData(sym):
    try:
        df_final = pdr.get_data_yahoo(sym, start = dt.datetime(2015,1,1), end = dt.date.today())
        df_final.drop("Adj Close", axis=1, inplace=True)
    except:
        return pd.DataFrame()

    return df_final

def getFinalData(sym, period="DAY"):
    df_origin = getAllData(sym)

    if period == "DAY":
        return df_origin
    else:
        if period == "1WEEK":
            df = df_origin.groupby(pd.Grouper(freq='1W'))
        elif period == "2WEEK":
            df = df_origin.groupby(pd.Grouper(freq='2W'))
        elif period == "MONTH":
            df = df_origin.groupby(pd.Grouper(freq='M'))

        lst_C = []
        for i in df:
            dd = convertData(i)
            lst_C.append(dd)

        final = pd.concat(lst_C)
        final = final[::-1]

        return final

def convertData(tup):
    index = tup[0]
    dataf = tup[1]
    col = dataf.columns
    high = dataf['High'].max()
    low = dataf['Low'].min()
    vol = dataf['Volume'].sum()
    close = dataf['Close'].iloc[-1]
    open = dataf['Open'].iloc[0]
    df = pd.DataFrame([low, high, open, close, vol], columns=[index], index=col)
    return df.T


def getListStocks():
    resp = requests.get("https://en.wikipedia.org/wiki/S%26P_100")
    convert_soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = convert_soup.find('table',{'class':'wikitable sortable'})

    tickers = []
    names = {}

    for rows in table.findAll('tr')[1:]:
        ticker = rows.findAll('td')[0].text.strip()
        name = rows.findAll('td')[1].text.strip()
        tickers.append(ticker)
        names[ticker] = name

    tickers.sort()
    tup = tuple(tickers)

    return tup, names
