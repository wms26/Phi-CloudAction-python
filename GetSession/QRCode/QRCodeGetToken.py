from time import sleep

from qrcode import make
from qrcode.main import QRCode

from TapTapLogin import TapTapLogin, logger
from json import dumps

if __name__ == '__main__':
    QRCode_info = TapTapLogin.RequestLoginQRCode()
    logger.info(f'获取二维码信息成功：{QRCode_info}')

    logger.info('已生成二维码！')
    make(QRCode_info['qrcode_url']).show()  # 生成二维码并展示

    # # 这段是在控制台打印二维码的
    # qr = QRCode()
    # qr.add_data(QRCode_info['qrcode_url'])
    # qr.print_ascii()

    wait_time = QRCode_info['interval']
    while True:
        Login_info: dict = TapTapLogin.CheckQRCodeResult(QRCode_info)
        if Login_info.get('data') is not None:
            logger.info(f'登录成功：{Login_info}')
            break
        logger.info('二维码登录未授权...')
        sleep(wait_time)

    Profile = TapTapLogin.GetProfile(Login_info['data'])
    logger.info(f'获取用户资料成功：{Profile}')

    Token = TapTapLogin.GetUserData({
        **Profile['data'],
        **Login_info['data']
    })
    logger.info(f'获取userdata成功：{Token}')
    with open('./.userdata', 'w', encoding='utf-8') as file:
        file.write(dumps(Token, ensure_ascii=False))
    logger.info(f'已输出.userdata文件到当前目录！')
    logger.info(f'你的sessionToken为：{Token["sessionToken"]}')
