# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from asyncio import run
from json import dumps
from sys import argv

from PhiCloudLib import PhigrosCloud, ReadDifficultyFile, logger, ParseGameSave, GetB19, CheckSaveHistory

# ---------------------- 定义赋值区喵 ----------------------

arguments = argv  # 获取调用脚本时的参数喵

if len(arguments) != 1:
    sessionToken = arguments[1]
else:
    sessionToken = ''  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------

async def main(token):
    async with PhigrosCloud(token) as cloud:
        difficulty = await ReadDifficultyFile('difficulty.tsv')  # 读取难度定数文件

        logger.info(f'玩家昵称："{await cloud.getPlayerId()}"')  # 获取玩家昵称并输出
        summary = await cloud.getSummary()  # 获取玩家summary
        logger.info(f'玩家summary：{summary}')

        # 获取并解析存档
        saveDict = {}
        saveData = await cloud.getSave(summary['url'], summary['checksum'])
        await ParseGameSave(saveData, saveDict, difficulty)

        # 写出存档解析json数据
        with open('./PhigrosSave.json', 'w', encoding='utf-8') as savefile:
            savefile.write(dumps(saveDict, ensure_ascii=False, indent=4))

        b19 = await GetB19(saveDict['record'])  # 获取b19

        # 输出并计算玩家rks
        rks = 0.0
        logger.info('玩家b19：')
        for song in b19:
            logger.info(song)
            rks += song['rks']
        logger.info(f'玩家rks：{rks / 20}')

        await CheckSaveHistory(token, summary, saveData, difficulty)  # 存储存档历史记录

        # 其他功能）↓
        # await cloud.refreshSessionToken()  # 刷新sessionToken喵(注意此功能尚未经过大量测试喵，刷新是即时的喵，旧token会立即失效喵)


if __name__ == '__main__':
    run(main(sessionToken))
