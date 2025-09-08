# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from struct import unpack, pack
from typing import Any, Dict, Optional, Union
from ..logger import logger

# ---------------------- 定义赋值区喵 ----------------------


class dataTypeAbstract:
    @staticmethod
    def read(data: bytes, pos: int): ...

    @staticmethod
    def write(data: bytearray, value): ...


class Bit:
    @staticmethod
    def read(data: int, index: int) -> int:
        """
        读取一个整数中指定索引的比特位值喵

        参数:
            int (data): 要读取的整数值喵
            int (index): 比特位索引喵 (0 到 7 ，其中 0 表示最低位喵)

        返回:
            (int): 指定索引的比特位值喵 (1 或 0 喵)
        """
        # return 1 if bool(data & (1 << index)) else 0
        return (data >> index) & 1

    @staticmethod
    def write(data: int, index: int, value: int) -> int:
        """
        修改一个整数中指定索引的比特位值喵

        参数:
            data (int): 要修改的整数值喵
            index (int): 比特位索引喵 (0 到 7 ，其中 0 表示最低位喵)
            value (int): 要设置的比特位值 (1 或 0 喵)

        返回:
            (int): 修改后的整数值
        """
        mask = 1 << index
        return (data & ~mask) | ((value & 1) << index)
        # if value == 0:
        #     return data & ~(1 << index)
        # else:
        #     return data | (1 << index)


class Bits(dataTypeAbstract):
    """比特位喵 (1字节喵)"""

    @staticmethod
    def read(data: bytes, pos: int) -> tuple[str, int]:
        """
        读取一个整数的所有比特位值喵 (1字节喵)

        参数:
            data (bytes): 要读取的字节数据喵
            pos (int): 数据在字节中的位置喵

        返回:
            (tuple[str, int]): 包含每个比特位的值 (1 或 0) 的列表以及下一个字节的位置喵
        """
        bits: list[int] = []
        for i in range(8):  # 一个字节有8位
            bit = Bit.read(data[pos], i)
            bits.append(bit)

        return str(bits), pos + 1

    @staticmethod
    def write(data: bytearray, value: str) -> bytearray:
        """
        根据给定的比特位值列表构建一个整数喵

        参数:
            data (bytearray): 存储结果的字节数组喵
            value (list[int]): 每个比特位的值 (1 或 0) 的列表喵

        返回:
            (bytearray): 更新后的数据序列喵
        """
        _value: type = eval(value)

        if not isinstance(_value, list):
            raise TypeError(
                f'传入的值不能够被解析为list喵！而被解析为："{_value.__class__.__name__}"'
            )

        byte = 0
        if len(_value) < 8:
            _value.extend([0] * (8 - len(_value)))

        for i, bit in enumerate(_value):
            byte = Bit.write(byte, i, bit)

        data.append(byte)
        return data

    @staticmethod
    def __class_getitem__(key: int):
        return _Bits(key)


class _Bits(dataTypeAbstract):
    """比特位喵 (1字节，带长度截取喵)"""

    def __init__(self, _len: int = 8):
        """比特位喵 (1字节，带长度截取喵)"""
        self._len = _len

    def read(self, data: bytes, pos: int) -> tuple[str, int]:
        """
        读取一个整数的所有比特位值喵 (1字节，带长度截取喵)

        参数:
            data (bytes): 要读取的字节数据喵
            pos (int): 数据在字节中的位置喵

        返回:
            (str, int]): 包含每个比特位的值 (1 或 0) 的列表以及下一个字节的位置喵
        """
        bits: list[int] = []
        for i in range(self._len):
            bit = Bit.read(data[pos], i)
            bits.append(bit)

        return str(bits), pos + 1

    @staticmethod
    def write(data: bytearray, value: str) -> bytearray:
        """
        根据给定的比特位值列表构建一个整数喵

        参数:
            data (bytearray): 存储结果的字节数组喵
            value (str): 每个比特位的值 (1 或 0) 的列表喵

        返回:
            (bytearray): 更新后的数据序列喵
        """
        _value: type = eval(value)

        if not isinstance(_value, list):
            raise TypeError(
                f'传入的值不能够被解析为list喵！而被解析为："{_value.__class__.__name__}"'
            )

        byte = 0

        if len(_value) < 8:
            _value.extend([0] * (8 - len(_value)))

        for i, bit in enumerate(_value):
            byte = Bit.write(byte, i, bit)

        data.append(byte)
        return data


