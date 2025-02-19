from phi_cloud_action import PhigrosCloud,unzipSave, decryptSave, formatSaveDict, checkSaveHistory, logger
from fastapi.responses import JSONResponse
from .request_models import TokenRequest
from .example import example

class get_cloud_summary(example):
    def __init__(self):
        self.route_path = "/get/cloud/summary"
        self.methods = ["POST"]

    def __call__(self, request: TokenRequest) -> JSONResponse:
        try:
            # 获取存档
            temp = self.get_saves(request.token)
            summary = temp.summary

            return JSONResponse(content={"code": 200, "status": "ok", "data": summary}, status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)