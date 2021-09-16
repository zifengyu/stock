import os
import sqlite3
import pandas as pd

# 合并利润表 (Point in time)
# [通联数据] - DataAPI.FdmtISGet
IS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'is')
IS_FILE = os.path.join(IS_FOLDER, 'is.csv.gz')
IS_COL = {
    "ticker": "股票代码",
    # "publishDate": "发布日期",
    "endDate": "截止日期",
    # "endDateRep": "报表截止日期",
    "secShortName": "证券简称",
    "tRevenue": "营业总收入",
    "revenue": "营业收入",
    "TCogs": "营业总成本",
    "COGS": "营业成本",
    "TProfit": "利润总额",
    "NIncome": "净利润",
    # "goingConcernNI": "持续经营净利润",
    "NIncomeAttrP": "归属于母公司所有者的净利润",
    "basicEPS": "基本每股收益",
    "dilutedEPS": "稀释每股收益",
}

# 名称	类型	描述
# secID	str	证券内部ID
# publishDate	str	发布日期
# endDate	str	截止日期
# endDateRep	str	报表截止日期
# partyID	int	机构内部ID
# ticker	str	股票代码
# secShortName	str	证券简称
# exchangeCD	str	通联编制的证券市场编码。例如，XSHG-上海证券交易所；XSHE-深圳证券交易所等。对应DataAPI.SysCodeGet.codeTypeID=10002。
# actPubtime	str	实际披露时间
# mergedFlag	str	合并类型。1-合并,2-母公司。对应DataAPI.SysCodeGet.codeTypeID=70003。
# reportType	str	报告类型。Q1-第一季报，S1-半年报，Q3-第三季报，CQ3-三季报（累计1-9月），A-年报。对应DataAPI.SysCodeGet.codeTypeID=70001。
# fiscalPeriod	str	会计期间
# accoutingStandards	str	会计准则
# currencyCD	str	货币代码。例如，USD-美元；CAD-加元等。对应DataAPI.SysCodeGet.codeTypeID=10004。
# tRevenue	float	营业总收入
# revenue	float	营业收入
# intIncome	float	利息收入
# intExp	float	利息支出
# premEarned	float	已赚保费
# commisIncome	float	手续费及佣金收入
# commisExp	float	手续费及佣金支出
# TCogs	float	营业总成本
# COGS	float	营业成本
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
# NIncome	float	净利润
# goingConcernNI	float	持续经营净利润
# quitConcernNI	float	终止经营净利润
# NIncomeAttrP	float	归属于母公司所有者的净利润
# minorityGain	float	少数股东损益
# basicEPS	float	基本每股收益
# dilutedEPS	float	稀释每股收益
# othComprIncome	float	其他综合收益
# TComprIncome	float	综合收益总额
# comprIncAttrP	float	归属于母公司所有者的综合收益总额
# comprIncAttrMS	float	归属于少数股东的综合收益总额
# updateTime	str	更新时间

def get_IS(ticker=None):
    """
    获取利润表
    """
    data = pd.read_csv(IS_FILE, dtype={'ticker': str}, compression='gzip')
    data.drop_duplicates(subset=['ticker', 'endDate'], keep='first', inplace=True)
    data = data[IS_COL.keys()]
    data = data.rename(columns=IS_COL)
    if ticker:
        data = data[data['股票代码'] == ticker].copy()
    return data


# 合并利润表（单季度，根据所有会计期末最新披露数据计算）
# [通联数据] - DataAPI.FdmtISQGet
ISQ_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'isq')
ISQ_FILE = os.path.join(ISQ_FOLDER, 'isq.csv.gz')
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
    data = pd.read_csv(ISQ_FILE, dtype={'ticker': str}, compression='gzip')
    data.drop_duplicates(subset=['ticker', 'endDate'], keep='first', inplace=True)
    data = data[ISQ_COL.keys()]
    data = data.rename(columns=ISQ_COL)
    if ticker:
        data = data[data['股票代码'] == ticker].copy()
    return data


