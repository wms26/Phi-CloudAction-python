# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiCloudLib.ActionLib import check_sessionToken
from requests import get
from base64 import b64decode
from struct import unpack

# ---------------------- 定义赋值区 ----------------------

global_headers = {
    'X-LC-Id': 'rAK3FfdieFob2Nn8Am',
    'X-LC-Key': 'Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0',
    'User-Agent': 'LeanCloud-CSharp-SDK/1.0.3',
    'Accept': 'application/json'
}


def getPlayerId(sessionToken: str):
    """获取玩家昵称\n
    sessionToken：正如其名，不用多说了吧"""
    if check_sessionToken(sessionToken):
        URL = 'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/users/me'
        headers = global_headers.copy()  # 浅复制请求头字典数据
        headers['X-LC-Session'] = sessionToken  # 将sessionToken添加到请求头中
        response = get(URL, headers=headers)  # 请求玩家信息
        return response.json()['nickname']  # 解析获取玩家昵称并返回


def getSummary(sessionToken: str):
    """获取summary
    sessionToken：正如其名，不用多说了吧"""
    if check_sessionToken(sessionToken):
        URL = 'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/classes/_GameSave?limit=1'
        headers = global_headers.copy()  # 浅复制请求头字典数据
        headers['X-LC-Session'] = sessionToken  # 将sessionToken附加到请求头中
        response = get(URL, headers=headers)  # 请求存档信息
        result = response.json()['results'][0]  # 解析存档信息
        summary = b64decode(result['summary'])  # base64解码summary数据
        summary = unpack('=BHfBx%ds12H' % summary[8], summary)  # 解析summary数据(这行是真的看不懂)
        return {  # 解析数据并返回一个字典
            'updateAt': result['updatedAt'],
            'url': result['gameFile']['url'],
            'saveVersion': summary[0],
            'challenge': summary[1],
            'rks': summary[2],
            'gameVersion': summary[3],
            'avatar': summary[4].decode(),
            'EZ': summary[5:8],
            'HD': summary[8:11],
            'IN': summary[11:14],
            'AT': summary[14:17]
        }


def getSave(url: str):
    """获取存档数据(未解析，需要zipfile解压)\n
    url：存档的URL\n
    (返回的数据可用readGameSave()读取)"""
    response = get(url, headers=global_headers)  # 请求存档文件
    return response.content  # 读取存档数据
