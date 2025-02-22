import httpx
from base64 import b64decode
from hashlib import md5
from json import dumps
from struct import unpack
from typing import Any, Optional, Union
from .ActionLib import checkSessionToken
from .logger import logger


# ---------------------- 定义赋值区喵 ----------------------

class PigeonRequest:
    def __init__(
        self,
        sessionToken: Optional[str] = None,
        client: Optional[httpx.AsyncClient] = None,
        headers: Optional[dict] = None,
    ):
        if client:
            self.client = client
        else:
            self.client = httpx.AsyncClient()

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

    async def request(
        self, method: str, url: str, headers: Optional[dict] = None, **kwargs
    ):
        method = method.upper()

        if headers is None:
            headers = self.headers

        if method == "GET":
            self._req = await self.client.get(url, headers=headers, **kwargs)

        elif method == "POST":
            self._req = await self.client.post(url, headers=headers, **kwargs)

        elif method == "PUT":
            self._req = await self.client.put(url, headers=headers, **kwargs)

        elif method == "DELETE":
            self._req = await self.client.delete(url, headers=headers, **kwargs)

        else:
            raise ValueError(f'传入的请求类型不合法喵！不应为"{method}"！')

        logger.debug(f"请求类型 ：{method}")
        logger.debug(f"请求URL ：{url}")
        logger.debug(f"请求头 ：{self._req.request.headers}")
        logger.debug(f"状态码 ：{self._req.status_code}")

        if self._req.request.content is None:
            logger.debug(f"请求数据 : *无请求数据*")
        elif isinstance(self._req.request.content, str):
            logger.debug(f"请求数据 : {repr(self._req.request.content)}")
        else:
            logger.debug(f"请求数据 : *{len(self._req.request.content)} bytes*")

        if self._req.content is None:
            logger.debug(f"返回数据 : *无返回数据*")
        else:
            try:
                logger.debug(f"返回数据 : {self._req.content.decode()}")
            except UnicodeDecodeError:
                logger.debug(f"返回数据 : *{len(self._req.content)} bytes*")

        self._req.raise_for_status()

        return self._req

    async def get(self, url: str, headers: Optional[dict] = None):
        return await self.request("GET", url, headers)

    async def post(
        self,
        url: str,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict] = None,
    ):
        return await self.request("POST", url, headers, data=data)

    async def put(
        self,
        url: str,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[dict] = None,
    ):
        return await self.request("PUT", url, headers, data=data)

    async def delete(self, url: str, headers: Optional[dict] = None):
        return await self.request("DELETE", url, headers)


