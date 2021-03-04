#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import time

import tushare as ts


def get_stock_daily(trade_date):
    """
    获取指定日期的所有A股日线数据
    :param trade_date: 指定交易日
    :return: 所有数据
    """
    pro = ts.pro_api()
    for _ in range(3):
        try:
            df = pro.daily(trade_date=trade_date)
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
    print(get_stock_daily_all('20210226').columns)
