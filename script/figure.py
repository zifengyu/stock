import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, WeekdayLocator, HourLocator, DayLocator, MONDAY
from matplotlib.finance import candlestick, plot_day_summary, candlestick2, date2num, datetime

def draw(data):
    fig, ax = plt.subplots()
    alldays = DayLocator()
    dayFormatter = DateFormatter('%m-%d')
    ax.xaxis.set_major_locator(alldays)
    ax.xaxis.set_major_formatter(dayFormatter)
    candlestick(ax, dataframe2quote(data), width=0.6)
    plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')
    
def dataframe2quote(data):
    quote = []
    for i in data.index:
        d = data.ix[i]
        time = date2num(datetime.date(int(d.date[0:4]), int(d.date[5:7]), int(d.date[8:10])))
        quote.append((time, d.open, d.close, d.high, d.low, d.volume))
    return quote
    
    