import argparse
import os
from pathlib import Path
from typing import List,Type,Optional
from pydantic import BaseModel, Field , ValidationError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import platform
import shutil
from importlib.resources import files
from .web.api.example import example
from phi_cloud_action import logger
from .utils import get_dev_mode
import inspect
from yaml import safe_load
import re

# 重写 argparse.ArgumentParser 类，修改帮助信息的显示格式喵~
class CustomArgumentParser(argparse.ArgumentParser):
    def print_help(self, *args, **kwargs):
        # 获取格式化的帮助信息
        help_text = self.format_help()
        
        # 去除短选项和长选项之间的空格
        help_text = help_text.replace('-c ,', '-c,').replace('--config', '--config ')
        
        # 输出修改后的帮助信息
        self._print_message(help_text, *args, **kwargs)

# 配置类 (使用 Pydantic)
class RoutesConfig(BaseModel):
    allow_routes: set[str] = None
    ban_routes: set[str] = None


class CORSConfig(BaseModel):
    switch: bool = Field(..., alias="CORS_switch")
    allow_origins: List[str] = Field(..., alias="CORS_allow_origins")
    allow_credentials: bool = Field(..., alias="CORS_allow_credentials")
    allow_methods: List[str] = Field(..., alias="CORS_allow_methods")
    allow_headers: List[str] = Field(..., alias="CORS_allow_headers")


class ServerConfig(BaseModel):
    host: str
    port: int
    cors: CORSConfig
    routes: RoutesConfig = None


class Config(BaseModel):
    net: ServerConfig


# 配置管理器
class ConfigManager:
    @staticmethod
    def get_default_dir() -> Path:
        """获取默认配置文件目录喵~"""
        package_name = 'phi_cloud_action'
        system: str = platform.system()

        if get_dev_mode():
            return Path.cwd() / package_name / "data"
    
        if system == 'Windows':
            appdata: Optional[str] = os.getenv('APPDATA')
            if appdata:
                return Path(appdata) / package_name
            else:
                return Path.home() / 'AppData' / 'Roaming' / package_name
        else:
            return Path.home() / '.config' / package_name

    def __init__(self) -> None:
        self.args: argparse.Namespace = self._parse_args()
        self.config_path: Path = self._get_config_path()
        self.config: Config = self._read_config()

    DEFAULT_DIR: Path = get_default_dir()
    CONFIG_FILE: str = 'RunConfig.yml'

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
            # 打开配置文件并读取
            with open(self.config_path, 'r', encoding="utf-8") as f:
                config_dict = safe_load(f)
            
            # 使用 model_validate 来解析配置文件
            return Config.model_validate(config_dict)
        
        except ValidationError as e:
            logger.error("配置文件解析失败，错误信息如下：")
            for error in e.errors():
                logger.error(f"字段: {error['loc']}, 错误: {error['msg']}")
            exit(1)

        except Exception as e:
            # 捕获其他异常并抛出更清晰的错误信息
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
                raise RuntimeError(f"配置文件初始化失败喵~: {str(e)}")


# 路由分类
def routes_classification(name:str) -> str:
    if name.startswith("/get/cloud"):
        group = "cloud"
    elif name.startswith("/get/saves"):
        group = "saves"
    elif name.startswith("/update"):
        group = "update"
    elif name.startswith("/get/token"):
        group = "token"
    else:
        group = "other"
    
    return group

# 路由注册
def register_routes(app: FastAPI, interface_class: Type[example], routes_config: RoutesConfig):
    route_classes = []

    # 获取路由对象
    for name, obj in inspect.getmembers(interface_class):
        if inspect.isclass(obj):
            for method_name, method_obj in inspect.getmembers(obj):
                if method_name == "api" and inspect.isfunction(method_obj):
                    instance: example = obj()
                    if hasattr(instance, "route_path") and hasattr(instance, "methods"):
                        route_classes.append(instance)

    # 辅助排序
    def sort_key(route_class: example):
        return (route_class.route_path.find("{") != -1, len(route_class.route_path))

    # 排序
    route_classes.sort(key=sort_key)

    # 获取白名单和黑名单, 只有在 routes_config 不为 None 时才会进行这些检查
    if routes_config:
        allow_route = set(routes_config.allow_routes) if routes_config.allow_routes else None
        ban_route = set(routes_config.ban_routes) if routes_config.ban_routes else None
    else:
        allow_route = ban_route = None

    for instance in route_classes:
        route_path = instance.route_path

        # 如果黑名单为 None，则不做检查，跳过黑名单检查
        if ban_route is not None and route_path in ban_route:
            logger.info(f"黑名单中，跳过路由: {route_path}")
            continue
        
        # 如果白名单为 None，则直接注册路由；否则检查是否在白名单中
        if allow_route is not None and route_path not in allow_route:
            logger.info(f"不在白名单中，跳过路由: {route_path}")
            continue

        logger.info(f"注册路由: {route_path}")

        # 获取名称
        name: str = route_path

        # 分类
        group = routes_classification(name)

        # summary名称
        title_name = re.sub(r'\{.*?\}', '', name)  # 清除{和}之间的内容
        title_name = title_name.replace("/", " ").title()

        # 注册路由
        app.add_api_route(
            route_path,
            instance.api,
            methods=instance.methods,
            summary=title_name,
            tags=[group]
        )

# 启动程序
def main():
    manager: ConfigManager = ConfigManager()
    config = manager.config.net  # 获取配置中的 net 部分
    app = FastAPI(debug=get_dev_mode())

    if config.cors.switch:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors.allow_origins,
            allow_credentials=config.cors.allow_credentials,
            allow_methods=config.cors.allow_methods,
            allow_headers=config.cors.allow_headers,
        )

    # 注册路由
    from .web import api
    register_routes(app, api, config.routes)

    logger.info(f"监听主机: {config.host}, 端口: {config.port} 喵~")
    logger.info(f"配置文件路径喵~: {manager.config_path}")

    run(app, host=config.host, port=config.port)


# 主程序入口喵~
if __name__ == '__main__':
    main()