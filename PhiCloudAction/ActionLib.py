# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from copy import deepcopy
from datetime import datetime
from io import BytesIO
from json import dumps, loads
from os import mkdir
from os.path import dirname, abspath, exists, join
from re import match
from typing import Any, Dict, List, Optional
from zipfile import ZipFile, ZIP_DEFLATED

from .AES import decrypt, encrypt
from .Structure import headGetStructure, getFileHead, Reader, Writer
from .logger import logger


# ---------------------- 定义赋值区喵 ----------------------


local_path = dirname(abspath(__file__))  # 获取此文件所在目录的绝对路径


def debugTempFiles(
    data, mode: str = "w", filetype: str = "txt", encoding: str = "utf-8"
):
    # 这个是测试debug用的，不用多管喵（
    # 算是写个临时文件用来debug数据处理情况喵
    if mode == "wb":
        with open("./awa." + filetype, mode) as f:
            f.write(data)  # 写入文件喵
    else:
        with open("./awa." + filetype, mode, encoding=encoding) as f:
            f.write(data)  # 写入文件喵


def checkSessionToken(sessionToken: str, _raise: bool = True) -> bool:
    """
    检查sessionToken格式是否合法喵

    参数:
        sessionToken (str): 玩家的sessionToken喵
        _raise (bool): 是否主动引发错误，若为False，则会在检测到不合法时返回False。默认为True

    返回:
        (bool): SessionToken是否合法喵
    """
    # 判断sessionToken是否为空喵
    if sessionToken == "" or sessionToken is None:
        if _raise:
            raise ValueError("sessionToken为空喵！")

        else:
            return False

    # 判断sessionToken的长度是否为25位喵
    elif len(sessionToken) != 25:
        if _raise:
            raise ValueError(
                f"sessionToken长度错误喵！应为25位，而不是{len(sessionToken)}位喵：{sessionToken}"
            )

        else:
            return False

    # 正则匹配判断sessionToken是否符合要求喵
    elif not match(r"^[0-9a-z]{25}$", sessionToken):
        if _raise:
            raise ValueError(
                f"sessionToken不合法喵！应只有数字与小写字母喵：{sessionToken}"
            )

        else:
            return False

    # 检查全部通过则是合法sessionToken喵
    else:
        logger.debug(f"sessionToken正确喵：{sessionToken}")
        return True


def readDifficultyFile(path: Optional[str] = None) -> Dict[str, List[float]]:
    """
    读取歌曲谱面定数文件喵

    参数:
        path (str): 歌曲谱面定数文件路径喵

    返回:
        (dict[str, list[float]]): 歌曲谱面定数数据喵。以歌曲id为键，值为单曲难度列表喵
    """
    # 如果没有提供文件路径喵
    if path is None:
        logger.debug("没有提供歌曲谱面定数文件路径，尝试自动寻找喵...")

        # 优先从工作路径下寻找定数文件喵
        if exists("./difficulty.tsv"):
            logger.debug(f'在工作目录下找到了歌曲谱面定数文件喵："./difficulty.tsv"')
            file_path = "./difficulty.tsv"

        elif exists("./info/difficulty.tsv"):
            logger.debug(
                f'在工作目录下找到了歌曲谱面定数文件喵："./info/difficulty.tsv"'
            )
            file_path = "./info/difficulty.tsv"

        # 其次尝试寻找此文件所在目录下是否有定数文件喵
        elif exists(join(local_path, "info/difficulty.tsv")):
            logger.debug(f'在库目录下找到了歌曲谱面定数文件喵："./info/difficulty.tsv"')
            file_path = join(local_path, "info/difficulty.tsv")

        else:
            raise ValueError("找不到歌曲谱面定数文件喵！")

    # 优先使用提供的文件路径喵
    else:
        if not exists(path):
            raise FileExistsError(f'文件"{path}"不存在喵！')

        file_path = path

    difficulty_list = {}  # 存储最终解析出来的歌曲谱面定数数据喵
    with open(file_path, encoding="UTF-8") as f:  # 打开歌曲谱面定数文件喵
        lines = f.readlines()  # 解析所有行，输出一个列表喵

    for line in lines:  # 遍历所有行喵
        # 将该行最后的"\n"截取掉，并以"\t"为分隔符解析为一个列表喵
        line = line[:-1].split("\t")
        diff = []  # 用来存储单首歌所有谱面的定数信息喵

        for i in range(1, len(line)):  # 遍历该行后面的所有难度值喵
            diff.append(float(line[i]))  # 将难度添加到列表中喵
        difficulty_list[line[0]] = diff  # 与总列表拼接在一起喵

    return difficulty_list  # 返回解析出来的各歌曲定数数据喵


