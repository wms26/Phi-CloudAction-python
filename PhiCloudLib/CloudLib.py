# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from requests import get, post, put, delete
from json import dumps


# ---------------------- 定义赋值区喵 ----------------------

# 注意！这是用于云存档操作的各种api请求，非必要请勿修改！

class PigeonCloud:
    def __init__(self, sessionToken: str):
        self.pigeon_headers = {
            'X-LC-Id': 'rAK3FfdieFob2Nn8Am',
            'X-LC-Key': 'Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0',
            'User-Agent': 'LeanCloud-CSharp-SDK/1.0.3',
            'Accept': 'application/json',
            'X-LC-Session': sessionToken
        }
        self.authorization_headsers = None

    def Authorization(self, authorization: str):
        self.authorization_headsers = {
            'Authorization': authorization
        }

    @staticmethod
    def addHeaders(header: dict, keyname: str, string):
        headers = header.copy()
        headers[keyname] = string
        return headers

    def UserInfo(self):
        """https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/users/me"""
        URL = 'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/users/me'
        return URL, get(URL, headers=self.pigeon_headers).json()

    def SaveInfo(self):
        """https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/classes/_GameSave"""
        URL = 'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/classes/_GameSave?limit=1'
        return URL, get(URL, headers=self.pigeon_headers).json()

    def RefreshSessionToken(self, objectId: str):
        """https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/users/[objectId]/refreshSessionToken"""
        URL = f'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/users/{objectId}/refreshSessionToken'
        return URL, get(URL, headers=self.pigeon_headers).json()

    def FileTokens(self, userObjectId: str, saveSize: [int, str], checksum: str):
        """https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/fileTokens \n
        tokenKey \n
        newObjectId \n
        authorization \n
        gameSaveTime"""
        URL = 'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/fileTokens'
        return URL, post(URL, headers=self.pigeon_headers, data=dumps({
            'name': '.save',
            '__type': 'File',
            'ACL': {userObjectId: {'read': True, 'write': True}},
            'prefix': 'gamesaves',
            'metaData': {'size': saveSize, '_checksum': checksum, 'prefix': 'gamesaves'}
        })).json()  # 请求fileToken喵

    def Uploads(self, tokenKey: str):
        """https://upload.qiniup.com/buckets/rAK3Ffdi/objects/[tokenKey]/uploads \n
        uploadId"""
        if self.authorization_headsers is None:
            print('[Error]请使用Authorization()提供authorization喵！')
            return False
        else:
            URL = f'https://upload.qiniup.com/buckets/rAK3Ffdi/objects/{tokenKey}/uploads'
            return URL, post(URL, headers=self.authorization_headsers).json()

    def Uploads1(self, tokenKey: str, uploadId: str, saveData: bytes):
        """https://upload.qiniup.com/buckets/rAK3Ffdi/objects/[tokenKey]/uploads/[uploadId]/1 \n
        etag"""
        if self.authorization_headsers is None:
            print('[Error]请使用Authorization()提供authorization喵！')
            return False
        else:
            URL = f'https://upload.qiniup.com/buckets/rAK3Ffdi/objects/{tokenKey}/uploads/{uploadId}/1'
            return URL, put(URL, headers=self.addHeaders(self.authorization_headsers,
                                                         'Content-Type',
                                                         'application/octet-stream'), data=saveData).json()

    def Uploads_Id(self, tokenKey: str, uploadId: str, etag: str):
        """https://upload.qiniup.com/buckets/rAK3Ffdi/objects/[tokenKey]/uploads/[uploadId]"""
        if self.authorization_headsers is None:
            print('[Error]请使用Authorization()提供authorization喵！')
            return False
        else:
            URL = f'https://upload.qiniup.com/buckets/rAK3Ffdi/objects/{tokenKey}/uploads/{uploadId}'
            return URL, post(URL, headers=self.addHeaders(self.authorization_headsers, 'Content-Type',
                                                          'application/octet-stream'),
                             data=dumps({'parts': [{'partNumber': 1, 'etag': etag}]})).json()

    def FileCallback(self, tokenKey: str):
        """https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/fileCallback"""
        URL = 'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/fileCallback'
        return URL, post(URL, headers=self.addHeaders(self.pigeon_headers, 'Content-Type', 'application/json'),
                         data=dumps({'result': True, 'token': tokenKey})).json()

    def UploadSummary(self, objectId: str, summary: str, gameSaveTime: str, newObjectId: str, userObjectId: str):
        """https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/classes/_GameSave/[objectId]?"""
        URL = f'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/classes/_GameSave/{objectId}?'
        return URL, put(URL, headers=self.addHeaders(self.pigeon_headers, 'Content-Type', 'application/json'),
                        data=dumps({
                            'summary': summary,
                            'modifiedAt': {'__type': 'Date', 'iso': gameSaveTime},
                            'gameFile': {'__type': 'Pointer', 'className': '_File', 'objectId': newObjectId},
                            'ACL': {userObjectId: {'read': True, 'write': True}},
                            'user': {'__type': 'Pointer', 'className': '_User', 'objectId': userObjectId}
                        }))

    def DeleteSave(self, objectId: str):
        """https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/files/[objectId]"""
        URL = f'https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/files/{objectId}'
        return URL, delete(URL, headers=self.pigeon_headers).json()
