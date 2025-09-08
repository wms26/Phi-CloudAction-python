from json import dumps
from sys import argv

from PhiCloudAction import (
    PhigrosCloud,
    parseSaveDict,
    readDifficultyFile,
    countRks,
    checkSaveHistory,
    getB19,
    getB30,
    logger,
)

if len(argv) == 1:
    sessionToken = ""

else:
    sessionToken = argv[1]

if __name__ == "__main__":
    with PhigrosCloud(sessionToken) as cloud:
        logger.info(f"玩家昵称：{cloud.getNickname()}")

        summary = cloud.getSummary()
        logger.info(f"玩家summary：{summary}")

        save_data = cloud.getSave()
        save_dict = parseSaveDict(save_data)

    with open("PhigrosSave.json", "w", encoding="utf-8") as file:
        file.write(dumps(save_dict, indent=4, ensure_ascii=False))

    logger.info("获取存档成功喵！")

    difficult = readDifficultyFile()
    save_dict = countRks(save_dict, difficult)

    b19 = getB19(save_dict)
    count_rks = 0.0
    for b in b19:
        logger.info(dumps(b, ensure_ascii=False))
        count_rks += b["rks"]
    logger.info(f"B19计算出来的RKS（旧算法，已弃用，仅作参考）：{count_rks / 20}")

    b30 = getB30(save_dict)
    count_rks = 0.0
    for b in b30:
        logger.info(dumps(b, ensure_ascii=False))
        count_rks += b["rks"]
    logger.info(f"B30计算出来的RKS：{count_rks / 30}")

    checkSaveHistory(sessionToken, summary, save_data, difficult)
