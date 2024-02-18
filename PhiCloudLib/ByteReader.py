# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from struct import unpack


# ---------------------- 定义赋值区 ----------------------

def getBit(byte, index: int):
    """获取一个字节中index位的值\n
    byte：字节数据\n
    index：要读取的位数"""
    return 1 if bool(byte & (1 << index)) else 0


def getBits(byte):
    """获取一个字节中所有位的值\n
    byte：字节数据\n
    (会以列表类型数据返回)"""
    bits: list = []
    for i in range(8):  # 一个字节有8位
        bit = (byte >> i) & 1
        bits.append(bit)
    return bits


class ByteReader:
    """用来读取解析数据"""

    def __init__(self, data: bytes, position=0):
        """用来读取解析数据\n
        data：待解析数据\n
        position：读取字节位置(默认为0)"""
        self.data = data
        self.position = position  # 当前文件的读取的字节位置

    def remaining(self):
        """返回剩余字节数"""
        return len(self.data) - self.position  # 总数据字节长度减当前读取的字节

    def getByte(self):
        """读取1字节的数据"""
        byte = self.data[self.position]  # 读取当前字节位置的数据
        self.position += 1  # 读取了一个字节
        return byte  # 返回读取的单字节数据

    def getShort(self):
        """读取2字节的短整数"""
        short = unpack('<H', self.data[self.position:self.position + 2])[0]
        self.position += 2
        return short

    def getInt(self):
        """读取4字节的整数"""
        integer = unpack('<I', self.data[self.position:self.position + 4])[0]
        self.position += 4
        return integer

    def getFloat(self):
        """读取4字节的单精度浮点数"""
        float_val = unpack('<f', self.data[self.position:self.position + 4])[0]
        self.position += 4
        return float_val

    def getVarInt(self):
        """读取一个2字节或1字节的变长整数"""
        if self.data[self.position] > 127:  # 如果当前字节位置数据的值大于127
            self.position += 2  # 向后移动两位
            var_int = (self.data[self.position - 2] & 0b01111111) ^ (self.data[self.position - 1] << 7)  # 脑子爆烧
        else:
            var_int = self.data[self.position]  # 读取当前字节位置数据的值
            self.position += 1  # 向后移动一位
        return var_int  # 最后返回读取到的变长整数

    def getString(self):
        """读取一段字节并解码为字符串"""
        length = self.getVarInt()  # 读当前位置的变长整数，代表后续字节长度
        string_val = self.data[self.position:self.position + length].decode('utf-8')  # 读取一段字节并uft-8解码
        self.position += length  # 根据总字节长度向后移动length位
        return string_val  # 返回读取到的数据

    # 下面两个函数意义不明(真的没有用到过)
    def insertBytes(self, bytes_val):
        self.data = self.data[:self.position] + bytes_val + self.data[self.position:]

    def replaceBytes(self, length, bytes_val):
        if len(bytes_val) == length:
            self.data = self.data[:self.position] + bytes_val + self.data[self.position + length:]
        else:
            self.data = self.data[:self.position] + bytes_val + self.data[self.position + length:]
