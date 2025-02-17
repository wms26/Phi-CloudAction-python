import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from phi_cloud_action.webapi import register_routes
from phi_cloud_action.web import api
from phi_cloud_action import logger, checkSessionToken
import os

app = FastAPI(debug=True)
register_routes(app, api)
client = TestClient(app)

# 从环境变量读取TOKEN
TOKEN = os.getenv("PHIGROS_TEST_TOKEN")
checkSessionToken(TOKEN, log_switch=False)

test_list = [
    {"url": "/get/cloud/b30", "json": {"b_num": 27, "token": "ABC123"}, "status_code": 400},
    {"url": "/get/cloud/b30", "json": {"b_num": 27, "token": TOKEN}, "status_code": 400}
]

@pytest.mark.parametrize("test_case", test_list)
def test1(test_case):
    url = test_case["url"]
    json = test_case["json"]
    status_code = test_case["status_code"]
    response = client.post(url, json=json)
    if not response.status_code == status_code:
        log = f"""
        未通过测试:
        接口:{url},数据:{json},预期状态码:{status_code}
        返回内容:{response.text}
        返回状态码:{response.status_code}
        """
        raise RuntimeError(log)
