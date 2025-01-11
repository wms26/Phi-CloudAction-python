# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .DataType import Bit, String, VarInt, ShortInt, Money, Bits

# ---------------------- 定义赋值区喵 ----------------------


class gameProgress04:
    """
    版本号≥3.8.1喵

    新增了"flagOfSongRecordKeyTakumi"喵
    """

    file_head = b"\x04"

    isFirstRun: Bit
    """是否首次运行喵"""

    legacyChapterFinished: Bit
    """过去的章节是否完成喵"""

    alreadyShowCollectionTip: Bit
    """是否展示收藏品Tip喵"""

    alreadyShowAutoUnlockINTip: Bit
    """是否展示自动解锁IN Tip喵"""

    completed: String
    """剧情完成喵 (用于显示全部歌曲和课题模式入口喵)"""

    songUpdateInfo: VarInt

    challengeModeRank: ShortInt
    """课题分喵"""

    money: Money
    """Data值喵"""

    unlockFlagOfSpasmodic: Bits[4]
    """Spasmodic解锁喵"""

    unlockFlagOfIgallta: Bits[4]
    """Igallta解锁喵"""

    unlockFlagOfRrharil: Bits[4]
    """Rrhar'il解锁喵"""

    flagOfSongRecordKey: Bits
    """
    部分歌曲IN达到S解锁AT喵
    
    (倒霉蛋, 船, Shadow, 心之所向, inferior, DESTRUCTION 3,2,1, Distorted Fate, Cuvism)
    """

    randomVersionUnlocked: Bits[6]
    """Random切片解锁喵"""

    chapter8UnlockBegin: Bit
    """第八章入场喵"""

    chapter8UnlockSecondPhase: Bit
    """第八章第二阶段喵"""

    chapter8Passed: Bit
    """第八章通过喵"""

    chapter8SongUnlocked: Bits[6]
    """第八章各曲目解锁喵"""

    flagOfSongRecordKeyTakumi: Bits[3]
    """第四章Takumi AT解锁喵"""


class gameProgress03:
    """版本号<3.8.1喵"""

    file_head = b"\x03"

    isFirstRun: Bit
    """是否首次运行喵"""

    legacyChapterFinished: Bit
    """过去的章节是否完成喵"""

    alreadyShowCollectionTip: Bit
    """是否展示收藏品Tip喵"""

    alreadyShowAutoUnlockINTip: Bit
    """是否展示自动解锁IN Tip喵"""

    completed: String
    """剧情完成喵 (用于显示全部歌曲和课题模式入口喵)"""

    songUpdateInfo: VarInt

    challengeModeRank: ShortInt
    """课题分喵"""

    money: Money
    """Data值喵"""

    unlockFlagOfSpasmodic: Bits[4]
    """Spasmodic解锁喵"""

    unlockFlagOfIgallta: Bits[4]
    """Igallta解锁喵"""

    unlockFlagOfRrharil: Bits[4]
    """Rrhar'il解锁喵"""

    flagOfSongRecordKey: Bits
    """
    部分歌曲IN达到S解锁AT喵
    
    (倒霉蛋, 船, Shadow, 心之所向, inferior, DESTRUCTION 3,2,1, Distorted Fate, Cuvism)
    """

    randomVersionUnlocked: Bits[6]
    """Random切片解锁喵"""

    chapter8UnlockBegin: Bit
    """第八章入场喵"""

    chapter8UnlockSecondPhase: Bit
    """第八章第二阶段喵"""

    chapter8Passed: Bit
    """第八章通过喵"""

    chapter8SongUnlocked: Bits[6]
    """第八章各曲目解锁喵"""