class Byte(dataTypeAbstract):
    """一个字节喵 (1字节喵)"""

    @staticmethod
    def read(data: bytes, pos: int):
        """
        读取一个字节的数据喵 (1字节喵)

        参数:
            data (bytes): 包含数据的字节序列喵
            pos (int): 当前数据的字节位置喵

        返回:
            (tuple[int, int]): 包含读取的字节和下一个数据的位置喵
        """
        return data[pos], pos + 1

    @staticmethod
    def write(data: bytearray, value):
        """
        将一段字节写入字节序列喵

        参数:
            data (bytearray): 包含数据的字节序列喵
            value (Any): 要写入的字节值喵

        返回:
            (bytearray): 修改后的数据序列喵
        """
        if isinstance(value, int):
            data.append(value)
        else:
            data.extend(value)

        return data


class ShortInt(dataTypeAbstract):
    """短整型喵 (2字节喵)"""

    @staticmethod
    def read(data: bytes, pos: int):
        """
        读取一个短整型的数据喵 (2字节喵)

        参数:
            data (bytes): 包含数据的字节序列喵
            pos (int): 当前数据的字节位置喵

        返回:
            (tuple[int, int]): 包含读取的短整型数据和下一个数据的位置喵
        """
        return unpack("<H", data[pos : pos + 2])[0], pos + 2

    @staticmethod
    def write(data: bytearray, value: int):
        """
        将短整型数据写入字节序列喵

        参数:
            data (bytearray): 用于存储数据的字节序列喵
            value (int): 待写入的短整型数据喵

        返回:
            (bytearray): 更新后的字节序列喵
        """
        data.extend(pack("<H", value))

        return data


class Int(dataTypeAbstract):
    """整型喵 (4 字节喵)"""

    @staticmethod
    def read(data: bytes, pos: int):
        """
        读取一个整型的数据喵 (4 字节喵)

        参数:
            data (bytes): 包含数据的字节序列喵
            pos (int): 当前数据的字节位置喵

        返回:
            (tuple[int, int]): 包含读取的整型数据和下一个数据的位置喵
        """
        return unpack("<I", data[pos : pos + 4])[0], pos + 4

    @staticmethod
    def write(data: bytearray, value: int):
        """
        将一个整型值写入到字节序列喵

        参数:
            data (bytearray): 存储数据的字节序列喵
            value (int): 需要写入的整型值喵

        返回:
            (bytearray): 更新后的字节序列喵
        """
        data.extend(pack("<I", value))

        return data


class Float(dataTypeAbstract):
    """浮点型喵 (4字节喵)"""

    @staticmethod
    def read(data: bytes, pos: int):
        """
        读取一个浮点型数据喵 (4字节喵)

        参数:
            data (bytes): 包含数据的字节序列喵
            pos (int): 当前数据的字节位置喵

        返回:
            (tuple[int, int]): 包含读取的浮点型数据和下一个数据的位置喵
        """
        return unpack("<f", data[pos : pos + 4])[0], pos + 4

    @staticmethod
    def write(data: bytearray, value: float):
        """
        将浮点型数据写入字节序列喵

        参数:
            data (bytearray): 存储数据的字节序列喵
            value (float): 需要写入的浮点型数据喵

        返回:
            (bytearray): 包含写入数据后的字节序列喵
        """
        data.extend(pack("<f", value))

        return data


