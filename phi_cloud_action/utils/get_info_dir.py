from dotenv import load_dotenv
from pathlib import Path
import os
from ..PhiCloudLib.logger import logger

# 加载 .env 文件，假设你想加载上级目录的 .env 文件
load_dotenv(str(Path(__file__).resolve().parent.parent / '.env'))

def get_info_dir() -> str:
    # 获取 DEV 环境变量的值，并确保它是小写
    dev_mode = os.getenv("DEV").lower()
    
    # 根据 DEV 环境变量的值返回不同的目录路径
    if dev_mode == "true":
        return Path.cwd() / "phi_cloud_action" / "data" / "info"
    else:
        return Path.cwd() / "info"
