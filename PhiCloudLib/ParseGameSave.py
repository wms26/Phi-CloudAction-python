# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiCloudLib.ByteReader import ByteReader, getBit, getBits


# ---------------------- 定义赋值区 ----------------------

class ParseGameKey:
    """解析gameKey"""

    def __init__(self, data: bytes):
        """解析gameKey\n
        data：待解析的gameKey数据"""
        Reader = ByteReader(data)  # 将data数据传给ByteReader来进行后续字节读取操作
        self.keySum: int = Reader.getVarInt()  # 总共key的数量，决定循环多少次
        self.all_keys: dict = {}  # 用来存储解析出来的数据

        for _ in range(self.keySum):  # 循环keySum次
            Key = {}  # 存储单个key的数据
            name: str = Reader.getString()  # key的昵称
            length: int = Reader.getByte()  # 总数据长度(不包含key的昵称)
            Key['type'] = getBits(Reader.getByte())[:-3]  # 获取key的类型标志
            flag = Key['flag'] = []  # 用来存储该key的状态(比如头像是否获得/曲绘是否解锁/收藏品是否获取/打开)

            for i in range(length - 1):  # 因为前面已经读取了一个类型标志了，所以减一
                flag.append(Reader.getByte())

            self.all_keys[name] = Key  # 将获取到的单个key数据存储进总字典总

        self.all_keys['lanotaReadKeys'] = Reader.getByte()  # 读取Lanota收藏品(解锁倒霉蛋和船的AT)
        self.all_keys['camelliaReadKey'] = Reader.getByte()  # 读取极星卫破译收藏品(解锁S.A.T.E.L.L.I.T.E.的AT)

    def getData(self):
        """以字典数据类型返回解析的所有数据"""
        return self.all_keys


class ParseGameProgress:
    """解析gameProgress"""

    def __init__(self, data: bytes):
        """解析gameProgress\n
        data：待解析的gameProgress数据"""
        Reader = ByteReader(data)  # 将data数据传给ByteReader来进行后续字节读取操作
        tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面4个数据（
        self.isFirstRun = tem[0]  # 首次运行
        self.legacyChapterFinished = tem[1]  # 过去的章节已完成
        self.alreadyShowCollectionTip = tem[2]  # 已展示收藏品Tip
        self.alreadyShowAutoUnlockINTip = tem[3]  # 已展示自动解锁IN Tip
        self.completed = Reader.getString()  # 剧情完成(显示全部歌曲和课题模式入口)
        self.songUpdateInfo = Reader.getVarInt()  #
        self.challengeModeRank = Reader.getShort()  # 课题分

        self.money = []  # 应该不用多说了吧（
        for i in range(5):
            self.money.append(Reader.getVarInt())

        self.unlockFlagOfSpasmodic = Reader.getByte()  # Spasmodic解锁
        self.unlockFlagOfIgallta = Reader.getByte()  # Igallta解锁
        self.unlockFlagOfRrharil = Reader.getByte()  # Rrhar'il解锁
        self.flagOfSongRecordKey = Reader.getByte()  # 部分歌曲的AT解锁
        self.randomVersionUnlocked = Reader.getByte()  # Random切片解锁
        tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面3个数据（
        self.chapter8UnlockBegin = tem[0]  # 第八章入场
        self.chapter8UnlockSecondPhase = tem[1]  # 第八章第二阶段
        self.chapter8Passed = tem[2]  # 第八章通过
        self.chapter8SongUnlocked = getBits(Reader.getByte())[:-2]  # 第八章各曲目解锁

        if Reader.remaining() > 0 or Reader.remaining() < 0:
            print(f'[Warn]警告，gameProgress文件尚未读取完毕！剩余字节：{Reader.remaining()}')

    def getData(self):
        """以字典数据类型返回解析的所有数据"""
        return {
            'isFirstRun': self.isFirstRun,  # 首次运行
            'legacyChapterFinished': self.legacyChapterFinished,  # 过去的章节已完成
            'alreadyShowCollectionTip': self.alreadyShowCollectionTip,  # 已展示收藏品Tip
            'alreadyShowAutoUnlockINTip': self.alreadyShowAutoUnlockINTip,  # 已展示自动解锁IN Tip
            'completed': self.completed,  # 剧情完成(显示全部歌曲和课题模式入口)
            'songUpdateInfo': self.songUpdateInfo,
            'challengeModeRank': self.challengeModeRank,  # 课题分
            'money': self.money,  # 应该不用多说了吧（
            'unlockFlagOfSpasmodic': self.unlockFlagOfSpasmodic,  # Spasmodic解锁
            'unlockFlagOfIgallta': self.unlockFlagOfIgallta,  # Igallta解锁
            'unlockFlagOfRrharil': self.unlockFlagOfRrharil,  # Rrhar'il解锁
            'flagOfSongRecordKey': self.flagOfSongRecordKey,  # 部分歌曲解锁AT
            'randomVersionUnlocked': self.randomVersionUnlocked,  # Random切片解锁
            'chapter8UnlockBegin': self.chapter8UnlockBegin,  # 第八章入场
            'chapter8UnlockSecondPhase': self.chapter8UnlockSecondPhase,  # 第八章第二阶段
            'chapter8Passed': self.chapter8Passed,  # 第八章通过
            'chapter8SongUnlocked': self.chapter8SongUnlocked  # 第八章各曲目解锁
        }