MKT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'market')
# MKT_FILE = os.path.join(MKT_FOLDER, 'market.csv')
MKT_COL = {
    "ticker": "通用交易代码",
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
def get_market(ticker=None):
    if ticker is None:
        return None

    f = os.path.join(MKT_FOLDER, ticker+'.csv')
    data = pd.read_csv(f, dtype={'ticker': str})
    data['tradeDate'] = pd.to_datetime(data['tradeDate'])
    data = data[MKT_COL.keys()]
    data = data.rename(columns=MKT_COL)
    return data


DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'market.db')
def get_market2(ticker):
    if ticker.startswith('6'):
        ticker = "sh." + ticker
    else:
        ticker = "sz." + ticker
    conn = sqlite3.connect(DB_FILE)
    # date	交易所行情日期	格式：YYYY-MM-DD
    # code	证券代码	格式：sh.600000。sh：上海，sz：深圳
    # close	今收盘价	精度：小数点后4位；单位：人民币元
    # peTTM	滚动市盈率	精度：小数点后6位
    results =[]
    for r in conn.execute('SELECT code, date, close, peTTM from history_day where code="{}"'.format(ticker)):
        results.append(r)
    conn.close()
    df = pd.DataFrame(results, columns=["通用交易代码","交易日期","前复权","滚动市盈率"])
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    return df

