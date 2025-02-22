from pydantic import BaseModel
# Token 请求模型喵~
class TokenRequest(BaseModel):
    token: str