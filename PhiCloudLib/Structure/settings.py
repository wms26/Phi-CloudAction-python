# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from .DataType import Bit, String, Float

# ---------------------- 定义赋值区喵 ----------------------


class settings01:
    file_head = b"\x01"

    chordSupport: Bit
    """多押辅助喵"""

    fcAPIndicator: Bit
    """FC/AP指示器喵"""

    enableHitSound: Bit
    """打击音效喵"""

    lowResolutionMode: Bit
    """低分辨率模式喵"""

    deviceName: String
    """设备名喵"""

    bright: Float
    """背景亮度喵"""

    musicVolume: Float
    """音乐音量喵"""

    effectVolume: Float
    """界面音效音量喵"""

    hitSoundVolume: Float
    """打击音效音量喵"""

    soundOffset: Float
    """谱面延迟喵"""

    noteScale: Float
    """按键缩放喵"""
