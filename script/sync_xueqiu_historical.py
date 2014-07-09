import pandas as pd
from pandas import DataFrame
import os




def sync_stock(stock_id):
    data_url  = 'http://xueqiu.com/S/' + stock_id + '/historical.csv'
    file_name = '../data/' + stock_id + '.csv'
    
    #Download historical data from Xueqiu and keep necessary columns
    df = pd.read_csv(data_url)
    df = DataFrame(df, columns = ['date', 'open', 'high', 'low', 'close', 'volume']) 
    
    #Load previous downloaded data from file
    if os.path.isfile(file_name):
        df2 = pd.read_csv(file_name)
    else:
        df2 = DataFrame()
    
    is_data_correct = True
    for i in df2.index:
        r = df.ix[i]
        r2 = df2.ix[i]
        if r['date'] != r2['date'] or abs(r['open'] - r2['open']) > 0.01 or abs(r['high'] - r2['high']) > 0.01       or abs(r['low'] - r2['low']) > 0.01        or abs(r['close'] - r2['close']) > 0.01 or abs(r['volume'] - r2['volume']) > 1:
            print stock_id, ',', i, ': Data is incorrect!'
            is_data_correct = False
            break
            
    if is_data_correct:
        df.to_csv(file_name, index = False)
        print stock_id, '... Completed'
        
def main():
    symbol_file = '../data/_symbols.txt'
    symbols = pd.read_csv(symbol_file, header=None)
    for i in symbols.index:
        row = symbols.ix[i]
        sync_stock(row[0])

if __name__ == '__main__':
    main()    