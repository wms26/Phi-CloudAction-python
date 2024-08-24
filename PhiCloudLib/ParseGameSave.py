# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from token import AWAIT

from .ByteReader import ByteReader, getBit, getBits
from .LibApi import logger


# ---------------------- 定义赋值区喵 ----------------------


async def ParseGameKey(saveDict: dict | bytes):
    """解析gameKey喵\n
    saveDict：存档的字典数据喵\n
    (如果传入了字节类型数据则会返回解析后字典数据喵)"""

    # 将data数据传给ByteReader来进行后续字节读取操作喵
    if type(saveDict) is dict:
        Reader = ByteReader(saveDict.copy()['key'])
        all_keys = saveDict['key'] = {}  # 用来存储解析出来的数据喵

    elif type(saveDict) is bytes:
        Reader = ByteReader(saveDict)
        all_keys = {}  # 用来存储解析出来的数据喵

    else:
        logger.warning(f'解析key时传入的数据类型不正确！应为dict或bytes！但传入了"{type(saveDict)}"类型')
        Reader = ByteReader(saveDict)
        all_keys = {}  # 用来存储解析出来的数据喵

    keySum: int = await Reader.getVarInt()  # 总共key的数量，决定循环多少次喵

    for _ in range(keySum):  # 循环keySum次喵
        name: str = await Reader.getString()  # key的昵称喵
        length: int = await Reader.getByte()  # 总数据长度喵(不包含key的昵称喵)
        Key = all_keys[name] = {}  # 存储单个key的数据喵
        Key['type']: str = str((await getBits(await Reader.getByte()))[:-3])  # 获取key的类型标志喵

        flag: list = []  # 用来存储该key的状态喵(比如头像是否获得/曲绘是否解锁/收藏品是否获取/打开喵)
        for i in range(length - 1):  # 因为前面已经读取了一个类型标志了喵，所以减一喵
            flag.append(await Reader.getByte())
        Key['flag'] = str(flag)

    all_keys['lanotaReadKeys'] = str(await getBits(await Reader.getByte()))  # 读取Lanota收藏品喵(解锁倒霉蛋和船的AT喵)
    all_keys['camelliaReadKey'] = str(await getBits(await Reader.getByte()))  # 读取极星卫破译收藏品喵(解锁S.A.T.E.L.L.I.T.E.的AT喵)

    if await Reader.remaining() > 0 or await Reader.remaining() < 0:
        logger.warning(f'警告喵，gameKey文件尚未读取完毕喵！剩余字节喵：{await Reader.remaining()}')

    if type(saveDict) is bytes:
        return all_keys


async def ParseGameProgress(saveDict: dict | bytes):
    """解析gameProgress喵\n
    saveDict：存档的字典数据喵\n
    (如果传入了字节类型数据则会返回解析后字典数据喵)"""

    # 将data数据传给ByteReader来进行后续字节读取操作喵
    if type(saveDict) is dict:
        Reader = ByteReader(saveDict.copy()['progress'])
        all_progress = saveDict['progress'] = {}  # 用来存储解析出来的数据喵

    elif type(saveDict) is bytes:
        Reader = ByteReader(saveDict)
        all_progress = {}  # 用来存储解析出来的数据喵

    else:
        logger.warning(f'解析key时传入的数据类型不正确！应为dict或bytes！但传入了"{type(saveDict)}"类型')
        Reader = ByteReader(saveDict)
        all_progress = {}  # 用来存储解析出来的数据喵

    tem: list = await getBits(await Reader.getByte())  # 鸽游用一个字节表示了下面4个数据喵（
    all_progress['isFirstRun']: int = tem[0]  # 首次运行喵
    all_progress['legacyChapterFinished']: int = tem[1]  # 过去的章节已完成喵
    all_progress['alreadyShowCollectionTip']: int = tem[2]  # 已展示收藏品Tip喵
    all_progress['alreadyShowAutoUnlockINTip']: int = tem[3]  # 已展示自动解锁IN Tip喵
    all_progress['completed']: int = await Reader.getString()  # 剧情完成喵(显示全部歌曲和课题模式入口喵)
    all_progress['songUpdateInfo']: int = await Reader.getVarInt()  # 喵喵喵？
    all_progress['challengeModeRank']: int = await Reader.getShort()  # 课题分喵

    money: list = []  # 应该不用多说了吧喵（
    for i in range(5):
        money.append(await Reader.getVarInt())
    all_progress['money']: str = str(money)

    all_progress['unlockFlagOfSpasmodic']: str = str((await getBits(await Reader.getByte()))[:-4])  # Spasmodic解锁喵
    all_progress['unlockFlagOfIgallta']: str = str((await getBits(await Reader.getByte()))[:-4])  # Igallta解锁喵
    all_progress['unlockFlagOfRrharil']: str = str((await getBits(await Reader.getByte()))[:-4])  # Rrhar'il解锁喵

    # (倒霉蛋, 船, Shadow, 心之所向, inferior, DESTRUCTION 3,2,1, Distorted Fate, Cuvism)
    all_progress['flagOfSongRecordKey']: str = str(await getBits(await Reader.getByte()))  # 部分歌曲IN达到S喵

    all_progress['randomVersionUnlocked']: str = str((await getBits(await Reader.getByte()))[:-2])  # Random切片解锁喵
    tem: list = await getBits(await Reader.getByte())  # 鸽游用一个字节表示了下面3个数据喵（
    all_progress['chapter8UnlockBegin']: int = tem[0]  # 第八章入场喵
    all_progress['chapter8UnlockSecondPhase']: int = tem[1]  # 第八章第二阶段喵
    all_progress['chapter8Passed']: int = tem[2]  # 第八章通过喵
    all_progress['chapter8SongUnlocked']: int = str((await getBits(await Reader.getByte()))[:-2])  # 第八章各曲目解锁喵
    all_progress['flagOfSongRecordKeyTakumi']: int = str((await getBits(await Reader.getByte()))[:-5])

    if await Reader.remaining() > 0 or await Reader.remaining() < 0:
        logger.warning(f'警告喵，gameProgress文件尚未读取完毕喵！剩余字节喵：{await Reader.remaining()}')

    if type(saveDict) is bytes:
        return all_progress


