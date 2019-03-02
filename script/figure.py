import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import *
from matplotlib.dates import DateFormatter, WeekdayLocator, HourLocator, DayLocator, MONDAY, MonthLocator
from matplotlib.finance import candlestick_ohlc, date2num, datetime

ohlc_dict = {
    'id': 'first',
    'open': 'first',
    'highest': 'max',
    'lowest': 'min',
    'close': 'last',
    'turnoverValue': 'sum'
}

index_dict = {
    'indexID': 'id',
    'openIndex': 'open',
    'highestIndex': 'highest',
    'lowestIndex': 'lowest',
    'closeIndex': 'close'
}

stock_dict = {
    'secID': 'id',
    'openPrice': 'open',
    'highestPrice': 'highest',
    'lowestPrice': 'lowest',
    'closePrice': 'close'
}

def draw(data):    
    chart_width = 0.5
    fig = plt.figure()
    
    gs1 = GridSpec(4, 1)
    ax1 = plt.subplot(gs1[:-1, :])
    ax2 = plt.subplot(gs1[-1, :])
    
    #locator = MonthLocator(bymonth=range(1, 13, 3))
    #formatter = DateFormatter('%Y-%m')
    #ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(NullFormatter())
    
    #reax1.set_yscale('log')
    #ax1.yaxis.set_major_locator(SymmetricalLogLocator(base=1.2, linthresh=1))
    ax1.yaxis.set_minor_locator(NullLocator())
    ax1.yaxis.set_major_formatter(ScalarFormatter())
    ax1.set_ylabel('Price')
    ax1.grid(True)
    
    quote = dataframe2quote(data)
    candlestick_ohlc(ax1, quote, width=chart_width, colorup='#ff1717', colordown='#53c156')

    
    plt.bar(range(len(data)), data['turnoverValue'], width=chart_width)
    ax2.set_ylabel('Volume')
    #ax2.xaxis.set_major_locator(locator)
    #ax2.xaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(ScalarFormatter())
    ax2.grid(True)
    
    plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')

    date_tickers=data.index
    
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)].strftime("%Y-%m-%d")
    
    ax1.xaxis.set_major_locator(MultipleLocator(5))
    ax2.xaxis.set_major_locator(MultipleLocator(5))
    ax2.xaxis.set_major_formatter(FuncFormatter(format_date))    
    
    #ax2.xaxis.set_major_formatter(FuncFormatter(format_date))
    #ax.set_xlabel(label)
    fig.suptitle(data.iloc[0]['id'], fontsize=12)
    
def draw2(data):    
    chart_width = 0.5
    fig = plt.figure()
    
    gs1 = GridSpec(4, 1)
    ax1 = plt.subplot(gs1[:-1, :])
    ax2 = plt.subplot(gs1[-1, :])
    
    locator = MonthLocator(bymonth=range(1, 13, 3))
    formatter = DateFormatter('%Y-%m')
    ax1.xaxis.set_major_locator(locator)
    #ax1.xaxis.set_major_formatter(NullFormatter())
    
    ax1.set_yscale('log')
    ax1.yaxis.set_major_locator(SymmetricalLogLocator(base=1.2, linthresh=1))
    ax1.yaxis.set_minor_locator(NullLocator())
    ax1.yaxis.set_major_formatter(ScalarFormatter())
    ax1.set_ylabel('Price')
    ax1.grid(True)
    
    quote = dataframe2quote(data)
    candlestick_ohlc(ax1, quote, width=chart_width, colorup='#ff1717', colordown='#53c156')

    
    plt.bar(data.index, data['turnoverValue'], width = 20)
    ax2.set_ylabel('Volume')
    ax2.xaxis.set_major_locator(locator)
    ax2.xaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(ScalarFormatter())
    ax2.grid(True)
    
    plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')
    fig.suptitle(data.iloc[0]['id'], fontsize=12)
      
    
def dataframe2quote(data):
    quote = []
    for i in range(data.shape[0]):
        d = data.iloc[i]
        time = date2num(data.index[i])
        quote.append((i, d.open, d.highest, d.lowest, d.close, d.turnoverValue))
    return quote
    
def day2month(data):
    data1 = data.resample('M', kind='period').apply(ohlc_dict)    
    data1 = data1.set_index(data1.index.start_time)
    return data1
    
def read_index_data(file_name):
    data1 = pd.read_csv(file_name)
    data1 = data1.set_index(pd.DatetimeIndex(data1['tradeDate']))
    return data1.rename(columns=index_dict)
    
def read_stock_data(file_name):
    data1 = pd.read_csv(file_name)
    data1 = data1.set_index(pd.DatetimeIndex(data1['tradeDate']))
    return data1.rename(columns=stock_dict)

    
if __name__ == '__main__':
    data1 = pd.read_csv('data/000016ZICN.csv')
    data1 = data1.set_index(pd.DatetimeIndex(data1['tradeDate']))

