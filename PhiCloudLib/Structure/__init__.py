# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from typing import Any, Dict
from .DataType import *

from .gameKey import *
from .gameProgress import *
from .settings import *
from .user import *

# ---------------------- 定义赋值区喵 ----------------------


def getStructure(file_head: Dict[str, bytes]) -> Dict[str, Any]:
    structure_list = {}

    # gameKey
    if file_head.get("gameKey") == b"\x03":
        from .gameKey import gameKey03

        structure_list["gameKey"] = gameKey03

    elif file_head.get("gameKey") == b"\x02":
        from .gameKey import gameKey02

        structure_list["gameKey"] = gameKey02

    elif isinstance(file_head.get("gameKey"), bytes):
        raise ValueError(
            f'文件头不正确，可能数据结构已更新喵！不应为：{file_head.get("gameKey")}'
        )

    # gameProgress
    if file_head.get("gameProgress") == b"\x04":
        from .gameProgress import gameProgress04

        structure_list["gameProgress"] = gameProgress04

    elif file_head.get("gameProgress") == b"\x03":
        from .gameProgress import gameProgress03

        structure_list["gameProgress"] = gameProgress03

    elif isinstance(file_head.get("gameProgress"), bytes):
        raise ValueError(
            f'文件头不正确，可能数据结构已更新喵！不应为：{file_head.get("gameProgress")}'
        )

    # gameRecord
    if file_head.get("gameRecord") == b"\x01":
        structure_list["gameRecord"] = GameRecord

    elif isinstance(file_head.get("gameRecord"), bytes):
        raise ValueError(
            f'文件头不正确，可能数据结构已更新喵！不应为：{file_head.get("gameRecord")}'
        )

    # settings
    if file_head.get("settings") == b"\x01":
        from .settings import settings01

        structure_list["settings"] = settings01

    elif isinstance(file_head.get("settings"), bytes):
        raise ValueError(
            f'文件头不正确，可能数据结构已更新喵！不应为：{file_head.get("settings")}'
        )

    # user
    if file_head.get("user") == b"\x01":
        from .user import user01

        structure_list["user"] = user01

    elif isinstance(file_head.get("user"), bytes):
        raise ValueError(
            f'文件头不正确，可能数据结构已更新喵！不应为：{file_head.get("user")}'
        )

    return structure_list


def getFileHead(save_dict: Dict[str, Any]):
    file_head = {}
    for key, file_dict in save_dict.items():
        if key == "gameKey":
            if file_dict.get("oldScoreClearedV390") is not None:
                file_head[key] = b"\x03"

            else:
                file_head[key] = b"\x02"

        elif key == "gameRecord":
            file_head[key] = b"\x01"

        elif key == "gameProgress":
            if file_dict.get("flagOfSongRecordKeyTakumi") is not None:
                file_head[key] = b"\x04"

            else:
                file_head[key] = b"\x03"

        elif key == "settings":
            file_head[key] = b"\x01"

        elif key == "user":
            file_head[key] = b"\x01"
            
    return file_head
