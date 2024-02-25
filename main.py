from PhiCloudLib.ParseGameSave import ParseGameKey, ParseGameProgress, ParseGameRecord, ParseGameSettings, ParseGameUser
from PhiCloudLib.ActionLib import readGameSave, readDifficulty, getB19
from PhiCloudLib.CloudAction import getPlayerId, getSummary, getSave
from PhiCloudLib.AES import decrypt
from argparse import ArgumentParser
from json import dumps

args_main = ArgumentParser(description='Phi-CloudAction-python v1.0',
                           usage='[-h] [-s sessionToken] [-p] [-m] [-e] [-r] [-t] [-u] [-g] [-b19] [-o output]',
                           add_help=False)
args_tree = args_main.add_argument_group(title='参数用法喵')
args_tree.add_argument('-h', '--help', action='help', help="显示本帮助信息并退出喵")
args_tree.add_argument('-s', '--session', type=str, default='', metavar='', help="Phigros的云存档sessionToken喵")
args_tree.add_argument('-p', '--playerId', action='store_true', help='获取玩家昵称喵')
args_tree.add_argument('-m', '--summary', action='store_true', help='获取云存档summary喵(不使用-o则打印至控制台喵)')
args_tree.add_argument('-e', '--progress', action='store_true', help='获取存档进度信息喵(不使用-o则打印至控制台喵)')
args_tree.add_argument('-r', '--record', action='store_true', help='获取存档所有成绩记录喵，需要difficulty.tsv喵(不使用-o则打印至控制台喵)')
args_tree.add_argument('-t', '--settings', action='store_true', help='获取存档设置信息喵(不使用-o则打印至控制台喵)')
args_tree.add_argument('-u', '--user', action='store_true', help='获取存档玩家信息喵(不使用-o则打印至控制台喵)')
args_tree.add_argument('-g', '--getSave', action='store_true', help='获取存档数据喵，需要difficulty.tsv喵(不使用-o则打印至控制台喵)')
args_tree.add_argument('-b19', '--getB19', action='store_true', help='获取存档的b19数据喵，需要difficulty.tsv喵(不使用-o则打印至控制台喵)')
args_tree.add_argument('-o', '--output', type=str, default='', metavar='', help='输出文件路径喵(带文件名及后缀喵)')
args = args_main.parse_args()
if args.playerId:
    print(getPlayerId(args.session))
if args.summary:
    summary = getSummary(args.session)
    if args.output == '' or args.output is None:
        print(summary)
    else:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(dumps(summary, ensure_ascii=False, indent=4))
if args.progress:
    summary = getSummary(args.session)
    progress = ParseGameProgress(decrypt(readGameSave(getSave(summary['url'], summary['checksum']), 'gameProgress'))).getData()
    if args.output == '' or args.output is None:
        print(progress)
    else:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(dumps(progress, ensure_ascii=False, indent=4))
if args.record:
    difficulty = readDifficulty('./difficulty.tsv')
    summary = getSummary(args.session)
    record = ParseGameRecord(decrypt(readGameSave(getSave(summary['url'], summary['checksum']), 'gameRecord')), difficulty).getData()
    if args.output == '' or args.output is None:
        print(record)
    else:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(dumps(record, ensure_ascii=False, indent=4))
if args.settings:
    summary = getSummary(args.session)
    settings = (ParseGameSettings(decrypt(readGameSave(getSave(summary['url'], summary['checksum']), 'settings'))).getData())
    if args.output == '' or args.output is None:
        print(settings)
    else:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(dumps(settings, ensure_ascii=False, indent=4))
if args.user:
    summary = getSummary(args.session)
    user = ParseGameUser(decrypt(readGameSave(getSave(summary['url'], summary['checksum']), 'user'))).getData()
    if args.output == '' or args.output is None:
        print(user)
    else:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(dumps(user, ensure_ascii=False, indent=4))
if args.getSave:
    difficulty = readDifficulty('./difficulty.tsv')
    summary = getSummary(args.session)
    save = getSave(summary['url'], summary['checksum'])
    saveData = {
        'user': ParseGameUser(decrypt(readGameSave(save, 'user'))).getData(),
        'setting': ParseGameSettings(decrypt(readGameSave(save, 'settings'))).getData(),
        'progress': ParseGameProgress(decrypt(readGameSave(save, 'gameProgress'))).getData(),
        'record': ParseGameRecord(decrypt(readGameSave(save, 'gameRecord')), difficulty).getData(),
        'key': ParseGameKey(decrypt(readGameSave(save, 'gameKey'))).getData()
    }
    if args.output == '' or args.output is None:
        print(saveData)
    else:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(dumps(saveData, ensure_ascii=False, indent=4))
if args.getB19:
    difficulty = readDifficulty('./difficulty.tsv')
    summary = getSummary(args.session)
    b19 = getB19(ParseGameRecord(decrypt(readGameSave(getSave(summary['url'], summary['checksum']), 'gameRecord')), difficulty).getData())
    if args.output == '' or args.output is None:
        print(b19)
    else:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(dumps(b19, ensure_ascii=False, indent=4))
