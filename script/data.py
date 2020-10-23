import os
import pandas as pd

# 合并利润表 (Point in time)
# [通联数据] - DataAPI.FdmtISGet
IS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'is')
IS_FILE = os.path.join(IS_FOLDER, 'is.csv')
IS_COL = {
    "ticker": "股票代码",           
    # "publishDate": "发布日期",     
    "endDate": "截止日期",          
    # "endDateRep": "报表截止日期",  
    "secShortName": "证券简称",   
    "tRevenue": "营业总收入",     
    # "revenue": "营业收入",
    "TCogs": "营业总成本",
    # "COGS": "营业成本",
    # "NIncome": "净利润",
    "NIncomeAttrP": "归属于母公司所有者的净利润",
    "basicEPS": "基本每股收益",
    "dilutedEPS": "稀释每股收益",
}

# 名称	类型	描述
# secID         str     证券内部ID
# partyID   	int	机构内部ID
# exchangeCD	str	通联编制的证券市场编码。例如，XSHG-上海证券交易所；XSHE-深圳证券交易所等。对应DataAPI.SysCodeGet.codeTypeID=10002。
# actPubtime	str	实际披露时间
# mergedFlag	str	合并类型。1-合并,2-母公司。对应DataAPI.SysCodeGet.codeTypeID=70003。
# reportType	str	报告类型。Q1-第一季报，S1-半年报，Q3-第三季报，CQ3-三季报（累计1-9月），A-年报。对应DataAPI.SysCodeGet.codeTypeID=70001。
# fiscalPeriod	str	会计期间
# accoutingStandards	str	会计准则
# currencyCD	str	货币代码。例如，USD-美元；CAD-加元等。对应DataAPI.SysCodeGet.codeTypeID=10004。
# intIncome	float	利息收入
# intExp	float	利息支出
# premEarned	float	已赚保费
# commisIncome	float	手续费及佣金收入
# commisExp	float	手续费及佣金支出
# premRefund	float	退保金
# NCompensPayout	float	赔付支出净额
# reserInsurContr	float	提取保险合同准备金净额
# policyDivPayt	float	保单红利支出
# reinsurExp	float	分保费用
# bizTaxSurchg	float	营业税金及附加
# sellExp	float	销售费用
# adminExp	float	管理费用
# finanExp	float	财务费用
# assetsImpairLoss	float	资产减值损失
# fValueChgGain	float	公允价值变动收益
# investIncome	float	投资收益
# AJInvestIncome	float	其中:对联营企业和合营企业的投资收益
# forexGain	float	汇兑收益
# assetsDispGain	float	资产处置收益
# othGain	float	其他收益
# operateProfit	float	营业利润
# NoperateIncome	float	营业外收入
# NoperateExp	float	营业外支出
# NCADisploss	float	非流动资产处置损失
# TProfit	float	利润总额
# incomeTax	float	所得税费用
# goingConcernNI	float	持续经营净利润
# quitConcernNI	float	终止经营净利润
# minorityGain	float	少数股东损益
# othComprIncome	float	其他综合收益
# TComprIncome	float	综合收益总额
# comprIncAttrP	float	归属于母公司所有者的综合收益总额
# comprIncAttrMS	float	归属于少数股东的综合收益总额
# updateTime	str	更新时间
def get_IS(ticker=None):
    """
    获取利润表
    """   
    data = pd.read_csv(IS_FILE, dtype={'ticker': str})
    data.drop_duplicates(subset=['ticker', 'endDate'], keep='first', inplace=True)
    data = data[IS_COL.keys()]
    data = data.rename(columns=IS_COL)
    if ticker:
        data = data[data['股票代码'] == ticker].copy()
    return data


