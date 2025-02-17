from phi_cloud_action import PhigrosCloud, unzipSave, decryptSave, formatSaveDict, getB30, checkSaveHistory, logger
from fastapi.responses import JSONResponse
from .request_models import TokenRequest,BNumRequest
from .example import example

class BNumAndTokenRequest(TokenRequest,BNumRequest):
    pass

class get_cloud_b30(example):
    def __init__(self):
        self.route_path = "/get/cloud/b30"
        self.methods = ["POST"]
        super().__init__()

    def __call__(self, request:BNumAndTokenRequest) -> JSONResponse:
        try:
            # 使用 request.token 来获取传递的 token 值
            with PhigrosCloud(request.token) as cloud:
                # 获取玩家summary喵
                summary = cloud.getSummary() 

                # 获取并解析存档喵
                save_data = cloud.getSave(summary["url"], summary["checksum"])
                save_dict = unzipSave(save_data)
                save_dict = decryptSave(save_dict)
                save_dict = formatSaveDict(save_dict)

                # 存档历史记录
                checkSaveHistory(request.token, summary, save_data, self.difficulty)

                # 获取b30喵
                b30 = getB30(save_dict["gameRecord"], self.difficulty, request.b_num)

                # 计算玩家rks喵
                rks = 0.0
                for song in b30():
                    rks += song["rks"]
                rks = rks / 30

            return JSONResponse(content={"code": 200,"status": "ok", "data": {"rks":rks,"b30":{"p3":b30.p3,"b27":b30.b27}}}, status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)