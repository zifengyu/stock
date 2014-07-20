import pandas as pd

def read_stock_data(stock_id):
    file_name = '../data/' + stock_id + '.csv'
    return pd.read_csv(file_name)
    
def is_inner(sd, index):
    x = sd.ix[index - 1]
    y = sd.ix[index]
    return x.high >= y.high and x.low <= y.low

def is_outer(sd, index):
    x = sd.ix[index - 1]
    y = sd.ix[index]
    return x.high <= y.high and x.low >= y.low

def cal_count(sd, func):
    ct = 0
    for i in sd[1:].index:
        if func(sd, i):
            ct += 1
    return ct
    

            