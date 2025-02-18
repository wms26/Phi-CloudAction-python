from pathlib import Path
import os
from ..PhiCloudLib.logger import logger

def get_info_dir() -> Path:
    # 获取 DEV 环境变量的值，并确保它是小写
    dev_mode = os.getenv("DEV","").lower()
    
    # 根据 DEV 环境变量的值返回不同的目录路径
    if dev_mode == "true":
        return Path.cwd() / "phi_cloud_action" / "data" / "info"
    else:
        return Path.cwd() / "info"
