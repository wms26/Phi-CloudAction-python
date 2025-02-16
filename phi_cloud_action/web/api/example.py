from abc import ABC, abstractmethod
from phi_cloud_action import readDifficultyFile
from typing import List,Literal

class example(ABC):
    def __init__(self):
        self.route_path:str
        self.methods:List[Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]]
        # 读取难度定数文件喵
        self.difficulty = readDifficultyFile("phi_cloud_action\data\info\difficulty.tsv")

    @abstractmethod
    def __call__(self):
        pass
