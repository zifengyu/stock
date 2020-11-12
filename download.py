import datetime
import shutil
import time
import random
import sqlite3

from tqdm import tqdm
import baostock as bs
import pandas as pd


START_DATE = '1990-01-01'
DB_FILE = 'data/market.db'
NOW = datetime.datetime.now()
BACKUP_FILE = 'data/market_{}{}{}.db'.format(NOW.year, NOW.month, NOW.day)

# 证券基本资料：query_stock_basic()
# 参数含义：
#   code：A股股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。可以为空；
#   code_name：股票名称，支持模糊查询，可以为空。
# 返回数据说明:
#   参数名称     参数描述
#   code        证券代码
#   code_name   证券名称
#   ipoDate	    上市日期
#   outDate 	退市日期
#   type	    证券类型，其中1：股票，2：指数,3：其它
#   status	    上市状态，其中1：上市，0：退市
def download_stock(conn):
    rs = bs.query_stock_basic()
    data_list = []
    while rs.error_code == '0' and rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)    
    result.to_sql("stock_basic", conn, if_exists="replace", index=False)
    print("stock basic:", result.shape)


# 获取历史A股K线数据：query_history_k_data_plus()

# 日线指标参数（包含停牌证券）
# 参数名称	参数描述	说明
# date	交易所行情日期	格式：YYYY-MM-DD
# code	证券代码	格式：sh.600000。sh：上海，sz：深圳
# open	今开盘价格	精度：小数点后4位；单位：人民币元
# high	最高价	精度：小数点后4位；单位：人民币元
# low	最低价	精度：小数点后4位；单位：人民币元
# close	今收盘价	精度：小数点后4位；单位：人民币元
# preclose	昨日收盘价	精度：小数点后4位；单位：人民币元
# volume	成交数量	单位：股
# amount	成交金额	精度：小数点后4位；单位：人民币元
# adjustflag	复权状态	不复权、前复权、后复权
# turn	换手率	精度：小数点后6位；单位：%
# tradestatus	交易状态	1：正常交易 0：停牌
# pctChg	涨跌幅（百分比）	精度：小数点后6位
# peTTM	滚动市盈率	精度：小数点后6位
# psTTM	滚动市销率	精度：小数点后6位
# pcfNcfTTM	滚动市现率	精度：小数点后6位
# pbMRQ	市净率	精度：小数点后6位
# isST	是否ST	1是，0否
def download_history_day(conn):
    df = pd.read_sql_query("select code from stock_basic", conn)
    cols = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
    
    first = True
    for c in tqdm(df['code']):
        # 日线"d"，后复权"2"
        rs = bs.query_history_k_data_plus(
            c,
            cols,
            start_date=START_DATE, frequency="d", adjustflag="2")

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        if first:
            result.to_sql("history_day", conn, if_exists="replace", index=False)
            first = False
        else:
            result.to_sql("history_day", conn, if_exists="append", index=False)
        time.sleep(random.random() / 2.0)


def vacuum(conn):
    conn.execute('VACUUM')


if __name__ == '__main__':    
    bs.login()    

    conn = sqlite3.connect(DB_FILE)
    download_stock(conn)
    download_history_day(conn)
    vacuum(conn)
    conn.close()

    shutil.copyfile(DB_FILE, BACKUP_FILE)
    bs.logout()