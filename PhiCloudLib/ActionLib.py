# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from copy import deepcopy
from datetime import datetime
from io import BytesIO
from json import dumps, loads
from os import mkdir
from os.path import exists
from re import match
from sys import exit as exti  # emm我也不知道为啥要这样子做（
from zipfile import ZipFile, ZIP_DEFLATED

from PhiCloudLib.AES import decrypt, encrypt
from PhiCloudLib.ParseGameSave import ParseGameRecord


# ---------------------- 定义赋值区喵 ----------------------

def Temporary_files(string, mode: str, filetype: str):  # 这个是测试debug用的喵，不用多管喵（
    with open('./awa.' + filetype, mode) as f:  # 算是写个临时文件用来debug数据处理情况喵
        f.write(string)  # 写入文件


file_headers = {  # 存档中各文件的版本号文件头喵
    'gameKey': b'\x02',
    'gameProgress': b'\x03',
    'gameRecord': b'\x01',
    'settings': b'\x01',
    'user': b'\x01'
}


def check_sessionToken(sessionToken: str, doExti=True):
    """检查sessionToken格式是否正确喵\n
    sessionToken：正如其名喵"""
    if sessionToken == '' or sessionToken is None:
        print('[Error]sessionToken为空喵！')
        if doExti:
            exti()
        return False

    elif len(sessionToken) != 25:
        print(f'[Error]sessionToken长度错误喵！当前为{len(sessionToken)}位喵，应为25位喵！')
        if doExti:
            exti()
        return False

    elif not match(r'^[0-9a-z]{25}$', sessionToken):
        print(f'[Error]sessionToken不合法喵！应只有数字与小写字母喵！')
        if doExti:
            exti()
        return False

    else:
        return True


def readDifficulty(path: str):
    """读取难度文件喵\n
    path：难度文件路径喵"""
    difficulty_list = {}
    with open(path, encoding="UTF-8") as f:  # 打开难度列表文件喵
        lines = f.readlines()  # 解析所有行喵，输出一个列表喵

    for line in lines:  # 遍历所有行喵
        line = line[:-1].split("\t")  # 将该行最后的\n截取掉喵，并以\t为分隔符解析为一个列表喵
        diff = []  # 用来存储单首歌的难度信息喵

        for i in range(1, len(line)):  # 遍历该行后面的那三个难度值喵
            diff.append(float(line[i]))  # 将难度添加到列表中喵
        difficulty_list[line[0]] = diff  # 与总列表拼接在一起喵

    return difficulty_list  # 返回解析出来的各歌曲难度列表喵


def unzipSave(saveData: bytes, filename: str):
    """读取存档压缩文件中的filename文件喵\n
    save_data：存档压缩文件数据喵\n
    filename：要读取的文件名喵"""
    with ZipFile(BytesIO(saveData)) as f:  # 打开存档文件喵(其实存档是个压缩包哦喵！)
        with f.open(filename) as saveFile:  # 打开存档中对应的文件喵
            file_header = saveFile.read(1)  # 读取当前文件的文件头喵
            print(f'[Info]"{filename}"文件的版本号文件头喵:', file_header)

            if file_header != file_headers[filename]:  # 从file_headers取当前文件对应的文件头喵，之后判断文件头喵
                raise Exception('版本号不正确喵，可能协议已更新喵。文件头应为:', file_headers[filename])

            return saveFile.read()  # 如果文件头正确喵，则返回当前读取的存档文件数据喵


