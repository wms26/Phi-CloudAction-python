# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .DataType import GameKey, Bits, Byte

# ---------------------- 定义赋值区喵 ----------------------


class gameKey03:
    """
    版本号≥3.9.0喵
    
    新增支线章节四《无相乡》喵

    新增"sideStory4BeginReadKey"和"oldScoreClearedV390"喵
    """

    file_head = b"\x03"

    keyList: GameKey
    """
    游戏中所有Key的状态值喵
    
    结构:
        type: key的状态标志喵(收藏品阅读、单曲解锁、收藏品、背景、头像喵)
        flag: key的标记喵(长度与type中1的数量一致，每位值相同，与收藏品碎片收集有关，默认为1喵)
    """

    lanotaReadKeys: Bits[6]
    """Lanota收藏品阅读进度喵(解锁倒霉蛋和船的AT喵)"""

    camelliaReadKey: Bits
    """极星卫收藏品阅读进度喵(解锁S.A.T.E.L.L.I.T.E.的AT喵)"""

    sideStory4BeginReadKey: Byte
    """解锁支线4喵"""

    oldScoreClearedV390: Byte
    """是否已清除改谱之前的成绩喵(如果为0则会清除喵)"""


class gameKey02:
    """
    版本号≥3.2.0喵

    新增《极星卫》外传章节喵

    新增"camelliaReadKey"喵
    """

    file_head = b"\x02"

    keyList: GameKey

    lanotaReadKeys: Bits[6]
    """Lanota收藏品阅读进度喵(解锁倒霉蛋和船的AT喵)"""

    camelliaReadKey: Bits
    """极星卫收藏品阅读进度喵(解锁S.A.T.E.L.L.I.T.E.的AT喵)"""


class gameKey01:
    """
    版本号≥2.3.0喵 (理论上应该是≥2.4.0，因为2.4.0才加入云存档喵ww)

    新增Lanota联动精选集喵

    新增"lanotaReadKeys"喵
    """

    file_head = b"\x01"

    keyList: GameKey

    lanotaReadKeys: Bits[6]
    """Lanota收藏品阅读进度喵(解锁倒霉蛋和船的AT喵)"""
