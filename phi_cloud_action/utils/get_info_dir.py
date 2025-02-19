from pathlib import Path
from ..PhiCloudLib.logger import logger
from .get_dev_mode import get_dev_mode

def get_info_dir() -> Path:
    # 根据 DEV 环境变量的值返回不同的目录路径
    if get_dev_mode():
        return Path.cwd() / "phi_cloud_action" / "data" / "info"
    else:
        return Path.cwd() / "info"
