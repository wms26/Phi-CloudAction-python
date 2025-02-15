from phi_cloud_action import PhigrosCloud, unzipSave, decryptSave
from fastapi.responses import JSONResponse
from .request_models import TokenRequest

class get_cloud_saves():
    def __init__(self):
        self.route_path = "/get/cloud/saves"
        self.methods = ["POST"]

    @staticmethod
    def __call__(request: TokenRequest) -> JSONResponse:
        try:
            # 使用 request.token 来获取传递的 token 值
            with PhigrosCloud(request.token) as cloud:
                # 获取并解析存档喵~
                save_data = cloud.getSave()
                save_dict = unzipSave(save_data)
                save_dict = decryptSave(save_dict)

            return JSONResponse(content={"code": 200, "status": "ok", "data": save_dict}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)