from phi_cloud_action import PhigrosCloud, unzipSave, decryptSave, checkSaveHistory, formatSaveDict, logger
from fastapi.responses import JSONResponse
from .request_models import TokenRequest
from .example import example

class get_cloud_saves(example):
    def __init__(self):
        self.route_path = "/get/cloud/saves"
        self.methods = ["POST"]

    async def api(self, request: TokenRequest) -> JSONResponse:
        try:
            # 获取存档
            temp = await self.get_saves(request.token)
            summary = temp.summary
            save_dict = temp.save_dict

            return JSONResponse(content={"code": 200, "status": "ok", "data": {"saves":save_dict,"summary":summary}}, status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)