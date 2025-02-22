# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from json import dumps
from sys import argv
import asyncio
from phi_cloud_action import (
    PhigrosCloud,
    unzipSave,
    decryptSave,
    logger,
)


# ---------------------- 定义赋值区喵 ----------------------

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = ""  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------

async def getSave(token):
    async with PhigrosCloud(token) as cloud:
        # 获取并解析存档喵
        save_data = await cloud.getSave()

        save_dict = unzipSave(save_data)
        save_dict = decryptSave(save_dict)

        # 写出存档解析json数据喵
        with open("./PhigrosSaves.json", "w", encoding="utf-8") as save_file:
            save_file.write(dumps(save_dict, ensure_ascii=False, indent=4))

        logger.info("获取存档成功喵！")


if __name__ == "__main__":
    asyncio.run(getSave(sessionToken))
