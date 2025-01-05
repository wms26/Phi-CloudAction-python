# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from json import dumps
from sys import argv

from PhiCloudLib import (
    PhigrosCloud,
    readDifficultyFile,
    decryptSave,
    unzipSave,
    formatSaveDict,
    getB19,
    checkSaveHistory,
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


def example(token):
    with PhigrosCloud(token) as cloud:
        difficulty = readDifficultyFile()  # 读取难度定数文件

        logger.info(f'玩家昵称："{cloud.getNickname()}"')  # 获取玩家昵称并输出
        summary = cloud.getSummary()  # 获取玩家summary
        logger.info(f"玩家summary：{summary}")

        # 获取并解析存档
        save_data = cloud.getSave(summary["url"], summary["checksum"])
        save_dict = unzipSave(save_data)
        save_dict = decryptSave(save_dict)
        save_dict = formatSaveDict(save_dict)

        # 写出存档解析json数据
        with open("./PhigrosSave.json", "w", encoding="utf-8") as save_file:
            save_file.write(dumps(save_dict, ensure_ascii=False, indent=4))

        save_dict["gameRecord"] = countRks(
            save_dict["gameRecord"], difficulty, False
        )
        b19 = getB19(save_dict["gameRecord"], difficulty)  # 获取b19

        # 输出并计算玩家rks
        rks = 0.0
        logger.info("玩家b19：")
        for song in b19:
            logger.info(song)
            rks += song["rks"]
        logger.info(f"玩家rks：{rks / 20}")

        # 存储存档历史记录
        checkSaveHistory(token, summary, save_data, difficulty)

        # 其他功能）↓
        # cloud.refreshSessionToken()  # 刷新sessionToken喵(注意此功能尚未经过大量测试喵，刷新是即时的喵，旧token会立即失效喵)


if __name__ == "__main__":
    example(sessionToken)
