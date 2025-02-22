from pydantic import BaseModel
# 存档 请求模型喵~
class SavesRequest(BaseModel):
    saves: dict