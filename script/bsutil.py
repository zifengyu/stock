import baostock as bs
import pandas as pd

START_DATE = '2010-01-01'

def get_price_daily(code):
    bs.login()
    rs = bs.query_history_k_data_plus(
        code, "date,open,high,low,close,volume,peTTM", start_date=START_DATE, frequency='d', adjustflag='2')    
    data_list = []
    while rs.error_code == '0' and rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    bs.logout()
    result[['open','high','low','close','volume','peTTM']] = result[['open','high','low','close','volume','peTTM']].astype('float64')
    return result


def get_bs_code(ticker):
    if ticker.startswith('6'):
        ticker = "sh." + ticker
    else:
        ticker = "sz." + ticker
    return ticker