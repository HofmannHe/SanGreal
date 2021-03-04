#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import os

import tushare as ts



def set_token():
    if os.getenv("TUSHARE_TOKEN") is not None:
        ts.set_token(os.getenv("TUSHARE_TOKEN"))
        logging.info("set_token")
    else:
        logging.error("need token")


if __name__ == "__main__":
    set_token()
