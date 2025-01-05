# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .DataType import *

# ---------------------- 定义赋值区喵 ----------------------


class gameProgress04:
    """版本号≥3.8.1"""

    file_head = b"\x04"

    isFirstRun: Bit
    legacyChapterFinished: Bit
    alreadyShowCollectionTip: Bit
    alreadyShowAutoUnlockINTip: Bit
    completed: String
    songUpdateInfo: VarInt
    challengeModeRank: ShortInt
    money: Money
    unlockFlagOfSpasmodic: Bits
    unlockFlagOfIgallta: Bits
    unlockFlagOfRrharil: Bits
    flagOfSongRecordKey: Bits
    randomVersionUnlocked: Bits
    chapter8UnlockBegin: Bit
    chapter8UnlockSecondPhase: Bit
    chapter8Passed: Bit
    chapter8SongUnlocked: Bits
    flagOfSongRecordKeyTakumi: Bits


class gameProgress03:
    """版本号<3.8.1"""

    file_head = b"\x03"

    isFirstRun: Bit
    legacyChapterFinished: Bit
    alreadyShowCollectionTip: Bit
    alreadyShowAutoUnlockINTip: Bit
    completed: String
    songUpdateInfo: VarInt
    challengeModeRank: ShortInt
    money: Money
    unlockFlagOfSpasmodic: Bits
    unlockFlagOfIgallta: Bits
    unlockFlagOfRrharil: Bits
    flagOfSongRecordKey: Bits
    randomVersionUnlocked: Bits
    chapter8UnlockBegin: Bit
    chapter8UnlockSecondPhase: Bit
    chapter8Passed: Bit
    chapter8SongUnlocked: Bits
