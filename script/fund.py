import sqlite3
import os

import pandas as pd

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def load_fund():
    DB_FILE = "stock.db"
    TABLE_NAME = "funds"
    
    with sqlite3.connect(os.path.join(DIR_PATH, '..', DB_FILE)) as conn:
        df = pd.read_sql_query("select * from {}".format(TABLE_NAME), conn)
        
    return df
    
    
def load_fund_holding():
    DB_FILE = "stock.db"
    TABLE_NAME = "fund_holdings"
    
    with sqlite3.connect(os.path.join(DIR_PATH, '..', DB_FILE)) as conn:
        df = pd.read_sql_query("select * from {} where holdingsecType=\"E\"".format(TABLE_NAME), conn)
        df = df.drop(['ticker', 'holdingsecType', 'holdingTicker', 'holdingExchangeCd', 'currencyCd'], axis=1)

    return df
    