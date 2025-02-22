from pydantic import BaseModel
from .example import example
from fastapi.responses import JSONResponse
from fastapi import Body,Query
from phi_cloud_action import logger
from ...libs import get_token,login

class DeviceInfo(BaseModel):
    device_id: str = Body(...)

class get_token_login(example):
    def __init__(self):
        self.route_path = "/get/token/login"
        self.methods = ["POST"]

    async def api(self,boby:DeviceInfo):
        try:
            device_id = boby.device_id
            logger.debug(f"device_id:{device_id}")
            # 总结就是,导包(x)
            data = await login(device_id=device_id)
            return JSONResponse({"code":200,"status":"ok","data":data},status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)
    
class get_token_device_code(example):
    def __init__(self):
        self.route_path = "/get/token/{device_code}"
        self.methods = ["POST"]

    async def api(self,device_code,boby:DeviceInfo):
        try:
            device_id = boby.device_id
            logger.debug(f"device_id:{device_id},device_code:{device_code}")
            # 总结就是,导包(x)
            data = await get_token(device_code=device_code,device_id=device_id)
            return JSONResponse({"code":200,"status":"ok","data":data},status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)