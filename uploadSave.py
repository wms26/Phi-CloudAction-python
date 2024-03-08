# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from PhiCloudLib.BuildGameSave import BuildGameKey, BuildGameProgress, BuildGameRecord, BuildGameSettings, BuildGameUser
from PhiCloudLib.ActionLib import zipGameSave, encryptGameSave
from PhiCloudLib.CloudAction import uploadSave
from json import loads

# ---------------------- 定义赋值区喵 ----------------------

sessionToken = ''

# ----------------------- 运行区喵 -----------------------

with open('./PhigrosSave.json', 'r', encoding='utf-8') as saveFile:
    saveDict: dict = loads(saveFile.read())
    for i in saveDict.keys():
        print(i, ':', saveDict[i])
    BuildGameKey(saveDict)
    BuildGameProgress(saveDict)
    BuildGameRecord(saveDict)
    BuildGameSettings(saveDict)
    BuildGameUser(saveDict)
    encryptGameSave(saveDict)

print('\n')
for i in saveDict.keys():
    print(i, ':', saveDict[i])
uploadSave(sessionToken, zipGameSave(saveDict))
