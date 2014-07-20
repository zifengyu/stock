import pandas as pd

def read_stock_data(stock_id):
    file_name = '../data/' + stock_id + '.csv'
    return pd.read_csv(file_name, index_col=0)
    
def is_inner(sd, index):
    x = sd.ix[index - 1]
    y = sd.ix[index]
    return x.high >= y.high and x.low <= y.low

def is_outer(sd, index):
    x = sd.ix[index - 1]
    y = sd.ix[index]
    return x.high <= y.high and x.low >= y.low
    
def is_low(se, index):
    if index > 0 and index < len(se) - 1:
        if (se[index - 1] > se[index] < se[index + 1]):
            return True        
    return False

def cal_count(sd, func):
    ct = 0
    for i in range(2, len(sd.index)):
        if func(sd, i):
            ct += 1
    return ct
    

            