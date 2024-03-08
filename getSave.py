# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from PhiCloudLib.ParseGameSave import ParseGameKey, ParseGameProgress, ParseGameRecord, ParseGameSettings, ParseGameUser
from PhiCloudLib.ActionLib import readGameSave, readDifficulty, decryptGameSave
from PhiCloudLib.CloudAction import getSummary, getSave
from json import dumps

# ---------------------- 定义赋值区喵 ----------------------

sessionToken = ''

# ----------------------- 运行区喵 -----------------------

difficulty = readDifficulty('./difficulty.tsv')  # 读取难度定数列表文件喵
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
ParseGameRecord(difficulty, saveDict)
ParseGameKey(saveDict)

# 写出解析后所有的存档数据喵
with open('./PhigrosSave.json', 'w', encoding='utf-8') as savefile:
    savefile.write(dumps(saveDict, ensure_ascii=False, indent=4))

for i in saveDict.keys():
    print(i, ':', saveDict[i])
