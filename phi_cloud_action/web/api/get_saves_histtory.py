from phi_cloud_action import readSaveHistory,logger
from fastapi.responses import JSONResponse
from .request_models import TokenRequest
from .example import example

class get_saves_histtory(example):
    def __init__(self):
        self.route_path = "/get/saves/histtory"
        self.methods = ["POST"]

    async def api(self, request:TokenRequest) -> JSONResponse:
        try:
            # 使用 request.token 来获取传递的 token 值
            data = readSaveHistory(request.token)
            return JSONResponse(content={
                "code": 200,
                "status": "ok",
                "data": {
                "histtory":{
                    "summary":data.summary,
                    "record":data.record
                    }
                }
                }, status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)