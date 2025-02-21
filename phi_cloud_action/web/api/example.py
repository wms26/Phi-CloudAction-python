from abc import ABC, abstractmethod
from phi_cloud_action import readDifficultyFile,logger,PhigrosCloud,unzipSave,decryptSave,formatSaveDict,checkSaveHistory
from typing import List, Literal,Dict
from ...utils import get_info_dir
from pydantic import BaseModel
import os

# 获取info目录
info_dir = get_info_dir()

# 读取定数文件名
difficulty_name = os.getenv("PHI_DIF_NAME","difficulty.tsv")
logger.debug(f"当前环境PHI_DIF_NAME:{difficulty_name}")

class Saves(BaseModel):
    save_dict: dict
    summary: dict
    save_data: bytes

class example(ABC):
    def __init__(self):        
        self.route_path: str
        self.methods: List[Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]]

    # 获取定数
    @staticmethod
    def get_difficulty(file_name: Literal["difficulty.tsv", "difficulty.csv"] = difficulty_name) -> Dict[str, List[float]]:
        """
        获取定数

        参数:
            file_name(str): 定数文件名

        返回:
            (dict) 定数,key是曲名,内容是列表,包含定数
        """
        # 获取路径
        difficulty_path = info_dir / file_name
        
        # 读取难度文件
        difficulty = readDifficultyFile(str(difficulty_path))
        return difficulty

    # 获取云存档
    @staticmethod
    def get_saves(token:str) -> Saves:
        """
        获取云存档并记录到历史记录

        参数:
            token(str): 玩家的token

        返回:
            (Saves) 玩家存档,包含save_dict、save_data和summary
        """
        with PhigrosCloud(token) as cloud:
            # 获取玩家summary喵
            summary = cloud.getSummary() 

            # 获取并解析存档喵
            save_data = cloud.getSave(summary["url"], summary["checksum"])
            save_dict = unzipSave(save_data)
            save_dict = decryptSave(save_dict)
            save_dict = formatSaveDict(save_dict)
        
        data = Saves(save_dict=save_dict,summary=summary,save_data=save_data)
        checkSaveHistory(token, summary, save_data, example.get_difficulty())
        return data
        
    @abstractmethod
    def api(self):
        pass
