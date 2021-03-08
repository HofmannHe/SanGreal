#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import pandas as pd
import platform
import sys
import time
import traceback
import tushare as ts
from sqlalchemy import inspect, create_engine
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.types import NVARCHAR, Integer, String
from sqlalchemy_utils import database_exists, create_database

from libs.data_dicts import database_tables


class Database:
    def __init__(self):
        self._DB_TYPE = os.environ.get('DB_TYPE', "postgresql")
        self._DB_ENGINE = os.environ.get('DB_ENGINE', "psycopg2")
        self._DB_HOST = os.environ.get('DB_HOST', "database")
        self._DB_PORT = os.environ.get('DB_PORT', "5432")
        self._DB_USER = os.environ.get('DB_USER', "postgres")
        self._DB_PASSWORD = os.environ.get('DB_PASSWORD', "password")
        self._DB_DATABASE = os.environ.get('DB_DATABASE', "stock_data")
        logging.info(f"DB_TYPE :{self._DB_TYPE},"
                     f"DB_ENGINE :{self._DB_ENGINE},"
                     f"DB_HOST :{self._DB_HOST},"
                     f"DB_USER :{self._DB_USER},"
                     f"DB_DATABASE :{self._DB_DATABASE}")
        self._DB_CONN_STR = f"{self._DB_TYPE}+{self._DB_ENGINE}://{self._DB_USER}:{self._DB_PASSWORD}@{self._DB_HOST}:{self._DB_PORT}/{self._DB_DATABASE}"

        if not database_exists(self._DB_CONN_STR):
            create_database(self._DB_CONN_STR, encoding='utf8')

        self._engine = create_engine(self._DB_CONN_STR)

        metadata = MetaData(self._engine)
        for table_name in database_tables:
            if table_name not in self._engine.table_names():
                Table(table_name, metadata,
                      *tuple(Column(column.name,
                                    column.datatype,
                                    primary_key=column.is_primary_key) for column in
                             database_tables[table_name].columns))
        metadata.create_all()

    def engine(self):
        engine = create_engine(
            self._DB_CONN_STR,
            encoding='utf8', convert_unicode=True)
        return engine


# def insert(data, database, table_name, write_index, primary_keys):
#     # 定义engine
#     engine = engine()
#     # 使用 http://docs.sqlalchemy.org/en/latest/core/reflection.html
#     # 使用检查检查数据库表是否有主键。
#     insp = inspect(engine)
#     col_name_list = data.columns.tolist()
#     # 如果有索引，把索引增加到varchar上面。
#     if write_index:
#         # 插入到第一个位置：
#         col_name_list.insert(0, data.index.name)
#     print(col_name_list)
#     data.to_sql(name=table_name, con=engine, schema=DB_DATABASE, if_exists='append',
#                 dtype={col_name: NVARCHAR(length=255) for col_name in col_name_list}, index=write_index)
#     # 判断是否存在主键
#     if insp.get_primary_keys(table_name) == []:
#         with engine_mysql.connect() as con:
#             # 执行数据库插入数据。
#             try:
#                 con.execute('ALTER TABLE `%s` ADD PRIMARY KEY (%s);' % (table_name, primary_keys))
#             except  Exception as e:
#                 print("################## ADD PRIMARY KEY ERROR :", e)
#
#
# # 插入数据。
# def insert(sql, params=()):
#     with conn() as db:
#         print("insert sql:" + sql)
#         try:
#             db.execute(sql, params)
#         except  Exception as e:
#             print("error :", e)
#
#
# # 查询数据
# def select(sql, params=()):
#     with conn() as db:
#         print("select sql:" + sql)
#         try:
#             db.execute(sql, params)
#         except  Exception as e:
#             print("error :", e)
#         result = db.fetchall()
#         return result
#
#
# # 计算数量
# def select_count(sql, params=()):
#     with conn() as db:
#         print("select sql:" + sql)
#         try:
#             db.execute(sql, params)
#         except  Exception as e:
#             print("error :", e)
#         result = db.fetchall()
#         # 只有一个数组中的第一个数据
#         if len(result) == 1:
#             return int(result[0][0])
#         else:
#             return 0


if __name__ == "__main__":
    test = Database()
