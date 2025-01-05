# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .DataType import *

# ---------------------- 定义赋值区喵 ----------------------


class settings01:
    file_head = b"\x01"

    chordSupport: Bit
    fcAPIndicator: Bit
    enableHitSound: Bit
    lowResolutionMode: Bit
    deviceName: String
    bright: Float
    musicVolume: Float
    effectVolume: Float
    hitSoundVolume: Float
    soundOffset: Float
    noteScale: Float
