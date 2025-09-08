from json import dumps
from sys import argv

from PhiCloudAction import PhigrosCloud, parseSaveDict, logger

if len(argv) == 1:
    sessionToken = ""

else:
    sessionToken = argv[1]

if __name__ == "__main__":
    with PhigrosCloud(sessionToken) as cloud:
        save_data = cloud.getSave()
        save_dict = parseSaveDict(save_data)
        with open("PhigrosSave.json", "w", encoding="utf-8") as file:
            file.write(dumps(save_dict, indent=4, ensure_ascii=False))

    logger.info("获取存档成功喵！")