def getB19(records: dict):
    """获取b19喵\n
    records：打歌成绩数据字典喵"""
    all_record = []  # 临时存储另一种格式的所有打歌成绩记录喵
    record = deepcopy(records)  # 深度拷贝打歌成绩数据字典喵(防止进行b19排序等操作影响到原数据喵)

    # 这段代码怪复杂的喵(至少对于本喵来说喵，明明是自己写的却看不太懂喵)
    for song in record.items():  # 遍历所有歌曲记录喵
        for song_record in song[1].items():  # 遍历每首歌的所有难度记录喵
            song_record[1]['name'] = song[0]  # 取歌名添加进原数据中喵
            song_record[1]['level'] = song_record[0]  # 将难度等级添加进原数据中喵
            all_record.append(song_record[1])  # 添加到全部记录列表中喵

    all_record.sort(key=lambda x: x["rks"], reverse=True)  # 对全部记录以rks为准进行排序
    try:
        b19 = [max(filter(lambda x: x["score"] == 1000000, all_record), key=lambda x: x["difficulty"])]  # 脑子爆烧唔(抄过来的喵)
    except ValueError:  # 如果找不到AP曲子就返回全部记录列表的前19个
        print('[Warn]好家伙喵，居然一首AP曲子都没有喵！')
        return all_record[:19]
    b19.extend(all_record[:19])  # 将全部记录列表中取前19个拼接到b19列表中喵，准确来说是b20喵(?)
    return b19  # 返回b19喵(准确来说应该得叫b20喵)


def readGameSave(saveData: bytes, saveDict: dict):
    """读取存档压缩包中所有文件喵\n
    saveData：存档压缩包数据喵\n
    saveDict：存档数据字典喵"""
    saveDict['user']: bytes = unzipSave(saveData, 'user')
    saveDict['progress']: bytes = unzipSave(saveData, 'gameProgress')
    saveDict['setting']: bytes = unzipSave(saveData, 'settings')
    saveDict['record']: bytes = unzipSave(saveData, 'gameRecord')
    saveDict['key']: bytes = unzipSave(saveData, 'gameKey')


def decryptGameSave(saveDict: dict):
    """解密存档数据字典中的所有文件的数据喵\n
    saveDict：存档数据字典喵"""
    saveDict['user']: bytes = decrypt(saveDict['user'])
    saveDict['progress']: bytes = decrypt(saveDict['progress'])
    saveDict['setting']: bytes = decrypt(saveDict['setting'])
    saveDict['record']: bytes = decrypt(saveDict['record'])
    saveDict['key']: bytes = decrypt(saveDict['key'])


def encryptGameSave(saveDict: dict):
    """加密存档数据字典中的所有文件的数据喵\n
    saveDict：存档数据字典喵"""
    saveDict['user']: bytes = encrypt(saveDict['user'])
    saveDict['progress']: bytes = encrypt(saveDict['progress'])
    saveDict['setting']: bytes = encrypt(saveDict['setting'])
    saveDict['record']: bytes = encrypt(saveDict['record'])
    saveDict['key']: bytes = encrypt(saveDict['key'])


def zipGameSave(saveDict: dict):
    """将存档数据字典中的所有文件数据加密后压缩成存档压缩包中喵\n
    saveDict：存档数据字典喵"""
    with BytesIO() as f:  # 创建一个内存中的文件对象喵
        with ZipFile(f, 'a', compression=ZIP_DEFLATED) as saveFile:  # 创建一个压缩包文件喵
            saveFile.writestr('gameKey', file_headers['gameKey'] + saveDict['key'])
            saveFile.writestr('gameProgress', file_headers['gameProgress'] + saveDict['progress'])
            saveFile.writestr('gameRecord', file_headers['gameRecord'] + saveDict['record'])
            saveFile.writestr('settings', file_headers['settings'] + saveDict['setting'])
            saveFile.writestr('user', file_headers['user'] + saveDict['user'])
        return f.getvalue()  # 返回压缩包数据喵


def find_differentKeys(dict1: dict, dict2: dict):
    """寻找两个字典中不同的键\n
    dict1：用于模板的字典\n
    dict2：用于比较的字典\n
    (将返回不同的根键列表，从后者向前者比较键的相同性)"""
    diff_keys = []  # 记录不同的大键

    for key in dict2.keys():  # 遍历第一个字典的大键
        if key not in dict1:  # 如果第二个字典中不存在对应的大键，直接记录为不同的大键
            diff_keys.append(key)
        else:
            if dict1[key] != dict2[key]:  # 比较对应大键的值是否相同，如果不同则记录为不同的大键
                diff_keys.append(key)

    return diff_keys  # 返回不同的大键


