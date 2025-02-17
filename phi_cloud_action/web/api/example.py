from abc import ABC, abstractmethod
from phi_cloud_action import readDifficultyFile,logger
from typing import List, Literal
from ...utils import get_info_dir

class example(ABC):
    def __init__(self):
        self.route_path: str
        self.methods: List[Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]]
        # 获取路径
        info_dir = get_info_dir()
        try:
            # 拼接路径
            difficulty_path = str(info_dir / "difficulty.tsv")
            # 读取难度定数文件
            self.difficulty = readDifficultyFile(difficulty_path)
        except FileNotFoundError:
            # 拼接路径
            difficulty_path = str(info_dir / "difficulty.csv")
            # 读取难度定数文件
            self.difficulty = readDifficultyFile(difficulty_path)
            
    @abstractmethod
    def __call__(self):
        pass
