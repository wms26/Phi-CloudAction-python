# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from PhiCloudLib.ByteReader import ByteReader, getBit, getBits


# ---------------------- 定义赋值区喵 ----------------------


def ParseGameKey(saveDict: dict):
    """解析gameKey喵\n
    saveDict：存档的字典数据喵"""
    Reader = ByteReader(saveDict.copy()['key'])  # 将data数据传给ByteReader来进行后续字节读取操作喵
    keySum: int = Reader.getVarInt()  # 总共key的数量，决定循环多少次喵
    all_keys = saveDict['key'] = {}  # 用来存储解析出来的数据喵

    for _ in range(keySum):  # 循环keySum次喵
        name: str = Reader.getString()  # key的昵称喵
        length: int = Reader.getByte()  # 总数据长度喵(不包含key的昵称喵)
        Key = all_keys[name] = {}  # 存储单个key的数据喵
        Key['type']: str = str(getBits(Reader.getByte())[:-3])  # 获取key的类型标志喵

        flag: list = []  # 用来存储该key的状态喵(比如头像是否获得/曲绘是否解锁/收藏品是否获取/打开喵)
        for i in range(length - 1):  # 因为前面已经读取了一个类型标志了喵，所以减一喵
            flag.append(Reader.getByte())
        Key['flag'] = str(flag)

    all_keys['lanotaReadKeys'] = Reader.getByte()  # 读取Lanota收藏品喵(解锁倒霉蛋和船的AT喵)
    all_keys['camelliaReadKey'] = Reader.getByte()  # 读取极星卫破译收藏品喵(解锁S.A.T.E.L.L.I.T.E.的AT喵)


def ParseGameProgress(saveDict: dict):
    """解析gameProgress喵\n
    saveDict：存档的字典数据喵"""
    Reader = ByteReader(saveDict.copy()['progress'])  # 将data数据传给ByteReader来进行后续字节读取操作喵
    all_progress = saveDict['progress'] = {}
    tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面4个数据喵（
    all_progress['isFirstRun']: int = tem[0]  # 首次运行喵
    all_progress['legacyChapterFinished']: int = tem[1]  # 过去的章节已完成喵
    all_progress['alreadyShowCollectionTip']: int = tem[2]  # 已展示收藏品Tip喵
    all_progress['alreadyShowAutoUnlockINTip']: int = tem[3]  # 已展示自动解锁IN Tip喵
    all_progress['completed']: int = Reader.getString()  # 剧情完成喵(显示全部歌曲和课题模式入口喵)
    all_progress['songUpdateInfo']: int = Reader.getVarInt()  # 喵喵喵？
    all_progress['challengeModeRank']: int = Reader.getShort()  # 课题分喵

    money: list = []  # 应该不用多说了吧喵（
    for i in range(5):
        money.append(Reader.getVarInt())
    all_progress['money']: str = str(money)

    all_progress['unlockFlagOfSpasmodic']: str = str(getBits(Reader.getByte())[:-4])  # Spasmodic解锁喵
    all_progress['unlockFlagOfIgallta']: str = str(getBits(Reader.getByte())[:-4])  # Igallta解锁喵
    all_progress['unlockFlagOfRrharil']: str = str(getBits(Reader.getByte())[:-4])  # Rrhar'il解锁喵

    # (倒霉蛋,船,Shadow,心之所向,inferior,DESTRUCTION 3,2,1,Distorted Fate)
    all_progress['flagOfSongRecordKey']: str = str(getBits(Reader.getByte()))  # 部分歌曲IN达到S喵

    all_progress['randomVersionUnlocked']: str = str(getBits(Reader.getByte())[:-2])  # Random切片解锁喵
    tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面3个数据喵（
    all_progress['chapter8UnlockBegin']: int = tem[0]  # 第八章入场喵
    all_progress['chapter8UnlockSecondPhase']: int = tem[1]  # 第八章第二阶段喵
    all_progress['chapter8Passed']: int = tem[2]  # 第八章通过喵
    all_progress['chapter8SongUnlocked']: int = str(getBits(Reader.getByte())[:-2])  # 第八章各曲目解锁喵

    if Reader.remaining() > 0 or Reader.remaining() < 0:
        print(f'[Warn]警告喵，gameProgress文件尚未读取完毕喵！剩余字节喵：{Reader.remaining()}')


