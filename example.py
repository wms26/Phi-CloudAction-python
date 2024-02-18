# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiCloudLib.CloudAction import getPlayerId, getSummary, getSave
from PhiCloudLib.AES import decrypt
from PhiCloudLib.ParseGameSave import ParseGameKey, ParseGameProgress, ParseGameRecord, ParseGameSettings, ParseGameUser
from PhiCloudLib.ActionLib import readGameSave, readDifficulty, getB19
import json

# ---------------------- 定义赋值区 ----------------------

sessionToken = 'm8xc5b7khmvsyp0nhqyin4llb'

# ----------------------- 运行区 -----------------------

difficulty = readDifficulty('./difficulty.tsv')  # 读取难度定数列表文件
print(getPlayerId(sessionToken))  # 获取玩家昵称
summary = getSummary(sessionToken)  # 获取summary
print(summary)

save = getSave(summary['url'])  # 获取存档数据

# 读取并解密然后解析存档数据
gameKey = ParseGameKey(decrypt(readGameSave(save, 'gameKey'))).getData()
gameProgress = ParseGameProgress(decrypt(readGameSave(save, 'gameProgress'))).getData()
gameRecord = ParseGameRecord(decrypt(readGameSave(save, 'gameRecord')), difficulty).getData()
settings = ParseGameSettings(decrypt(readGameSave(save, 'settings'))).getData()
user = ParseGameUser(decrypt(readGameSave(save, 'user'))).getData()

# 写出解析后所有的存档数据
with open('./PhigrosSave.json', 'w', encoding='utf-8') as savefile:
    saveData = {
        'user': user,
        'setting': settings,
        'progress': gameProgress,
        'record': gameRecord,
        'key': gameKey
    }
    savefile.write(json.dumps(saveData, ensure_ascii=False, indent=4))

b19 = getB19(gameRecord)  # 获取b19(准确来说是b20(?))
rks = 0  # 定义一个rks用于后续计算
for song in b19:  # 遍历b19列表
    rks += song['rks']  # 计算玩家rks
    print(song)  # 输出单条b19
print(rks / 20)  # 输出玩家rks
