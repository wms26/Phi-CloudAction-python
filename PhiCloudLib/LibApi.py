from datetime import datetime
from time import time
from logging import getLogger, INFO, DEBUG, StreamHandler, basicConfig
from os import mkdir
from os.path import join, exists

from colorlog import ColoredFormatter


def set_logger(level=DEBUG):
    log_path = './log/'
    if not exists(log_path):
        mkdir(log_path)
    log_name = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{int(time())}.log'
    log_format = '[%(asctime)s] [%(module)s-%(funcName)s][%(name)s] [%(levelname)s] - %(message)s'
    basicConfig(filename=join(log_path, log_name), level=level, format=log_format)


def get_logger(name: str | None = None, level: int = INFO):
    set_logger()
    loggers = getLogger(name)  # 创建logger对象
    loggers.setLevel(DEBUG)

    console_handler = StreamHandler()  # 创建控制台日志处理器
    console_handler.setLevel(level)

    color_formatter = ColoredFormatter(
        '%(log_color)s[%(asctime)s] [%(module)s-%(funcName)s][%(name)s] [%(levelname)s] - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )  # 定义颜色输出格式
    # 将颜色输出格式添加到控制台日志处理器
    console_handler.setFormatter(color_formatter)

    for handler in loggers.handlers:  # 移除默认的handler
        loggers.removeHandler(handler)

    loggers.addHandler(console_handler)  # 将控制台日志处理器添加到logger对象
    return loggers


logger = get_logger('PCA', DEBUG)
logger.debug('Logger is loading completed.')
