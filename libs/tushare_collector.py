#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import time

import tushare as ts
from tenacity import retry, stop_after_attempt, wait_exponential
from functools import partial
from sqlalchemy.sql import select

from libs.dabatase import Database

pro = ts.pro_api()
custom_retry = partial(retry,
                       wait=wait_exponential(multiplier=1, max=60),
                       stop=stop_after_attempt(5),
                       )


@custom_retry
def get_stock_daily(trade_date):
    """
    获取指定日期的所有A股日线数据
    https://tushare.pro/document/2?doc_id=27
    :param trade_date: 指定交易日
    :return: 所有数据
    """
    df = pro.daily(trade_date=trade_date)
    return df


def get_adj_factor_daily(trade_date):
    """
    获取指定日期的所有A股复权因子
    :param trade_date: 指定交易日
    :return: 所有数据
    """
    for _ in range(3):
        try:
            df = pro.adj_factor(trade_date=trade_date)
        except:
            time.sleep(1)
        else:
            return df


def get_stock_daily_all(trade_date):
    """
    获取指定日期的所有A股数据并拼接成宽表
    :param trade_date: 指定交易日
    :return: 所有数据
    """
    df = get_stock_daily(trade_date)
    return df


if __name__ == "__main__":
    from initialize import set_token

    set_token()
    trade_date = '19901220'
    data = get_stock_daily_all(trade_date=trade_date)
    database = Database()
    result = database.select('tushare.pro_api.daily',
                             ts_code=None,
                             start_date=trade_date,
                             end_date=trade_date).shape[0]
    if result == 0:
        database.insert(data, 'tushare.pro_api.daily')
    else:
        print('TODO')
