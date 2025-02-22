from pydantic import BaseModel
# b_num 请求模型喵~
class BNumRequest(BaseModel):
    b_num: int = 27