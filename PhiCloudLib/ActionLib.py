# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from copy import deepcopy
from io import BytesIO
from zipfile import ZipFile
from re import match


# ---------------------- 定义赋值区 ----------------------

def Temporary_files(string, mode: str, filetype: str):  # 这个是测试debug用的，不用多管（
    with open('./awa.' + filetype, mode) as f:  # 算是写个临时文件用来debug数据处理情况
        f.write(string)


file_headers = {  # 存档中各文件的版本号文件头
    'gameKey': b'\x02',
    'gameProgress': b'\x03',
    'gameRecord': b'\x01',
    'settings': b'\x01',
    'user': b'\x01'
}


def check_sessionToken(sessionToken: str):
    if sessionToken == '' or sessionToken is None:
        print('[Error]sessionToken为空！')
        return False
    elif len(sessionToken) != 25:
        print(f'[Error]sessionToken长度错误！当前为{len(sessionToken)}位，应为25位！')
        return False
    elif not match(r'^[0-9a-z]{25}$', sessionToken):
        print(f'[Error]sessionToken不合法！应只有数字与小写字母！')
        return False
    else:
        return True


def readDifficulty(path: str):
    """读取难度文件\n
    path：难度文件路径"""
    difficulty_list = {}
    with open(path, encoding="UTF-8") as f:  # 打开难度列表文件
        lines = f.readlines()  # 解析所有行，输出一个列表

    for line in lines:  # 遍历所有行
        line = line[:-1].split("\t")  # 将该行最后的\n截取掉，并以\t为分隔符解析为一个列表
        diff = []  # 用来存储单首歌的难度信息

        for i in range(1, len(line)):  # 遍历该行后面的那三个难度值
            diff.append(float(line[i]))  # 将难度添加到列表中
        difficulty_list[line[0]] = diff  # 与总列表拼接在一起

    return difficulty_list  # 返回解析出来的各歌曲难度列表


def readGameSave(save_data: bytes, filename: str):
    """读取存档压缩文件中的filename文件\n
    save_data：存档压缩文件数据\n
    filename：要读取的文件名"""
    with ZipFile(BytesIO(save_data)) as f:  # 打开存档文件(其实存档是个压缩包哦！)
        with f.open(filename) as saveFile:  # 打开存档中对应的文件
            print(f'[Info]"{filename}"文件的版本号文件头为:', saveFile.read(1))
            saveFile.seek(0)

            if saveFile.read(1) != file_headers[filename]:  # 从file_headers取当前文件对应的文件头，之后判断文件头
                raise Exception('版本号不正确，可能协议已更新。文件头应为:', file_headers[filename])

            return saveFile.read()  # 如果文件头正确，则返回当前读取的存档文件数据


def getB19(records: dict):
    """获取b19\n
    records：打歌成绩数据字典"""
    all_record = []  # 临时存储另一种格式的所有打歌成绩记录
    record = deepcopy(records)  # 深度拷贝打歌成绩数据字典(防止进行b19排序等操作影响到原数据)

    # 这段代码怪复杂的(至少对于我来说，明明是自己写的却看不太懂)
    for song in record.items():  # 遍历所有歌曲记录
        for song_record in song[1].items():  # 遍历每首歌的所有难度记录
            song_record[1]['name'] = song[0]  # 取歌名添加进原数据中
            all_record.append(song_record[1])  # 添加到全部记录列表中

    all_record.sort(key=lambda x: x["rks"], reverse=True)  # 对全部记录以rks为准进行排序
    b19 = [max(filter(lambda x: x["score"] == 1000000, all_record), key=lambda x: x["difficulty"])]  # 脑子爆烧(抄过来的)
    b19.extend(all_record[:19])  # 将全部记录列表中取前19个拼接到b19列表中，准确来说是b20(?)
    return b19  # 返回b19(准确来说应该得叫b20)

# ----------------------- 运行区 -----------------------
