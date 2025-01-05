# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from json import dumps
from sys import argv

from PhiCloudLib import (
    PhigrosCloud,
    readDifficultyFile,
    unzipSave,
    decryptSave,
    countRks,
    logger,
)


# ---------------------- 定义赋值区喵 ----------------------

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = ""  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------


def getSave(token):
    with PhigrosCloud(token) as cloud:
        difficulty = readDifficultyFile()  # 读取难度定数文件

        # 获取并解析存档
        save_data = cloud.getSave()
        save_dict = unzipSave(save_data)
        save_dict = decryptSave(save_dict)
        save_dict["gameRecord"] = countRks(save_dict["gameRecord"], difficulty)

        # 写出存档解析json数据
        with open("./PhigrosSave.json", "w", encoding="utf-8") as save_file:
            save_file.write(dumps(save_dict, ensure_ascii=False, indent=4))

        logger.info("获取存档成功喵！")


if __name__ == "__main__":
    getSave(sessionToken)