# 合并利润表（单季度，根据所有会计期末最新披露数据计算）
# [通联数据] - DataAPI.FdmtISQGet
ISQ_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'isq')
ISQ_FILE = os.path.join(ISQ_FOLDER, 'isq.csv')
ISQ_COL = {
    "ticker": "股票代码",                 
    "endDate": "截止日期",              
    "secShortName": "证券简称",   
    # "tRevenue": "营业总收入",     
    "revenue": "营业收入",
    # "NIncome": "净利润",
    "NIncomeAttrP": "归属于母公司所有者的净利润",
}
# 名称	类型	描述
# secID	str	证券编码
# partyID	int	机构编码
# exchangeCD	str	通联编制的证券市场编码。XSHG-上海证券交易所；XSHE-深圳证券交易所。对应DataAPI.SysCodeGet.codeTypeID=10002。
# intIncome	float	利息收入
# premEarned	float	已赚保费
# commisIncome	float	手续费及佣金收入
# TCogs	float	营业总成本
# COGS	float	营业成本
# intExp	float	利息支出
# commisExp	float	手续费及佣金支出
# premRefund	float	退保金
# NCompensPayout	float	赔付支出净额
# reserInsurContr	float	提取保险合同准备金净额
# policyDivPayt	float	保单红利支出
# reinsurExp	float	分保费用
# bizTaxSurchg	float	营业税金及附加
# sellExp	float	销售费用
# adminExp	float	管理费用
# finanExp	float	财务费用
# assetsImpairLoss	float	资产减值损失
# fValueChgGain	float	公允价值变动收益
# investIncome	float	投资收益
# AJInvestIncome	float	其中:对联营企业和合营企业的投资收益
# forexGain	float	汇兑收益
# assetsDispGain	float	资产处置收益
# othGain	float	其他收益
# operateProfit	float	营业利润
# NoperateIncome	float	营业外收入
# NoperateExp	float	营业外支出
# NCADisploss	float	非流动资产处置损失
# TProfit	float	利润总额
# incomeTax	float	所得税费用
# goingConcernNI	float	持续经营净利润
# quitConcernNI	float	终止经营净利润
# minorityGain	float	少数股东损益
# othComprIncome	float	其他综合收益
# TComprIncome	float	综合收益总额
# comprIncAttrP	float	归属于母公司所有者的综合收益总额
# comprIncAttrMS	float	归属于少数股东的综合收益总额
def get_ISQ(ticker=None):
    """
    获取季度利润表
    """   
    data = pd.read_csv(ISQ_FILE, dtype={'ticker': str})
    data.drop_duplicates(subset=['ticker', 'endDate'], keep='first', inplace=True)
    data = data[ISQ_COL.keys()]
    data = data.rename(columns=ISQ_COL)
    if ticker:
        data = data[data['股票代码'] == ticker].copy()
    return data


MKT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'market')
MKT_COL = {           
    "tradeDate": "交易日期",              
    "closePrice": "收盘价",     
    "accumAdjFactor": "累积前复权因子",
    "PE": "滚动市盈率",
}
# 名称	类型	描述
# secID	str	通联编制的证券编码，可使用DataAPI.SecIDGet获取
# ticker	str	通用交易代码
# secShortName	str	证券简称
# exchangeCD	str	通联编制的交易市场编码
# tradeDate	str	交易日期
# preClosePrice	float	昨收盘(前复权)
# actPreClosePrice	float	实际昨收盘价(未复权)
# openPrice	float	开盘价
# highestPrice	float	最高价
# lowestPrice	float	最低价
# closePrice	float	收盘价
# turnoverVol	float	成交量
# turnoverValue	float	成交金额，A股单位为元，B股单位为美元或港币
# dealAmount	int	成交笔数
# turnoverRate	float	日换手率，成交量/无限售流通股数
# accumAdjFactor	float	累积前复权因子，前复权价=未复权价*累积前复权因子。前复权是对历史行情进行调整，除权除息当日的行情无需调整。最近一次除权除息日至最新交易日期间的价格也无需调整，该期间前复权因子等于1。
# negMarketValue	float	流通市值，收盘价*无限售流通股数
# marketValue	float	总市值，收盘价*总股本数
# chgPct	float	涨跌幅，收盘价/昨收盘价-1
# PE	float	滚动市盈率，即市盈率TTM，总市值/归属于母公司所有者的净利润TTM
# PE1	float	动态市盈率，总市值/归属于母公司所有者的净利润（最新一期财报年化）
# PB	float	市净率，总市值/归属于母公司所有者权益合计
# isOpen	int	股票今日是否开盘标记：0-未开盘，1-交易日
# vwap	float	VWAP，成交金额/成交量
def get_market(ticker):
    data_file = os.path.join(MKT_FOLDER, ticker+".csv")
    data = pd.read_csv(data_file, dtype={'ticker': str})
    data['tradeDate'] = pd.to_datetime(data['tradeDate'])
    data = data[MKT_COL.keys()]
    data = data.rename(columns=MKT_COL)
    return data
