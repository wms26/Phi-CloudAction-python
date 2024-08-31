# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from base64 import b64decode
from hashlib import md5
from json import dumps
from struct import unpack

from httpx import AsyncClient

from .ActionLib import CheckSessionToken
from .ErrorException import SaveFileChecksumError
from .LibApi import logger


# ---------------------- 定义赋值区喵 ----------------------

class PigeonRequest:
    def __init__(self, sessionToken: str = None, client: AsyncClient = None, headers: dict = None):
        if client:
            self.client = client
        else:
            self.client = AsyncClient()

        if headers:
            self.headers = headers
        else:
            self.headers = {
                'X-LC-Id': 'rAK3FfdieFob2Nn8Am',
                'X-LC-Key': 'Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0',
                'User-Agent': 'LeanCloud-CSharp-SDK/1.0.3',
                'Accept': 'application/json',
                'X-LC-Session': sessionToken
            }  # 全局的默认请求头喵

        self.req = None

    async def addHeaders(self, headers: dict = None, **kwargs):
        if headers:
            header = {
                **self.headers,
                **headers,
                **kwargs
            }
        else:
            header = {
                **self.headers,
                **kwargs
            }
        return PigeonRequest(client=self.client, headers=header)

    async def get(self, url: str, headers: dict = None):
        if headers:
            self.req = await self.client.get(url, headers=headers)
        else:
            self.req = await self.client.get(url, headers=self.headers)
        self.req.raise_for_status()

        logger.debug(f'Request type：GET')
        logger.debug(f'Request URL：{url}')
        logger.debug(f'Request header：{self.headers}')
        logger.debug(f'Status code：{self.req.status_code}')
        try:
            logger.debug(f'Return data：{self.req.content.decode()}')
        except UnicodeDecodeError:
            logger.debug(f'Return data：Decoding data failed')

        return self.req

    async def post(self, url: str, data: str | bytes = None, headers: dict = None):
        if headers:
            self.req = await self.client.post(url, content=data, headers=headers)
        else:
            self.req = await self.client.post(url, content=data, headers=self.headers)
        self.req.raise_for_status()

        logger.debug(f'Request type：POST')
        logger.debug(f'Request URL：{url}')
        logger.debug(f'Request header：{self.headers}')
        try:
            logger.debug(f'Request data：{data.decode()}')
        except AttributeError:
            logger.debug(f'Request data：{data}')
        except UnicodeDecodeError:
            logger.debug(f'Request data：*{len(data)} bytes*')
        logger.debug(f'Status code：{self.req.status_code}')
        try:
            logger.debug(f'Return data：{self.req.content.decode()}')
        except UnicodeDecodeError:
            logger.debug(f'Return data：Decoding data failed')

        return self.req

    async def put(self, url: str, data: str | bytes = None, headers: dict = None):
        if headers:
            self.req = await self.client.put(url, content=data, headers=headers)
        else:
            self.req = await self.client.put(url, content=data, headers=self.headers)
        self.req.raise_for_status()

        logger.debug(f'Request type：PUT')
        logger.debug(f'Request URL：{url}')
        logger.debug(f'Request header：{self.headers}')
        try:
            logger.debug(f'Request data：{data.decode()}')
        except AttributeError:
            logger.debug(f'Request data：{data}')
        except UnicodeDecodeError:
            logger.debug(f'Request data：*{len(data)} bytes*')
        logger.debug(f'Status code：{self.req.status_code}')
        try:
            logger.debug(f'Return data：{self.req.content.decode()}')
        except UnicodeDecodeError:
            logger.debug(f'Return data：Decoding data failed')

        return self.req

    async def delete(self, url: str, headers: dict = None):
        if headers:
            self.req = await self.client.delete(url, headers=headers)
        else:
            self.req = await self.client.delete(url, headers=self.headers)

        logger.debug(f'Request type：DELETE')
        logger.debug(f'Request URL：{url}')
        logger.debug(f'Request header：{self.headers}')
        logger.debug(f'Status code：{self.req.status_code}')
        try:
            logger.debug(f'Return data：{self.req.content.decode()}')
        except UnicodeDecodeError:
            logger.debug(f'Return data：Decoding data failed')

        return self.req