BS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'bs')
BS_FILE = os.path.join(BS_FOLDER, 'bs.csv.gz')
BS_COL = {
    "ticker": "股票代码",
    "endDate": "截止日期",
    "cashCEquiv": "货币资金",
    "inventories": "存货",
    "AR": "应收账款",
    "TCA": "流动资产合计",
    "fixedAssets": "固定资产",
    "TNCA": "非流动资产合计",
    "TAssets": "资产总计",
    "AP": "应付账款",
    "TLiab": "负债合计",
    "othEquityInstr": "其他权益工具",
    "TShEquity": "所有者权益合计",
}
# 名称	类型	描述
# secID	str	证券内部ID
# publishDate	str	发布日期
# endDate	str	截止日期
# endDateRep	str	报表截止日期
# partyID	int	机构内部ID
# ticker	str	股票代码
# secShortName	str	证券简称
# exchangeCD	str	通联编制的证券市场编码。例如，XSHG-上海证券交易所；XSHE-深圳证券交易所等。对应DataAPI.SysCodeGet.codeTypeID=10002。
# actPubtime	str	实际披露时间
# mergedFlag	str	合并类型。1-合并,2-母公司。对应DataAPI.SysCodeGet.codeTypeID=70003。
# reportType	str	报告类型。Q1-一季度，S1-半年度，Q3-三季度，A-年度。对应DataAPI.SysCodeGet.codeTypeID=70001。
# fiscalPeriod	str	会计期间
# accoutingStandards	str	会计准则
# currencyCD	str	货币代码。例如，USD-美元；CAD-加元等。对应DataAPI.SysCodeGet.codeTypeID=10004。
# cashCEquiv	float	货币资金
# settProv	float	结算备付金
# loanToOthBankFi	float	拆出资金
# tradingFA	float	交易性金融资产
# NotesReceiv	float	应收票据
# AR	float	应收账款
# prepayment	float	预付款项
# premiumReceiv	float	应收保费
# reinsurReceiv	float	应收分保账款
# reinsurReserReceiv	float	应收分保合同准备金
# intReceiv	float	应收利息
# divReceiv	float	应收股利
# othReceiv	float	其他应收款
# purResaleFa	float	买入返售金融资产
# inventories	float	存货
# NCAWithin1Y	float	一年内到期的非流动资产
# othCA	float	其他流动资产
# TCA	float	流动资产合计
# disburLA	float	发放委托贷款及垫款
# availForSaleFa	float	可供出售金融资产
# htmInvest	float	持有至到期投资
# LTReceive	float	长期应收款
# LTEquityInvest	float	长期股权投资
# investRealEstate	float	投资性房地产
# fixedAssets	float	固定资产
# CIP	float	在建工程
# constMaterials	float	工程物资
# fixedAssetsDisp	float	固定资产清理
# producBiolAssets	float	生产性生物资产
# oilAndGasAssets	float	油气资产
# intanAssets	float	无形资产
# RD	float	开发支出
# goodwill	float	商誉
# LTAmorExp	float	长期待摊费用
# deferTaxAssets	float	递延所得税资产
# othNCA	float	其他非流动资产
# TNCA	float	非流动资产合计
# TAssets	float	资产总计
# STBorr	float	短期借款
# CBBorr	float	向中央银行借款
# depos	float	吸收存款及同业存放
# loanFrOthBankFi	float	拆入资金
# tradingFL	float	交易性金融负债
# NotesPayable	float	应付票据
# AP	float	应付账款
# advanceReceipts	float	预收款项
# soldForRepurFa	float	卖出回购金融资产款
# commisPayable	float	应付手续费及佣金
# payrollPayable	float	应付职工薪酬
# taxesPayable	float	应交税费
# intPayable	float	应付利息
# divPayable	float	应付股利
# othPayable	float	其他应付款
# reinsurPayable	float	应付分保账款
# insurReser	float	保险合同准备金
# fundsSecTradAgen	float	代理买卖证券款
# fundsSecUndwAgen	float	代理承销证券款
# NCLWithin1Y	float	一年内到期的非流动负债
# othCL	float	其他流动负债
# TCL	float	流动负债合计
# LTBorr	float	长期借款
# bondPayable	float	应付债券
# preferredStockL	float	其中：优先股
# perpetualBondL	float	其中：永续债
# LTPayable	float	长期应付款
# specificPayables	float	专项应付款
# estimatedLiab	float	预计负债
# deferTaxLiab	float	递延所得税负债
# othNCL	float	其他非流动负债
# TNCL	float	非流动负债合计
# TLiab	float	负债合计
# paidInCapital	float	实收资本(或股本)
# othEquityInstr	float	其他权益工具
# preferredStockE	float	其中：优先股
# perpetualBondE	float	其中：永续债
# capitalReser	float	资本公积
# treasuryShare	float	减:库存股
# othCompreIncome	float	其他综合收益
# specialReser	float	专项储备
# surplusReser	float	盈余公积
# ordinRiskReser	float	一般风险准备
# retainedEarnings	float	未分配利润
# forexDiffer	float	外币报表折算差额
# TEquityAttrP	float	归属于母公司所有者权益合计
# minorityInt	float	少数股东权益
# TShEquity	float	所有者权益合计
# TLiabEquity	float	负债和所有者权益总计
# updateTime	str	更新时间
def get_BS(ticker=None):
    """
    获取资产负债表
    """
    data = pd.read_csv(BS_FILE, dtype={'ticker': str}, compression='gzip')
    data.drop_duplicates(subset=['ticker', 'endDate'], keep='first', inplace=True)
    data = data[BS_COL.keys()]
    data = data.rename(columns=BS_COL)
    if ticker:
        data = data[data['股票代码'] == ticker].copy()
    return data


CF_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'cf')
CF_FILE = os.path.join(CF_FOLDER, 'cf.csv.gz')
CF_COL = {
    "ticker": "股票代码",
    "endDate": "截止日期",
    "CInfFrOperateA": "经营活动现金流入小计",
    "COutfOperateA": "经营活动现金流出小计",
    "NCFOperateA": "经营活动产生的现金流量净额",
    "CInfFrInvestA": "投资活动现金流入小计",
    "COutfFrInvestA": "投资活动现金流出小计",
    "NCFFrInvestA": "投资活动产生的现金流量净额",
    "CInfFrFinanA": "筹资活动现金流入小计",
    "COutfFrFinanA": "筹资活动现金流出小计",
    "NCFFrFinanA": "筹资活动产生的现金流量净额",
    "NChangeInCash": "现金及现金等价物净增加额",
}

