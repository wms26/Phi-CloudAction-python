import struct


class ByteReader:
    def __init__(self, data, position=0):
        self.data = bytes.fromhex(data)  # 将HEX转换为字节数据(?)
        self.position = position  # 当前文件的读取的字节位置(?)

    def remaining(self):
        """返回剩余字节数"""
        return len(self.data) - self.position  # 总数据字节长度减当前读取的字节

    def getByte(self):
        """读取1字节的数据"""
        byte = self.data[self.position]  # 读取当前字节位置的数据
        self.position += 1  # 读取了一个字节
        return byte  # 返回读取的单字节数据

    def getAllByte(self):
        """读取当前字节位置之后所有数据并base64解码"""
        return self.data[self.position:].decode('base64')

    def getShort(self):
        """读取2字节的短整数"""
        short = struct.unpack('>H', self.data[self.position:self.position + 2])[0]
        self.position += 2
        return short

    def getInt(self):
        """读取4字节的整数"""
        integer = struct.unpack('>I', self.data[self.position:self.position + 4])[0]
        self.position += 4
        return integer

    def getFloat(self):
        """读取4字节的单精度浮点数"""
        float_val = struct.unpack('<f', self.data[self.position:self.position + 4])[0]
        self.position += 4
        return float_val

    def getVarInt(self):
        """读取一个变长整数"""
        if self.data[self.position] > 127:  # 如果当前字节位置数据的值大于127
            self.position += 2  # 向后移动两位
            var_int = (self.data[self.position - 2] & 0b01111111) ^ (self.data[self.position - 1] << 7)  # 脑子爆烧
        else:
            var_int = self.data[self.position]  # 读取当前字节位置数据的值
            self.position += 1  # 向后移动一位
        return var_int  # 最后返回读取到的变长整数

    def skipVarInt(self, num=None):
        """跳过num个变长整数"""
        if num:
            for _ in range(num):
                self.skipVarInt()
        else:
            if self.data[self.position] < 0:
                self.position += 2
            else:
                self.position += 1

    def getBytes(self):
        """读取一段字节"""
        length = self.getByte()  # 获取当前字节位置数据的值，代表后续字节长度
        bytes_val = self.data[self.position:self.position + length]  # 取一段字节数据
        self.position += length  # 根据总字节长度向后移动length位
        return bytes_val  # 返回读取到的数据

    def getString(self):
        """读取一段字节并解码为字符串"""
        length = self.getVarInt()  # 读当前位置的变长整数，代表后续字节长度
        string_val = self.data[self.position:self.position + length].decode('utf-8')  # 读取一段字节并uft-8解码
        self.position += length  # 根据总字节长度向后移动length位
        return string_val  # 返回读取到的数据

    def skipString(self):
        """跳过一段字节"""
        length = self.getByte()
        self.position += length + 1

    def insertBytes(self, bytes_val):
        self.data = self.data[:self.position] + bytes_val + self.data[self.position:]

    def replaceBytes(self, length, bytes_val):
        if len(bytes_val) == length:
            self.data = self.data[:self.position] + bytes_val + self.data[self.position + length:]
        else:
            self.data = self.data[:self.position] + bytes_val + self.data[self.position + length:]
