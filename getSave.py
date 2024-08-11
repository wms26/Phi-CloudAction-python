# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from asyncio import run
from json import dumps
from sys import argv

from PhiCloudLib import PhigrosCloud, ReadDifficultyFile, logger, ParseGameSave, FormatGameKey

# ---------------------- 定义赋值区喵 ----------------------

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = 'vikx9y9w3epmftlq88b5tx9b2'  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------

async def main(token):
    async with PhigrosCloud(token) as cloud:
        difficulty = await ReadDifficultyFile('difficulty.tsv')  # 读取难度定数文件

        # 获取并解析存档
        saveDict = {}
        saveData = await cloud.getSave()
        await ParseGameSave(saveData, saveDict, difficulty)

        await FormatGameKey(saveDict)

        # 写出存档解析json数据
        with open('./PhigrosSave.json', 'w', encoding='utf-8') as savefile:
            savefile.write(dumps(saveDict, ensure_ascii=False, indent=4))

        logger.info('获取存档成功喵！')


if __name__ == '__main__':
    run(main(sessionToken))
