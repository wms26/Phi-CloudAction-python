import hmac
import base64
import json
import time
import random
import requests

class Share:
    def __init__(self):
        self.client = requests.Session()
        self.tap_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "TapTapAndroidSDK/3.16.5"
        }
        self.phi_headers = {
            "User-Agent": "LeanCloud-CSharp-SDK/1.0.3",
            "X-LC-Id": "rAK3FfdieFob2Nn8Am",
            "X-LC-Key": "Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0",
            "Content-Type": "application/json"
        }

share = Share()

def mac(token):
    ts = int(time.time())
    nonce = random.randint(0, 2**32 - 1)
    input_str = f"{ts}\n{nonce}\nGET\n/account/basic-info/v1?client_id=rAK3FfdieFob2Nn8Am\nopen.tapapis.cn\n443\n\n"
    
    _mac = hmac.new(token['mac_key'].encode(), input_str.encode(), digestmod='sha1')
    mac_base64 = base64.b64encode(_mac.digest()).decode()
    
    return f"MAC id=\"{token['kid']}\",ts=\"{ts}\",nonce=\"{nonce}\",mac=\"{mac_base64}\""

def login(device_id):
    url = "https://www.taptap.com/oauth2/v1/device/code"
    payload = f"client_id=rAK3FfdieFob2Nn8Am&response_type=device_code&scope=basic_info&version=1.2.0&platform=unity&info=%7b%22device_id%22%3a%22{device_id}%22%7d"
    
    response = share.client.post(url, headers=share.tap_headers, data=payload)
    json_response = response.json()
    
    return json_response['data']

def get_token(device_code, device_id):
    url = "https://www.taptap.com/oauth2/v1/token"
    payload = f"grant_type=device_token&client_id=rAK3FfdieFob2Nn8Am&secret_type=hmac-sha-1&code={device_code}&version=1.0&platform=unity&info=%7b%22device_id%22%3a%22{device_id}%22%7d"
    
    response = share.client.post(url, headers=share.tap_headers, data=payload)
    json_response = response.json()
    
    if not json_response['success']:
        return json_response['data']
    
    token = json_response['data']
    token_info = get_account_info(token)
    user_info = register_user(token, token_info)
    
    return user_info

def get_account_info(token):
    url = "https://openapi.taptap.com/account/basic-info/v1?client_id=rAK3FfdieFob2Nn8Am"
    headers = share.tap_headers.copy()
    headers['Authorization'] = mac(token)
    
    response = share.client.get(url, headers=headers)
    json_response = response.json()
    
    return json_response['data']

def register_user(token, account):
    url = "https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/users"
    headers = share.phi_headers
    payload = json.dumps({
        "authData": {
            "taptap": {
                "kid": token['kid'],
                "access_token": token['kid'],
                "token_type": "mac",
                "mac_key": token['mac_key'],
                "mac_algorithm": "hmac-sha-1",
                "openid": account['openid'],
                "unionid": account['unionid']
            }
        }
    })
    
    response = share.client.post(url, headers=headers, data=payload)
    return response.text