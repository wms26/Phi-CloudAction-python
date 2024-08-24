# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from asyncio import run
from sys import argv

from PhiCloudLib import PhigrosCloud, logger

# ---------------------- 定义赋值区喵 ----------------------

nickname = ''

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = ''  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------

async def main(token):
    async with PhigrosCloud(token) as cloud:
        global nickname
        logger.info(f'玩家昵称："{await cloud.getNickname()}"')  # 获取玩家昵称并输出

        if nickname is None or nickname == '':
            nickname = input('请输入你要更改的名称：')

        req = await cloud.uploadNickname(nickname)
        logger.debug(req.json())

        logger.info('上传昵称成功喵！')


if __name__ == '__main__':
    run(main(sessionToken))