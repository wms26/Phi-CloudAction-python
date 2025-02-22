# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from copy import deepcopy
from datetime import datetime
from io import BytesIO
from json import dumps, loads
import csv
import warnings
from os import mkdir
from os.path import exists, join
from re import match
from zipfile import ZipFile, ZIP_DEFLATED
import json

from typing import Any, Dict, List

from .AES import decrypt, encrypt
from .Structure import getStructure, getFileHead, Reader, Writer
from .logger import logger
from .other import add_game_record,complete_game_record,get_info_dir


# ---------------------- 定义赋值区喵 ----------------------
class b30():
    def __init__(self,p3:list,b27:list):
        self.p3:list = p3
        self.b27:list = b27
        self.b30:list = p3 + b27

    def __call__(self):
        return self.b30
    
class savesHistory():
    def __init__(self,summary:dict,record:dict):
        self.summary:dict = summary
        self.record:dict = record
        self.saves:dict = {"summary":summary,"record":record}

    def __call__(self):
        return self.saves

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


# 存档压缩包中的文件列表喵
SAVE_LIST = [
    "gameKey",
    "gameProgress",
    "gameRecord",
    "settings",
    "user",
]


def checkSessionToken(sessionToken: str,log_switch:bool = True):
    """
    检查sessionToken格式是否合法喵

    参数:
        sessionToken (str): 玩家的sessionToken喵
        log_switch (bool): 是否开启日志输出,默认为开

    返回:
        (bool): 是否合法喵
    """
    if sessionToken == "" or sessionToken is None:
        raise ValueError("sessionToken为空喵！")

    elif len(sessionToken) != 25:
        raise ValueError(
            f"sessionToken长度错误喵！应为25位，而不是{len(sessionToken)}位喵：{sessionToken}"
        )

    elif not match(r"^[0-9a-z]{25}$", sessionToken):
        raise ValueError(
            f"sessionToken不合法喵！应只有数字与小写字母喵：{sessionToken}"
        )

    else:
        if log_switch:
            logger.debug(f"sessionToken正确喵：{sessionToken}")
        return True

# 读取定数文件喵

def readDifficultyFile(path = str(get_info_dir() / "difficulty.tsv")) -> Dict[str, List[float]]:
    if path.endswith('.tsv'):
        return readFile.difficulty_tsv(path)
    elif path.endswith('.csv'):
        return readFile.difficulty_csv(path)
    else:
        raise ValueError("定数文件应该是.tsv或.csv")
    
class readFile():
    
    # 读取json喵
    @staticmethod
    def json(path: str) -> Dict:
        """
        从 JSON 文件读取数据喵~
        """
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
        
    # 读取tsv定数
    @staticmethod
    def difficulty_tsv(path: str) -> Dict[str, List[float]]:
        """
        读取难度文件喵

        参数:
            path (str): 难度文件路径喵

        返回:
            (dict[str, list[float]]): 难度数据喵。以歌曲id为键，值为单曲难度列表喵
        """
        difficulty_list = {}

        with open(path, encoding="UTF-8", newline='') as f:  # 打开难度列表文件喵
            reader = csv.reader(f, delimiter="\t")  # 使用csv.reader并设置分隔符为tab
            for row in reader:
                song_id = row[0]
                diff = [float(value) for value in row[1:]]  # 转换后面的难度值为float并存入列表
                difficulty_list[song_id] = diff  # 将歌曲id和难度列表存入字典

        return difficulty_list  # 返回解析出来的各歌曲难度列表喵
    
    # 读取csv定数
    @staticmethod
    def difficulty_csv(path: str = "./info/difficulty.csv") -> Dict[str, List[float]]:
        """
        读取带有标题行的难度文件喵。

        参数:
            path (str): 难度文件路径喵

        返回:
            (dict[str, list[float]]): 难度数据。以歌曲ID为键，值为单曲难度列表
        """
        difficulty_list = {}

        with open(path, encoding="UTF-8") as f:
            reader = csv.reader(f, delimiter=',')  # 使用csv库读取文件
            next(reader)  # 跳过标题行

            for row in reader:
                song_id = row[0]  # 获取歌曲ID
                diff_values = [float(x) for x in row[1:] if x]  # 忽略空值
                difficulty_list[song_id] = diff_values

        return difficulty_list

def unzipFile(zip_data: bytes, filename: str):
    """
    读取压缩文件中的文件喵

    参数:
        zip_data (bytes): 压缩包数据喵
        filename (str): 要读取的文件名喵

    返回:
        (bytes): 文件数据喵
    """
    # 打开存档文件喵
    with ZipFile(BytesIO(zip_data)) as zip_file:
        # 打开压缩包中中对应的文件喵
        with zip_file.open(filename) as file:
            logger.debug(f'解压单文件"{filename}"喵')
            return file.read()  # 返回文件数据喵


