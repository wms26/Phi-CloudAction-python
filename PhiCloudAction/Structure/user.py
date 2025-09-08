# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .DataType import Byte, String

# ---------------------- 定义赋值区喵 ----------------------


class user01:
    file_head = b"\x01"

    showPlayerId: Byte
    """右上角展示用户id喵"""

    selfIntro: String
    """自我介绍喵"""

    avatar: String
    """头像喵"""

    background: String
    """背景曲绘喵"""
