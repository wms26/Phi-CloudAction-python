from ByteWriter import *
from ByteReader import *


class BuildGameKey:
    """构建gameKey"""

    def __init__(self, data: dict):
        """构建gameKey\n
        data：解析后的字典数据"""
        Writer = ByteWriter()
        lanotaReadKeys = data.pop('lanotaReadKeys')
        camelliaReadKey = data.pop('camelliaReadKey')
        Writer.writeVarInt(len(data))

        for keys in data.items():
            Writer.writeString(keys[0])
            Writer.writeByte(len(keys[1]['flag']) + 1)
            Writer.writeByte(setBits(keys[1]['type'] + [0, 0, 0]))

            for flag in keys[1]['flag']:
                Writer.writeByte(flag)

        Writer.writeByte(lanotaReadKeys)
        Writer.writeByte(camelliaReadKey)
        self.buildData = Writer.getData()

    def getData(self):
        return self.buildData


class BuildGameProgress:
    """构建gameProgress"""

    def __init__(self, data: dict):
        """构建gameProgress\n
        data：解析之后的字典数据"""
        Writer = ByteWriter()
        tem: list = getBits(0)
        tem[0] = data['isFirstRun']
        tem[1] = data['legacyChapterFinished']
        tem[2] = data['alreadyShowCollectionTip']
        tem[3] = data['alreadyShowAutoUnlockINTip']
        Writer.writeByte(setBits(tem))

        Writer.writeString(data['completed'])
        Writer.writeVarInt(data['songUpdateInfo'])
        Writer.writeShort(data['challengeModeRank'])

        money: list = data['money']
        for i in money:
            Writer.writeVarInt(i)

        Writer.writeByte(data['unlockFlagOfSpasmodic'])
        Writer.writeByte(data['unlockFlagOfIgallta'])
        Writer.writeByte(data['unlockFlagOfRrharil'])
        Writer.writeByte(data['flagOfSongRecordKey'])
        Writer.writeByte(data['randomVersionUnlocked'])

        tem: list = getBits(0)
        tem[0] = data['chapter8UnlockBegin']
        tem[1] = data['chapter8UnlockSecondPhase']
        tem[2] = data['chapter8Passed']
        Writer.writeByte(setBits(tem))

        Writer.writeByte(setBits(data['chapter8SongUnlocked'] + [0, 0]))
        self.buildData: bytes = Writer.getData()

        if len(self.buildData) != 20:
            print(f'[Warn]gameProgress数据大小为：{len(self.buildData)}')
            print(f'[Warn]gameProgress数据大小不正确！应为：20！')

    def getData(self):
        return self.buildData


class BuildGameRecord:
    """构建gameRecord"""

    def __init__(self, data: dict):
        """解析gameRecord\n
        data：解析后的字典数据"""
        diff_list: dict = {
            'EZ': 0,
            'HD': 1,
            'IN': 2,
            'AT': 3,
            'Legacy': 4
        }
        Writer = ByteWriter()
        Writer.writeVarInt(len(data))

        for song in data.items():
            Writer.writeString(song[0] + '.0')
            Writer.writeVarInt(len(song[1]) * (4 + 4) + 1 + 1)
            unlock: list = getBits(0)
            fc: list = getBits(0)
            record_writer = ByteWriter()
            for record in song[1].items():
                unlock[diff_list[record[0]]] = 1
                record_writer.writeInt(record[1]['score'])
                record_writer.writeFloat(record[1]['acc'])
                fc[diff_list[record[0]]] = record[1]['fc']
            Writer.writeByte(setBits(unlock))
            Writer.writeByte(setBits(fc))
            Writer.writeBytes(record_writer.getData())

        self.buildData = Writer.getData()

    def getData(self):
        return self.buildData


class BuildGameSettings:
    """构建settings"""

    def __init__(self, data: dict):
        """构建settings\n
        data：解析后的字典数据"""
        Writer = ByteWriter()
        tem: list = getBits(0)
        tem[0] = data['chordSupport']
        tem[1] = data['fcAPIndicator']
        tem[2] = data['enableHitSound']
        tem[3] = data['lowResolutionMode']
        Writer.writeByte(setBits(tem))
        Writer.writeString(data['deviceName'])
        Writer.writeFloat(data['bright'])
        Writer.writeFloat(data['musicVolume'])
        Writer.writeFloat(data['effectVolume'])
        Writer.writeFloat(data['hitSoundVolume'])
        Writer.writeFloat(data['soundOffset'])
        Writer.writeFloat(data['noteScale'])
        self.buildData: bytes = Writer.getData()

    def getData(self):
        return self.buildData


class BuildGameUser:
    """构建user"""

    def __init__(self, data: dict):
        """构建user\n
        data：解析后的字典数据"""
        Writer = ByteWriter()
        Writer.writeByte(data['showPlayerId'])
        Writer.writeString(data['selfIntro'])
        Writer.writeString(data['avatar'])
        Writer.writeString(data['background'])
        self.buildData: bytes = Writer.getData()

    def getData(self):
        return self.buildData
