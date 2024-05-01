# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from PhiCloudLib.ByteReader import getBits
from PhiCloudLib.ByteWriter import ByteWriter, setBits


# ---------------------- 定义赋值区喵 ----------------------

def BuildGameKey(saveDict: dict):
    """构建gameKey喵\n
    saveDict：存档的字典数据喵"""
    Writer = ByteWriter()
    all_key: dict = saveDict['key']
    lanotaReadKeys: int = all_key.pop('lanotaReadKeys')
    camelliaReadKey: int = all_key.pop('camelliaReadKey')
    Writer.writeVarInt(len(saveDict))

    for keys in all_key.items():
        Writer.writeString(keys[0])
        Writer.writeByte(len(eval(keys[1]['flag'])) + 1)
        Writer.writeByte(setBits(eval(keys[1]['type']) + [0, 0, 0]))

        for flag in eval(keys[1]['flag']):
            Writer.writeByte(flag)

    Writer.writeByte(lanotaReadKeys)
    Writer.writeByte(camelliaReadKey)
    saveDict['key']: bytes = Writer.getData()


def BuildGameProgress(saveDict: dict):
    """构建gameProgress喵\n
    saveDict：存档的字典数据喵"""
    Writer = ByteWriter()
    all_progress: dict = saveDict['progress']
    tem: list = getBits(0)
    tem[0]: int = all_progress['isFirstRun']
    tem[1]: int = all_progress['legacyChapterFinished']
    tem[2]: int = all_progress['alreadyShowCollectionTip']
    tem[3]: int = all_progress['alreadyShowAutoUnlockINTip']
    Writer.writeByte(setBits(tem))

    Writer.writeString(all_progress['completed'])
    Writer.writeVarInt(all_progress['songUpdateInfo'])
    Writer.writeShort(all_progress['challengeModeRank'])

    money: list = eval(all_progress['money'])
    for i in money:
        Writer.writeVarInt(i)

    Writer.writeByte(setBits(eval(all_progress['unlockFlagOfSpasmodic']) + [0, 0, 0, 0]))
    Writer.writeByte(setBits(eval(all_progress['unlockFlagOfIgallta']) + [0, 0, 0, 0]))
    Writer.writeByte(setBits(eval(all_progress['unlockFlagOfRrharil']) + [0, 0, 0, 0]))
    Writer.writeByte(setBits(eval(all_progress['flagOfSongRecordKey'])))
    Writer.writeByte(setBits(eval(all_progress['randomVersionUnlocked']) + [0, 0]))

    tem: list = getBits(0)
    tem[0]: int = all_progress['chapter8UnlockBegin']
    tem[1]: int = all_progress['chapter8UnlockSecondPhase']
    tem[2]: int = all_progress['chapter8Passed']
    Writer.writeByte(setBits(tem))

    Writer.writeByte(setBits(eval(all_progress['chapter8SongUnlocked']) + [0, 0]))
    buildData: bytes = Writer.getData()

    saveDict['progress']: dict = buildData


def BuildGameRecord(saveDict: dict):
    """解析gameRecord喵\n
    saveDict：存档的字典数据喵"""
    diff_list: dict = {
        'EZ': 0,
        'HD': 1,
        'IN': 2,
        'AT': 3,
        'Legacy': 4
    }
    all_record: dict = saveDict['record']
    Writer = ByteWriter()
    Writer.writeVarInt(len(all_record))

    for song in all_record.items():
        Writer.writeString(song[0] + '.0')
        Writer.writeVarInt(len(song[1]) * (4 + 4) + 1 + 1)
        unlock: list = getBits(0)
        fc: list = getBits(0)
        record_writer = ByteWriter()
        for record in song[1].items():
            unlock[diff_list[record[0]]]: int = 1
            record_writer.writeInt(record[1]['score'])
            record_writer.writeFloat(record[1]['acc'])
            fc[diff_list[record[0]]]: int = record[1]['fc']
        Writer.writeByte(setBits(unlock))
        Writer.writeByte(setBits(fc))
        Writer.writeBytes(record_writer.getData())

    saveDict['record']: bytes = Writer.getData()


def BuildGameSettings(saveDict: dict):
    """构建settings喵\n
    saveDict：存档的字典数据喵"""
    Writer = ByteWriter()
    all_setting: dict = saveDict['setting']
    tem: list = getBits(0)
    tem[0]: int = all_setting['chordSupport']
    tem[1]: int = all_setting['fcAPIndicator']
    tem[2]: int = all_setting['enableHitSound']
    tem[3]: int = all_setting['lowResolutionMode']
    Writer.writeByte(setBits(tem))
    Writer.writeString(all_setting['deviceName'])
    Writer.writeFloat(all_setting['bright'])
    Writer.writeFloat(all_setting['musicVolume'])
    Writer.writeFloat(all_setting['effectVolume'])
    Writer.writeFloat(all_setting['hitSoundVolume'])
    Writer.writeFloat(all_setting['soundOffset'])
    Writer.writeFloat(all_setting['noteScale'])

    saveDict['setting']: bytes = Writer.getData()


def BuildGameUser(saveDict: dict):
    """构建user喵\n
    saveDict：存档的字典数据喵"""
    Writer = ByteWriter()
    all_user: dict = saveDict['user']
    Writer.writeByte(all_user['showPlayerId'])
    Writer.writeString(all_user['selfIntro'])
    Writer.writeString(all_user['avatar'])
    Writer.writeString(all_user['background'])

    saveDict['user']: bytes = Writer.getData()
