from pydantic import BaseModel
from .example import example
from fastapi.responses import JSONResponse
from fastapi import Body,Query
from ...PhiCloudLib.logger import logger
from ..libs import (login,get_token)

class DeviceInfo(BaseModel):
    device_id: str

class get_token_login(example):
    def __init__(self):
        self.route_path = "/get/token/login"
        self.methods = ["POST"]

    def __call__(self,boby:DeviceInfo = Body(...)):
        device_id = boby.device_id
        logger.debug(f"device_id:{device_id}")
        data = login(device_id=device_id)
        return JSONResponse(data,status_code=200)
    
class get_token_device_code(example):
    def __init__(self):
        self.route_path = "/get/token/{device_code}"
        self.methods = ["POST"]

    def __call__(self,device_code,boby:DeviceInfo = Body(...)):
        device_id = boby.device_id
        logger.debug(f"device_id:{device_id},device_code:{device_code}")
        data = get_token(device_code=device_code,device_id=device_id)
        return JSONResponse(data,status_code=200)