class PhigrosCloud:
    def __init__(self, sessionToken: str, client: Optional[Any] = None):
        if checkSessionToken(sessionToken):
            self.create_client = False
            if client:
                self.client = client
            else:
                self.client = httpx.AsyncClient()
                self.create_client = True

            self.request = PigeonRequest(sessionToken, self.client)
            self.baseUrl = "https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.create_client:
            await self.close()

    async def __enter__(self):
        return self

    async def __exit__(self, exc_type, exc_val, exc_tb):
        if self.create_client:
            await self.close()

    async def close(self):
        await self.client.aclose()

    async def getNickname(self) -> str:
        """
        获取玩家昵称喵

        返回:
            (str): 玩家昵称喵
        """
        logger.debug("调用函数：getNickname()")

        # 请求并解析获取玩家昵称喵
        return_data = (await self.request.get(self.baseUrl + "users/me")).json()[
            "nickname"
        ]

        logger.debug(f'函数"getNickname()"返回：{return_data}')
        return return_data

    async def getSummary(self):
        """
        获取玩家summary喵

        返回:
            (dict): 玩家summary数据喵
        """
        logger.debug("调用函数：getSummary()")

        # 请求并初步解析存档信息喵
        result = (
            await self.request.get(self.baseUrl + "classes/_GameSave?limit=1")
        ).json()["results"][0]
        summary = b64decode(result["summary"])  # base64解码summary数据喵

        # 解析summary数据喵
        summary = unpack("=BHfBx%ds12H" % summary[8], summary)
        return_data = {  # 解析数据并返回一个字典喵
            "checksum": result["gameFile"]["metaData"]["_checksum"],
            "updateAt": result["updatedAt"],
            "url": result["gameFile"]["url"],
            "saveVersion": summary[0],
            "challenge": summary[1],
            "rks": summary[2],
            "gameVersion": summary[3],
            "avatar": summary[4].decode(),
            "EZ": summary[5:8],
            "HD": summary[8:11],
            "IN": summary[11:14],
            "AT": summary[14:17],
        }

        logger.debug(f'函数"getSummary()"返回：{return_data}')
        return return_data

    async def getSave(
        self, url: Optional[str] = None, checksum: Optional[str] = None
    ) -> bytes:
        """
        获取存档数据喵 (压缩包数据喵)

        参数:
            url (str | None): 存档的 URL 喵。留空自动获取当前token的数据喵
            checksum (str | None): 存档的 md5 校验值喵。留空自动获取当前token的数据喵

        返回:
            (bytes): 存档压缩包数据喵
        """
        logger.debug("调用函数：getSave()")

        if url is None:
            summary = await self.getSummary()
            url = summary["url"]
            if checksum is None:
                checksum = summary["checksum"]

        elif checksum is None:
            checksum = (await self.getSummary())["checksum"]

        # 请求存档文件并获取数据喵
        save_data = (await self.request.get(url)).content  # type: ignore
        if len(save_data) <= 30:
            logger.error(
                f"严重警告喵！！！获取到的云存档大小不足 30 字节喵！当前大小喵：{len(save_data)}"
            )
            raise ValueError(
                f"获取到的云存档大小不足 30 字节喵！当前大小喵：{len(save_data)}"
            )

        save_md5 = md5()  # 创建一个md5对象，用来计算md5校验值喵
        save_md5.update(save_data)  # 将存档数据更新进去喵
        actual_checksum = save_md5.hexdigest()
        if checksum != actual_checksum:
            logger.error("严重警告喵！！！存档校验不通过喵！")
            raise ValueError(
                f"存档校验不通过喵！本地存档md5：{actual_checksum}，云端存档md5：{checksum}"
            )

        logger.debug(f'函数"getSave()"返回：*{len(save_data)} bytes*')
        return save_data

    async def refreshSessionToken(self):
        """
        刷新sessionToken喵

        返回:
            (str): 新的sessionToken喵
        """
        logger.debug("调用函数：refreshSessionToken()")

        objectId = (await self.request.get(self.baseUrl + "users/me")).json()[
            "objectId"
        ]

        new_sessionToken = (
            await self.request.put(
                self.baseUrl + f"users/{objectId}/refreshSessionToken"
            )
        ).json()["sessionToken"]

        logger.debug(f'函数"refreshSessionToken()"返回：{new_sessionToken}')
        return new_sessionToken

    async def uploadNickname(self, name: str):
        """
        更新玩家昵称喵

        参数:
            name (str): 要更改的昵称喵

        返回:
            (None): 无喵~
        """
        logger.debug("调用函数：uploadNickname()")

        response = (await self.request.get(self.baseUrl + "users/me")).json()
        userObjectId = response["objectId"]
        logger.debug(f"userObjectId{userObjectId}")

        await self.request.put(
            url=self.baseUrl + f"users/{userObjectId}",
            data=dumps({"nickname": name}),
            headers={
                **self.request.headers,
                "Content-Type": "application/json",
            },
        )

        logger.debug('函数"uploadNickname()"无返回')

    async def uploadSummary(self, summary: dict):
        """
        上传summary喵

        参数:
            summarys (dict): 要上传的summary喵
        """
        logger.debug("调用函数：uploadSummary()")

        from struct import pack
        from base64 import b64encode
        from datetime import datetime

        avatar_data = summary["avatar"].encode()
        _summary = bytearray()
        _summary.extend(pack("=B", summary["saveVersion"]))
        _summary.extend(pack("=H", summary["challenge"]))
        _summary.extend(pack("=f", summary["rks"]))
        _summary.extend(pack("=B", summary["gameVersion"]))
        _summary.append(len(avatar_data))
        _summary.extend(avatar_data)
        for key in ["EZ", "HD", "IN", "AT"]:
            for i in summary[key]:
                _summary.extend(pack("=H", i))

        _summary = b64encode(_summary).decode()

        save_info = (
            await self.request.get(self.baseUrl + "classes/_GameSave?limit=1")
        ).json()["results"][0]

        objectId = save_info["objectId"]
        userObjectId = save_info["user"]["objectId"]
        checksum = save_info["gameFile"]["metaData"]["_checksum"]
        saveSize = save_info["gameFile"]["metaData"]["size"]
        fileObjectId = save_info["gameFile"]["objectId"]

        logger.debug(f"objectId：{objectId}")
        logger.debug(f"userObjectId：{userObjectId}")
        logger.debug(f"checksum：{checksum}")
        logger.debug(f"saveSize：{saveSize}")

        logger.debug(f'现summary：{save_info["summary"]}')
        logger.debug(f"新summary：{summary}")

        await self.request.put(
            url=self.baseUrl + f"classes/_GameSave/{objectId}?",
            data=dumps(
                {
                    "summary": summary,
                    "modifiedAt": {
                        "__type": "Date",
                        "iso": datetime.utcnow().isoformat(
                            timespec="milliseconds"
                        )
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