class VarInt(dataTypeAbstract):
    """变长整型喵 (1-2字节喵)"""

    @staticmethod
    def read(data: bytes, pos: int):
        """
        读取一个变长整型数据喵 (1-2字节喵)

        参数:
            data (bytes): 包含数据的字节序列喵
            pos (int): 当前数据的字节位置喵

        返回:
            (tuple[int, int]): 包含读取的变长整型数据和下一个数据的位置喵
        """
        if data[pos] > 127:  # 如果当前字节位置数据的值大于127喵
            pos += 2  # 将指针后移2位喵
            # 脑子爆烧唔喵
            var_int = (data[pos - 2] & 0b01111111) ^ (data[pos - 1] << 7)
        else:
            var_int = data[pos]  # 读取当前字节位置数据的值喵
            pos += 1  # 将指针后移1位喵

        return var_int, pos  # 最后返回读取到的变长整数喵

    @staticmethod
    def write(data: bytearray, value: int):
        """
        将变长整型数据写入字节序列喵

        参数:
            data (bytearray): 用于存储数据的字节序列喵
            value (int): 需要写入的变长整型数据喵

        返回:
            (bytearray): 更新后的字节序列喵
        """
        if value > 127:  # 如果大于127喵，则写入两个字节喵
            data = Byte.write(data, (value & 0b01111111) | 0b10000000)
            data = Byte.write(data, value >> 7)
        else:
            data = Byte.write(data, value)  # 写入一个字节喵

        return data


class String(dataTypeAbstract):
    """字符串"""

    @staticmethod
    def read(data: bytes, pos: int):
        """
        读取一个字符串数据喵

        参数:
            data (bytes): 包含数据的字节序列喵
            pos (int): 当前数据的字节位置喵

        返回:
            (tuple[int, int]): 包含读取的字符串和下一个数据的位置喵
        """
        string_len, pos = VarInt.read(
            data, pos
        )  # 读当前位置的变长整数喵，代表后续字节长度喵
        string_val = data[pos : pos + string_len].decode()  # 读取一段字节并uft-8解码喵

        return string_val, pos + string_len  # 返回读取到的数据喵

    @staticmethod
    def write(data: bytearray, value: str):
        """
        将字符串数据写入字节序列喵

        参数:
            data (bytearray): 用于存储数据的字节序列喵
            value (str): 需要写入的变长整型数据喵

        返回:
            (bytearray): 更新后的字节序列喵
        """
        encoded_string = value.encode("utf-8")
        data = VarInt.write(data, len(encoded_string))
        data.extend(encoded_string)

        return data


class GameKey(dataTypeAbstract):
    @staticmethod
    def read(data: bytes, pos: int):
        all_keys = {}
        reader = Reader(data, pos)
        keySum = reader.type_read(VarInt)  # 总共key的数量，决定循环多少次喵

        for _ in range(keySum):  # 循环keySum次喵
            name = reader.type_read(String)  # key的名称喵
            # 总数据长度喵(不包含key的昵称喵)
            length = reader.type_read(Byte)
            one_key = all_keys[name] = {}  # 存储单个key的数据喵
            # 获取key的状态标志喵(收藏品阅读、单曲解锁、收藏品、背景、头像喵)
            one_key["type"] = str((reader.type_read(Bits[5])))

            # 用来存储该key的标记喵(长度与type中1的数量一致，每位值相同，与收藏品碎片收集有关，默认为1喵)
            flag = []
            # 因为前面已经读取了一个类型标志了，所以减一喵
            for _ in range(length - 1):
                flag_value, reader.pos = Byte.read(data, reader.pos)
                flag.append(flag_value)
            one_key["flag"] = str(flag)

        return all_keys, reader.pos

    @staticmethod
    def write(data: bytearray, value: dict):
        writer = Writer(data)

        writer.type_write(VarInt, len(value))

        for keys in value.items():
            writer.type_write(String, keys[0])
            writer.type_write(Byte, len(eval(keys[1]["flag"])) + 1)
            writer.type_write(Bits, keys[1]["type"])

            for flag in eval(keys[1]["flag"]):
                writer.type_write(Byte, flag)

        return writer.get_data()


