from abc import ABC, abstractmethod
from phi_cloud_action import readDifficultyFile
from typing import List, Literal
from ...utils import get_info_dir

class Example(ABC):
    def __init__(self):
        # 获取路径
        info_dir = get_info_dir()
        difficulty_path = info_dir / "difficulty.tsv"
        
        # 如果路径不存在，尝试使用 CSV 文件
        if not difficulty_path.exists():
            difficulty_path = info_dir / "difficulty.csv"
        
        # 读取难度文件
        self.difficulty_data = readDifficultyFile(str(difficulty_path))
        
        self.route_path: str
        self.methods: List[Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]]

    @abstractmethod
    def __call__(self):
        pass
