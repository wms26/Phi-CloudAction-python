import argparse
import os
from pathlib import Path
from typing import Dict, Any, Union, Optional
from yaml import safe_load
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import platform
import shutil  # 用于文件复制喵~
from importlib.resources import files  # 导入 importlib.resources 喵~
from phi_cloud_action import PhigrosCloud, unzipSave, decryptSave, logger
from pydantic import BaseModel

# 重写 argparse.ArgumentParser 类，修改帮助信息的显示格式喵~
class CustomArgumentParser(argparse.ArgumentParser):
    def print_help(self, *args, **kwargs):
        # 获取格式化的帮助信息
        help_text = self.format_help()
        
        # 去除短选项和长选项之间的空格
        help_text = help_text.replace('-c ,', '-c,').replace('--config ', '--config')
        
        # 输出修改后的帮助信息
        self._print_message(help_text, *args, **kwargs)

# 配置类喵~
class Config:
    def __init__(self, host: str, port: int, cors_switch: bool, cors_allow_origins: list, cors_allow_credentials: bool, cors_allow_methods: list, cors_allow_headers: list) -> None:
        self.host = host
        self.port = port
        self.CORS_siwtch = cors_switch
        self.CORS_allow_origins = cors_allow_origins
        self.CORS_allow_credentials = cors_allow_credentials
        self.CORS_allow_methods = cors_allow_methods
        self.CORS_allow_headers = cors_allow_headers

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """从字典创建 Config 实例喵~"""
        server_config: Dict[str, Any] = config_dict.get('net')
        host: str = server_config.get('host')
        port: int = server_config.get('port')
        cors: dict = server_config.get('cors')
        cors_switch: bool = cors.get('switch')
        cors_config: dict = cors.get('config')
        cors_allow_origins: list = cors_config.get('allow_origins')
        cors_allow_credentials: bool = cors_config.get('allow_credentials')
        cors_allow_methods: list = cors_config.get('allow_methods')
        cors_allow_headers: list = cors_config.get('allow_headers')
        return cls(host, port, cors_switch, cors_allow_origins, cors_allow_credentials, cors_allow_methods, cors_allow_headers)

# 配置管理器喵~
class ConfigManager:
    @staticmethod
    def get_default_dir() -> Path:
        """获取默认配置文件目录喵~"""
        package_name = 'phi_cloud_action'
        system: str = platform.system()
        if system == 'Windows':
            appdata: Optional[str] = os.getenv('APPDATA')
            if appdata:
                return Path(appdata) / package_name
            else:
                return Path.home() / 'AppData' / 'Roaming' / package_name
        else:
            return Path.home() / '.config' / package_name

    DEFAULT_DIR: Path = get_default_dir()
    CONFIG_FILE: str = 'RunConfig.yml'

    def __init__(self) -> None:
        self.args: argparse.Namespace = self._parse_args()
        self.config_path: Path = self._get_config_path()
        self._ensure_config_file_exists()  # 确保配置文件存在喵~
        self.config: Config = self._read_config()

    def _parse_args(self) -> argparse.Namespace:
        """解析命令行参数喵~"""
        parser = CustomArgumentParser(
            description="phi_cloud_action.webapi 配置管理器喵~",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument('-c', '--config', type=str, help='自定义配置文件路径喵~', metavar="")
        return parser.parse_args()


    def _get_config_path(self) -> Path:
        """获取配置文件路径喵~"""
        if self.args.config:
            return Path(self.args.config)
        return self.DEFAULT_DIR / self.CONFIG_FILE

    def _read_config(self) -> Config:
        """读取并返回配置对象喵~"""
        try:
            with open(self.config_path, 'r', encoding="utf-8") as f:
                config_dict: Dict[str, Any] = safe_load(f)

            # 检查配置文件格式喵~
            if 'net' not in config_dict:
                raise ValueError("配置文件格式错误，缺少 'net' 部分喵~")

            return Config.from_dict(config_dict)

        except Exception as e:
            raise RuntimeError(f"读取配置文件失败喵~: {str(e)}")

    def _ensure_config_file_exists(self) -> None:
        """检查配置文件是否存在，不存在则从包内复制喵~"""
        if not self.config_path.exists():
            try:
                # 创建目标目录喵~
                self.config_path.parent.mkdir(parents=True, exist_ok=True)

                logger.info(f"配置文件 {self.config_path} 不存在，正在从包内复制喵~...")

                # 处理包名（直接运行脚本时 __package__ 为 None）喵~
                package_name = __package__ or "phi_cloud_action"
                package_config_path = files(package_name) / 'data' / self.CONFIG_FILE

                logger.info(f"从包内获取配置文件路径喵: {package_config_path}")

                if package_config_path.is_file():
                    shutil.copy(package_config_path, self.config_path)
                    logger.info(f"配置文件已从 {package_config_path} 拷贝到 {self.config_path} 喵~")
                else:
                    raise FileNotFoundError(f"包内默认配置文件 {package_config_path} 找不到喵~。")

            except Exception as e:
                logger.error(f"配置文件初始化失败喵~: {str(e)}")
                raise

# Token 请求模型喵~
class TokenRequest(BaseModel):
    token: str

# 获取并解析存档数据喵~
def get_cloud_saves(request: TokenRequest) -> JSONResponse:
    try:
        # 使用 request.token 来获取传递的 token 值
        with PhigrosCloud(request.token) as cloud:
            # 获取并解析存档喵~
            save_data = cloud.getSave()

            save_dict = unzipSave(save_data)
            save_dict = decryptSave(save_dict)

        return JSONResponse(content={"code": 200, "status": "ok", "data": save_dict}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)


# 主程序入口喵~
if __name__ == '__main__':
    try:
        manager: ConfigManager = ConfigManager()
        config = manager.config
        # FastAPI 实例喵~
        app = FastAPI()

        # 配置 CORS 喵~
        if config.CORS_siwtch:  # 根据 CORS 配置中的开关进行判断
            app.add_middleware(
                CORSMiddleware,
                allow_origins=config.CORS_allow_origins,
                allow_credentials=config.CORS_allow_credentials,
                allow_methods=config.CORS_allow_methods, 
                allow_headers=config.CORS_allow_headers,  
            )
        
        # 配置路由喵~
        app.add_api_route("/get/cloud/saves", get_cloud_saves, methods=["POST"])

        # 输出配置信息喵~
        logger.info(f"监听主机: {config.host}, 端口: {config.port} 喵~")
        logger.info(f"配置文件路径喵~: {manager.config_path}")

        # 启动 FastAPI Web 服务喵~
        run(app, host=config.host, port=config.port)

    except Exception as e:
        logger.error(f"发生错误喵~: {e}")
        exit(1)