def unzipSave(zip_data: bytes) -> Dict[str, bytes]:
    """
    读取存档压缩包

    参数:
        zip_data (bytes): 压缩包数据喵

    返回:
        (dict[str, bytes]): 存档原始数据喵
    """
    save_dict = {}
    # 打开存档文件喵(其实存档是个压缩包哦喵！)
    with ZipFile(BytesIO(zip_data)) as zip_file:
        # 打开压缩包中中对应的文件喵

        for file in zip_file.filelist:
            filename = file.filename
            logger.debug(f'解压"{filename}"文件喵')
            with zip_file.open(filename) as file:
                save_dict[filename] = file.read()  # 读取文件数据喵

    logger.debug("解压完毕喵！")
    return save_dict


def zipSave(save_dict: Dict[str, Any]):
    """
    创建存档压缩包

    参数:
        save_dict (dict[str, Any]): 存档原始数据喵

    返回:
        (bytes): 压缩包数据喵
    """
    with BytesIO() as file:
        with ZipFile(file, "w", compression=ZIP_DEFLATED) as zip_file:
            for filename, filedata in save_dict.items():
                logger.debug(f'压缩"{filename}"文件喵')
                zip_file.writestr(filename, filedata)

        logger.debug("压缩完毕喵！")
        return file.getvalue()


def countRks(
    record_data: dict, difficulty: Dict[str, list], countRks: bool = True
):
    """
    为反序列化后的gameRecord中的每条成绩添加难度定数并计算等效rks

    参数:
        record_data (dict):gameRecord反序列化数据/存档反序列化数据
        difficulty (dict): 所有歌曲难度定数数据
        countRks (bool): 是否计算rks。默认为True，如果为False则只会添加难度定数

    返回:
        (dict): 处理后的 gameRecord反序列化数据/存档反序列化数据
    """
    diff_list = {"EZ": 0, "HD": 1, "IN": 2, "AT": 3, "Legacy": 4}

    if record_data.get("gameRecord") is not None and isinstance(
        record_data["gameRecord"], dict
    ):
        gameRecord = record_data["gameRecord"]

    else:
        gameRecord = record_data

    for songName, song in gameRecord.items():
        for diff in song.keys():
            try:
                record_diff: float = difficulty[songName][diff_list[diff]]
                acc = gameRecord[songName][diff]["acc"]
                if countRks and acc > 70:
                    rks: float = (((acc - 55) / 45) ** 2) * record_diff

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
                    rks: float = 0

            except KeyError:
                record_diff: float = 0
                rks: float = 0
                logger.warning(f"歌曲{songName}的{diff}定数不存在喵！")
            except IndexError:
                record_diff: float = 0
                rks: float = 0
                logger.warning(f"歌曲{songName}可能存在旧谱记录喵！")

            if countRks:
                gameRecord[songName][diff].update(
                    {"difficulty": record_diff, "rks": rks}
                )

            else:
                gameRecord[songName][diff].update(
                    {
                        "difficulty": record_diff,
                    }
                )

    return record_data

def getB30(records: dict, difficult: dict,b_num: int = 27) -> b30:
    """
    获取b30喵

    参数:
        records (dict): 打歌成绩数据喵
        difficult (dict): 歌曲难度数据喵
        b_num (int): 返回的b的数量,不包含p3,默认为27

    返回:
        (b30): b30喵,可以访问属性p3、b27和b30获得数据喵。也可以当函数使用,会返回b30
    """
    diff_list = {"EZ": 0, "HD": 1, "IN": 2, "AT": 3, "Legacy": 4}
    all_record = []  # 存储所有打歌成绩记录喵

    # 深度拷贝打歌成绩数据字典喵(防止进行b30排序等操作影响到原数据喵)
    record = deepcopy(records)

    for song in record.items():  # 遍历所有歌曲记录喵
        for song_record in song[1].items():  # 遍历每首歌的所有难度记录喵
            song_record[1]["name"] = song[0]  # 取歌名添加进原数据中喵
            song_record[1]["level"] = song_record[0]  # 将难度等级添加进原数据中喵
            if song_record[1]["acc"] < 70:  # 如果acc小于70，则跳过该记录
                continue
            try:
                difficulty: float = difficult[song[0]][diff_list[song_record[0]]]
            except IndexError as e:
                logger.error("没有找到定数,可能是difficulty.tsv版本太旧,请更新")
                raise RuntimeError
            song_record[1]["rks"] = (
                ((song_record[1]["acc"] - 55) / 45) ** 2
            ) * difficulty
            all_record.append(song_record[1])  # 添加到全部记录列表中喵

    # 对全部记录以rks为准进行排序
    def sort_by_rks(record):
        """
        以rks进行排序的辅助函数喵
        """
        return record["rks"]
    
    all_record.sort(key=sort_by_rks, reverse=True)

    # 获取3个最高等效rks的phi成绩
    phi_top_3 = []
    try:
        for record in all_record:
            if record["score"] == 1000000:
                phi_top_3.append(record)
                if len(phi_top_3) == 3:
                    break
        if not phi_top_3:
            raise ValueError("没有AP曲子喵！")
    except ValueError:
        logger.warning("好家伙，居然一首AP曲子都没有喵！")
        phi_top_3 = []

    # 获取N个最高rks的成绩
    top_27 = all_record[:b_num]
    
    return b30(p3=phi_top_3,b27=top_27)

