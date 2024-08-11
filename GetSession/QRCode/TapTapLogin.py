from base64 import b64encode
from datetime import datetime
from hashlib import md5
from hashlib import sha256, sha1
from hmac import new
from json import dumps
from logging import getLogger, INFO, DEBUG, StreamHandler, basicConfig
from os import mkdir
from os.path import join, exists
from random import randint
from time import time
from uuid import uuid4

from colorlog import ColoredFormatter
from requests import Session


def set_logger(level=DEBUG):
    log_path = './log/'
    if not exists(log_path):
        mkdir(log_path)
    log_name = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{int(time())}.log'
    log_format = '[%(asctime)s] [%(module)s-%(funcName)s][%(name)s] [%(levelname)s] - %(message)s'
    basicConfig(filename=join(log_path, log_name), level=level, format=log_format)


def get_logger(name: str | None = None, level: int = INFO):
    set_logger()
    loggers = getLogger(name)  # 创建logger对象
    loggers.setLevel(DEBUG)

    console_handler = StreamHandler()  # 创建控制台日志处理器
    console_handler.setLevel(level)

    color_formatter = ColoredFormatter(
        '%(log_color)s[%(asctime)s] [%(module)s-%(funcName)s][%(name)s] [%(levelname)s] - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )  # 定义颜色输出格式
    # 将颜色输出格式添加到控制台日志处理器
    console_handler.setFormatter(color_formatter)

    for handler in loggers.handlers:  # 移除默认的handler
        loggers.removeHandler(handler)

    loggers.addHandler(console_handler)  # 将控制台日志处理器添加到logger对象
    return loggers


logger = get_logger('PhiQRCodeLogin', INFO)
logger.debug('Logger is loading completed.')


class TapTapLogin:
    AppKey: str = 'Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0'  # 构建请求头要用
    CloudServerAddress: str = 'https://rak3ffdi.cloud.tds1.tapapis.cn'  # 独属phi的Taptap云服务域名）
    ClientId: str = 'rAK3FfdieFob2Nn8Am'  # 独属phi的ID
    Client: Session = Session()

    ChinaWebHost: str = 'https://accounts.tapapis.cn'
    ChinaApiHost: str = 'https://open.tapapis.cn'
    ChinaCodeUrl: str = ChinaWebHost + '/oauth2/v1/device/code'
    ChinaTokenUrl: str = ChinaWebHost + '/oauth2/v1/token'
    TapSDKVersion: str = '2.1'

    @staticmethod
    def GetMd5Hash(string: str) -> str:
        """获取string的md5hash"""
        md5_hash = md5(string.encode())
        return md5_hash.hexdigest()

    @staticmethod
    def RequestLoginQRCode():
        """请求一个新QRCode的信息"""
        device_id: str = uuid4().hex  # 随机一个device_id出来
        data: dict = {
            'client_id': TapTapLogin.ClientId,
            'response_type': 'device_code',
            'scope': "public_profile",
            'version': TapTapLogin.TapSDKVersion,
            'platform': 'unity',
            'info': {'device_id': device_id}
        }
        QRCode_info: dict = TapTapLogin.Request(
            url=TapTapLogin.ChinaCodeUrl,
            method="POST",
            data=data
        )

        return {
            'device_id': device_id,
            **QRCode_info['data']
        }  # 把device_id先放进去，省的后面还要另外处理

    @staticmethod
    def CheckQRCodeResult(qrCodeData):
        """检查QRCode的登录授权情况"""
        data: dict = {
            'grant_type': 'device_token',
            'client_id': TapTapLogin.ClientId,
            'secret_type': 'hmac-sha-1',
            'code': qrCodeData['device_code'],
            'version': '1.0',
            'platform': 'unity',
            'info': dumps({'device_id': qrCodeData['device_id']})
        }
        try:
            result = TapTapLogin.Request(
                url=TapTapLogin.ChinaTokenUrl,
                method='POST',
                data=data
            )

            return result

        except Exception as e:
            return {'error': e}

    @staticmethod
    def GetProfile(token: dict):
        """获取用户信息，可用于后面获取userdata"""
        if not token:
            raise ValueError("传入的token无效！")

        hasPublicProfile: bool = "public_profile" in token["scope"]
        if hasPublicProfile:
            ChinaProfileUrl: str = TapTapLogin.ChinaApiHost + "/account/profile/v1?client_id="
        else:
            ChinaProfileUrl: str = TapTapLogin.ChinaApiHost + "/account/basic-info/v1?client_id="

        url: str = ChinaProfileUrl + TapTapLogin.ClientId
        uri: str = url.split('//')[1]
        sign: str = 'MAC ' + TapTapLogin.ParseAuthorizationHeader(
            kid=token['kid'],
            mac_key=token['mac_key'],
            mac_algorithm=token['mac_algorithm'],
            method='GET',
            uri='/' + uri.split('/', 1)[1],
            host=uri.split('/')[0],
            port='443',
            timestamp=int(time())
        )

        response: dict = TapTapLogin.Request(
            url=url,
            method='GET',
            headers={'Authorization': sign}
        )

        return response

    @staticmethod
    def GetUserData(data: dict):
        """获取Phigros的userdata"""
        url: str = f'{TapTapLogin.CloudServerAddress}/1.1/users'
        response: dict = TapTapLogin.Request(
            url=url,
            method='POST',
            headers={
                'X-LC-Id': TapTapLogin.ClientId,
                'Content-Type': 'application/json'  # 想研究原理的注意一下，此处得保证请求头的Content-Type为application/json
            },
            data={'authData': {'taptap': data}},
            addAppKey=True
        )
        return response

    @staticmethod
    def Request(url: str, method: str, headers: dict = None, data: dict = None, addAppKey: bool = False) -> dict:
        """综合请求函数"""
        headers: dict = headers or {}  # 如果没有传入headers则创建一个空字典，防止构建请求头时出错
        TapTapLogin.ParseHeaders(headers, addAppKey)  # 构建请求头
        method: str = method.upper()  # 将请求类型转为大写便于判断

        if method == 'POST':  # 如果是POST请求
            if headers.get('Content-Type') == 'application/json':  # 对GetUserData做适配性判断
                data: str = dumps(data)  # 序列化为标准json字符串
            else:
                data: dict = {key: str(value) for key, value in data.items()}  # 将所有值转为字符串

            response = TapTapLogin.Client.post(url, headers=headers, data=data)

        elif method == 'GET':  # 如果是GET请求
            response = TapTapLogin.Client.get(url, headers=headers)

        else:
            raise ValueError('不支持的请求类型！')

        logger.debug(f'Request type：{method}')
        logger.debug(f'Request URL：{url}')
        logger.debug(f'Request header：{headers}')
        logger.debug(f'Request data：{data}')
        logger.debug(f'Return header：{response.headers}')
        logger.debug(f'Status code：{response.status_code}')
        try:
            logger.debug(f'Return data：{response.content.decode()}')
        except UnicodeDecodeError:
            logger.debug(f'Return data：Decoding data failed')

        response.raise_for_status()  # 对非200状态码抛出错误
        return response.json()  # 将响应数据反序列化为字典

    @staticmethod
    def ParseAuthorizationHeader(kid, mac_key, mac_algorithm, method, uri, host, port, timestamp):
        """构建Authorization请求头"""
        nonce = str(randint(0, 2147483647))
        normalized_string = f"{timestamp}\n{nonce}\n{method}\n{uri}\n{host}\n{port}\n\n"

        if mac_algorithm == "hmac-sha-256":
            hash_generator = new(mac_key.encode(), normalized_string.encode(), sha256)
        elif mac_algorithm == "hmac-sha-1":
            hash_generator = new(mac_key.encode(), normalized_string.encode(), sha1)
        else:
            raise ValueError("Unsupported MAC algorithm")

        hash_value = b64encode(hash_generator.digest()).decode()
        return f'id="{kid}",ts="{timestamp}",nonce="{nonce}",mac="{hash_value}"'

    @staticmethod
    def ParseHeaders(headers, addAppKey: bool = False):
        """构造签名请求头"""
        timestamp = int(time() * 1000)
        if addAppKey:  # GetUserData会用到带AppKey的签名
            data = f'{timestamp}{TapTapLogin.AppKey}'
        else:
            data = str(timestamp)

        hash_value = TapTapLogin.GetMd5Hash(data)
        sign = f'{hash_value},{timestamp}'
        headers['X-LC-Sign'] = sign
