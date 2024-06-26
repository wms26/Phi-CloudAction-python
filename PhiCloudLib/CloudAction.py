# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from base64 import b64decode, b64encode
from datetime import datetime
from hashlib import md5
from struct import unpack, pack
from time import sleep

from requests import get

from PhiCloudLib.ActionLib import check_sessionToken
from PhiCloudLib.CloudLib import PigeonCloud

# ---------------------- 定义赋值区喵 ----------------------

global_headers = {  # 全局的请求头喵(理论上没有什么用了喵，在CloudLib已经重写了喵)
    'X-LC-Id': 'rAK3FfdieFob2Nn8Am',
    'X-LC-Key': 'Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0',
    'User-Agent': 'LeanCloud-CSharp-SDK/1.0.3',
    'Accept': 'application/json'
}


def getPlayerId(sessionToken: str):
    """获取玩家昵称喵\n
    sessionToken：正如其名喵，不用多说了吧喵"""
    if check_sessionToken(sessionToken):
        pigeon_req = PigeonCloud(sessionToken)
        return pigeon_req.UserInfo()[1]['nickname']  # 请求并解析获取玩家昵称并返回喵


def getSummary(sessionToken: str):
    """获取summary喵\n
    sessionToken：正如其名，不用多说了吧喵"""
    if check_sessionToken(sessionToken):
        pigeon_req = PigeonCloud(sessionToken)
        result = pigeon_req.SaveInfo()[1]['results'][0]  # 请求并初步解析存档信息喵
        summary = b64decode(result['summary'])  # base64解码summary数据喵
        summary = unpack('=BHfBx%ds12H' % summary[8], summary)  # 解析summary数据喵(这行是真的看不懂喵)
        return {  # 解析数据并返回一个字典喵
            'checksum': result['gameFile']['metaData']['_checksum'],  # 这是存档的md5校验值喵
            'updateAt': result['updatedAt'],  # 这是存档更新时间喵
            'url': result['gameFile']['url'],  # 这是存档直链喵
            'saveVersion': summary[0],  # 这是存档版本喵
            'challenge': summary[1],  # 课题分喵
            'rks': summary[2],  # 正如其名不多讲了喵
            'gameVersion': summary[3],  # 这是游戏版本喵
            'avatar': summary[4].decode(),  # 这是头像喵
            'EZ': summary[5:8],  # EZ难度的评级情况
            'HD': summary[8:11],  # HD难度的评级情况
            'IN': summary[11:14],  # IN难度的评级情况
            'AT': summary[14:17]  # AT难度的评级情况
        }


def getSave(url: str, checksum: str):
    """获取存档数据喵(未解析喵，需要zipfile解压喵)\n
    url：存档的URL喵\n
    checksum：存档的md5校验值\n
    (返回的数据可用readGameSave()读取喵)"""
    response = get(url, headers=global_headers)  # 请求存档文件喵
    saveData = response.content  # 获取存档数据喵
    if len(saveData) <= 30:
        print(f'[Warn]严重警告喵！！！获取到的云存档大小不足30字节喵！当前大小喵：{len(saveData)}')
        print('[Warn]可能云存档已丢失喵！！！请重新将本地存档同步至云端喵！')
        print('[Warn]将延迟5秒钟喵！！！')
        sleep(5)
    savemd5 = md5()  # 创建一个md5对象喵，用来计算md5校验值喵
    savemd5.update(saveData)  # 将存档数据更新进去喵
    if checksum != savemd5.hexdigest():  # 对比校验值喵，不正确则输出警告并等待喵
        print('[Warn]严重警告喵！！！存档校验不通过喵！')
        print('[Warn]这可能是因为不正确地上传存档导致的喵！')
        print('[Warn]将延迟5秒钟喵！！！')
        sleep(5)
    return saveData  # 返回存档数据喵


def refreshSessionToken(sessionToken: str):
    """刷新sessionToken喵\n
    sessionToken：正如其名不用多说了吧喵\n
    注意喵：原先的sessionToken将会失效喵！\n
    (会返回新的sessionToken喵！)\n
    (刷新是即时的喵，旧token会立即失效喵，新的会即时生效喵)"""
    if check_sessionToken(sessionToken):
        pigeon_req = PigeonCloud(sessionToken)
        objectId = pigeon_req.UserInfo()[1]['objectId']  # 获取玩家的objectId喵
        response = pigeon_req.RefreshSessionToken(objectId)[1]  # 发送刷新sessionToken请求喵
        return response['sessionToken']  # 获取新sessionToken喵


