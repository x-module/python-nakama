# -*- coding: utf-8 -*-
"""日志管理模块

提供统一的日志记录功能,支持控制台彩色输出和文件滚动。
"""
import inspect
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter

from nakama.common.decorator import singleton


@singleton
class Logger:
    """日志管理类
    
    提供统一的日志记录功能，支持：
    1. 控制台彩色输出
    2. 文件按天切割
    3. 单例模式确保日志一致性
    """

    def __init__(self, log_dir: str = "logs", log_level=logging.DEBUG):
        root_path = os.getcwd()
        log_dir = f"{root_path}/data/{log_dir}"

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        # 彩色输出格式
        color_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s[%(levelname)s]%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'
            }
        )
        console_handler.setFormatter(color_formatter)

        # 文件处理器
        file_handler = TimedRotatingFileHandler(
            filename=os.path.join(log_dir, "app.log"),
            when="midnight",  # 每天午夜分割
            interval=1,  # 间隔1天
            backupCount=30,  # 保留30天的日志
            encoding="utf-8"
        )
        # 设置日志文件名格式为 app.2024-03-14.log
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setLevel(log_level)

        # 文件日志格式
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)

        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def _log_with_caller_info(self, level: int, msg: str, *args, **kwargs):
        """添加调用者信息的日志记录"""
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back.f_back
            lineno = caller_frame.f_lineno
            module = inspect.getmodule(caller_frame)
            # 在消息中添加调用位置信息
            msg_with_caller = f"[{module.__name__}:{lineno}] {msg}"
            self.logger.log(level, msg_with_caller, *args, **kwargs)
        finally:
            del frame  # 避免内存泄漏

    def debug(self, msg: str, *args, **kwargs):
        """记录DEBUG级别日志"""
        self._log_with_caller_info(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """记录INFO级别日志"""
        self._log_with_caller_info(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """记录WARNING级别日志"""
        self._log_with_caller_info(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """记录ERROR级别日志"""
        self._log_with_caller_info(logging.ERROR, msg, *args, **kwargs)

    def fatal(self, msg: str, *args, **kwargs):
        """记录FATAL级别日志并退出程序"""
        self._log_with_caller_info(logging.FATAL, msg, *args, **kwargs)
        sys.exit(1)

    def critical(self, msg: str, *args, **kwargs):
        """记录CRITICAL级别日志"""
        self._log_with_caller_info(logging.CRITICAL, msg, *args, **kwargs)
