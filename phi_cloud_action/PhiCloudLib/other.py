# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------

from typing import Dict
import json

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


# 读取json喵
def read_json(json_file: str) -> Dict:
    """
    从 JSON 文件读取数据喵~
    """
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

# 写入json喵
def write_json(data: Dict, output_file: str) -> None:
    """
    将数据写入到 JSON 文件喵~
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