def unzipFile(zip_data: bytes, file_name: Optional[str] = None) -> Dict[str, bytes]:
    """
    读取压缩包并解压文件数据

    参数:
        zip_data (bytes): 压缩包数据喵
        file_name (str | None): 文件名，用于解压单个文件,为None时解压所有文件喵。默认为None喵

    返回:
        (dict[str, bytes]): 压缩包文件数据喵
    """
    files_dict = {}
    # 打开压缩包喵(其实存档是个压缩包哦喵！)
    with ZipFile(BytesIO(zip_data)) as zip_file:
        # 如果指定了文件名，那么将尝试解压单个文件喵
        if file_name is not None:
            # 获取压缩包文件名列表，用来判断指定的文件名是否存在喵
            file_name_list = [i.filename for i in zip_file.filelist]
            if file_name in file_name_list:
                # 如果文件存在于压缩包中喵
                with zip_file.open(file_name) as file:
                    files_dict[file_name] = file.read()

            else:
                # 如果文件不存在于压缩包中喵
                raise FileNotFoundError(f"无法在压缩包中找到文件喵：{file_name}")

        # 默认解压全部文件喵
        else:
            # 遍历压缩包所有文件喵
            for file in zip_file.filelist:
                # 获取压缩包文件名喵
                filename = file.filename
                logger.debug(f'解压"{filename}"文件喵')
                with zip_file.open(filename) as file:
                    files_dict[filename] = file.read()  # 读取文件数据喵

    logger.debug("解压完毕喵！")
    return files_dict


def zipSave(files_dict: Dict[str, Any]) -> bytes:
    """
    创建压缩包喵

    参数:
        files_dict (dict[str, Any]): 压缩包文件数据喵

    返回:
        (bytes): 压缩包数据喵
    """
    with BytesIO() as file:
        with ZipFile(file, "w", compression=ZIP_DEFLATED) as zip_file:
            for filename, filedata in files_dict.items():
                logger.debug(f'压缩"{filename}"文件喵')
                zip_file.writestr(filename, filedata)

        logger.debug("压缩完毕喵！")
        return file.getvalue()


def addDifficulty(record_data: dict, difficulty: Dict[str, list]) -> Dict[str, dict]:
    """
    为所有成绩添加谱面定数信息喵

    参数:
        record_data (dict): gameRecord/存档 反序列化数据喵
        difficulty (dict[str, list]): 歌曲谱面定数数据

    返回:
        (dict[str, dict]): 添加谱面定数信息后的 gameRecord/存档 反序列化数据喵
    """
    # 各难度的映射字典喵
    diff_list = {"EZ": 0, "HD": 1, "IN": 2, "AT": 3, "Legacy": 4}

    # 为单独传入gameRecord反序列化数据和传入存档反序列化数据两种情况提供支持喵
    if record_data.get("gameRecord") is not None and isinstance(
        record_data["gameRecord"], dict
    ):
        gameRecord = record_data["gameRecord"]

    else:
        gameRecord = record_data

    # 遍历所有歌曲成绩喵
    for songName, song in gameRecord.items():
        # 遍历单个歌曲中所有难度的成绩喵
        for diff in song.keys():
            try:
                # 尝试从定数数据获取该歌曲难度的谱面定数喵
                record_diff: float = difficulty[songName][diff_list[diff]]

            except KeyError:
                # 如果发生KeyError错误，那么就是因为歌曲名不存在于定数数据喵
                record_diff: float = 0
                logger.warning(f'歌曲"{songName}"的{diff}定数不存在喵！')

            except IndexError:
                # 如果出现IndexError，那么就是因为难度索引超出了喵
                record_diff: float = 0
                logger.warning(f'歌曲"{songName}"可能存在旧谱记录喵！')

            gameRecord[songName][diff].update({"difficulty": record_diff})

    return record_data