async def ParseGameRecord(saveDict: dict | bytes, diff: dict, countRks: bool = True):
    """解析gameRecord喵\n
    diff：各歌曲难度字典列表喵(可以通过readDifficulty()获取喵)\n
    saveDict：存档的字典数据喵\n
    (如果传入了字节类型数据则会返回解析后字典数据喵)"""

    diff_list: tuple = ('EZ', 'HD', 'IN', 'AT', 'Legacy')

    # 将data数据传给ByteReader来进行后续字节读取操作喵
    if type(saveDict) is dict:
        Reader = ByteReader(saveDict.copy()['record'])
        all_record = saveDict['record'] = {}  # 用来存储解析出来的数据喵

    elif type(saveDict) is bytes:
        Reader = ByteReader(saveDict)
        all_record = {}  # 用来存储解析出来的数据喵

    else:
        logger.warning(f'解析record时传入的数据类型不正确！应为dict或bytes！但传入了"{type(saveDict)}"类型')
        Reader = ByteReader(saveDict)
        all_record = {}  # 用来存储解析出来的数据喵

    songSum: int = await Reader.getVarInt()  # 总歌曲数目喵

    for num in range(songSum):
        songName: str = (await Reader.getString())[:-2]  # 歌曲名字喵
        length: int = await Reader.getVarInt()  # 数据总长度喵(不包括歌曲名字喵)
        end_position: int = Reader.position + length  # 单首歌数据结束字节位置喵
        unlock: int = await Reader.getByte()  # 每个难度解锁情况喵
        fc: int = await Reader.getByte()  # 每个难度fc情况喵
        song = all_record[songName] = {}  # 存储单首歌的成绩数据喵

        for level in range(5):  # 遍历每首歌的EZ、HD、IN、AT、Legacy(旧谱喵)难度的成绩喵
            if await getBit(unlock, level):  # 判断当前难度是否解锁喵
                score: int = await Reader.getInt()  # 读取分数喵
                acc: float = await Reader.getFloat()  # 读取acc喵
                try:
                    difficulty: float = diff[songName][level]
                    if countRks:
                        rks: float = (((acc - 55) / 45) ** 2) * difficulty
                    else:
                        rks: float = 0

                    # from decimal import Decimal, getcontext  # 备用的计算方式喵，虽然感觉没有什么用喵
                    # getcontext().prec = 30  # 设置Decimal上下文的小数精度为8位喵
                    # rks = float(format(((Decimal(acc) - Decimal('55')) / Decimal('45')) ** 2 * Decimal(difficulty), '.15f'))  # 计算单曲rks喵
                except KeyError:
                    difficulty: float = 0
                    rks: float = 0
                    logger.warning(f'歌曲{songName}的{diff_list[level]}定数不存在喵！')
                except IndexError:
                    difficulty: float = 0
                    rks: float = 0
                    logger.warning(f'歌曲{songName}可能存在旧谱记录喵！')

                if countRks:
                    song[diff_list[level]]: dict = {  # 按难度存储进单首歌的成绩数据中喵
                        'difficulty': difficulty,  # 定数喵
                        'score': score,  # 分数喵
                        'acc': acc,  # 正如其名喵，就是ACC喵
                        'fc': await getBit(fc, level),  # 是否Full Combo喵(FC)
                        'rks': rks  # 单曲rks喵
                    }
                else:
                    song[diff_list[level]]: dict = {  # 按难度存储进单首歌的成绩数据中喵
                        'difficulty': difficulty,  # 定数喵
                        'score': score,  # 分数喵
                        'acc': acc,  # 正如其名喵，就是ACC喵
                        'fc': await getBit(fc, level),  # 是否Full Combo喵(FC)
                    }

        if Reader.position != end_position:
            logger.error(f'在读取"{songName}"的数据时发生错误喵！当前字节位置喵：{await Reader.position}')
            logger.error(f'错误喵！！！当前读取字节位置不正确喵！应为：{end_position}喵')

    if await Reader.remaining() > 0 or await Reader.remaining() < 0:
        logger.warning(f'警告喵，gameRecord文件尚未读取完毕喵！剩余字节喵：{await Reader.remaining()}')

    if type(saveDict) is bytes:
        return all_record


