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
    checkSaveHistory,
    readSaveHistory,
    logger
)


# ---------------------- 定义赋值区喵 ----------------------

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = ""  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------

async def archives(token):
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

        # 存储存档历史记录喵
        checkSaveHistory(token, summary, save_data, difficulty)
        
        # 输出存档记录喵
        SaveHistory = readSaveHistory(token)
        logger.info(SaveHistory.saves)

if __name__ == "__main__":
    asyncio.run(archives(sessionToken))
