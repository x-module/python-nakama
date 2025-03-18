import logging
import os
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter


class Logger:
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, name: str = "ProjectLogger", log_dir="logs", log_level=logging.DEBUG):
        if self._initialized and self.logger.name == name:
            return
        self._initialized = True

        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # 定义颜色格式              "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        color_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s [%(name)s][%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(color_formatter)

        # 创建日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 创建按天分割的文件处理器
        file_handler = TimedRotatingFileHandler(
            filename=os.path.join(log_dir, "app.log"),
            when="midnight",  # 每天午夜分割
            interval=1,  # 间隔 1 天
            backupCount=7,  # 保留最近 7 天的日志
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)

        # 定义文件格式
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)

        # 添加处理器到日志记录器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