def uploadSave(sessionToken: str, saveData: bytes):  # 一坨*喵！不想改这么快了喵
    """上传存档至云端喵\n
    sessionToken：正如其名不用多说了吧喵\n
    saveData：存档压缩包数据喵"""
    if check_sessionToken(sessionToken):
        pigeon_req = PigeonCloud(sessionToken)

        # 请求存档信息喵
        URL, response = pigeon_req.SaveInfo()
        print('\n请求URL喵:', URL)
        print('返回数据喵:', response)

        # 更改summary的版本号喵，方便云存档同步喵
        print('现summary喵:', response['results'][0]['summary'])
        summary = bytearray(b64decode(response['results'][0]['summary']))  # base64解码summary数据喵
        summary[7] = 81  # 修改版本号喵，方便后期存档云同步喵
        summary = b64encode(summary)  # 把summary数据编码回去喵
        print('新summary喵:', summary)

        objectId = response['results'][0]['objectId']  # 获取objectId喵
        userObjectId = response['results'][0]['user']['objectId']  # 获取user的ObjectId喵
        print('objectId:', objectId)
        print('userObjectId:', userObjectId)

        # 计算存档的md5校验值喵
        md5hash = md5()  # 创建一个md5对象喵，用于后续计算存档数据md5校验值喵
        md5hash.update(saveData)  # 将存档数据更新到md5对象内喵
        checksum = md5hash.hexdigest()  # 计算md5校验值喵
        print('校验值saveChecksum喵:', checksum)

        # 请求fileToken喵
        URL, response = pigeon_req.FileTokens(userObjectId, len(saveData), checksum)
        print('\n请求URL喵:', URL)
        print('返回数据喵:', response)
        tokenKey = b64encode(response['key'].encode()).decode('utf-8')  # 获取key喵
        newObjectId = response['objectId']  # 获取新的objectId喵
        authorization = "UpToken " + response['token']  # 获取上传用的token喵
        print('tokenKey:', tokenKey)
        print('newObjectId:', newObjectId)
        print('authorization:', authorization)

        pigeon_req.Authorization(authorization)  # 将authorization传入喵，后续请求要用喵

        # 获取uploadId喵
        URL, response = pigeon_req.Uploads(tokenKey)
        print('\n请求URL喵:', URL)
        print('返回数据喵:', response)
        uploadId = response['uploadId']  # 获取上传用ID喵
        print('uploadId:', uploadId)

        # 获取etag并上传存档喵
        URL, response = pigeon_req.Uploads1(tokenKey, uploadId, saveData)
        print('\n请求URL喵:', URL)
        print('返回数据喵:', response)
        etag = response['etag']  # 获取etag喵
        print('etag:', etag)

        # 把etag请求上去喵(我也不知道有什么用喵)
        URL, response = pigeon_req.Uploads_Id(tokenKey, uploadId, etag)
        print('\n请求URL喵:', URL)
        print('返回数据喵:', response)

        # 发送fileCallback请求喵
        URL, response = pigeon_req.FileCallback(tokenKey)
        print('\n请求URL喵:', URL)
        print('返回数据喵:', response)

        # 上传summary喵
        URL, response = pigeon_req.UploadSummary(objectId, summary.decode(),
                                                 datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
                                                 newObjectId, userObjectId)
        print('\n请求URL喵:', URL)
        print('返回数据喵:', response)

        # 删除旧存档喵
        URL, response = pigeon_req.DeleteSave(objectId)
        print('\n请求URL喵:', URL)
        print('返回数据喵:', response)


def uploadSummary(sessionToken: str, summarys: dict):
    """上传summary喵(从上传存档里面独立出来的喵)\n
    sessionToken：正如其名不用多说了吧喵\n
    summarys：要上传的summary喵\n
    (注意这个只能用来看喵，没有任何实际用处喵，同步之后就没用了喵)"""
    if check_sessionToken(sessionToken):
        pigeon_req = PigeonCloud(sessionToken)

        # 将解析过的summary构建回去喵
        avatar_data = summarys['avatar'].encode()  # 对头像名称进行编码
        summary = bytearray()  # 创建一个空的summary数据喵
        summary.extend(pack('=B', summarys['saveVersion']))
        summary.extend(pack('=H', summarys['challenge']))
        summary.extend(pack('=f', summarys['rks']))
        summary.extend(pack('=B', summarys['gameVersion']))
        summary.append(len(avatar_data))
        summary.extend(avatar_data)
        for key in ['EZ', 'HD', 'IN', 'AT']:
            for i in summarys[key]:
                summary.extend(pack('=H', i))

        summary = b64encode(summary).decode()  # 把summary数据编码回去喵

        URL, response = pigeon_req.SaveInfo()  # 请求存档信息喵
        print('\n请求URL：' + URL)
        print('返回数据:', response)
        objectId = response['results'][0]['objectId']  # 获取objectId
        userObjectId = response['results'][0]['user']['objectId']  # 获取user的ObjectId
        checksum = response['results'][0]['gameFile']['metaData']['_checksum']  # 存档的md5校验值
        saveSize = response['results'][0]['gameFile']['metaData']['size']  # 存档的大小
        fileId = response['results'][0]['gameFile']['objectId']  # 存档的objectId
        print('objectId:', objectId)
        print('userObjectId:', userObjectId)
        print('checksum:', checksum)
        print('saveSize:', saveSize)

        print('现summary:', response['results'][0]['summary'])
        print('新summary:', summary)

        # 上传summary喵
        URL, response = pigeon_req.UploadSummary(objectId, summary,
                                                 datetime.utcnow().isoformat(timespec='milliseconds') + 'Z', fileId,
                                                 userObjectId)
        print('\n' + URL)
        print('返回数据:', response)
