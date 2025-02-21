from sys import argv
import threading
from phi_cloud_action import (
    get_token,
    login,
    logger,
    get_qr_text
)

# ---------------------- 定义赋值区喵 ----------------------
arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    device_id = arguments[1]
else:
    device_id = ""  # 填你想要的设备型号

# ----------------------- 运行区喵 -----------------------

def printToken(device_id):
    last_login_successful:bool = True  # 标志变量，记录上次 login 是否成功

    while True:
        # 如果上次 login 成功，执行 login 操作
        if last_login_successful:
            logger.debug(f"device_id:{device_id}")
            data0 = login(device_id=device_id)
        else:
            logger.debug(f"上次登录失败，跳过 login 操作喵。")

        # 获取二维码url和设备code
        qrcode_url = data0["qrcode_url"]
        device_code = data0["device_code"]
        expires_in = data0["expires_in"]
        logger.debug(f"qrcode_url:{qrcode_url},device_code:{device_code}")

        # 获取二维码并打印
        qr_text = get_qr_text(qrcode_url)
        temp0 = f"""\n二维码url:\n{qrcode_url}\n二维码:\n{qr_text}\n"""
        logger.info(temp0)

        # 超时处理函数
        def timeout():
            logger.info("授权超时喵！请重新授权")
            nonlocal timeout_flag
            timeout_flag.set()  # 设置事件标志

        # 设置超时标志
        timeout_flag = threading.Event()

        # 启动超时线程
        timeout_thread = threading.Timer(expires_in, timeout)
        timeout_thread.start()

        # 等待扫码输入
        user_input = input("同意授权后按 Enter 键喵：(输入exit退出)")

        # 处理退出
        if user_input == "exit" or timeout_flag.is_set():
            timeout_thread.cancel()
            exit(0)

        # 获取token并打印
        data1:dict = get_token(device_code=device_code, device_id=device_id)

        # 检查 code 是否存在且不等于 -1
        if data1.get("code","") != -1:
            try:
                logger.info(f"您的token喵!:{data1['sessionToken']}")
                timeout_thread.cancel()  # 成功后取消定时器
                exit(0)
            except Exception:
                logger.error(f"未知错误,请联系开发者")
                logger.debug(data1)
                exit(1)
        else:
            # 处理错误的情况
            if data1.get("error") == "authorization_waiting":
                logger.error("请同意授权")
            elif data1.get("error") == "authorization_pending":
                logger.error("请扫码同意授权")
            else:
                logger.error("登录未成功")
            last_login_successful = False
            continue  # 跳过本次循环，重新开始获取二维码

if __name__ == "__main__":
    printToken(device_id)
