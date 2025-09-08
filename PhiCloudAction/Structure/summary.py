from .DataType import Byte, ShortInt, Float, VarInt, String, Summary


class summary:
    saveVersion: Byte
    """存档版本号喵"""

    challenge: ShortInt
    """课题分喵"""

    rks: Float
    """RKS喵"""

    gameVersion: VarInt
    """游戏版本号喵"""

    avatar: String
    """头像喵"""

    EZ: Summary
    """EZ难度谱面的完成情况喵（Cleared, Full Combo, Phi）"""

    HD: Summary
    """HD难度谱面的完成情况喵（Cleared, Full Combo, Phi）"""

    IN: Summary
    """IN难度谱面的完成情况喵（Cleared, Full Combo, Phi）"""

    AT: Summary
    """AT难度谱面的完成情况喵（Cleared, Full Combo, Phi）"""
