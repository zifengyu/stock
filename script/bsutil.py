import baostock as bs
import datetime
import pandas as pd

START_DATE = '2010-01-01'

def get_price_daily(code):
    rs = bs.query_history_k_data_plus(
        code, "date,open,high,low,close,volume,peTTM", start_date=START_DATE, frequency='d', adjustflag='2')    
    data_list = []
    while rs.error_code == '0' and rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result = result[result['volume'] != '']
    result[['open','high','low','close','volume','peTTM']] = result[['open','high','low','close','volume','peTTM']].astype('float64', errors='ignore')
    return result


def get_price_weekly(code):    
    rs = bs.query_history_k_data_plus(
        code, "date,open,high,low,close,volume", start_date=START_DATE, frequency='w', adjustflag='2')    
    data_list = []
    while rs.error_code == '0' and rs.next():        
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result = result[result['volume'] != '']
    result[['open','high','low','close','volume']] = result[['open','high','low','close','volume']].astype('float64', errors='ignore')
    return result


# 季频盈利能力：query_profit_data()
# 返回数据说明
# 参数名称	参数描述	算法说明
# code	证券代码	
# pubDate	公司发布财报的日期	
# statDate	财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30	
# roeAvg	净资产收益率(平均)(%)	归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
# npMargin	销售净利率(%)	净利润/营业收入*100%
# gpMargin	销售毛利率(%)	毛利/营业收入*100%=(营业收入-营业成本)/营业收入*100%
# netProfit	净利润(元)	
# epsTTM	每股收益	归属母公司股东的净利润TTM/最新总股本
# MBRevenue	主营营业收入(元)	
# totalShare	总股本	
# liqaShare	流通股本	
def get_profit_data(code):
    cols = {                   
        "netProfit": "净利润",
        "epsTTM": "每股收益",
        "pubDate": "发布日期",
    }
    profit_list = []
    fields = None
    current_year = datetime.datetime.now().year
    for year in range(current_year, current_year-5, -1):
        for quarter in range(4, 0, -1):
            rs_profit = bs.query_profit_data(code=code, year=year, quarter=quarter)
            while rs_profit.error_code == '0' and rs_profit.next():        
                profit_list.append(rs_profit.get_row_data())
                if fields is None:
                    fields = rs_profit.fields
    result_profit = pd.DataFrame(profit_list, columns=fields)
    result_profit.set_index('statDate', inplace=True)  
    result_profit['netProfit'] = result_profit['netProfit'].astype('float64').astype('int')
    result_profit['epsTTM'] = result_profit['epsTTM'].astype('float64').round(3)
    result_profit = result_profit[cols.keys()]
    result_profit = result_profit.rename(columns=cols)
    return result_profit



def get_bs_code(ticker):
    if ticker.startswith('6'):
        ticker = "sh." + ticker
    else:
        ticker = "sz." + ticker
    return ticker
