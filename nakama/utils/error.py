#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   2025/8/29 21:03
# @Author Tudou <244395692@qq.com>
# @file   error.py
# @desc   error.py
from nakama.utils.logger import Logger


def handle_errors(func):
    logger = Logger("handle_errors")
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error("system error:{}".format(e))
            return None
    return wrapper
