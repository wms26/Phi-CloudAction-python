from phi_cloud_action import Update, logger
from typing import Optional
from phi_cloud_action.PhiCloudLib.other import SOURCE_INFO
from fastapi.responses import JSONResponse
from fastapi import Body, Query
from pydantic import BaseModel
from .example import example
import os

class boby(BaseModel):
    source_info: Optional[dict] = SOURCE_INFO

# 更新信息的处理类
class update_info(example):
    def __init__(self):
        # 路由路径和请求方法
        self.route_path = "/update/info"
        self.methods = ["GET", "POST"]

    def api(self, source: str = Query(...), body: boby = Body(None), max_retries: int = 3):
        try:
            # 获取请求中的源信息，Pydantic会自动进行验证喵~
            source_info = body.source_info  # 通过Pydantic的model来获取 source_info 喵~

            # 如果没有提供 source，返回错误信息喵~
            if not source:
                return JSONResponse(content={"code": 400, "status": "error", "message": f"请选择源:{source_info}"}, status_code=400)
                        
            # 执行更新操作喵~
            Update.info(source=source, max_retries=max_retries, source_info=source_info)

            # 设置新成的源
            os.environ["PHI_DIF_NAME"] = source_info[source]["save_name"]
            logger.debug(f"当前环境PHI_DIF_NAME:{os.getenv("PHI_DIF_NAME")}")

            # 返回成功的响应喵~
            return JSONResponse(content={
                "code": 200,
                "status": "ok",
                "data": {}
            }, status_code=200)
        except Exception as e:
            # 捕获异常并记录日志喵~
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)