# 名称	类型	描述
# secID	str	证券内部ID
# publishDate	str	发布日期
# endDate	str	截止日期
# endDateRep	str	报表截止日期
# partyID	int	机构内部ID
# ticker	str	股票代码
# secShortName	str	证券简称
# exchangeCD	str	通联编制的证券市场编码。例如，XSHG-上海证券交易所；XSHE-深圳证券交易所等。对应DataAPI.SysCodeGet.codeTypeID=10002。
# actPubtime	str	实际披露时间
# mergedFlag	str	合并类型。1-合并,2-母公司。对应DataAPI.SysCodeGet.codeTypeID=70003。
# reportType	str	报告类型。Q1-第一季报，S1-半年报，Q3-第三季报，CQ3-三季报（累计1-9月），A-年报。对应DataAPI.SysCodeGet.codeTypeID=70001。
# fiscalPeriod	str	会计期间
# accoutingStandards	str	会计准则
# currencyCD	str	货币代码。例如，USD-美元；CAD-加元等。对应DataAPI.SysCodeGet.codeTypeID=10004。
# CFrSaleGS	float	销售商品、提供劳务收到的现金
# NDeposIncrCFI	float	客户存款和同业存放款项净增加额
# NIncrBorrFrCB	float	向中央银行借款净增加额
# NIncBorrOthFI	float	向其他金融机构拆入资金净增加额
# premFrOrigContr	float	收到原保险合同保费取得的现金
# NReinsurPrem	float	收到再保险业务现金净额
# NIncPhDeposInv	float	保户储金及投资款净增加额
# NIncDispTradFA	float	处置交易性金融资产净增加额
# IFCCashIncr	float	收取利息、手续费及佣金的现金
# NIncFrBorr	float	拆入资金净增加额
# NCApIncrRepur	float	回购业务资金净增加额
# refundOfTax	float	收到的税费返还
# CFrOthOperateA	float	收到其他与经营活动有关的现金
# CInfFrOperateA	float	经营活动现金流入小计
# CPaidGS	float	购买商品、接受劳务支付的现金
# NIncDisburOfLA	float	客户贷款及垫款净增加额
# NIncrDeposInFI	float	存放中央银行和同业款项净增加额
# origContrCIndem	float	支付原保险合同赔付款项的现金
# CPaidIFC	float	支付利息、手续费及佣金的现金
# CPaidPolDiv	float	支付保单红利的现金
# CPaidToForEmpl	float	支付给职工以及为职工支付的现金
# CPaidForTaxes	float	支付的各项税费
# CPaidForOthOpA	float	支付其他与经营活动有关的现金
# COutfOperateA	float	经营活动现金流出小计
# NCFOperateA	float	经营活动产生的现金流量净额
# procSellInvest	float	收回投资收到的现金
# gainInvest	float	取得投资收益收到的现金
# dispFixAssetsOth	float	处置固定资产、无形资产和其他长期资产收回的现金净额
# NDispSubsOthBizC	float	处置子公司及其他营业单位收到的现金净额
# CFrOthInvestA	float	收到其他与投资活动有关的现金
# CInfFrInvestA	float	投资活动现金流入小计
# purFixAssetsOth	float	购建固定资产、无形资产和其他长期资产支付的现金
# CPaidInvest	float	投资支付的现金
# NIncrPledgeLoan	float	质押贷款净增加额
# NCPaidAcquis	float	取得子公司及其他营业单位支付的现金净额
# CPaidOthInvestA	float	支付其他与投资活动有关的现金
# COutfFrInvestA	float	投资活动现金流出小计
# NCFFrInvestA	float	投资活动产生的现金流量净额
# CFrCapContr	float	吸收投资收到的现金
# CFrMinoSSubs	float	其中:子公司吸收少数股东投资收到的现金
# CFrBorr	float	取得借款收到的现金
# CFrIssueBond	float	发行债券收到的现金
# CFrOthFinanA	float	收到其他与筹资活动有关的现金
# CInfFrFinanA	float	筹资活动现金流入小计
# CPaidForDebts	float	偿还债务支付的现金
# CPaidDivProfInt	float	分配股利、利润或偿付利息支付的现金
# divProfSubsMinoS	float	其中:子公司支付给少数股东的股利、利润
# CPaidOthFinanA	float	支付其他与筹资活动有关的现金
# COutfFrFinanA	float	筹资活动现金流出小计
# NCFFrFinanA	float	筹资活动产生的现金流量净额
# forexEffects	float	汇率变动对现金及现金等价物的影响
# NChangeInCash	float	现金及现金等价物净增加额
# NCEBegBal	float	加:期初现金及现金等价物余额
# NCEEndBal	float	期末现金及现金等价物余额
# updateTime	str	更新时间
def get_CF(ticker=None):
    """
    获取现金流量表
    """
    data = pd.read_csv(CF_FILE, dtype={'ticker': str}, compression='gzip')
    data.drop_duplicates(subset=['ticker', 'endDate'], keep='first', inplace=True)
    data = data[CF_COL.keys()]
    data = data.rename(columns=CF_COL)
    if ticker:
        data = data[data['股票代码'] == ticker].copy()
    return data