class PhigrosCloud:
    def __init__(self, sessionToken: str, client: AsyncClient = None):
        if CheckSessionToken(sessionToken):
            self.create_client = False
            if client:
                self.client = client
            else:
                self.client = AsyncClient()
                self.create_client = True
            self.request = PigeonRequest(sessionToken, client)
            self.baseUrl = 'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/'

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.create_client:
            await self.close()

    async def close(self):
        await self.client.aclose()

    async def getNickname(self):
        """获取玩家昵称喵"""
        logger.debug('调用函数：getPlayerId()')
        return_data = (await self.request.get(self.baseUrl + 'users/me')).json()['nickname']  # 请求并解析获取玩家昵称喵
        logger.debug(f'函数"getPlayerId()"返回：{return_data}')
        return return_data

    async def getSummary(self):
        """获取summary喵"""
        logger.debug('调用函数：getSummary()')
        # 请求并初步解析存档信息喵
        result = (await self.request.get(self.baseUrl + 'classes/_GameSave?limit=1')).json()['results'][0]
        summary = b64decode(result['summary'])  # base64解码summary数据喵
        summary = unpack('=BHfBx%ds12H' % summary[8], summary)  # 解析summary数据喵(这行是真的看不懂喵)
        return_data = {  # 解析数据并返回一个字典喵
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
        logger.debug(f'函数"getSummary()"返回：{return_data}')
        return return_data

    async def getSave(self, url: str = None, checksum: str = None):
        """获取存档数据喵(未解析喵，需要zipfile解压喵)\n
        url：存档的URL喵\n
        checksum：存档的md5校验值\n
        (返回的数据可用ReadGameSave()读取喵)"""
        logger.debug('调用函数：getSave()')
        if not url:
            summary = await self.getSummary()
            url = summary['url']
            if not checksum:
                checksum = summary['checksum']
        elif not checksum:
            checksum = (await self.getSummary())['checksum']

        saveData = (await self.client.get(url)).content  # 请求存档文件并获取数据喵
        if len(saveData) <= 30:
            logger.error(f'严重警告喵！！！获取到的云存档大小不足30字节喵！当前大小喵：{len(saveData)}')
            logger.error('可能云存档已丢失喵！！！请重新将本地存档同步至云端喵！')
            raise ValueError('获取到的云存档大小不足30字节喵！当前大小喵：{len(saveData)}')
        savemd5 = md5()  # 创建一个md5对象喵，用来计算md5校验值喵
        savemd5.update(saveData)  # 将存档数据更新进去喵
        actual_checksum = savemd5.hexdigest()
        if checksum != actual_checksum:  # 对比校验值喵，不正确则输出警告并等待喵
            logger.error('严重警告喵！！！存档校验不通过喵！')
            logger.error('这可能是因为不正确地上传存档导致的喵！')
            raise SaveFileChecksumError(checksum, actual_checksum)
        logger.debug(f'函数"getSave()"返回：*{len(saveData)} bytes*')
        return saveData  # 返回存档数据喵

    async def refreshSessionToken(self):
        """刷新sessionToken喵\n
        sessionToken：正如其名不用多说了吧喵\n
        注意喵：原先的sessionToken将会失效喵！\n
        (会返回新的sessionToken喵！)\n
        (刷新是即时的喵，旧token会立即失效喵，新的会即时生效喵)"""
        logger.debug('调用函数：refreshSessionToken()')
        objectId = (await self.request.get(self.baseUrl + 'users/me')).json()['objectId']  # 获取玩家的objectId喵
        return_data = (await self.request.put(self.baseUrl + f'users/{objectId}/refreshSessionToken')
                       ).json()[1]['sessionToken']  # 发送刷新sessionToken请求喵
        logger.debug(f'函数"refreshSessionToken()"返回：{return_data}')
        return return_data

    async def uploadNickname(self, name: str):
        """用于更新玩家昵称\n
        name：要更改的昵称"""

        # 请求存档信息喵
        response = (await self.request.get(self.baseUrl + 'users/me')).json()
        userObjectId = response['objectId']  # 获取user的ObjectId喵
        logger.debug(f'userObjectId：{userObjectId}')

        # 请求更新用户信息喵
        response = (await self.request.put(
            url=self.baseUrl + f'users/{userObjectId}',
            data=dumps({
                'nickname': name
            }),
            headers={
                **self.request.headers,
                'Content-Type': 'application/json'
            }
        ))

        return response

    # async def uploadSummary(self, summarys: dict):
    #     """上传summary喵(从上传存档里面独立出来的喵)\n
    #     summarys：要上传的summary喵\n
    #     (注意这个只能用来看喵，没有任何实际用处喵，同步之后就没用了喵)"""
    #
    #     from struct import pack
    #     from json import dumps
    #     from datetime import datetime
    #
    #     # 将解析过的summary构建回去喵
    #     avatar_data = summarys['avatar'].encode()  # 对头像名称进行编码
    #     summary = bytearray()  # 创建一个空的summary数据喵
    #     summary.extend(pack('=B', summarys['saveVersion']))
    #     summary.extend(pack('=H', summarys['challenge']))
    #     summary.extend(pack('=f', summarys['rks']))
    #     summary.extend(pack('=B', summarys['gameVersion']))
    #     summary.append(len(avatar_data))
    #     summary.extend(avatar_data)
    #     for key in ['EZ', 'HD', 'IN', 'AT']:
    #         for i in summarys[key]:
    #             summary.extend(pack('=H', i))
    #
    #     summary = b64encode(summary).decode()  # 把summary数据编码回去喵
    #
    #     response = (await self.request.get(self.baseUrl + 'classes/_GameSave?limit=1')).json()['results'][0]  # 请求存档信息喵
    #
    #     objectId = response['objectId']  # 获取objectId
    #     userObjectId = response['user']['objectId']  # 获取user的ObjectId
    #     checksum = response['gameFile']['metaData']['_checksum']  # 存档的md5校验值
    #     saveSize = response['gameFile']['metaData']['size']  # 存档的大小
    #     fileObjectId = response['gameFile']['objectId']  # 存档的objectId
    #     logger.debug(f'objectId：{objectId}')
    #     logger.debug(f'userObjectId：{userObjectId}')
    #     logger.debug(f'checksum：{checksum}')
    #     logger.debug(f'saveSize：{saveSize}')
    #
    #     logger.debug(f'现summary：{response["summary"]}')
    #     logger.debug(f'新summary：{summary}')
    #
    #     # 上传summary喵
    #     await self.request.put(
    #         url=self.baseUrl + 'classes/_GameSave/{objectId}?',
    #         data=dumps({
    #             'summary': summary,
    #             'modifiedAt': {'__type': 'Date', 'iso': datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'},
    #             'gameFile': {'__type': 'Pointer', 'className': '_File', 'objectId': fileObjectId},
    #             'ACL': {userObjectId: {'read': True, 'write': True}},
    #             'user': {'__type': 'Pointer', 'className': '_User', 'objectId': userObjectId}
    #         }),
    #         headers={
    #             **self.request.headers,
    #             'Content-Type': 'application/json'
    #         }
    #     )
