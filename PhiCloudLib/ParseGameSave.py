# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from PhiCloudLib.ByteReader import ByteReader, getBit, getBits


# ---------------------- 定义赋值区喵 ----------------------

class ParseGameKey:
    """解析gameKey喵"""

    def __init__(self, data: bytes):
        """解析gameKey喵\n
        data：待解析的gameKey数据喵"""
        Reader = ByteReader(data)  # 将data数据传给ByteReader来进行后续字节读取操作喵
        self.keySum: int = Reader.getVarInt()  # 总共key的数量，决定循环多少次喵
        self.all_keys: dict = {}  # 用来存储解析出来的数据喵

        for _ in range(self.keySum):  # 循环keySum次喵
            Key = {}  # 存储单个key的数据喵
            name: str = Reader.getString()  # key的昵称喵
            length: int = Reader.getByte()  # 总数据长度喵(不包含key的昵称喵)
            Key['type'] = getBits(Reader.getByte())[:-3]  # 获取key的类型标志喵
            flag = Key['flag'] = []  # 用来存储该key的状态喵(比如头像是否获得/曲绘是否解锁/收藏品是否获取/打开喵)

            for i in range(length - 1):  # 因为前面已经读取了一个类型标志了喵，所以减一喵
                flag.append(Reader.getByte())

            self.all_keys[name] = Key  # 将获取到的单个key数据存储进总字典喵

        self.all_keys['lanotaReadKeys'] = Reader.getByte()  # 读取Lanota收藏品喵(解锁倒霉蛋和船的AT喵)
        self.all_keys['camelliaReadKey'] = Reader.getByte()  # 读取极星卫破译收藏品喵(解锁S.A.T.E.L.L.I.T.E.的AT喵)

    def getData(self):
        """以字典数据类型返回解析的所有数据喵"""
        return self.all_keys


class ParseGameProgress:
    """解析gameProgress喵"""

    def __init__(self, data: bytes):
        """解析gameProgress喵\n
        data：待解析的gameProgress数据喵"""
        Reader = ByteReader(data)  # 将data数据传给ByteReader来进行后续字节读取操作喵
        tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面4个数据喵（
        self.isFirstRun = tem[0]  # 首次运行喵
        self.legacyChapterFinished = tem[1]  # 过去的章节已完成喵
        self.alreadyShowCollectionTip = tem[2]  # 已展示收藏品Tip喵
        self.alreadyShowAutoUnlockINTip = tem[3]  # 已展示自动解锁IN Tip喵
        self.completed = Reader.getString()  # 剧情完成喵(显示全部歌曲和课题模式入口喵)
        self.songUpdateInfo = Reader.getVarInt()  # 喵喵喵？
        self.challengeModeRank = Reader.getShort()  # 课题分喵

        self.money = []  # 应该不用多说了吧喵（
        for i in range(5):
            self.money.append(Reader.getVarInt())

        self.unlockFlagOfSpasmodic = Reader.getByte()  # Spasmodic解锁喵
        self.unlockFlagOfIgallta = Reader.getByte()  # Igallta解锁喵
        self.unlockFlagOfRrharil = Reader.getByte()  # Rrhar'il解锁喵
        self.flagOfSongRecordKey = Reader.getByte()  # 部分歌曲的AT解锁喵
        self.randomVersionUnlocked = Reader.getByte()  # Random切片解锁喵
        tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面3个数据喵（
        self.chapter8UnlockBegin = tem[0]  # 第八章入场喵
        self.chapter8UnlockSecondPhase = tem[1]  # 第八章第二阶段喵
        self.chapter8Passed = tem[2]  # 第八章通过喵
        self.chapter8SongUnlocked = getBits(Reader.getByte())[:-2]  # 第八章各曲目解锁喵

        if Reader.remaining() > 0 or Reader.remaining() < 0:
            print(f'[Warn]警告喵，gameProgress文件尚未读取完毕喵！剩余字节喵：{Reader.remaining()}')

    def getData(self):
        """以字典数据类型返回解析的所有数据喵"""
        return {
            'isFirstRun': self.isFirstRun,  # 首次运行喵
            'legacyChapterFinished': self.legacyChapterFinished,  # 过去的章节已完成喵
            'alreadyShowCollectionTip': self.alreadyShowCollectionTip,  # 已展示收藏品Tip喵
            'alreadyShowAutoUnlockINTip': self.alreadyShowAutoUnlockINTip,  # 已展示自动解锁IN Tip喵
            'completed': self.completed,  # 剧情完成喵(显示全部歌曲和课题模式入口喵)
            'songUpdateInfo': self.songUpdateInfo,  # 喵喵喵？
            'challengeModeRank': self.challengeModeRank,  # 课题分喵
            'money': self.money,  # 应该不用多说了吧喵（
            'unlockFlagOfSpasmodic': self.unlockFlagOfSpasmodic,  # Spasmodic解锁喵
            'unlockFlagOfIgallta': self.unlockFlagOfIgallta,  # Igallta解锁喵
            'unlockFlagOfRrharil': self.unlockFlagOfRrharil,  # Rrhar'il解锁喵
            'flagOfSongRecordKey': self.flagOfSongRecordKey,  # 部分歌曲解锁AT喵
            'randomVersionUnlocked': self.randomVersionUnlocked,  # Random切片解锁喵
            'chapter8UnlockBegin': self.chapter8UnlockBegin,  # 第八章入场喵
            'chapter8UnlockSecondPhase': self.chapter8UnlockSecondPhase,  # 第八章第二阶段喵
            'chapter8Passed': self.chapter8Passed,  # 第八章通过喵
            'chapter8SongUnlocked': self.chapter8SongUnlocked  # 第八章各曲目解锁喵
        }


