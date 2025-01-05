from json import loads, dumps
from os import listdir
from os.path import exists, join

saveHistory_path = "./saveHistory/"

if exists(saveHistory_path):
    dir_list = listdir(saveHistory_path)
    if len(dir_list) > 0:
        for session in dir_list:
            with open(
                join(saveHistory_path, session, "recordHistory.json"),
                "r",
                encoding="utf-8",
            ) as file:
                recordHistory: dict = loads(file.read())

            for key in recordHistory.keys():
                print(key)
            print(f"共有{len(recordHistory.keys())}条记录")

            for key in recordHistory.keys():
                if not exists(join(saveHistory_path, session, f"{key}.save")):
                    print(f'"{key}"存档文件不存在！')

            for date in recordHistory.keys():
                for song in recordHistory[date].keys():
                    for record in recordHistory[date][song].keys():
                        del recordHistory[date][song][record]["rks"]

            with open(
                join(saveHistory_path, session, "recordHistory.json"),
                "w",
                encoding="utf-8",
            ) as file:
                file.write(dumps(recordHistory, indent=4, ensure_ascii=False))
