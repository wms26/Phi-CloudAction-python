# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from PhiCloudLib.BuildGameSave import BuildGameKey, BuildGameProgress, BuildGameRecord, BuildGameSettings, BuildGameUser
from PhiCloudLib.CloudAction import uploadSave
from PhiCloudLib.ActionLib import zipGameSave
from PhiCloudLib.AES import encrypt
from json import loads

# ---------------------- 定义赋值区喵 ----------------------

sessionToken = ''

# ----------------------- 运行区喵 -----------------------

with open('./PhigrosSave.json', 'r', encoding='utf-8') as saveFile:
    data = loads(saveFile.read())
    gameKey = encrypt(BuildGameKey(data['key']).getData())
    gameProgress = encrypt(BuildGameProgress(data['progress']).getData())
    gameRecord = encrypt(BuildGameRecord(data['record']).getData())
    settings = encrypt(BuildGameSettings(data['setting']).getData())
    user = encrypt(BuildGameUser(data['user']).getData())

uploadSave(sessionToken, zipGameSave(gameKey, gameProgress, gameRecord, settings, user))
