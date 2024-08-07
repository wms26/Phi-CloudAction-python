# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from struct import pack


# ---------------------- 定义赋值区喵 ----------------------

async def writeBit(data, index: int, value: int):
    if value == 0:
        return data & ~(1 << index)
    else:
        return data | (1 << index)


async def writeBits(bits: list):
    """将位列表转换回字节喵"""
    byte = 0
    for i, bit in enumerate(bits):
        byte |= bit << i
    return byte


class ByteWriter:
    """用来写入数据喵"""

    def __init__(self):
        """用来写入数据喵"""
        self.data = bytearray()

    async def writeByte(self, byte):
        """写入1字节的数据喵"""
        self.data.append(byte)

    async def writeShort(self, short: int):
        """写入2字节的短整数喵"""
        self.data.extend(pack('<H', short))

    async def writeInt(self, integer: int):
        """写入4字节的整数喵"""
        self.data.extend(pack('<I', integer))

    async def writeFloat(self, float_val: float):
        """写入4字节的单精度浮点数喵"""
        self.data.extend(pack('<f', float_val))

    async def writeVarInt(self, var_int: int):
        """写入一个2字节或1字节的变长整数喵"""
        if var_int > 127:  # 如果大于127喵，则写入两个字节喵
            await self.writeByte((var_int & 0b01111111) | 0b10000000)
            await self.writeByte(var_int >> 7)
        else:
            await self.writeByte(var_int)  # 写入一个字节喵

    async def writeBytes(self, bytes_val):
        """写入一段字节喵"""
        self.data.extend(bytes_val)

    async def writeString(self, string_val: str):
        """写入一段字符串并编码为字节喵"""
        encoded_string = string_val.encode('utf-8')
        await self.writeVarInt(len(encoded_string))
        self.data.extend(encoded_string)

    async def getData(self):
        """获取写入的数据喵"""
        return bytes(self.data)
