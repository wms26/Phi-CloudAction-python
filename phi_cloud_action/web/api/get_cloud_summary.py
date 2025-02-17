from phi_cloud_action import PhigrosCloud,unzipSave, decryptSave, formatSaveDict, checkSaveHistory, logger
from fastapi.responses import JSONResponse
from .request_models import TokenRequest
from .example import example

class get_cloud_summary(example):
    def __init__(self):
        self.route_path = "/get/cloud/summary"
        self.methods = ["POST"]
        super().__init__()

    def __call__(self, request: TokenRequest) -> JSONResponse:
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

            return JSONResponse(content={"code": 200, "status": "ok", "data": summary}, status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)