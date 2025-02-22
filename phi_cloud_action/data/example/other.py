# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from sys import argv
import asyncio
from phi_cloud_action import (
    PhigrosCloud,
    logger
)


# ---------------------- 定义赋值区喵 ----------------------

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = ""  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------

async def refresh_token(token):
    async with PhigrosCloud(token) as cloud:
        # 刷新sessionToken喵(注意此功能尚未经过大量测试，刷新是即时的，旧token会立即失效喵)
        token = await cloud.refreshSessionToken()
        logger.info(f"新的token为:{token}")


if __name__ == "__main__":
    asyncio.run(refresh_token(sessionToken))
