import os

def get_dev_mode() -> bool:
    # 获取 DEV 环境变量的值，并确保它是小写
    dev_mode = os.getenv("DEV","").lower()
    
    # 根据 DEV 环境变量的值返回不同的目录路径
    if dev_mode == "true":
        return True
    else:
        return False