def countRks(
    record_data: dict, difficulty: Dict[str, list], onlyCountRks: bool = False
) -> Dict[str, dict]:
    """
    为反序列化后的gameRecord中的每条成绩添加难度定数并计算等效rks喵

    参数:
        record_data (dict):gameRecord/存档 反序列化数据喵
        difficulty (dict): 歌曲定数数据喵
        onlyCountRks (bool): 是否仅计算rks喵。默认为False，如果为True则只会计算等效rks而不添加谱面定数喵

    返回:
        (dict): 处理后的 gameRecord/存档 反序列化数据喵
    """
    if not onlyCountRks:
        record_data = addDifficulty(record_data, difficulty)

    if record_data.get("gameRecord") is not None and isinstance(
        record_data["gameRecord"], dict
    ):
        gameRecord = record_data["gameRecord"]

    else:
        gameRecord = record_data

    for songName, song in gameRecord.items():
        for diff in song.keys():
            try:
                record_diff: float = gameRecord[songName][diff]["difficulty"]
                acc = gameRecord[songName][diff]["acc"]
                if acc > 70:
                    rks = (((acc - 55) / 45) ** 2) * record_diff

                    # # 备用的计算方式喵，虽然感觉没有什么用喵
                    # from decimal import (
                    #     Decimal,
                    #     getcontext,
                    # )

                    # getcontext().prec = 30  # 设置Decimal上下文的小数精度为8位喵
                    # rks = float(
                    #     format(
                    #         ((Decimal(acc) - Decimal("55")) / Decimal("45"))
                    #         ** 2
                    #         * Decimal(record_diff),
                    #         ".15f",
                    #     )
                    # )  # 计算单曲rks喵

                else:
                    rks = 0.0

            except KeyError:
                rks: float = 0
                logger.warning(f'歌曲"{songName}"的{diff}定数不存在喵！')

            gameRecord[songName][diff].update({"rks": rks})

    return record_data


def getBest(
    record_data: dict, phi_count: int = 3, best_count: int = 27
) -> Dict[str, List[dict]]:
    """
    获取best成绩喵

    参数:
        record_data (dict): gameRecord/存档 反序列化数据喵
        phi (int): 要返回phi榜的前几条成绩喵。默认为3喵
        best (int): 要返回best榜的前几条成绩喵。默认为27喵

    返回:
        (dict[str, list[dict]]): best列表喵
    """
    all_record = []  # 存储所有打歌成绩记录喵

    if record_data.get("gameRecord") is not None and isinstance(
        record_data["gameRecord"], dict
    ):
        gameRecord = record_data["gameRecord"]

    else:
        gameRecord = record_data

    # 深度拷贝打歌成绩数据字典喵(防止进行best排序等操作影响到原数据喵)
    record = deepcopy(gameRecord)

    for song in record.items():  # 遍历所有歌曲记录喵
        for song_record in song[1].items():  # 遍历每首歌的所有难度记录喵
            song_record[1]["name"] = song[0]  # 取歌名添加进原数据中喵

            # 将难度等级添加进原数据中喵
            song_record[1]["level"] = song_record[0]
            all_record.append(song_record[1])  # 添加到全部记录列表中喵

    # 对全部记录以rks为准进行排序喵
    all_record.sort(key=lambda x: x["rks"], reverse=True)
    try:
        # 脑子爆烧唔，应该是取最高等效rks的phi成绩喵(抄过来的喵x)
        phi_list = list(filter(lambda x: x["score"] == 1000000, all_record))[:phi_count]

    except ValueError:
        logger.warning("好家伙，居然一首AP曲子都没有喵！")
        phi_list = []

    for p in phi_list:
        all_record.remove(p)

    # 返回best列表喵
    return {"phi": phi_list, "best": all_record[:best_count]}


