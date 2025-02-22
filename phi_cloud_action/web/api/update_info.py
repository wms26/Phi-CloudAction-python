from phi_cloud_action import Update, logger
from typing import Optional
from phi_cloud_action.PhiCloudLib.other import SOURCE_INFO
from fastapi.responses import JSONResponse
from fastapi import Body, Query
from pydantic import BaseModel
from .example import example
import os

# 定义 body 的 Pydantic 模型，source_info 字段可选
class boby(BaseModel):
    source_info: Optional[dict] = None  # source_info 字段可选，默认值为 None

# 更新信息的处理类
class update_info(example):
    def __init__(self):
        # 路由路径和请求方法
        self.route_path = "/update/info"
        self.methods = ["GET", "POST"]

    async def api(self, source: str = Query(...), body: Optional[boby] = Body(None), max_retries: int = 3):
        try:
            # 如果请求体没有传递 body（即 body 为 None），则使用默认的 SOURCE_INFO
            if body and body.source_info:
                source_info = body.source_info  # 请求体中的 source_info
            else:
                source_info = SOURCE_INFO  # 使用默认的 SOURCE_INFO

            # 执行更新操作
            Update.info(source=source, max_retries=max_retries, source_info=source_info)

            # 设置环境变量
            os.environ["PHI_DIF_NAME"] = source_info[source]["save_name"]
            logger.debug(f"当前环境 PHI_DIF_NAME: {os.getenv('PHI_DIF_NAME')}")

            return JSONResponse(content={
                "code": 200,
                "status": "ok",
                "data": {}
            }, status_code=200)
        except Exception as e:
            logger.warning(repr(e))
            return JSONResponse(content={"code": 400, "status": "error", "message": str(e)}, status_code=400)
