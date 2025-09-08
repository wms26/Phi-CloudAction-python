# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from base64 import b64decode
from hashlib import md5
from json import dumps
from typing import Any, Optional, Union

from requests import Session

from .ActionLib import checkSessionToken
from .Structure import Reader, summary
from .logger import logger


# ---------------------- 定义赋值区喵 ----------------------


class PigeonRequest:
    def __init__(
        self,
        sessionToken: Optional[str] = None,
        client: Optional[Session] = None,
        headers: Optional[dict] = None,
    ):
        if client:
            self.client = client
        else:
            self.client = Session()

        if headers:
            self.headers = headers
        else:
            self.headers = {
                "X-LC-Id": "rAK3FfdieFob2Nn8Am",
                "X-LC-Key": "Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0",
                "User-Agent": "LeanCloud-CSharp-SDK/1.0.3",
                "Accept": "application/json",
                "X-LC-Session": sessionToken,
            }  # 全局的默认请求头喵

        self._req = None

    def addHeaders(self, headers: Optional[dict] = None, **kwargs):
        if headers:
            header = {**self.headers, **headers, **kwargs}

        else:
            header = {**self.headers, **kwargs}

        return PigeonRequest(client=self.client, headers=header)

    def request(self, method: str, url: str, headers: Optional[dict] = None, **kwargs):
        method = method.upper()

        if headers is None:
            headers = self.headers

        if method == "GET":
            self._req = self.client.get(url, headers=headers, **kwargs)

        elif method == "POST":
            self._req = self.client.post(url, headers=headers, **kwargs)

        elif method == "PUT":
            self._req = self.client.put(url, headers=headers, **kwargs)

        elif method == "DELETE":
            self._req = self.client.delete(url, headers=headers, **kwargs)

        else:
            raise ValueError(f'传入的请求类型不合法喵！不应为"{method}"！')

        logger.debug(f"请求类型 ：{method}")
        logger.debug(f"请求URL ：{url}")
        logger.debug(f"请求头 ：{self._req.request.headers}")
        logger.debug(f"状态码 ：{self._req.status_code}")

        if self._req.request.body is None:
            logger.debug(f"请求数据 : *无请求数据*")

        elif isinstance(self._req.request.body, str):
            logger.debug(f"请求数据 : {repr(self._req.request.body)}")

        else:
            logger.debug(f"请求数据 : *{len(self._req.request.body)} bytes*")

        if self._req.content is None:
            logger.debug(f"返回数据 : *无返回数据*")

        else:
            try:
                logger.debug(f"返回数据 : {self._req.content.decode()}")

            except UnicodeDecodeError:
                logger.debug(f"返回数据 : *{len(self._req.content)} bytes*")

        self._req.raise_for_status()

        return self._req

    def get(self, url: str, headers: Optional[dict] = None):
        return self.request("GET", url, headers)

    def post(
        self,
        url: str,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict] = None,
    ):
        return self.request("POST", url, headers, data=data)

    def put(
        self,
        url: str,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict] = None,
    ):
        return self.request("PUT", url, headers, data=data)

    def delete(self, url: str, headers: Optional[dict] = None):
        return self.request("DELETE", url, headers)