class ParseGameRecord:
    """解析gameRecord喵"""

    def __init__(self, data: bytes, diff: dict):
        """解析gameRecord喵\n
        data：待解析的gameRecord数据喵\n
        diff：各歌曲难度字典列表喵(可以通过readDifficulty()获取喵)"""
        diff_list: tuple = ('EZ', 'HD', 'IN', 'AT', 'Legacy')
        Reader = ByteReader(data)  # 将data数据传给ByteReader来进行后续字节读取操作喵
        self.Record: dict = {}
        self.songSum: int = Reader.getVarInt()  # 总歌曲数目喵

        for num in range(self.songSum):
            songName: str = Reader.getString()[:-2]  # 歌曲名字喵
            length: int = Reader.getVarInt()  # 数据总长度喵(不包括歌曲名字喵)
            end_position: int = Reader.position + length  # 单首歌数据结束字节位置喵
            unlock: int = Reader.getByte()  # 每个难度解锁情况喵
            fc: int = Reader.getByte()  # 每个难度fc情况喵
            song: dict = {}  # 存储单首歌的成绩数据喵

            for level in range(5):  # 遍历每首歌的EZ、HD、IN、AT、Legacy(旧谱喵)难度的成绩喵
                if getBit(unlock, level):  # 判断当前难度是否解锁喵
                    score: int = Reader.getInt()  # 读取分数喵
                    acc: float = Reader.getFloat()  # 读取acc喵
                    song_diff = {
                        'difficulty': diff[songName][level],  # 定数喵
                        'score': score,  # 分数喵
                        'acc': acc,  # 正如其名喵，就是ACC喵
                        'fc': getBit(fc, level),  # 是否喵Full Combo(FC)
                        'rks': (((acc - 55) / 45) ** 2) * diff[songName][level]  # 单曲rks喵
                    }
                    song[diff_list[level]] = song_diff  # 按难度存储进单首歌的成绩数据中喵

            if Reader.position != end_position:
                print(f'[Error]在读取"{songName}"的数据时发生错误喵！当前字节位置喵：{Reader.position}')
                print(f'[Error]错误喵！！！当前读取字节位置不正确喵！应为：{end_position}喵')

            self.Record[songName] = song  # 按歌名存储单首歌的成绩数据喵

        if Reader.remaining() > 0 or Reader.remaining() < 0:
            print(f'[Warn]警告喵，gameRecord文件尚未读取完毕喵！剩余字节喵：{Reader.remaining()}')

    def getData(self):
        """以字典数据类型返回解析的所有数据喵"""
        return self.Record


class ParseGameSettings:
    """解析settings喵"""

    def __init__(self, data: bytes):
        """解析settings喵\n
        data：待解析的settings数据喵"""
        Reader = ByteReader(data)  # 将data数据传给ByteReader来进行后续字节读取操作喵
        tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面4个数据喵（
        self.chordSupport = tem[0]  # 多押辅助喵
        self.fcAPIndicator = tem[1]  # 开启FC/AP指示器喵
        self.enableHitSound = tem[2]  # 开启打击音效喵
        self.lowResolutionMode = tem[3]  # 低分辨率模式喵
        self.deviceName = Reader.getString()  # 设备名喵
        self.bright = Reader.getFloat()  # 背景亮度喵
        self.musicVolume = Reader.getFloat()  # 音乐音量喵
        self.effectVolume = Reader.getFloat()  # 界面音效音量喵
        self.hitSoundVolume = Reader.getFloat()  # 打击音效音量喵
        self.soundOffset = Reader.getFloat()  # 谱面延迟喵
        self.noteScale = Reader.getFloat()  # 按键缩放喵

        if Reader.remaining() > 0 or Reader.remaining() < 0:
            print(f'[Warn]警告喵，settings文件尚未读取完毕喵！剩余字节喵：{Reader.remaining()}')

    def getData(self):
        """以字典数据类型返回解析的所有数据喵"""
        return {
            'chordSupport': self.chordSupport,  # 多押辅助喵
            'fcAPIndicator': self.fcAPIndicator,  # 开启FC/AP指示器喵
            'enableHitSound': self.enableHitSound,  # 开启打击音效喵
            'lowResolutionMode': self.lowResolutionMode,  # 低分辨率模式喵
            'deviceName': self.deviceName,  # 设备名喵
            'bright': self.bright,  # 背景亮度喵
            'musicVolume': self.musicVolume,  # 音乐音量喵
            'effectVolume': self.effectVolume,  # 界面音效音量喵
            'hitSoundVolume': self.hitSoundVolume,  # 打击音效音量喵
            'soundOffset': self.soundOffset,  # 谱面延迟喵
            'noteScale': self.noteScale,  # 按键缩放喵
        }


class ParseGameUser:
    """解析user喵"""

    def __init__(self, data):
        """解析user喵\n
        data：待解析的user数据喵"""
        Reader = ByteReader(data)
        self.showPlayerId = Reader.getByte()  # 右上角展示用户id喵
        self.selfIntro = Reader.getString()  # 自我介绍喵
        self.avatar = Reader.getString()  # 头像喵
        self.background = Reader.getString()  # 背景曲绘喵

        if Reader.remaining() > 0 or Reader.remaining() < 0:
            print(f'[Warn]警告喵，user文件尚未读取完毕喵！剩余字节喵：{Reader.remaining()}')

    def getData(self):
        return {
            'showPlayerId': self.showPlayerId,  # 右上角展示用户id喵
            'selfIntro': self.selfIntro,  # 自我介绍喵
            'avatar': self.avatar,  # 头像喵
            'background': self.background  # 背景曲绘喵
        }
