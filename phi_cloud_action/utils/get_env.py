import os

def get_env(env_name:str) -> str:
    # 获取 DEV 环境变量的值，并确保它是小写
    return os.getenv(env_name,"")