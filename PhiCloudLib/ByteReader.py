# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from struct import unpack


# ---------------------- 定义赋值区喵 ----------------------

async def readBit(byte, index: int):
    """获取一个字节中index位的值喵\n
    byte：字节数据喵\n
    index：要读取的位数喵"""
    return 1 if bool(byte & (1 << index)) else 0


async def readBits(byte):
    """获取一个字节中所有位的值喵\n
    byte：字节数据喵\n
    (会以列表类型数据返回喵)"""
    bits: list = []
    for i in range(8):  # 一个字节有8位喵
        bit = (byte >> i) & 1
        bits.append(bit)
    return bits


class ByteReader:
    """用来读取解析数据喵"""

    def __init__(self, data: bytes, position=0):
        """用来读取解析数据喵\n
        data：待解析数据喵\n
        position：读取字节位置喵(默认为0喵)"""
        self.data = data  # 待解析的数据喵
        self.position = position  # 当前文件的读取的字节位置喵

    async def remaining(self):
        """返回剩余字节数喵"""
        return len(self.data) - self.position  # 总数据字节长度减当前读取的字节喵

    async def getByte(self):
        """读取1字节的数据喵"""
        byte = self.data[self.position]  # 读取当前字节位置的数据喵
        self.position += 1  # 将指针后移1位喵
        return byte  # 返回读取的1字节数据喵

    async def getShort(self):
        """读取2字节的短整数喵"""
        short = unpack('<H', self.data[self.position:self.position + 2])[0]
        self.position += 2  # 将指针后移2位喵
        return short  # 返回读取的短整数喵

    async def getInt(self):
        """读取4字节的整数喵"""
        integer = unpack('<I', self.data[self.position:self.position + 4])[0]
        self.position += 4  # 将指针后移4位喵
        return integer  # 返回读取的整数喵

    async def getFloat(self):
        """读取4字节的单精度浮点数喵"""
        float_val = unpack('<f', self.data[self.position:self.position + 4])[0]
        self.position += 4  # 将指针后移4位喵
        return float_val  # 返回读取的单精度浮点数喵

    async def getVarInt(self):
        """读取一个2字节或1字节的变长整数喵"""
        if self.data[self.position] > 127:  # 如果当前字节位置数据的值大于127喵
            self.position += 2  # 将指针后移2位喵
            var_int = (self.data[self.position - 2] & 0b01111111) ^ (self.data[self.position - 1] << 7)  # 脑子爆烧唔喵
        else:
            var_int = self.data[self.position]  # 读取当前字节位置数据的值喵
            self.position += 1  # 将指针后移1位喵
        return var_int  # 最后返回读取到的变长整数喵

    async def getString(self):
        """读取一段字节并解码为字符串喵"""
        length = await self.getVarInt()  # 读当前位置的变长整数喵，代表后续字节长度喵
        string_val = self.data[self.position:self.position + length].decode('utf-8')  # 读取一段字节并uft-8解码喵
        self.position += length  # 根据总字节长度将指针向后移动length位喵
        return string_val  # 返回读取到的数据喵

    # 下面两个函数意义不明喵(真的没有用到过喵)
    def insertBytes(self, bytes_val):  # 不知道是干啥用的喵
        self.data = self.data[:self.position] + bytes_val + self.data[self.position:]

    def replaceBytes(self, length, bytes_val):  # 看上去应该是替换一定长度字节的数据用的喵？
        if len(bytes_val) == length:
            self.data = self.data[:self.position] + bytes_val + self.data[self.position + length:]
        else:
            self.data = self.data[:self.position] + bytes_val + self.data[self.position + length:]
