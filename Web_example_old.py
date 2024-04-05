from PhiCloudLib.ByteWriter import ByteWriter
from base64 import b64encode, b64decode
from Crypto.Cipher import PKCS1_OAEP
from random import randint, shuffle
from Crypto.PublicKey import RSA
from requests import post
from json import dumps
from re import match

sessionToken = ''

host = 'http://127.0.0.1:5000'


def random_split_string(input_string: str, max_length: int, min_length=1):
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
    # 生成特殊的base64
    try:
        b64data = b64encode(data.encode('utf-8')).decode()
    except AttributeError:
        b64data = b64encode(data).decode()

    equals_count = 0
    # 反向遍历字符串
    for pos in range(len(b64data)):
        if b64data[-pos - 1] == '=':
            b64data = b64data[:-1]
            equals_count += 1
        else:
            break

    b64data = str(equals_count) + b64data
    return b64data


def par_base64(data: str):
    # 解码特殊的base64
    if match(r'^[0-9]', data):
        num: int = int(data[0])
        data: str = data[1:] + '=' * num
        return b64decode(data).decode()

    return None


def gen_dictRequest(data: dict):
    # 生成请求数据
    Writer = ByteWriter()
    Writer.writeByte(len(data))
    for item in data.items():
        Writer.writeString(item[0])
        Writer.writeString(gen_base64(item[1]))
    return Writer.getData()


def gen_data(data: str):
    # 生成请求数据
    random_data: list = random_split_string(data, 10)
    shuffle_data: list = random_data.copy()
    shuffle(shuffle_data)
    Writer = ByteWriter()
    Writer.writeShort(len(random_data))
    for item in shuffle_data:
        Writer.writeShort(random_data.index(item))
        Writer.writeString(item)
    return Writer.getData()


# 请求RSA公钥
URL = host + '/api/bind_key'
res = post(URL)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + dumps(res.json(), ensure_ascii=False))
public_key = res.json()['massage']
rsa = PKCS1_OAEP.new(RSA.import_key(b64decode(public_key)))

# 请求playerId
req = b64encode(rsa.encrypt(gen_data(sessionToken)))
URL = host + '/api/getPlayerId'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())

# 请求summary
req = b64encode(rsa.encrypt(gen_data(sessionToken)))
URL = host + '/api/getSummary'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())

# 请求save
req = b64encode(rsa.encrypt(gen_data(sessionToken)))
URL = host + '/api/getSave'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())

# 请求b19
req = b64encode(rsa.encrypt(gen_data(sessionToken)))
URL = host + '/api/getB19'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())

# 获取money
req = b64encode(rsa.encrypt(gen_data(sessionToken)))
URL = host + '/api/getMoney'
res = post(URL, data=req)
print('\n[Info]请求地址：' + URL)
print('[Info]状态码：' + str(res.status_code))
if res.status_code != 200:
    print('\n[Error]返回数据：' + res.text)
    exit()
print('[Info]返回数据：' + b64decode(res.content).decode())
