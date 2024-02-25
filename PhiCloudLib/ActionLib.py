# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from io import BytesIO
from re import match


# ---------------------- 定义赋值区喵 ----------------------

def Temporary_files(string, mode: str, filetype: str):  # 这个是测试debug用的喵，不用多管喵（
    with open('./awa.' + filetype, mode) as f:  # 算是写个临时文件用来debug数据处理情况喵
        f.write(string)


file_headers = {  # 存档中各文件的版本号文件头喵
    'gameKey': b'\x02',
    'gameProgress': b'\x03',
    'gameRecord': b'\x01',
    'settings': b'\x01',
    'user': b'\x01'
}


def check_sessionToken(sessionToken: str):
    if sessionToken == '' or sessionToken is None:
        print('[Error]sessionToken为空喵！')
        return False
    elif len(sessionToken) != 25:
        print(f'[Error]sessionToken长度错误喵！当前为{len(sessionToken)}位喵，应为25位喵！')
        return False
    elif not match(r'^[0-9a-z]{25}$', sessionToken):
        print(f'[Error]sessionToken不合法喵！应只有数字与小写字母喵！')
        return False
    else:
        return True


def readDifficulty(path: str):
    """读取难度文件喵\n
    path：难度文件路径喵"""
    difficulty_list = {}
    with open(path, encoding="UTF-8") as f:  # 打开难度列表文件喵
        lines = f.readlines()  # 解析所有行喵，输出一个列表喵

    for line in lines:  # 遍历所有行
        line = line[:-1].split("\t")  # 将该行最后的\n截取掉喵，并以\t为分隔符解析为一个列表喵
        diff = []  # 用来存储单首歌的难度信息喵

        for i in range(1, len(line)):  # 遍历该行后面的那三个难度值喵
            diff.append(float(line[i]))  # 将难度添加到列表中喵
        difficulty_list[line[0]] = diff  # 与总列表拼接在一起喵

    return difficulty_list  # 返回解析出来的各歌曲难度列表喵


def readGameSave(saveData: bytes, filename: str):
    """读取存档压缩文件中的filename文件喵\n
    save_data：存档压缩文件数据喵\n
    filename：要读取的文件名喵"""
    with ZipFile(BytesIO(saveData)) as f:  # 打开存档文件喵(其实存档是个压缩包哦喵！)
        with f.open(filename) as saveFile:  # 打开存档中对应的文件喵
            print(f'[Info]"{filename}"文件的版本号文件头喵:', saveFile.read(1))
            saveFile.seek(0)

            if saveFile.read(1) != file_headers[filename]:  # 从file_headers取当前文件对应的文件头喵，之后判断文件头喵
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
            all_record.append(song_record[1])  # 添加到全部记录列表中喵

    all_record.sort(key=lambda x: x["rks"], reverse=True)  # 对全部记录以rks为准进行排序
    b19 = [max(filter(lambda x: x["score"] == 1000000, all_record), key=lambda x: x["difficulty"])]  # 脑子爆烧唔(抄过来的喵)
    b19.extend(all_record[:19])  # 将全部记录列表中取前19个拼接到b19列表中喵，准确来说是b20喵(?)
    return b19  # 返回b19喵(准确来说应该得叫b20喵)


def zipGameSave(gameKey: bytes, gameProgress: bytes, gameRecord: bytes, settings: bytes, user: bytes):
    with BytesIO() as f:
        with ZipFile(f, 'a', compression=ZIP_DEFLATED) as saveFile:
            saveFile.writestr('gameKey', file_headers['gameKey'] + gameKey)
            saveFile.writestr('gameProgress', file_headers['gameProgress'] + gameProgress)
            saveFile.writestr('gameRecord', file_headers['gameRecord'] + gameRecord)
            saveFile.writestr('settings', file_headers['settings'] + settings)
            saveFile.writestr('user', file_headers['user'] + user)
        return f.getvalue()