class Money(dataTypeAbstract):
    @staticmethod
    def read(data: bytes, pos: int):
        money = []
        for _ in range(5):
            money_value, pos = VarInt.read(data, pos)
            money.append(money_value)

        return money, pos

    @staticmethod
    def write(data: bytearray, value: list):
        for money_value in value:
            data = VarInt.write(data, money_value)

        return data


class GameRecord(dataTypeAbstract):
    @staticmethod
    def read(data: bytes, pos: int):
        all_record = {}  # 用来存储解析出来的数据喵
        diff_list: tuple = ("EZ", "HD", "IN", "AT", "Legacy")

        reader = Reader(data, pos)
        songSum: int = reader.type_read(VarInt)  # 总歌曲数目喵

        for _ in range(songSum):
            songName: str = (reader.type_read(String))[:-2]  # 歌曲名字喵
            # 数据总长度喵(不包括歌曲名字喵)
            length: int = reader.type_read(VarInt)
            end_position: int = reader.pos + length  # 单首歌数据结束字节位置喵
            unlock: int = reader.type_read(Byte)  # 每个难度解锁情况喵
            fc: int = reader.type_read(Byte)  # 每个难度fc情况喵
            song = all_record[songName] = {}  # 存储单首歌的成绩数据喵

            # 遍历每首歌的EZ、HD、IN、AT、Legacy(旧谱)难度的成绩喵
            for level in range(5):
                if Bit.read(unlock, level):  # 判断当前难度是否解锁喵
                    score: int = reader.type_read(Int)  # 读取分数喵
                    acc: float = reader.type_read(Float)  # 读取acc喵

                    song[diff_list[level]] = {  # 按难度存储进单首歌的成绩数据中喵
                        "score": score,  # 分数喵
                        "acc": acc,  # ACC喵
                        "fc": Bit.read(fc, level),  # 是否Full Combo喵(FC)
                    }

            if reader.pos != end_position:
                logger.error(
                    f'在读取"{songName}"的数据时发生错误喵！当前位置：{reader.pos}'
                )
                logger.error(
                    f"错误喵！！！当前读取字节位置不正确喵！应为：{end_position}"
                )

        return all_record, reader.pos

    @staticmethod
    def write(data: bytearray, value: dict):
        diff_list: dict = {"EZ": 0, "HD": 1, "IN": 2, "AT": 3, "Legacy": 4}

        writer = Writer(data)
        writer.type_write(VarInt, len(value))

        for name, song in value.items():
            writer.type_write(String, name + ".0")

            # 这行不是冗余代码啊喵！本喵这样子写是有原因的！
            writer.type_write(VarInt, len(song) * (4 + 4) + 1 + 1)
            unlock = eval(Bits.read(b"\x00", 0)[0])
            fc = eval(Bits.read(b"\x00", 0)[0])
            record_writer = Writer()
            for diff, index in diff_list.items():
                if song.get(diff) is not None:
                    unlock[index] = 1
                    record_writer.type_write(Int, song[diff]["score"])
                    record_writer.type_write(Float, song[diff]["acc"])
                    fc[index] = song[diff]["fc"]

            writer.type_write(Bits, str(unlock))
            writer.type_write(Bits, str(fc))
            writer.type_write(Byte, record_writer.get_data())

        return writer.get_data()


class Summary(dataTypeAbstract):
    @staticmethod
    def read(data: bytes, pos: int):
        reader = Reader(data, pos)
        return [reader.type_read(ShortInt) for _ in range(3)], reader.pos

    @staticmethod
    def write(data: bytearray, value: list):
        writer = Writer(data)
        for i in value:
            writer.type_write(ShortInt, i)

        return writer.get_data()


