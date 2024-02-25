# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区喵 -----------------------
from PhiCloudLib.CloudAction import getPlayerId, getSummary, getSave
from PhiCloudLib.AES import decrypt
from PhiCloudLib.ParseGameSave import ParseGameKey, ParseGameProgress, ParseGameRecord, ParseGameSettings, ParseGameUser
from PhiCloudLib.ActionLib import readGameSave, readDifficulty, getB19
import json

# ---------------------- 定义赋值区喵 ----------------------

sessionToken = 'm8xc5b7khmvsyp0nhqyin4llb'

# ----------------------- 运行区喵 -----------------------

difficulty = readDifficulty('./difficulty.tsv')  # 读取难度定数列表文件喵
print(getPlayerId(sessionToken))  # 获取玩家昵称喵
summary = getSummary(sessionToken)  # 获取summary喵
print(summary)

save = getSave(summary['url'], summary['checksum'])  # 获取存档数据喵

# 读取并解密然后解析存档数据喵
gameKey = ParseGameKey(decrypt(readGameSave(save, 'gameKey'))).getData()
gameProgress = ParseGameProgress(decrypt(readGameSave(save, 'gameProgress'))).getData()
gameRecord = ParseGameRecord(decrypt(readGameSave(save, 'gameRecord')), difficulty).getData()
settings = ParseGameSettings(decrypt(readGameSave(save, 'settings'))).getData()
user = ParseGameUser(decrypt(readGameSave(save, 'user'))).getData()

# 写出解析后所有的存档数据喵
with open('./PhigrosSave.json', 'w', encoding='utf-8') as savefile:
    saveData = {
        'user': user,
        'setting': settings,
        'progress': gameProgress,
        'record': gameRecord,
        'key': gameKey
    }
    savefile.write(json.dumps(saveData, ensure_ascii=False, indent=4))

b19 = getB19(gameRecord)  # 获取b19喵(准确来说是b20喵(?))
rks = 0  # 定义一个rks用于后续计算喵
for song in b19:  # 遍历b19列表喵
    rks += song['rks']  # 计算玩家rks喵
    print(song)  # 输出单条b19喵
print(f'根据b19计算玩家的rks喵：{rks / 20}')  # 输出玩家rks喵