def getB19(records: dict) -> List[dict]:
    """
    获取b19喵（现在Phigros已不使用b19进行计算rks了，请使用`getB30()`喵！）

    参数:
        records (dict): gameRecord/存档 反序列化数据喵

    返回:
        (list[dict]): b19列表喵
    """
    best_dict = getBest(records, 1, 19)
    phi, best = best_dict["phi"], best_dict["best"]

    phi.extend(best)
    return phi  # 返回b19喵(准确来说应该得叫b20喵)


def getB30(records: dict):
    """
    获取b30喵

    参数:
        records (dict): gameRecord/存档 反序列化数据喵

    返回:
        (list[dict]): b30列表喵
    """
    best_dict = getBest(records, 3, 27)
    phi, best = best_dict["phi"], best_dict["best"]

    phi.extend(best)
    return phi  # 返回b30喵


def decryptSave(save_dict: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    反序列化存档原始数据喵

    参数:
        save_dict (dict[str, Any]): 存档原始数据喵

    返回:
        (dict[str, dict]): 存档反序列化数据喵
    """
    file_head = {}  # 存储文件头数据喵
    # 获取每个文件的文件头喵（起始第一个字节喵）
    for key, value in save_dict.items():
        file_head[key] = value[0].to_bytes()

    # 根据文件头获取反序列化用的结构类喵
    structure_list = headGetStructure(file_head)

    for key, value in save_dict.items():
        save_dict[key] = decrypt(value[1:])

        reader = Reader(save_dict[key])
        save_dict[key] = reader.parseStructure(structure_list[key])

    return save_dict


def encryptSave(save_dict: Dict[str, Any]):
    """
    序列化存档数据喵

    参数:
        save_dict (dict[str, dict]): 存档反序列化数据喵

    返回:
        (dict[str, bytes]): 存档序列化数据喵
    """
    file_head = getFileHead(save_dict)
    structure_list = headGetStructure(file_head)

    for key, value in save_dict.items():
        reader = Writer()
        value = reader.buildStructure(structure_list[key], save_dict[key])

        save_dict[key] = file_head[key] + encrypt(value)

    return save_dict


def parseSaveDict(save_data: bytes):
    """
    反序列化存档原始数据为存档字典数据喵

    参数:
        save_data (bytes): 存档原始数据喵

    返回:
        (dict[str, dict[str, Any]]): 存档反序列化数据喵
    """
    return decryptSave(unzipFile(save_data))


def buildSaveDict(save_dict: Dict[str, dict]):
    """
    序列化存档字典数据为存档原始数据喵

    参数:
        save_dict (dict[str, dict]): 存档反序列化数据喵

    返回:
        (bytes): 存档原始数据喵
    """
    return zipSave(encryptSave(save_dict))


def findDifferentKeys(dict1: dict, dict2: dict):
    """
    寻找两个字典中不同的根键喵

    (将返回不同的根键列表，从后者向前者比较键的相同性喵)

    参数:
        dict1 (dict): 用于模板的字典喵
        dict2 (dict): 用于比较的字典喵

    返回:
        (list): 不同的根键列表喵
    """
    diff_keys = []  # 记录不同的根键喵

    for key in dict2.keys():  # 遍历第一个字典的根键喵
        # 如果第二个字典中不存在对应的根键，直接记录对应的根键喵
        if key not in dict1:
            diff_keys.append(key)

        else:
            # 比较对应根键的值是否相同，如果不同则记录对应的根键喵
            if dict1[key] != dict2[key]:
                diff_keys.append(key)

    return diff_keys  # 返回不同的大键喵


def readRecordHistory(recordHistory: Dict[str, dict]):
    """
    解析recordHistory喵

    参数:
        recordHistory (dict[str, dict]): recordHistory数据喵

    返回:
        (dict[str, dict]): 解析数据喵
    """
    # recordHistory = dict(sorted(recordHistory.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d_%H-%M-%S")))
    records = {}
    for history in recordHistory.values():
        if isinstance(history, dict):
            for name, record in history.items():
                records[name] = record

    return records


def checkSaveHistory(
    sessionToken: str,
    summary: dict,
    save_data: bytes,
    difficulty: Dict[str, list],
):
    """
    更新存档历史记录喵

    (存档历史记录存储在saveHistory文件夹下喵)

    参数
        sessionToken (str): 玩家的sessionToken喵
        summary (dict): 玩家的summary喵
        save_data (bytes): 存档原始数据喵
        difficulty (dict[str, list]): 难度定数数据喵

    返回:
        (bool): 是否更新了存档历史记录喵
    """
    nowTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 如果历史文件夹不存在则创建喵
    if not exists("saveHistory/"):
        mkdir("saveHistory/")
        logger.info("存档历史记录文件夹不存在喵！已创建喵！")

    # 如果对应token历史文件夹不存在则创建喵
    if not exists(f"saveHistory/{sessionToken}/"):
        mkdir(f"saveHistory/{sessionToken}/")
        logger.info("对应sessionToken的存档历史文件夹不存在喵！已创建喵！")

    if not exists(f"saveHistory/{sessionToken}/summaryHistory.json"):
        summaryHistory = {}
        logger.info("对应sessionToken的summary历史文件不存在，将会创建喵！")

    else:
        with open(
            f"saveHistory/{sessionToken}/summaryHistory.json",
            "r",
            encoding="utf-8",
        ) as file:
            summaryHistory = loads(file.read())

    if not exists(f"saveHistory/{sessionToken}/recordHistory.json"):
        recordHistory = {}
        logger.info("对应sessionToken的record历史文件不存在喵！已创建喵！")

    else:
        with open(
            f"saveHistory/{sessionToken}/recordHistory.json",
            "r",
            encoding="utf-8",
        ) as file:
            recordHistory = loads(file.read())

    # 获取历史所有校验值喵
    checksumHistory = [i.get("checksum") for i in summaryHistory.values()]

    # 如果没有相同校验值，则添加进历史记录并保存存档喵
    if not summary["checksum"] in checksumHistory:
        record_old = readRecordHistory(recordHistory)
        save_dict = unzipFile(save_data)

        del save_dict["gameKey"]
        del save_dict["gameProgress"]
        del save_dict["settings"]
        del save_dict["user"]

        save_dict = decryptSave(save_dict)
        record_new = save_dict["gameRecord"]
        differentRecord = findDifferentKeys(record_old, record_new)

        if differentRecord != []:
            summaryHistory[nowTime] = summary

            new_record = {}
            for key in differentRecord:
                new_record[key] = record_new[key]

            with open(
                f"saveHistory/{sessionToken}/summaryHistory.json",
                "w",
                encoding="utf-8",
            ) as file:
                file.write(dumps(summaryHistory, indent=4, ensure_ascii=False))

            with open(f"saveHistory/{sessionToken}/{nowTime}.save", "wb") as save:
                save.write(save_data)

            with open(
                f"saveHistory/{sessionToken}/recordHistory.json",
                "w",
                encoding="utf-8",
            ) as file:
                recordHistory[nowTime] = new_record
                file.write(dumps(recordHistory, indent=4, ensure_ascii=False))

            logger.info(f"已保存了新的record历史记录喵！歌曲数：{len(differentRecord)}")
            logger.info(f"已保存了新的存档历史记录喵！时间：{nowTime}")
            return True

        else:
            logger.info("歌曲记录相同，未记录为新存档记录喵！")
            return False

    else:
        logger.info("checksum未变动，未记录为新存档记录喵！")
        return False


def readTxtFile(path: str) -> List[str]:
    """
    读取txt文件喵

    参数:
        path (str): txt文件路径喵

    返回:
        (list[str]): txt文件所有行数据
    """
    txt_list = []
    with open(path, encoding="UTF-8") as f:  # 打开tsv列表文件喵
        lines = f.readlines()  # 解析所有行喵，输出一个列表喵

    for line in lines:  # 遍历所有行喵
        txt_list.append(line[:-1])  # 将该行最后的\n截取掉喵

    return txt_list  # 返回解析出来的数据喵


def readTsvFile(path: str):
    """
    读取tsv文件喵

    参数:
        path (str): tsv文件路径喵

    返回:
        (dict[str, list[str]]): tsv文件解析数据
    """
    tsv_list = {}
    with open(path, encoding="UTF-8") as f:  # 打开tsv列表文件喵
        lines = f.readlines()  # 解析所有行喵，输出一个列表喵

    for line in lines:  # 遍历所有行喵
        # 将该行最后的\n截取掉喵，并以\t为分隔符解析为一个列表喵
        line = line[:-1].split("\t")
        flags = []  # 用来存储单行信息喵

        for i in range(1, len(line)):  # 遍历该行后面的值喵
            flags.append(line[i])  # 添加到列表中喵
        tsv_list[line[0]] = flags  # 与总列表拼接在一起喵

    return tsv_list  # 返回解析出来的数据喵


def formatGameKey(save_dict: dict, filePath: str = "./") -> Dict[str, dict]:
    """
    为gameKey反序列化数据添加key类型标记喵（调试用，未来可能会删除喵）

    参数:
        save_dict (dict): 存档反序列化数据/gameKey数据喵
        filePath (str): 标记类型用的信息文件目录喵

    返回:
        (dict): 标记类型后的 存档反序列化数据/gamKey数据喵
    """
    if save_dict.get("gameKey") is not None:
        gameKeys = save_dict["gameKey"]["keyList"]

    else:
        gameKeys = save_dict

    allKey = {
        "avatar": readTxtFile(join(filePath, "avatar.txt")),
        "collection": readTsvFile(join(filePath, "collection.tsv")),
        "illustration": readTxtFile(join(filePath, "illustration.txt")),
        "single": readTxtFile(join(filePath, "single.txt")),
    }

    for key in allKey["avatar"]:
        try:
            gameKeys[key]["4avatar"] = eval(gameKeys[key]["type"])[4]
        except KeyError:
            pass

    for key in allKey["collection"].keys():
        try:
            gameKeys[key]["02collection"] = str(
                [eval(gameKeys[key]["type"])[0], eval(gameKeys[key]["type"])[2]]
            )
        except KeyError:
            pass

    for key in allKey["illustration"]:
        try:
            gameKeys[key]["3illustration"] = eval(gameKeys[key]["type"])[3]
        except KeyError:
            pass

    for key in allKey["single"]:
        try:
            gameKeys[key]["1single"] = eval(gameKeys[key]["type"])[1]
        except KeyError:
            pass

    return save_dict


def formatSaveDict(save_dict: Dict[str, dict]):
    """
    给save_dict排序喵（调试用，未来可能会删除喵）

    参数:
        save_dict (dict[str, dict]): 存档反序列化数据喵

    返回:
        (dict[str. dict]): 排序后的存档反序列化数据喵
    """
    new_save_dict = {}

    for key in ["user", "gameProgress", "settings", "gameRecord", "gameKey"]:
        if save_dict.get(key) is not None:
            new_save_dict[key] = save_dict[key]

    return new_save_dict
