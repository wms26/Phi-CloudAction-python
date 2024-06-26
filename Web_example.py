from base64 import b64encode, b64decode
from random import randint, shuffle

from requests import post

from PhiCloudLib.ByteWriter import ByteWriter

reqData_encrypt = False  # 用于声明请求的数据是否使用本喵自己搓的“特殊混淆处理”

sessionToken = ''

host = 'http://127.0.0.1:5000'


def random_split_string(input_string: str, max_length: int, min_length=1):
    """将一段字符串随机分割为不同长度的字符串，并返回列表\n
    input_string：要截取的字符串\n
    max_length：最大长度\n
    min_length：最小长度，默认为1"""
    string_length = len(input_string)  # 获取字符串长度

    # 如果设置了最大子串长度，则需要验证其合理性
    if max_length is not None and max_length < min_length:
        raise ValueError("最大字符串长度必须大于最小子串长度！")

    elif max_length is None:
        raise ValueError("最大字符串长度不能为空！")

    substrings = []  # 初始化空列表用于存放子串
    position = 0  # 从第一个字符开始

    while position < string_length:
        # 随机生成下一个子串的结束位置（注意不能超过当前剩余部分的最大长度）
        end_pos = randint(position + min_length, min(string_length, position + max_length))

        # 添加子串到列表
        substrings.append(input_string[position:end_pos])

        # 更新当前位置为上一个子串的结束位置加一
        position = end_pos

    return substrings


def gen_base64(data):
    """生成特殊的base64\n
    data：要编码处理的数据"""
    try:
        b64data = b64encode(data.encode('utf-8')).decode()
    except AttributeError:
        b64data = b64encode(data).decode()

    equals_count = 0  # 记录尾部等于号的数量
    for pos in range(len(b64data)):  # 反向遍历字符串，记录并删除尾部的等于号
        if b64data[-pos - 1] == '=':
            b64data = b64data[:-1]
            equals_count += 1
        else:
            break

    b64data = str(equals_count) + b64data  # 将尾部等于号数量拼接到开头
    return b64data


def gen_data(data: str):
    """生成请求数据\n
    data：要进行“混淆处理”的字符串"""
    random_data: list = random_split_string(data, 10)
    shuffle_data: list = random_data.copy()
    shuffle(shuffle_data)
    Writer = ByteWriter()
    Writer.writeShort(len(random_data))
    for item in shuffle_data:
        Writer.writeShort(random_data.index(item))
        Writer.writeString(item)
    return Writer.getData()


# 请求playerId
if reqData_encrypt:
    req = gen_base64(gen_data(sessionToken))
else:
    req = sessionToken
URL = host + '/api/getPlayerId'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())

# 请求summary
if reqData_encrypt:
    req = gen_base64(gen_data(sessionToken))
else:
    req = sessionToken
URL = host + '/api/getSummary'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())

# 请求save
if reqData_encrypt:
    req = gen_base64(gen_data(sessionToken))
else:
    req = sessionToken
URL = host + '/api/getSave'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())

# 请求b19
if reqData_encrypt:
    req = gen_base64(gen_data(sessionToken))
else:
    req = sessionToken
URL = host + '/api/getB19'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())

# 获取money
if reqData_encrypt:
    req = gen_base64(gen_data(sessionToken))
else:
    req = sessionToken
URL = host + '/api/getMoney'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())
