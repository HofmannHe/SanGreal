#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import logging

from tenacity import retry, stop_after_attempt, wait_exponential
from functools import partial

from libs.data_dicts import data_sources
from libs.dabatase import Database

custom_retry = partial(retry,
                       wait=wait_exponential(multiplier=1, max=60),
                       stop=stop_after_attempt(5),
                       )


@custom_retry
def get_data(api, trade_date):
    return api(trade_date=trade_date)


def collect_data(table_name, trade_date) -> bool:
    """
    获取指定日期的表数据并存入数据库
    :param table_name: 表名
    :param trade_date: 指定交易日
    :return: 所有数据
    """
    data = get_data(
        data_sources[table_name].data_source,
        trade_date
    )
    if data.shape[0] == 0:
        logging.warning(f"No data is get from {table_name}.")
        return False

    database = Database()
    result = database.select(table_name,
                             ts_code=None,
                             start_date=trade_date,
                             end_date=trade_date).shape[0]
    if result == 0:
        database.insert(data, table_name)
        return True
    elif data.shape[0] == result:
        logging.warning('Insert failed: Data exists in database.')
        return False
    else:
        logging.error('Data conflict.')
        return False


if __name__ == "__main__":
    from initialize import set_token

    set_token()
    collect_data('tushare.pro_api.daily', '19901225')