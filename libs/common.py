#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import time
import traceback

import pandas as pd
import tushare as ts
from sqlalchemy import inspect, create_engine
from sqlalchemy.types import NVARCHAR


# 通用函数。获得日期参数。
def run_with_args(run_fun):
    tmp_datetime_show = datetime.datetime.now()  # 修改成默认是当日执行 + datetime.timedelta()
    tmp_datetime_str = tmp_datetime_show.strftime("%Y-%m-%d %H:%M:%S.%f")
    str_db = "MYSQL_HOST :" + MYSQL_HOST + ", MYSQL_USER :" + MYSQL_USER + ", MYSQL_DB :" + MYSQL_DB
    print("\n######################### " + str_db + "  ######################### ")
    print("\n######################### begin run %s %s  #########################" % (run_fun, tmp_datetime_str))
    start = time.time()
    # 要支持数据重跑机制，将日期传入。循环次数
    if len(sys.argv) == 3:
        # python xxx.py 2017-07-01 10
        tmp_year, tmp_month, tmp_day = sys.argv[1].split("-")
        loop = int(sys.argv[2])
        tmp_datetime = datetime.datetime(int(tmp_year), int(tmp_month), int(tmp_day))
        for i in range(0, loop):
            # 循环插入多次数据，重复跑历史数据使用。
            # time.sleep(5)
            tmp_datetime_new = tmp_datetime + datetime.timedelta(days=i)
            try:
                run_fun(tmp_datetime_new)
            except Exception as e:
                print("error :", e)
                traceback.print_exc()
    elif len(sys.argv) == 2:
        # python xxx.py 2017-07-01
        tmp_year, tmp_month, tmp_day = sys.argv[1].split("-")
        tmp_datetime = datetime.datetime(int(tmp_year), int(tmp_month), int(tmp_day))
        try:
            run_fun(tmp_datetime)
        except Exception as e:
            print("error :", e)
            traceback.print_exc()
    else:
        # tmp_datetime = datetime.datetime.now() + datetime.timedelta(days=-1)
        try:
            run_fun(tmp_datetime_show)  # 使用当前时间
        except Exception as e:
            print("error :", e)
            traceback.print_exc()
    print("######################### finish %s , use time: %s #########################" % (
        tmp_datetime_str, time.time() - start))


# 设置基础目录，每次加载使用。
bash_stock_tmp = "/data/cache/hist_data_cache/%s/%s/"
if not os.path.exists(bash_stock_tmp):
    os.makedirs(bash_stock_tmp)  # 创建多个文件夹结构。
    print("######################### init tmp dir #########################")


# 增加读取股票缓存方法。加快处理速度。
def get_hist_data_cache(code, date_start, date_end):
    cache_dir = bash_stock_tmp % (date_end[0:7], date_end)
    # 如果没有文件夹创建一个。月文件夹和日文件夹。方便删除。
    # print("cache_dir:", cache_dir)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_file = cache_dir + "%s^%s.gzip.pickle" % (date_end, code)
    # 如果缓存存在就直接返回缓存数据。压缩方式。
    if os.path.isfile(cache_file):
        print("######### read from cache #########", cache_file)
        return pd.read_pickle(cache_file, compression="gzip")
    else:
        print("######### get data, write cache #########", code, date_start, date_end)
        stock = ts.get_hist_data(code, start=date_start, end=date_end)
        if stock is None:
            return None
        stock = stock.sort_index(0)  # 将数据按照日期排序下。
        stock.to_pickle(cache_file, compression="gzip")
        return stock
