# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from sys import argv

from phi_cloud_action import PhigrosCloud, logger

# ---------------------- 定义赋值区喵 ----------------------

nickname = ""

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = ""  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------


def uploadNickname(token):
    with PhigrosCloud(token) as cloud:
        global nickname
        logger.info(f'玩家昵称："{cloud.getNickname()}"')  # 获取玩家昵称并输出喵

        if nickname is None or nickname == "":
            nickname = input("请输入你要更改的名称：")

        cloud.uploadNickname(nickname)
        logger.info("上传昵称成功喵！")


if __name__ == "__main__":
    uploadNickname(sessionToken)
