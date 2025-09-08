# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from datetime import datetime
from time import time
from logging import (
    getLogger,
    INFO,
    DEBUG,
    StreamHandler,
    FileHandler,
    Formatter,
)
from os import mkdir
from os.path import join, exists
from typing import Optional
import sys

try:
    from colorlog import ColoredFormatter # type: ignore

except ImportError:
    from ._colorlog import ColoredFormatter

# ---------------------- 定义赋值区喵 ----------------------


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("致命错误：", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def set_local_logger(level=DEBUG):
    log_path = "./log/"
    if not exists(log_path):
        mkdir(log_path)
    log_name = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{int(time())}.log'
    log_format = "[%(asctime)s] [%(module)s-%(funcName)s][%(name)s] [%(levelname)s] - %(message)s"

    # 创建日志记录器喵
    logger = getLogger()
    logger.setLevel(level)

    # 创建文件处理器并设置编码喵
    file_handler = FileHandler(join(log_path, log_name), encoding="utf-8")
    file_handler.setLevel(level)

    # 创建日志格式化器喵
    formatter = Formatter(log_format)
    file_handler.setFormatter(formatter)

    # 将文件处理器添加到日志记录器喵
    logger.addHandler(file_handler)


def get_logger(name: Optional[str] = None, level: int = INFO):
    set_local_logger()
    loggers = getLogger(name)  # 创建logger对象喵
    loggers.setLevel(DEBUG)

    console_handler = StreamHandler()  # 创建控制台日志处理器喵
    console_handler.setLevel(level)

    color_formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s] [%(module)s-%(funcName)s][%(name)s] [%(levelname)s] - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )  # 定义颜色输出格式
    # 将颜色输出格式添加到控制台日志处理器
    console_handler.setFormatter(color_formatter)

    for handler in loggers.handlers:  # 移除默认的handler喵
        loggers.removeHandler(handler)

    loggers.addHandler(console_handler)  # 将控制台日志处理器添加到logger对象喵
    return loggers


# ----------------------- 运行区喵 -----------------------

logger = get_logger("PCA", DEBUG)
logger.debug("Logger 加载完成喵")