class Reader:
    """反序列化存档数据的操作类喵"""

    def __init__(self, data: Union[bytes, bytearray], pos: int = 0):
        """
        反序列化存档数据的操作类喵

        参数:
            data (bytes | bytearray): 要读取的二进制数据喵
            pos (int): 当前读写位置喵。默认为 0 喵
        """
        self.data = data
        self.pos = pos
        self.bit_read = [bytes(), False, 0]

        self.read_dict = {}

    def type_read(self, type_class) -> Any:
        """
        使用数据类型提供的read()方法进行反序列化数据喵

        参数:
            type_class (class): 定义了read()方法的数据类型喵

        返回:
            (Any): 反序列化的数据喵
        """
        if type_class == Bit:
            if not self.bit_read[1]:
                self.bit_read[0], self.pos = Byte.read(self.data, self.pos)
                self.bit_read[1] = True

            read_data = Bit.read(self.bit_read[0], self.bit_read[2])
            self.bit_read[2] += 1

        else:
            if self.bit_read[1]:
                self.bit_read[1] = False
                self.bit_read[2] = 0

            read_data, self.pos = type_class.read(self.data, self.pos)

        return read_data

    def parseStructure(self, structure) -> Dict[str, Any]:
        """
        按照数据结构类定义的结构进行反序列化数据喵

        参数:
            structure (class): 数据结构类喵

        返回:
            (dict[str, Any]): 反序列化的数据喵
        """
        obj = structure()

        if not isinstance(obj, dataTypeAbstract):
            for key, type_obj in structure.__annotations__.items():
                if not __debug__:
                    print(key, type_obj)

                self.read_dict[key] = self.type_read(type_obj)

                if not __debug__:
                    print(key, getattr(obj, key))

        else:
            self.read_dict = self.type_read(obj)

        if self.remaining() == 0:
            logger.debug(
                f'结构"{obj.__class__.__name__}"读取完毕喵！剩余{self.remaining()}字节喵！'
            )

        else:
            logger.error(
                f'结构"{obj.__class__.__name__}"尚未读取完毕喵！剩余{self.remaining()}字节喵！'
            )

        return self.read_dict

    def remaining(self) -> int:
        """
        返回剩余未反序列化的数据长度喵

        返回:
            (int): 剩余未反序列化的数据长度喵
        """
        return len(self.data) - self.pos


class Writer:
    """序列化存档数据的操作类喵"""

    def __init__(self, data: Optional[Union[bytearray, bytes]] = None):
        """
        序列化存档数据的操作类喵

        参数:
            data (bytes | bytearray | None): 若不为空，则基于此数据向后拼接序列化数据喵
        """
        if data is None:
            self.data = bytearray()

        elif isinstance(data, bytes):
            self.data = bytearray(data)

        elif isinstance(data, bytearray):
            self.data = data

        else:
            raise TypeError(f'传入的数据类型不合法喵！不应为"{type(data)}"喵！')

        self.bit_temp = [0, False, 0]

    def type_write(self, type_fc, value):
        """
        使用数据类型提供的write()方法进行序列化数据喵

        参数:
            type_class (class): 定义了write()方法的数据类型喵
            value (Any): 要序列化的数据喵
        """
        if type_fc == Bit:
            if not self.bit_temp[1]:
                self.bit_temp[0] = 0
                self.bit_temp[1] = True

            self.bit_temp[0] = Bit.write(self.bit_temp[0], self.bit_temp[2], value)
            self.bit_temp[2] += 1

        else:
            if self.bit_temp[1]:
                self.bit_temp[1] = False
                self.bit_temp[2] = 0
                self.data = Byte.write(self.data, self.bit_temp[0])

            self.data = type_fc.write(self.data, value)

    def buildStructure(self, structure, data: dict) -> bytearray:
        """
        按照数据结构类定义的结构进行反序列化数据喵

        参数:
            structure (class): 数据结构类喵

        返回:
            (dict[str, Any]): 反序列化的数据喵
        """
        obj = structure()

        if not isinstance(obj, dataTypeAbstract):
            for key, type_obj in structure.__annotations__.items():
                if not __debug__:
                    print(key, type_obj)

                self.type_write(type_obj, data[key])

                if not __debug__:
                    print(key, getattr(obj, key))

        else:
            self.type_write(obj, data)

        return self.data

    def get_data(self) -> bytearray:
        """
        返回已经序列化的数据喵

        返回:
            (bytearray): 已序列化的数据喵
        """
        return self.data