async def ParseGameSettings(saveDict: dict | bytes):
    """解析settings喵\n
    saveDict：存档的字典数据喵\n
    (如果传入了字节类型数据则会返回解析后字典数据喵)"""

    # 将data数据传给ByteReader来进行后续字节读取操作喵
    if type(saveDict) is dict:
        Reader = ByteReader(saveDict.copy()['setting'])
        all_settings = saveDict['setting'] = {}  # 用来存储解析出来的数据喵

    elif type(saveDict) is bytes:
        Reader = ByteReader(saveDict)
        all_settings = {}  # 用来存储解析出来的数据喵

    else:
        logger.warning(f'解析setting时传入的数据类型不正确！应为dict或bytes！但传入了"{type(saveDict)}"类型')
        Reader = ByteReader(saveDict)
        all_settings = {}  # 用来存储解析出来的数据喵

    tem: list = await getBits(await Reader.getByte())  # 鸽游用一个字节表示了下面4个数据喵（
    all_settings['chordSupport']: int = tem[0]  # 多押辅助喵
    all_settings['fcAPIndicator']: int = tem[1]  # 开启FC/AP指示器喵
    all_settings['enableHitSound']: int = tem[2]  # 开启打击音效喵
    all_settings['lowResolutionMode']: int = tem[3]  # 低分辨率模式喵
    all_settings['deviceName']: str = await Reader.getString()  # 设备名喵
    all_settings['bright']: float = await Reader.getFloat()  # 背景亮度喵
    all_settings['musicVolume']: float = await Reader.getFloat()  # 音乐音量喵
    all_settings['effectVolume']: float = await Reader.getFloat()  # 界面音效音量喵
    all_settings['hitSoundVolume']: float = await Reader.getFloat()  # 打击音效音量喵
    all_settings['soundOffset']: float = await Reader.getFloat()  # 谱面延迟喵
    all_settings['noteScale']: float = await Reader.getFloat()  # 按键缩放喵

    if await Reader.remaining() > 0 or await Reader.remaining() < 0:
        logger.warning(f'警告喵，settings文件尚未读取完毕喵！剩余字节喵：{await Reader.remaining()}')

    if type(saveDict) is bytes:
        return all_settings


async def ParseGameUser(saveDict: dict | bytes):
    """解析user喵\n
    saveDict：存档的字典数据喵\n
    (如果传入了字节类型数据则会返回解析后字典数据喵)"""

    # 将data数据传给ByteReader来进行后续字节读取操作喵
    if type(saveDict) is dict:
        Reader = ByteReader(saveDict.copy()['user'])
        all_user = saveDict['user'] = {}  # 用来存储解析出来的数据喵

    elif type(saveDict) is bytes:
        Reader = ByteReader(saveDict)
        all_user = {}  # 用来存储解析出来的数据喵

    else:
        logger.warning(f'解析user时传入的数据类型不正确！应为dict或bytes！但传入了"{type(saveDict)}"类型')
        Reader = ByteReader(saveDict)
        all_user = {}  # 用来存储解析出来的数据喵

    all_user['showPlayerId']: int = await Reader.getByte()  # 右上角展示用户id喵
    all_user['selfIntro']: str = await Reader.getString()  # 自我介绍喵
    all_user['avatar']: str = await Reader.getString()  # 头像喵
    all_user['background']: str = await Reader.getString()  # 背景曲绘喵

    if await Reader.remaining() > 0 or await Reader.remaining() < 0:
        logger.warning(f'警告喵，user文件尚未读取完毕喵！剩余字节喵：{await Reader.remaining()}')

    if type(saveDict) is bytes:
        return all_user