# 兼容性
def getB19(records: dict, difficult: dict):
    warnings.warn("getB19 is deprecated, use getB30.", DeprecationWarning, 2)
    return getB30(records, difficult).b30  # 调用新函数


def decryptSave(save_dict: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    反序列化存档原始数据喵

    参数:
        save_dict (dict[str, Any]): 存档原始数据喵(unzipSave()可得喵)

    返回:
        (dict[str, dict]): 存档反序列化数据喵
    """
    file_head = {}
    for key, value in save_dict.items():
        file_head[key] = value[0].to_bytes()

    structure_list = getStructure(file_head)

    for key, value in save_dict.items():
        save_dict[key] = decrypt(value[1:])

        reader = Reader(save_dict[key])
        save_dict[key] = reader.parseStructure(structure_list[key])

    return save_dict


def encryptSave(save_dict: Dict[str, Any]):
    """
    序列化存档数据喵

    参数:
        save_dict (dict[str, dict]): 反序列化存档数据喵

    返回:
        (dict[str, bytes]): 序列化存档数据喵
    """

    file_head = getFileHead(save_dict)
    structure_list = getStructure(file_head)

    for key, value in save_dict.items():
        reader = Writer()
        value = reader.buildStructure(structure_list[key], save_dict[key])

        save_dict[key] = file_head[key] + encrypt(value)

    return save_dict


def parseSave(save_data: bytes):
    """
    反序列化存档数据

    参数:
        save_data (bytes): 存档数据

    返回:
        (dict[str, dict[str, Any]]): 反序列化后的存档数据
    """
    return decryptSave(unzipSave(save_data))


def buildSave(save_dict: Dict[str, dict]):
    """
    序列化存档数据

    参数:
        save_dict (dict[str, dict]): 反序列化后的存档数据

    返回:
        (bytes): 存档数据
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

    return diff_keys  # 返回不同的大键


def loadRecordHistory(recordHistory: Dict[str, dict]):
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

def readSaveHistory(sessionToken:str) -> savesHistory:
    """
    读取存档历史记录喵

    参数
        sessionToken (str): 玩家的sessionToken喵

    返回:
        (savesHistory): 存档历史记录喵,可以访问属性summary、record和saves获得数据喵。也可以当函数使用,会返回saves
    """
    recordHistory_path = f"saveHistory/{sessionToken}/recordHistory.json"
    summaryHistory_path = f"saveHistory/{sessionToken}/summaryHistory.json"
    if not exists(recordHistory_path) or not exists(summaryHistory_path):
        raise RuntimeError("存档不存在喵!")
    recordHistory:dict = readFile.json(recordHistory_path)
    summaryHistory:dict = readFile.json(summaryHistory_path)
    return savesHistory(record=recordHistory,summary=summaryHistory)

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
        save_data (bytes): 存档数据喵
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
        record_old = loadRecordHistory(recordHistory)
        save_dict = unzipSave(save_data)

        del save_dict["gameKey"]
        del save_dict["gameProgress"]
        del save_dict["settings"]
        del save_dict["user"]

        save_dict = countRks(decryptSave(save_dict), difficulty, False)
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

            with open(
                f"saveHistory/{sessionToken}/{nowTime}.save", "wb"
            ) as save:
                save.write(save_data)

            with open(
                f"saveHistory/{sessionToken}/recordHistory.json",
                "w",
                encoding="utf-8",
            ) as file:
                recordHistory[nowTime] = new_record
                file.write(dumps(recordHistory, indent=4, ensure_ascii=False))

            logger.info(
                f"已保存了新的record历史记录喵！歌曲数：{len(differentRecord)}"
            )
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
    为gameKey反序列化数据添加key类型标记

    参数:
        save_dict (dict): 存档数据/gameKey数据
        filePath (str): 标记类型用的信息文件目录

    返回:
        (dict): 标记类型后的 存档数据/gamKey数据
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
    new_save_dict = {}

    for key in ["user", "gameProgress", "settings", "gameRecord", "gameKey"]:
        if save_dict.get(key) is not None:
            new_save_dict[key] = save_dict[key]

    return new_save_dict
