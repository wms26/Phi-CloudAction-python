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

    def api(self, request:BNumAndTokenRequest) -> JSONResponse:
        try:
            # 获取存档
            temp = self.get_saves(request.token)
            save_dict = temp.save_dict

            # 获取难度定数
            difficulty = self.get_difficulty()

            # 获取b30喵
            b30 = getB30(save_dict["gameRecord"], difficulty, request.b_num)

            # 计算玩家rks喵
            rks = 0.0
            for song in b30():
                rks += song["rks"]
            rks = rks / 30

            return JSONResponse(content={"code": 200,"status": "ok", "data": {"rks":rks,"b30":{"p3":b30.p3,"b27":b30.b27}}}, status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)