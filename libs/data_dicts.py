#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import time
from dataclasses import dataclass, is_dataclass
from typing import List
from sqlalchemy.types import Integer, String, Date, Unicode, Numeric, CHAR
from sqlalchemy import Column
from functools import partial

DefaultColumn = partial(Column, nullable=False)


def nested_dataclass(*args, **kwargs):
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args_, **kwargs_):
            for name, value in kwargs_.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs_[name] = new_obj
            original_init(self, *args_, **kwargs_)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


@nested_dataclass(frozen=True, eq=False)
class DataTable:
    """数据类，用于存放表结构"""
    description: str
    reference: str
    frequency: str
    update_time: time
    columns: List[Column]


data_sources = {
    'tushare.pro_api.daily':
        DataTable(description='股市日线数据',
                  reference='https://tushare.pro/document/2?doc_id=27',
                  frequency='daily',
                  update_time=time.fromisoformat('17:30:00+08:00'),
                  columns=[
                      DefaultColumn('ts_code', String(16), comment='股票代码', primary_key=True),
                      DefaultColumn('trade_date', Date, comment='交易日期', primary_key=True),
                      DefaultColumn('open', Numeric(10, 2), comment='开盘价'),
                      DefaultColumn('high', Numeric(10, 2), comment='最高价'),
                      DefaultColumn('low', Numeric(10, 2), comment='最低价'),
                      DefaultColumn('close', Numeric(10, 2), comment='收盘价'),
                      DefaultColumn('pre_close', Numeric(10, 2), comment='昨收价'),
                      DefaultColumn('change', Numeric(10, 2), comment='涨跌额（未复权）'),
                      DefaultColumn('pct_chg', Numeric(10, 4), comment='涨跌幅（未复权）'),
                      DefaultColumn('vol', Integer, comment='成交量（手）'),
                      DefaultColumn('amount', Numeric(12, 3), comment='成交额（千元）'),
                  ]
                  )
}

# data_sources = {
#     'tushare.pro_api.daily':
#         DataTable(description='股市日线数据',
#                   frequency='daily',
#                   update_time=time.fromisoformat('17:30:00+08:00'),
#                   columns=[
#                       DataColumn('date', '日期', Date, is_primary_key=True),
#                       DataColumn('code', '代码', String(16), is_primary_key=True),
#                       DataColumn('market', '市场', String(16), is_primary_key=True),
#                       DataColumn('name', '名称', Unicode),
#                       DataColumn('change_percent', '涨跌幅', Numeric(10, 4)),
#                       DataColumn('trade', '现价', Numeric(10, 2)),
#                       DataColumn('open', '开盘价', Numeric(10, 2)),
#                       DataColumn('high', '最高价', Numeric(10, 2)),
#                       DataColumn('low', '最低价', Numeric(10, 2)),
#                       DataColumn('adjust_before', '复权因子', Numeric(10, 3)),
#                       DataColumn('settlement', '昨日收盘价', Numeric(10, 2)),
#                       DataColumn('volume', '成交量', Integer),
#                       DataColumn('turnover_ratio', '换手率', Numeric(10, 4)),
#                       DataColumn('amount', '成交额', Numeric(10, 2)),
#                       DataColumn('per', '市盈率', Numeric(10, 4)),
#                       DataColumn('pb', '市净率', Numeric(10, 4)),
#                       DataColumn('market_cap', '总市值', Numeric(10, 2)),
#                       DataColumn('nmc', '流通市值', Numeric(10, 2)), ],
#                   )}

# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="基本面数据",
#         name="股票列表",
#         table_name="ts_stock_basics",
#         columns=["code", "name", "industry", "area", "pe", "outstanding", "totals", "totalAssets", "liquidAssets",
#                  "fixedAssets", "reserved", "reservedPerShare", "esp", "bvps", "pb", "timeToMarket",
#                  "undp", "perundp", "rev", "profit", "gpr", "npr", "holders"],
#         column_names=["代码", "名称", "所属行业", "地区", "市盈率", "流通股本(亿)", "总股本(亿)", "总资产(万)", "流动资产",
#                       "固定资产", "公积金", "每股公积金", "每股收益", "每股净资", "市净率", "上市日期", "未分利润",
#                       "每股未分配", "收入同比(%)", "利润同比(%)", "毛利率(%)", "净利润率(%)", "股东人数"
#                       ],
#         primary_key=[],
#         order_by=" code asc "
#     )
# )

# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="基本面数据",
#         name="沪深300成份股",
#         table_name="ts_stock_hs300s",
#         columns=["code", "name", "weight"],
#         column_names=["代码", "名称", "权重"],
#         primary_key=[],
#         order_by=" code asc "
#     )
# )

# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="基本面数据",
#         name="中证500成份股",
#         table_name="ts_stock_zz500s",
#         columns=["code", "name", "weight"],
#         column_names=["代码", "名称", "权重"],
#         primary_key=[],
#         order_by=" code asc "
#     )
# )

# "code", "name: pchange", "amount", "buy", "bratio", "sell", "sratio", "reason", "date"
# 代码 名称 当日涨跌幅 龙虎榜成交额(万) 买入额(万) 买入占总成交比例 卖出额(万) 卖出占总成交比例 上榜原因 日期


# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="每日数据",
#         name="龙虎榜",
#         table_name="ts_top_list",
#         columns=["date", "code", "name", "pchange", "amount", "buy", "bratio", "sell", "sratio", "reason"],
#         column_names=["日期", "代码", "名称", "当日涨跌幅", "龙虎榜成交额(万)", "买入额(万)", "买入占总成交比例", "卖出额(万)",
#                       "卖出占总成交比例", "上榜原因"],
#         primary_key=[],
#         order_by=" date desc  "
#     )
# )
# # 实时行情
# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="每日数据",
#         name="每日股票数据",
#         table_name="ts_today_all",
#         columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
#                  "turnoverratio", "amount", "per", "pb", "mktcap", "nmc"],
#         column_names=["日期", "代码", "名称", "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
#                       "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值"],
#         primary_key=[],
#         order_by=" date desc  "
#     )
# )
# # 大盘指数行情列表
# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="每日数据",
#         name="每日大盘指数行情",
#         table_name="ts_index_all",
#         columns=["date", "code", "name", "change", "open", "preclose", "close", "high", "low", "volume", "amount"],
#         column_names=["日期", "代码", "名称", "涨跌幅", "开盘点位", "昨日收盘点位", "收盘点位", "最高点位", "最低点位", "成交量(手)", "成交金额（亿元）"],
#         primary_key=[],
#         order_by=" date desc  "
#     )
# )
#
# # 每日股票指标猜想。
# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="每日数据猜想",
#         name="每日股票指标All猜想",
#         table_name="guess_indicators_daily",
#         columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
#                  "turnoverratio", "amount", "per", "pb", "mktcap", "nmc",
#                  'adx', 'adxr', 'boll', 'boll_lb', 'boll_ub', 'cci', 'cci_20', 'close_-1_r',
#                  'close_-2_r', 'code', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'date', 'dma', 'dx',
#                  'kdjd', 'kdjj', 'kdjk', 'macd', 'macdh', 'macds', 'mdi', 'pdi',
#                  'rsi_12', 'rsi_6', 'trix', 'trix_9_sma', 'vr', 'vr_6_sma', 'wr_10', 'wr_6'],
#         column_names=["日期", "代码", "名称",
#                       "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
#                       "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值",
#                       'adx', 'adxr', 'boll', 'boll_lb', 'boll_ub', 'cci', 'cci_20', 'close_-1_r',
#                       'close_-2_r', 'code', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'date', 'dma', 'dx',
#                       'kdjd', 'kdjj', 'kdjk', 'macd', 'macdh', 'macds', 'mdi', 'pdi',
#                       'rsi_12', 'rsi_6', 'trix', 'trix_9_sma', 'vr', 'vr_6_sma', 'wr_10', 'wr_6'],
#         primary_key=[],
#         order_by=" date desc  "
#     )
# )
# # 每日股票指标lite猜想买入。
# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="每日数据猜想",
#         name="每日股票指标买入猜想",
#         table_name="guess_indicators_lite_buy_daily",
#         columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
#                  "turnoverratio", "amount", "per", "pb", "mktcap", "nmc",
#                  "kdjj", "rsi_6", "cci"],
#         column_names=["日期", "代码", "名称",
#                       "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
#                       "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值",
#                       "kdjj", "rsi_6", "cci"],
#         primary_key=[],
#         order_by=" buy_date desc  "
#     )
# )
#
# # 每日股票指标lite猜想卖出。
# STOCK_WEB_DATA_LIST.append(
#     StockWebData(
#         mode="query",
#         type="每日数据猜想",
#         name="每日股票指标卖出猜想",
#         table_name="guess_indicators_lite_sell_daily",
#         columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
#                  "turnoverratio", "amount", "per", "pb", "mktcap", "nmc",
#                  "kdjj", "rsi_6", "cci"],
#         column_names=["日期", "代码", "名称",
#                       "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
#                       "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值",
#                       "kdjj", "rsi_6", "cci"],
#         primary_key=[],
#         order_by=" buy_date desc  "
#     )
# )