class ParseGameRecord:
    """解析gameRecord"""

    def __init__(self, data: bytes, diff: dict):
        """解析gameRecord\n
        data：待解析的gameRecord数据\n
        diff：各歌曲难度字典列表(可以通过readDifficulty()获取)"""
        diff_list: tuple = ('EZ', 'HD', 'IN', 'AT', 'Legacy')
        Reader = ByteReader(data)  # 将data数据传给ByteReader来进行后续字节读取操作
        self.Record: dict = {}
        self.songSum: int = Reader.getVarInt()  # 总歌曲数目

        for num in range(self.songSum):
            songName: str = Reader.getString()[:-2]  # 歌曲名字
            length: int = Reader.getVarInt()  # 数据总长度(不包括歌曲名字)
            end_position: int = Reader.position + length  # 单首歌数据结束字节位置
            unlock: int = Reader.getByte()  # 每个难度解锁情况
            fc: int = Reader.getByte()  # 每个难度fc情况
            song: dict = {}  # 存储单首歌的成绩数据

            for level in range(5):  # 遍历每首歌的EZ、HD、IN、AT、Legacy(旧谱)难度的成绩
                if getBit(unlock, level):  # 判断当前难度是否解锁
                    score: int = Reader.getInt()  # 读取分数
                    acc: float = Reader.getFloat()  # 读取acc
                    song_diff = {
                        'difficulty': diff[songName][level],  # 定数
                        'score': score,  # 分数
                        'acc': acc,  # 正如其名，就是ACC辣
                        'fc': getBit(fc, level),  # 是否Full Combo(FC)
                        'rks': (((acc - 55) / 45) ** 2) * diff[songName][level]  # 单曲rks
                    }
                    song[diff_list[level]] = song_diff  # 按难度存储进单首歌的成绩数据中

            if Reader.position != end_position:
                print(f'[Error]在读取"{songName}"的数据时发生错误！当前字节位置：{Reader.position}')
                print(f'[Error]错误！！！当前读取字节位置不正确！应为：{end_position}')

            self.Record[songName] = song  # 按歌名存储单首歌的成绩数据

        if Reader.remaining() > 0 or Reader.remaining() < 0:
            print(f'[Warn]警告，gameRecord文件尚未读取完毕！剩余字节：{Reader.remaining()}')

    def getData(self):
        """以字典数据类型返回解析的所有数据"""
        return self.Record


class ParseGameSettings:
    """解析settings"""

    def __init__(self, data: bytes):
        """解析settings\n
        data：待解析的settings数据"""
        Reader = ByteReader(data)  # 将data数据传给ByteReader来进行后续字节读取操作
        tem: list = getBits(Reader.getByte())  # 鸽游用一个字节表示了下面4个数据（
        self.chordSupport = tem[0]  # 多押辅助
        self.fcAPIndicator = tem[1]  # 开启FC/AP指示器
        self.enableHitSound = tem[2]  # 开启打击音效
        self.lowResolutionMode = tem[3]  # 低分辨率模式
        self.deviceName = Reader.getString()  # 设备名
        self.bright = Reader.getFloat()  # 背景亮度
        self.musicVolume = Reader.getFloat()  # 音乐音量
        self.effectVolume = Reader.getFloat()  # 界面音效音量
        self.hitSoundVolume = Reader.getFloat()  # 打击音效音量
        self.soundOffset = Reader.getFloat()  # 谱面延迟
        self.noteScale = Reader.getFloat()  # 按键缩放

        if Reader.remaining() > 0 or Reader.remaining() < 0:
            print(f'[Warn]警告，settings文件尚未读取完毕！剩余字节：{Reader.remaining()}')

    def getData(self):
        """以字典数据类型返回解析的所有数据"""
        return {
            'chordSupport': self.chordSupport,  # 多押辅助
            'fcAPIndicator': self.fcAPIndicator,  # 开启FC/AP指示器
            'enableHitSound': self.enableHitSound,  # 开启打击音效
            'lowResolutionMode': self.lowResolutionMode,  # 低分辨率模式
            'deviceName': self.deviceName,  # 设备名
            'bright': self.bright,  # 背景亮度
            'musicVolume': self.musicVolume,  # 音乐音量
            'effectVolume': self.effectVolume,  # 界面音效音量
            'hitSoundVolume': self.hitSoundVolume,  # 打击音效音量
            'soundOffset': self.soundOffset,  # 谱面延迟
            'noteScale': self.noteScale,  # 按键缩放
        }


class ParseGameUser:
    """解析user"""

    def __init__(self, data):
        """解析user\n
        data：待解析的user数据"""
        Reader = ByteReader(data)
        self.showPlayerId = Reader.getByte()  # 右上角展示用户id
        self.selfIntro = Reader.getString()  # 自我介绍
        self.avatar = Reader.getString()  # 头像
        self.background = Reader.getString()  # 背景曲绘

        if Reader.remaining() > 0 or Reader.remaining() < 0:
            print(f'[Warn]警告，user文件尚未读取完毕！剩余字节：{Reader.remaining()}')

    def getData(self):
        return {
            'showPlayerId': self.showPlayerId,  # 右上角展示用户id
            'selfIntro': self.selfIntro,  # 自我介绍
            'avatar': self.avatar,  # 头像
            'background': self.background  # 背景曲绘
        }