class PhigrosCloud:
    def __init__(self, sessionToken: str, client: Optional[Any] = None):
        if checkSessionToken(sessionToken):
            self.create_client = False
            if client:
                self.client = client
            else:
                self.client = Session()
                self.create_client = True

            self.request = PigeonRequest(sessionToken, client)
            self.baseUrl = "https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.create_client:
            self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.create_client:
            self.close()

    def close(self):
        self.client.close()

    def getNickname(self) -> str:
        """
        获取玩家昵称喵

        返回:
            (str): 玩家昵称喵
        """
        logger.debug("调用函数：getNickname()")

        # 请求并解析获取玩家昵称喵
        return_data = (self.request.get(self.baseUrl + "users/me")).json()["nickname"]

        logger.debug(f'函数"getNickname()"返回：{return_data}')
        return return_data

    def getSummary(self):
        """
        获取玩家summary喵

        返回:
            (dict): 玩家summary数据喵
        """
        logger.debug("调用函数：getSummary()")

        # 请求并初步解析存档信息喵
        result = (self.request.get(self.baseUrl + "classes/_GameSave?limit=1")).json()[
            "results"
        ][0]
        summary_data = b64decode(result["summary"])  # base64解码summary数据喵

        # 解析summary数据喵（谢谢废酱喵！）
        summary_dict = Reader(summary_data).parseStructure(summary)

        return_data = {  # 解析数据并返回一个字典喵
            # 这是存档的md5校验值喵
            "checksum": result["gameFile"]["metaData"]["_checksum"],
            "updateAt": result["updatedAt"],  # 这是存档更新时间喵
            "url": result["gameFile"]["url"],  # 这是存档直链喵
            "saveVersion": summary_dict["saveVersion"],  # 这是存档版本喵
            "challenge": summary_dict["challenge"],  # 课题分喵
            "rks": summary_dict["rks"],  # 正如其名不多讲了喵
            "gameVersion": summary_dict["gameVersion"],  # 这是游戏版本喵
            "avatar": summary_dict["avatar"],  # 这是头像喵
            "EZ": summary_dict["EZ"],  # EZ难度的评级情况喵
            "HD": summary_dict["HD"],  # HD难度的评级情况喵
            "IN": summary_dict["IN"],  # IN难度的评级情况喵
            "AT": summary_dict["AT"],  # AT难度的评级情况喵
        }

        logger.debug(f'函数"getSummary()"返回：{return_data}')
        return return_data

    def getSave(
        self, url: Optional[str] = None, checksum: Optional[str] = None
    ) -> bytes:
        """
        获取存档数据喵 (压缩包数据喵)

        参数:
            url (str | None): 存档的URL喵。留空自动获取当前token的数据喵
            checksum (str | None): 存档的md5校验值喵。留空自动获取当前token的数据喵

        返回:
            (bytes): 存档压缩包数据喵
        """
        logger.debug("调用函数：getSave()")

        if url is None:
            summary = self.getSummary()
            url = summary["url"]
            if checksum is None:
                checksum = summary["checksum"]

        elif checksum is None:
            checksum = (self.getSummary())["checksum"]

        # 请求存档文件并获取数据喵
        save_data = (self.request.get(url)).content  # type: ignore
        if len(save_data) <= 30:
            logger.error(
                f"严重警告喵！！！获取到的云存档大小不足 30 字节喵！当前大小喵：{len(save_data)}"
            )
            logger.error("可能云存档已丢失喵！！！请重新将本地存档同步至云端喵！")
            raise ValueError(
                f"获取到的云存档大小不足 30 字节喵！当前大小喵：{len(save_data)}"
            )

        save_md5 = md5()  # 创建一个md5对象，用来计算md5校验值喵
        save_md5.update(save_data)  # 将存档数据更新进去喵
        actual_checksum = save_md5.hexdigest()
        if checksum != actual_checksum:  # 对比校验值喵，不正确则输出警告并等待喵
            logger.error("严重警告喵！！！存档校验不通过喵！")
            logger.error("这可能是因为不正确地上传存档导致的喵！")
            raise ValueError(
                f"存档校验不通过喵！本地存档md5：{actual_checksum}，云端存档md5：{checksum}"
            )

        logger.debug(f'函数"getSave()"返回：*{len(save_data)} bytes*')
        return save_data  # 返回存档数据喵

    def refreshSessionToken(self):
        """
        刷新sessionToken喵

        注意：原先的sessionToken会立即失效喵！刷新是即时的喵，旧token会立即失效喵，新的也会立即生效喵

        返回:
            (str): 新的sessionToken喵
        """
        logger.debug("调用函数：refreshSessionToken()")

        # 获取玩家的objectId喵
        objectId = (self.request.get(self.baseUrl + "users/me")).json()["objectId"]

        # 发送刷新sessionToken请求喵
        new_sessionToken = (
            self.request.put(self.baseUrl + f"users/{objectId}/refreshSessionToken")
        ).json()[1]["sessionToken"]

        logger.debug(f'函数"refreshSessionToken()"返回：{new_sessionToken}')
        return new_sessionToken

    def uploadNickname(self, name: str):
        """
        用于更新玩家昵称喵

        参数:
            name (str): 要更改的昵称喵

        返回:
            (None): 无喵~
        """
        logger.debug("调用函数：uploadNickname()")

        # 请求存档信息喵
        response = (self.request.get(self.baseUrl + "users/me")).json()
        userObjectId = response["objectId"]  # 获取user的ObjectId喵
        logger.debug(f"userObjectId{userObjectId}")

        # 请求更新用户信息喵
        self.request.put(
            url=self.baseUrl + f"users/{userObjectId}",
            data=dumps({"nickname": name}),
            headers={
                **self.request.headers,
                "Content-Type": "application/json",
            },
        )

        logger.debug('函数"uploadNickname()"无返回')

    def uploadSummary(self, summary: dict):
        """
        上传summary喵(从上传存档里面独立出来的喵)

        (注意这个只能用来看，没有任何实际用处，上传覆盖之后就没了喵)

        参数:
            summarys (dict): 要上传的summary喵
        """
        logger.debug("调用函数：uploadSummary()")

        from struct import pack
        from base64 import b64encode
        from json import dumps
        from datetime import datetime, timezone

        # 将解析过的summary构建回去喵
        avatar_data = summary["avatar"].encode()  # 对头像名称进行编码喵
        _summary = bytearray()  # 创建一个空的summary数据喵
        _summary.extend(pack("=B", summary["saveVersion"]))
        _summary.extend(pack("=H", summary["challenge"]))
        _summary.extend(pack("=f", summary["rks"]))
        _summary.extend(pack("=B", summary["gameVersion"]))
        _summary.append(len(avatar_data))
        _summary.extend(avatar_data)
        for key in ["EZ", "HD", "IN", "AT"]:
            for i in summary[key]:
                _summary.extend(pack("=H", i))

        _summary = b64encode(_summary).decode()  # 把summary数据编码回去喵

        # 请求存档信息喵
        save_info = (
            self.request.get(self.baseUrl + "classes/_GameSave?limit=1")
        ).json()["results"][0]

        objectId = save_info["objectId"]  # 获取objectId喵
        userObjectId = save_info["user"]["objectId"]  # 获取user的ObjectId喵
        # 存档的md5校验值喵
        checksum = save_info["gameFile"]["metaData"]["_checksum"]
        saveSize = save_info["gameFile"]["metaData"]["size"]  # 存档的大小喵
        fileObjectId = save_info["gameFile"]["objectId"]  # 存档的objectId喵

        logger.debug(f"objectId：{objectId}")
        logger.debug(f"userObjectId：{userObjectId}")
        logger.debug(f"checksum：{checksum}")
        logger.debug(f"saveSize：{saveSize}")

        logger.debug(f'现summary：{save_info["summary"]}')
        logger.debug(f"新summary：{summary}")

        # 上传summary喵
        self.request.put(
            url=self.baseUrl + "classes/_GameSave/{objectId}?",
            data=dumps(
                {
                    "summary": summary,
                    "modifiedAt": {
                        "__type": "Date",
                        "iso": datetime.now(timezone.utc)
                        .replace(tzinfo=None)
                        .isoformat(timespec="milliseconds")
                        + "Z",
                    },
                    "gameFile": {
                        "__type": "Pointer",
                        "className": "_File",
                        "objectId": fileObjectId,
                    },
                    "ACL": {userObjectId: {"read": True, "write": True}},
                    "user": {
                        "__type": "Pointer",
                        "className": "_User",
                        "objectId": userObjectId,
                    },
                }
            ),
            headers={
                **self.request.headers,
                "Content-Type": "application/json",
            },
        )

        logger.debug('函数"uploadSummary()"无返回')
