# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from struct import pack


# ---------------------- 定义赋值区 ----------------------

def setBit(data, index: int, value: int):
    if value == 0:
        return data & ~(1 << index)
    else:
        return data | (1 << index)


def setBits(bits: list):
    """将位列表转换回字节"""
    byte = 0
    for i, bit in enumerate(bits):
        byte |= bit << i
    return byte


class ByteWriter:
    """用来写入数据"""

    def __init__(self):
        """用来写入数据"""
        self.data = bytearray()

    def writeByte(self, byte):
        """写入1字节的数据"""
        self.data.append(byte)

    def writeShort(self, short: int):
        """写入2字节的短整数"""
        self.data.extend(pack('<H', short))

    def writeInt(self, integer: int):
        """写入4字节的整数"""
        self.data.extend(pack('<I', integer))

    def writeFloat(self, float_val: float):
        """写入4字节的单精度浮点数"""
        self.data.extend(pack('<f', float_val))

    def writeVarInt(self, var_int: int):
        """写入一个2字节或1字节的变长整数"""
        if var_int > 127:  # 如果大于127，则写入两个字节
            self.writeByte((var_int & 0b01111111) | 0b10000000)  # 脑子爆烧
            self.writeByte(var_int >> 7)  # 脑子爆烧
        else:
            self.writeByte(var_int)  # 写入一个字节

    def writeBytes(self, bytes_val):
        """写入一段字节"""
        self.data.extend(bytes_val)

    def writeString(self, string_val: str):
        """写入一段字符串并编码为字节"""
        encoded_string = string_val.encode('utf-8')
        self.writeVarInt(len(encoded_string))
        self.data.extend(encoded_string)

    def getData(self):
        """获取写入的数据"""
        return bytes(self.data)