def load_recordHistory(recordHistory: dict):
    """解析record历史"""
    # sorted_history = dict(sorted(recordHistory.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d_%H-%M-%S")))
    records = {}
    for history in recordHistory.values():
        for name, record in history.items():
            records[name] = record

    return records


def check_saveUpload(sessionToken: str, summary: dict, saveData: bytes, difficulty: dict):
    """存储存档历史记录"""
    if not exists('saveHistory/'):  # 如果历史文件夹不存在则创建喵
        mkdir('saveHistory/')
        print('[Info]存档历史记录文件夹不存在喵！已创建喵！')

    if not exists(f'saveHistory/{sessionToken}/'):  # 如果对应token历史文件夹不存在则创建喵
        mkdir(f'saveHistory/{sessionToken}/')
        print('[Info]对应sessionToken的存档历史文件夹不存在喵！已创建喵！')

    if not exists(f'saveHistory/{sessionToken}/summaryHistory.json'):  # 如果对应token的summary历史文件不存在则创建并写入存档喵
        nowTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        with open(f'saveHistory/{sessionToken}/summaryHistory.json', 'w', encoding='utf-8') as file:
            file.write(dumps({nowTime: summary}, indent=4, ensure_ascii=False))
        print('[Info]对应sessionToken的summary历史文件不存在喵！已创建喵！')

        with open(f'saveHistory/{sessionToken}/{nowTime}.save', 'wb') as save:
            save.write(saveData)
        print(f'[Info]已保存了新的存档历史记录喵！时间喵：{nowTime}')

    if not exists(f'saveHistory/{sessionToken}/recordHistory.json'):
        nowTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        with open(f'saveHistory/{sessionToken}/recordHistory.json', 'w', encoding='utf-8') as file:
            record_new = ParseGameRecord(decrypt(unzipSave(saveData, 'gameRecord')), difficulty)
            file.write(dumps({nowTime: record_new}, indent=4, ensure_ascii=False))
        print('[Info]对应sessionToken的record历史文件不存在喵！已创建喵！')

    else:  # 若对应token的summary的历史文件存在则进行对比喵
        with open(f'saveHistory/{sessionToken}/summaryHistory.json', 'r', encoding='utf-8') as file:
            summaryHistory: dict = loads(file.read())

        checksumHistory = [i.get('checksum') for i in summaryHistory.values()]  # 获取历史所有校验值喵

        # 如果没有相同校验值喵，则添加进历史记录并写入存档喵
        if not summary['checksum'] in checksumHistory:
            with open(f'saveHistory/{sessionToken}/recordHistory.json', 'r', encoding='utf-8') as file:
                recordHistory = loads(file.read())

            record_old = load_recordHistory(recordHistory)
            record_new = ParseGameRecord(decrypt(unzipSave(saveData, 'gameRecord')), difficulty)
            differentRecord = find_differentKeys(record_old, record_new)

            if differentRecord:
                nowTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                summaryHistory[nowTime] = summary

                new_record = {}
                for key in differentRecord:
                    new_record[key] = record_new[key]

                with open(f'saveHistory/{sessionToken}/summaryHistory.json', 'w', encoding='utf-8') as file:
                    file.write(dumps(summaryHistory, indent=4, ensure_ascii=False))

                with open(f'saveHistory/{sessionToken}/{nowTime}.save', 'wb') as save:
                    save.write(saveData)

                with open(f'saveHistory/{sessionToken}/recordHistory.json', 'w', encoding='utf-8') as file:
                    recordHistory[nowTime] = new_record
                    file.write(dumps(recordHistory, indent=4, ensure_ascii=False))
                print(f'[Info]已保存了新的record历史记录喵！歌曲数：{len(differentRecord)}')
                print(f'[Info]已保存了新的存档历史记录喵！时间喵：{nowTime}')

            else:
                print('[Info]歌曲记录相同喵！未记录为新存档记录喵！')

        else:
            print('[Info]checksum重复喵！未记录为新存档记录喵！')
