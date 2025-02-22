# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from sys import argv
import asyncio
from phi_cloud_action import (
    PhigrosCloud,
    readDifficultyFile,
    decryptSave,
    unzipSave,
    formatSaveDict,
    getB30,
    logger,
)


# ---------------------- 定义赋值区喵 ----------------------

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = ""  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------


async def printB30(token):
    async with PhigrosCloud(token) as cloud:

        # 读取难度定数文件喵
        difficulty = readDifficultyFile()

        # 获取玩家summary喵
        summary = await cloud.getSummary() 

        # 获取并解析存档喵
        save_data = await cloud.getSave(summary["url"], summary["checksum"])
        save_dict = unzipSave(save_data)
        save_dict = decryptSave(save_dict)
        save_dict = formatSaveDict(save_dict)

        # 获取b30喵
        b30 = getB30(save_dict["gameRecord"], difficulty)

        # 输出并计算玩家rks喵
        rks = 0.0
        logger.info("玩家b30：")
        for song in b30():
            logger.info(song)
            rks += song["rks"]
        logger.info(f"玩家rks：{rks / 30}")

if __name__ == "__main__":
    asyncio.run(printB30(sessionToken))
