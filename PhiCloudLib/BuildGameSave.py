# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .ByteReader import getBits
from .ByteWriter import ByteWriter, writeBits


# ---------------------- 定义赋值区喵 ----------------------

async def BuildGameKey(saveDict: dict):
    """构建gameKey喵\n
    saveDict：存档的字典数据喵"""
    Writer = ByteWriter()
    awa = False
    try:
        all_key: dict = saveDict['key']
    except KeyError:
        all_key: dict = saveDict
        awa = True
    lanotaReadKeys: int = await writeBits(eval(all_key.pop('lanotaReadKeys')))
    camelliaReadKey: int = await writeBits(eval(all_key.pop('camelliaReadKey')))
    await Writer.writeVarInt(len(saveDict))

    for keys in all_key.items():
        await Writer.writeString(keys[0])
        await Writer.writeByte(len(eval(keys[1]['flag'])) + 1)
        await Writer.writeByte(await writeBits(eval(keys[1]['type']) + [0, 0, 0]))

        for flag in eval(keys[1]['flag']):
            await Writer.writeByte(flag)

    await Writer.writeByte(lanotaReadKeys)
    await Writer.writeByte(camelliaReadKey)
    if not awa:
        saveDict['key']: bytes = await Writer.getData()
    else:
        return await Writer.getData()


async def BuildGameProgress(saveDict: dict):
    """构建gameProgress喵\n
    saveDict：存档的字典数据喵"""
    Writer = ByteWriter()
    awa = False
    try:
        all_progress: dict = saveDict['progress']
    except KeyError:
        all_progress: dict = saveDict
        awa = True
    tem: list = await getBits(0)
    tem[0]: int = all_progress['isFirstRun']
    tem[1]: int = all_progress['legacyChapterFinished']
    tem[2]: int = all_progress['alreadyShowCollectionTip']
    tem[3]: int = all_progress['alreadyShowAutoUnlockINTip']
    await Writer.writeByte(await writeBits(tem))

    await Writer.writeString(all_progress['completed'])
    await Writer.writeVarInt(all_progress['songUpdateInfo'])
    await Writer.writeShort(all_progress['challengeModeRank'])

    money: list = eval(all_progress['money'])
    for i in money:
        await Writer.writeVarInt(i)

    await Writer.writeByte(await writeBits(eval(all_progress['unlockFlagOfSpasmodic']) + [0, 0, 0, 0]))
    await Writer.writeByte(await writeBits(eval(all_progress['unlockFlagOfIgallta']) + [0, 0, 0, 0]))
    await Writer.writeByte(await writeBits(eval(all_progress['unlockFlagOfRrharil']) + [0, 0, 0, 0]))
    await Writer.writeByte(await writeBits(eval(all_progress['flagOfSongRecordKey'])))
    await Writer.writeByte(await writeBits(eval(all_progress['randomVersionUnlocked']) + [0, 0]))

    tem: list = await getBits(0)
    tem[0]: int = all_progress['chapter8UnlockBegin']
    tem[1]: int = all_progress['chapter8UnlockSecondPhase']
    tem[2]: int = all_progress['chapter8Passed']
    await Writer.writeByte(await writeBits(tem))

    await Writer.writeByte(await writeBits(eval(all_progress['chapter8SongUnlocked']) + [0, 0]))
    await Writer.writeByte(await writeBits(eval(all_progress['flagOfSongRecordKeyTakumi']) + [0, 0, 0, 0, 0]))

    if not awa:
        saveDict['progress']: bytes = await Writer.getData()
    else:
        return await Writer.getData()


async def BuildGameRecord(saveDict: dict):
    """解析gameRecord喵\n
    saveDict：存档的字典数据喵"""
    diff_list: dict = {
        'EZ': 0,
        'HD': 1,
        'IN': 2,
        'AT': 3,
        'Legacy': 4
    }
    awa = False
    try:
        all_record: dict = saveDict['record']
    except KeyError:
        all_record: dict = saveDict
        awa = True
    Writer = ByteWriter()
    await Writer.writeVarInt(len(all_record))

    for song in all_record.items():
        await Writer.writeString(song[0] + '.0')
        await Writer.writeVarInt(len(song[1]) * (4 + 4) + 1 + 1)  # 此处不是冗余代码啊喵！本喵这样子写是有原因的！
        unlock: list = await getBits(0)
        fc: list = await getBits(0)
        record_writer = ByteWriter()
        for record in song[1].items():
            unlock[diff_list[record[0]]]: int = 1
            await record_writer.writeInt(record[1]['score'])
            await record_writer.writeFloat(record[1]['acc'])
            fc[diff_list[record[0]]]: int = record[1]['fc']
        await Writer.writeByte(await writeBits(unlock))
        await Writer.writeByte(await writeBits(fc))
        await Writer.writeBytes(await record_writer.getData())

    if not awa:
        saveDict['record']: bytes = await Writer.getData()
    else:
        return await Writer.getData()


async def BuildGameSettings(saveDict: dict):
    """构建settings喵\n
    saveDict：存档的字典数据喵"""
    Writer = ByteWriter()
    awa = False
    try:
        all_setting: dict = saveDict['setting']
    except KeyError:
        all_setting: dict = saveDict
        awa = True
    tem: list = await getBits(0)
    tem[0]: int = all_setting['chordSupport']
    tem[1]: int = all_setting['fcAPIndicator']
    tem[2]: int = all_setting['enableHitSound']
    tem[3]: int = all_setting['lowResolutionMode']
    await Writer.writeByte(await writeBits(tem))
    await Writer.writeString(all_setting['deviceName'])
    await Writer.writeFloat(all_setting['bright'])
    await Writer.writeFloat(all_setting['musicVolume'])
    await Writer.writeFloat(all_setting['effectVolume'])
    await Writer.writeFloat(all_setting['hitSoundVolume'])
    await Writer.writeFloat(all_setting['soundOffset'])
    await Writer.writeFloat(all_setting['noteScale'])

    if not awa:
        saveDict['setting']: bytes = await Writer.getData()
    else:
        return await Writer.getData()


async def BuildGameUser(saveDict: dict):
    """构建user喵\n
    saveDict：存档的字典数据喵"""
    Writer = ByteWriter()
    awa = False
    try:
        all_user: dict = saveDict['user']
    except KeyError:
        all_user: dict = saveDict
        awa = True
    await Writer.writeByte(all_user['showPlayerId'])
    await Writer.writeString(all_user['selfIntro'])
    await Writer.writeString(all_user['avatar'])
    await Writer.writeString(all_user['background'])

    if not awa:
        saveDict['user']: bytes = await Writer.getData()
    else:
        return await Writer.getData()