def ParseGameRecord(diff: dict, saveDict: dict):
    """解析gameRecord喵\n
    diff：各歌曲难度字典列表喵(可以通过readDifficulty()获取喵)\n
    saveDict：存档的字典数据喵"""
    diff_list: tuple = ('EZ', 'HD', 'IN', 'AT', 'Legacy')
    Reader = ByteReader(saveDict.copy()['record'])  # 将data数据传给ByteReader来进行后续字节读取操作喵
    all_record = saveDict['record'] = {}
    songSum: int = Reader.getVarInt()  # 总歌曲数目喵

    for num in range(songSum):
        songName: str = Reader.getString()[:-2]  # 歌曲名字喵
        length: int = Reader.getVarInt()  # 数据总长度喵(不包括歌曲名字喵)
        end_position: int = Reader.position + length  # 单首歌数据结束字节位置喵
        unlock: int = Reader.getByte()  # 每个难度解锁情况喵
        fc: int = Reader.getByte()  # 每个难度fc情况喵
        song = all_record[songName] = {}  # 存储单首歌的成绩数据喵

        for level in range(5):  # 遍历每首歌的EZ、HD、IN、AT、Legacy(旧谱喵)难度的成绩喵
            if getBit(unlock, level):  # 判断当前难度是否解锁喵
                score: int = Reader.getInt()  # 读取分数喵
                acc: float = Reader.getFloat()  # 读取acc喵
                try:
                    difficulty: float = diff[songName][level]
                    rks: float = (((acc - 55) / 45) ** 2) * difficulty  # 计算单曲rks
                except KeyError:
                    difficulty: float = 0
                    rks: float = 0
                    print(f'[Warn]歌曲{songName}的{diff_list[level]}定数不存在喵！')
                except IndexError:
                    difficulty: float = 0
                    rks: float = 0
                    print(f'[Warn]歌曲{songName}可能存在旧谱记录喵！')
                song[diff_list[level]]: dict = {  # 按难度存储进单首歌的成绩数据中喵
                    'difficulty': difficulty,  # 定数喵
                    'score': score,  # 分数喵
                    'acc': acc,  # 正如其名喵，就是ACC喵
                    'fc': getBit(fc, level),  # 是否喵Full Combo(FC)
                    'rks': rks  # 单曲rks喵
                }

        if Reader.position != end_position:
            print(f'[Error]在读取"{songName}"的数据时发生错误喵！当前字节位置喵：{Reader.position}')
            print(f'[Error]错误喵！！！当前读取字节位置不正确喵！应为：{end_position}喵')

    if Reader.remaining() > 0 or Reader.remaining() < 0:
        print(f'[Warn]警告喵，gameRecord文件尚未读取完毕喵！剩余字节喵：{Reader.remaining()}')


def ParseGameSettings(saveDict: dict):
    """解析settings喵\n
    saveDict：存档的字典数据喵"""
    Reader = ByteReader(saveDict.copy()['setting'])  # 将data数据传给ByteReader来进行后续字节读取操作喵
    all_settings = saveDict['setting'] = {}
    tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面4个数据喵（
    all_settings['chordSupport']: int = tem[0]  # 多押辅助喵
    all_settings['fcAPIndicator']: int = tem[1]  # 开启FC/AP指示器喵
    all_settings['enableHitSound']: int = tem[2]  # 开启打击音效喵
    all_settings['lowResolutionMode']: int = tem[3]  # 低分辨率模式喵
    all_settings['deviceName']: str = Reader.getString()  # 设备名喵
    all_settings['bright']: float = Reader.getFloat()  # 背景亮度喵
    all_settings['musicVolume']: float = Reader.getFloat()  # 音乐音量喵
    all_settings['effectVolume']: float = Reader.getFloat()  # 界面音效音量喵
    all_settings['hitSoundVolume']: float = Reader.getFloat()  # 打击音效音量喵
    all_settings['soundOffset']: float = Reader.getFloat()  # 谱面延迟喵
    all_settings['noteScale']: float = Reader.getFloat()  # 按键缩放喵

    if Reader.remaining() > 0 or Reader.remaining() < 0:
        print(f'[Warn]警告喵，settings文件尚未读取完毕喵！剩余字节喵：{Reader.remaining()}')


def ParseGameUser(saveDict: dict):
    """解析user喵\n
    saveDict：存档的字典数据喵"""
    Reader = ByteReader(saveDict.copy()['user'])
    all_user = saveDict['user'] = {}
    all_user['showPlayerId']: int = Reader.getByte()  # 右上角展示用户id喵
    all_user['selfIntro']: str = Reader.getString()  # 自我介绍喵
    all_user['avatar']: str = Reader.getString()  # 头像喵
    all_user['background']: str = Reader.getString()  # 背景曲绘喵

    if Reader.remaining() > 0 or Reader.remaining() < 0:
        print(f'[Warn]警告喵，user文件尚未读取完毕喵！剩余字节喵：{Reader.remaining()}')
