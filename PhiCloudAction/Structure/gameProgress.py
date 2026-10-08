# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .DataType import (
    Bit,
    Byte,
    String,
    VarInt,
    ShortInt,
    Money,
    Bits,
    _NibbleHigh,
    _NibbleLow,
)

# ---------------------- 定义赋值区喵 ----------------------


class gameProgress06:
    """
    版本号≥4.0.1喵

    第九章二阶段内容的更新喵

    新增了：
    - `chapter9Phase2SongUnlocked`
    - `chapter9Phase2Begin`
    - `chapter9Phase2Passed`
    - `c9BaselineChallengeReached`
    - `chapter9Phase2Step`
    """

    file_head = b"\x06"

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

    chapter9UnlockBegin: Bit
    """第九章第一阶段入场喵"""

    chapter9SecretChallengePendingLifeUnlock: Bit
    """新生命档位提升提示尚未确认喵 (应该就是提升生命档位上限的提示没有被确认)"""

    chapter9SongUnlocked: Bits[6]
    """
    第九章第一阶段各曲目解锁喵
    
    (Implexrough、About The Universe、Evanescent、Exoplanetary Mirage、Entrance to the Chaos、True Home, True World)
    """

    chapter9SecretChallengeLifeTier: _NibbleLow
    """
    已解锁生命档位上限
    
    | 档位下标 | 对应生命值 |
    |:---:|---:|
    | 0 | 1 |
    | 1 | 10 |
    | 2 | 50 |
    | 3 | 100 |
    | 4 | 200 |
    """

    chapter9SecretChallengeSelectedLifeTier: _NibbleHigh
    """下次挑战选用的生命档位 (各档位与`chapter9SecretChallengeLifeTier`使用同一个对照表)"""

    chapter9SecretPassword: String
    """第九章解锁密码喵 (输对通过了才会存的哦，默认就是"0")"""

    chapter9Phase2SongUnlocked: Bits[6]
    """
    第九章第二阶段各曲目解锁喵
    
    (Ametrine, Petrichor, ハテ, Desultory Signals, Message, What do you want more than a Happy ending?)
    """

    chapter9Phase2Begin: Bit
    """第九章第二阶段入场喵"""

    chapter9Phase2Passed: Bit
    """第九章第二阶段通过喵"""

    c9BaselineChallengeReached: Bit
    """已开启第九章第二阶段最后的挑战 (通过了也存true哦)"""

    chapter9Phase2Step: Byte
    """
    第九章第二阶段剧情阶段
    
    | step | 大致解释喵 |
    |:---:|:---|
    | 0 | 第二部分入场 |
    | 1 | 等待完成 True Home, True World(Rework) |
    | 2 | Ametrine 已解锁 |
    | 3 | Petrichor 已解锁 |
    | 4 | 已到达最终挑战 (通过了也存4哦) |
    """


class gameProgress05:
    """
    版本号=4.0.0喵

    第九章一阶段的更新喵

    新增了：
    - `chapter9UnlockBegin`
    - `chapter9SecretChallengePendingLifeUnlock`
    - `chapter9SongUnlocked`
    - `chapter9SecretChallengeLifeTier`
    - `chapter9SecretChallengeSelectedLifeTier`
    - `chapter9SecretPassword`
    """

    file_head = b"\x05"

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

    chapter9UnlockBegin: Bit
    """第九章第一阶段入场喵"""

    chapter9SecretChallengePendingLifeUnlock: Bit
    """新生命档位提升提示尚未确认喵 (应该就是提升生命档位上限的提示没有被确认)"""

    chapter9SongUnlocked: Bits[6]
    """
    第九章第一阶段各曲目解锁喵
    
    (Implexrough, About The Universe, Evanescent, Exoplanetary Mirage, Entrance to the Chaos, True Home, True World)
    """

    chapter9SecretChallengeLifeTier: _NibbleLow
    """
    已解锁生命档位上限
    
    | 档位下标 | 对应生命值 |
    |:---:|---:|
    | 0 | 1 |
    | 1 | 10 |
    | 2 | 50 |
    | 3 | 100 |
    | 4 | 200 |
    """

    chapter9SecretChallengeSelectedLifeTier: _NibbleHigh
    """下次挑战选用的生命档位 (各档位与`chapter9SecretChallengeLifeTier`使用同一个对照表)"""

    chapter9SecretPassword: String
    """第九章解锁密码喵 (输对通过了才会存的哦，默认就是"0")"""


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
