# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------

from typing import Dict,Literal
import json
from .logger import logger
import os
import requests
from tqdm import tqdm
from ..utils import get_info_dir

# ---------------------- 定义赋值区喵 ----------------------


# 补全存档喵
def complete_game_record(
    records: Dict[str, Dict[str, Dict[str, int]]],  # 打歌成绩数据喵
    difficult: Dict[str, Dict[str, Dict[str, int]]],  # 每首歌的各个难度的难度系数喵
    add_record: bool = False,  # 是否添加成绩，默认为 False 喵
    add_record_mode_list: list[str] = ["EZ", "HD"],  # 需要添加成绩的难度列表，默认为 ["EZ", "HD"] 喵
    score: int = 1000000,  # 默认分数喵
    acc: float = 100.0,  # 默认准确度喵
    fc: bool = True  # 是否全连，默认为 True 喵
) -> Dict[str, Dict[str, Dict[str, int]]]:  # 返回值类型
    """
    补全存档数据喵~如果某个歌曲记录缺失，默认添加空的成绩喵

    参数：
        records (dict): 打歌成绩数据喵~
        difficult (dict): 每首歌的各个难度的难度系数喵~
        add_record (bool): 是否添加成绩，默认为 False 喵~
        add_record_mode_list (list): 需要添加成绩的难度列表，默认为 ["EZ", "HD"] 喵~
        score (int): 分数，默认为 1000000 喵~
        acc (float): 准确度，默认为 100.0 喵~
        fc (bool): 是否全连，默认为 True 喵~

    返回：
        dict: 更新后的打歌成绩数据喵~
    """
    for game_name, values in difficult.items():
        if game_name not in records:  # 如果该游戏还不存在，就添加
            records[game_name] = {}

        if add_record:
            for mode in add_record_mode_list:
                if mode not in records[game_name]:
                    records[game_name][mode] = {"score": score, "acc": acc, "fc": int(fc)}  # 给没记录的模式添加成绩喵～

    return records


# 更新存档数据喵
def add_game_record(
    records: Dict[str, Dict[str, Dict[str, int]]],  # 打歌成绩数据喵~
    difficult: Dict[str, Dict[str, Dict[str, int]]],  # 每首歌的各个难度的难度系数喵~
    mode_list: list[str] = ["EZ", "HD"],  # 需要更新的模式列表，默认为 ["EZ", "HD"] 喵~
    score: int = 1000000,  # 默认分数喵~
    acc: float = 100.0,  # 默认准确度喵~
    fc: bool = True,  # 是否全连，默认为 True 喵~
    force_replace: bool = False  # 是否强制替换已有记录，默认为 False 喵~
) -> Dict[str, Dict[str, Dict[str, int]]]:
    """
    更新存档数据喵~

    参数：
        records (dict): 打歌成绩数据喵~
        difficult (dict): 每首歌的各个难度的难度系数喵~
        mode_list (list): 需要更新的模式列表，默认为 ["EZ", "HD"] 喵~
        score (int): 游戏得分，默认为 1000000 喵~
        acc (float): 准确度，默认为 100.0 喵~
        fc (bool): 是否全连，默认为 True 喵~
        force_replace (bool): 是否强制替换已有记录，默认为 False 喵~

    返回：
        dict: 更新后的打歌成绩数据喵~
    """
    for game_name, values in difficult.items():
        if game_name in records:  # 如果该游戏已存在，就更新
            for mode in mode_list:
                if mode in records[game_name]:
                    if force_replace:  # 如果需要强制替换，直接更新喵～
                        records[game_name][mode].update({"score": score, "acc": acc, "fc": int(fc)})
                else:
                    # 如果该模式没有成绩数据，就直接替换喵~
                    records[game_name][mode] = {"score": score, "acc": acc, "fc": int(fc)}

            # 按照 EZ, HD, IN, AT 顺序重新排序，只保留存在的难度喵~
            records[game_name] = {k: records[game_name][k] for k in ["EZ", "HD", "IN", "AT"] if k in records[game_name]}

    return records


def download_file(urls: list, folder_path: str, filename: str, max_retries: int = 3):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # 构造文件保存路径
    file_path = os.path.join(folder_path, filename)  # 注意这里没有多余的路径

    for attempt in range(max_retries):
        for url in urls:
            try:
                response = requests.head(url)
                response.raise_for_status()
                file_size = int(response.headers.get('content-length', 0))

                # 发送GET请求下载文件并显示进度条
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as file, tqdm(
                        desc=filename,
                        total=file_size,
                        unit='B',
                        unit_scale=True
                    ) as bar:
                        for chunk in r.iter_content(chunk_size=1024):
                            file.write(chunk)
                            bar.update(len(chunk))  # 更新进度条
                return True  # 下载成功
            except Exception as e:
                logger.error(f"下载失败，尝试 URL: {url}, 错误: {e}")
        
        if attempt < max_retries - 1:
            logger.warning(f"第 {attempt+1} 次尝试失败，正在重试...")
        else:
            logger.error(f"所有 URL 都下载失败，最大尝试次数为 {max_retries} 次。")
            return False  # 如果所有尝试都失败，返回 False
    
    return False


# 更新函数
def update(download_urls, save_name, max_retries: int = 3):
    save_path = os.path.join(get_info_dir(), save_name)
    logger.debug(f"保存路径: {save_path}")
    
    # 尝试下载源直到某个源成功
    for attempt in range(max_retries):
        if download_file(download_urls, get_info_dir(), save_name, max_retries):
            logger.info(f"更新 {save_name} 完成喵!")
            return True # 成功后退出
        else:
            logger.warning(f"第 {attempt+1} 次尝试下载失败，换源...")
            # 试着使用下一个下载 URL
            if len(download_urls) > 1:
                download_urls = download_urls[1:]  # 删除当前URL，尝试下一个
            else:
                logger.error(f"所有URL下载失败，更新 {save_name} 失败喵!")
                raise RuntimeError(f"更新 {save_name} 失败喵!")
    return False

# 难度定数表下载源
SOURCE_INFO = {
    "Catrong": {
        "download_urls": [
            "https://github.com/Catrong/phi-plugin-resources/raw/refs/heads/main/info/difficulty.csv",
        ],
        "save_name": "difficulty.csv"
    },
    "7aGiven": {
        "download_urls": [
            "https://github.com/7aGiven/Phigros_Resource/raw/refs/heads/info/difficulty.tsv",
        ],
        "save_name": "difficulty.tsv"
    }
}

class Update:
    @staticmethod
    def info(source:str, max_retries: int = 3,source_info:dict = SOURCE_INFO):
        source_data = source_info.get(source)
        logger.debug(f"下载源: {source_data}")
        if not source_data:
            raise ValueError(f"未知来源: {source}")
        update(source_data["download_urls"], source_data["save_name"], max_retries)

    # 咕咕咕,更新本体未来再写
    @staticmethod
    def pca():
        pass
