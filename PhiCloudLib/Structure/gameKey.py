# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .DataType import *

# ---------------------- 定义赋值区喵 ----------------------


class gameKey03:
    """版本号≥3.9.0"""

    file_head = b"\x03"

    keyList: GameKey
    lanotaReadKeys: Bits
    camelliaReadKey: Bits
    sideStory4BeginReadKey: Bits
    oldScoreClearedV390: Bits


class gameKey02:
    """版本号<3.9.0"""

    file_head = b"\x02"

    keyList: GameKey
    lanotaReadKeys: Bits
    camelliaReadKey: Bits
