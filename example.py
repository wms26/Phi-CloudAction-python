# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from PhiCloudLib.ParseGameSave import ParseGameUser, ParseGameProgress, ParseGameSettings, ParseGameKey, ParseGameRecord
from PhiCloudLib.BuildGameSave import BuildGameKey, BuildGameProgress, BuildGameRecord, BuildGameSettings, BuildGameUser
from PhiCloudLib.ActionLib import readDifficulty, readGameSave, decryptGameSave, getB19, encryptGameSave, zipGameSave
from PhiCloudLib.CloudAction import getPlayerId, getSummary, getSave, uploadSave
from json import dumps, loads

# ---------------------- 定义赋值区喵 ----------------------

sessionToken = ''  # 填你的sessionToken喵


# ----------------------- 运行区喵 -----------------------

difficulty = readDifficulty('./difficulty.tsv')  # 读取难度定数列表文件喵
print(getPlayerId(sessionToken))  # 获取玩家昵称喵
summary = getSummary(sessionToken)  # 获取summary喵
print(summary)

save = getSave(summary['url'], summary['checksum'])  # 获取存档数据喵

# 读取并解密然后解析存档数据喵
saveDict = {}
readGameSave(save, saveDict)
decryptGameSave(saveDict)
ParseGameUser(saveDict)
ParseGameProgress(saveDict)
ParseGameSettings(saveDict)
ParseGameRecord(saveDict, difficulty)
ParseGameKey(saveDict)

# 写出解析后所有的存档数据喵
# with open('./PhigrosSave.json', 'w', encoding='utf-8') as savefile:
#     savefile.write(dumps(saveDict, ensure_ascii=False, indent=4))

b19 = getB19(saveDict['record'])  # 获取b19喵(准确来说是b20喵(?))
rks = 0  # 定义一个rks用于后续计算喵
for song in b19:  # 遍历b19列表喵
    rks += song['rks']  # 计算玩家rks喵
    print(song)  # 输出单条b19喵
print(f'根据b19计算玩家的rks喵：{rks / 20}')  # 输出玩家rks喵

# 其他功能）↓

# refreshSessionToken(sessionToken)  # 刷新sessionToken喵(注意此功能尚未经过大量测试喵，刷新是即时的喵，旧token会立即失效喵)

# summary['challenge'] = 566  # 将课题分改为彩色(5)66分）
# uploadSummary(sessionToken, summary)  # 上传summary）

# 下面这部分是上传前面写出的json存档数据文件的
# with open('./PhigrosSave.json', 'r', encoding='utf-8') as saveFile:
#     saveDict: dict = loads(saveFile.read())
#     BuildGameKey(saveDict)
#     BuildGameProgress(saveDict)
#     BuildGameRecord(saveDict)
#     BuildGameSettings(saveDict)
#     BuildGameUser(saveDict)
#     encryptGameSave(saveDict)

# zipGameSave会在打包各文件前加上对应的版本号文件头，与原存档同样的数据结构）
# uploadSave(sessionToken, zipGameSave(saveDict))  # 打包并上传存档）