def merge_data():
    data = pd.read_csv(IS_FILE, dtype={'ticker': str}, compression='gzip')
    files = [f for f in os.listdir(IS_FOLDER) if f.endswith('.csv')]
    if len(files) > 0:
        for f in files:
            print("process", f)
            data_file = os.path.join(IS_FOLDER, f)
            data = data.append(pd.read_csv(data_file, dtype={'ticker': str}), ignore_index=True)
        data = data.sort_values(by=['ticker', 'publishDate'], ascending=False)
        data.drop_duplicates(subset=['ticker', 'publishDate', 'endDate', 'endDateRep', 'actPubtime'], keep='first', inplace=True)
        data.to_csv(IS_FILE, index=False, compression='gzip')

    data = pd.DataFrame()
    files = [f for f in os.listdir(ISQ_FOLDER) if f.endswith('.csv')]
    if len(files) > 0:
        for f in files:
            print("process", f)
            data_file = os.path.join(ISQ_FOLDER, f)
            data = data.append(pd.read_csv(data_file, dtype={'ticker': str}), ignore_index=True)
        data = data.append(pd.read_csv(ISQ_FILE, dtype={'ticker': str}, compression='gzip'))
        data = data.sort_values(by=['ticker', 'endDate'], ascending=False)
        data.drop_duplicates(subset=['ticker', 'endDate'], keep='first', inplace=True)
        data.to_csv(ISQ_FILE, index=False, compression='gzip')

    data = pd.read_csv(BS_FILE, dtype={'ticker': str}, compression='gzip')
    files = [f for f in os.listdir(BS_FOLDER) if f.endswith('.csv')]
    if len(files) > 0:
        for f in files:
            print("process", f)
            data_file = os.path.join(BS_FOLDER, f)
            data = data.append(pd.read_csv(data_file, dtype={'ticker': str}), ignore_index=True)
        data = data.sort_values(by=['ticker', 'publishDate'], ascending=False)
        data.drop_duplicates(subset=['ticker', 'publishDate', 'endDate', 'endDateRep', 'actPubtime'], keep='first', inplace=True)
        data.to_csv(BS_FILE, index=False, compression='gzip')

    # data = pd.DataFrame()
    # files = [f for f in os.listdir(MKT_FOLDER) if f.endswith('.csv')]
    # for f in files:
    #     data_file = os.path.join(MKT_FOLDER, f)
    #     data = data.append(pd.read_csv(data_file, dtype={'ticker': str}), ignore_index=True)
    # data.drop_duplicates(subset=['ticker', 'tradeDate'], keep='first', inplace=True)
    # for t in data['ticker'].unique():
    #     data_file = os.path.join(MKT_FOLDER, t+'.csv')
    #     data[data['ticker'] == t].to_csv(data_file, index=False)
