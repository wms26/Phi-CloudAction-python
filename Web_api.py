from base64 import b64decode, b64encode
from datetime import datetime
from os import mkdir
from os.path import exists
from re import match
from traceback import format_exc

from flask import Flask, request, jsonify, send_from_directory

from PhiCloudLib.ActionLib import check_sessionToken, readDifficulty, readGameSave, decryptGameSave, unzipSave, decrypt, \
    getB19
from PhiCloudLib.ByteReader import ByteReader
from PhiCloudLib.CloudAction import getPlayerId, getSummary, getSave, refreshSessionToken
from PhiCloudLib.ParseGameSave import ParseGameUser, ParseGameProgress, ParseGameSettings, ParseGameKey, ParseGameRecord

app = Flask(__name__)

reqData_encrypt = False  # 用于声明请求的数据是否使用本喵自己搓的“特殊混淆处理”


def out_ErrorLog(req=None, *args):  # 输出错误日志
    nowDate = datetime.now().strftime('%Y-%m-%d')
    if not exists('ErrorLog'):  # 如果错误日志目录不存在则创建
        mkdir('ErrorLog')

    with open(f'ErrorLog/{nowDate}_error.log', 'a', encoding='utf-8') as f:  # 写入错误日志
        f.write(f'[{datetime.now().strftime("%H:%M:%S")}]发生错误：\n')
        if req:
            f.write(f'请求方法：{req.method}\n')
            f.write(f'请求IP：{req.remote_addr}\n')
            req_headers = req.headers
            f.write(f'请求头：\n')
            for key, value in req_headers.items():
                f.write(f'{key}: {value}\n')

            if req.method == 'POST':
                f.write(f'请求数据：{req.data.decode()}\n')

            elif req.method == 'GET':
                f.write(f'请求参数：{req.args}\n')

        f.write('错误信息：\n')
        for data in args:
            if type(data) is not str:
                data = str(data)
            f.write(f'{data}\n')
        f.write('\n')


def check_req(req):  # 检查请求合法性
    if req.method == 'POST':
        if reqData_encrypt:
            try:  # 检查token是否正确
                req_data = par_data(par_base64(req.data.decode()).encode())
            except Exception:
                trace_info = format_exc()
                print(trace_info)
                return 3, 'Invalid token in request'

        else:
            req_data = req.data.decode()

        if not req_data:  # 检查请求数据是否为空
            return 2, 'Missing request data'

        if not check_sessionToken(req_data, False):  # 检查sessionToken合法性
            return 3, 'Invalid token in request'

        return 0, req_data

    elif req.method == 'GET':
        try:  # 检查token是否正确
            req_data = par_base64(request.args.get('token'))
        except Exception:
            trace_info = format_exc()
            print(trace_info)
            return 3, 'Error3:Invalid token in request'

        if not req_data:  # 检查请求数据是否为空
            return 2, 'Error2:Missing request data'

        if not check_sessionToken(req_data, False):  # 检查sessionToken合法性
            return 3, 'Error3:Invalid token in request'

        return 0, req_data

    else:
        return 9, 'Invalid request method'


def par_base64(data: str | bytes):
    # 解码特殊的base64
    if data is not None and match(r'^[0-9]', data):
        num: int = int(data[0])
        data: str = data[1:] + '=' * num
        return b64decode(data).decode()

    elif data is not None:
        return b64decode(data).decode()

    return None


def par_data(data: bytes):
    if data is not None:
        Reader = ByteReader(data)
        data_sum = Reader.getShort()
        data_dict: dict = {}
        for i in range(data_sum):
            key = Reader.getShort()
            data_dict[key] = Reader.getString()
        print(data_dict)
        parser_data = ''
        for i in sorted(data_dict.items()):
            parser_data = parser_data + i[1]
        print(parser_data)

        return parser_data

    else:
        return None


# 获取playerId
@app.route('/api/getPlayerId', methods=['GET', 'POST'])
def api_getPlayerId():
    try:
        if request.method == 'POST':
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return jsonify(code=check[0], massage=check[1]), 403

            return b64encode(str(dict(code=0, massage=getPlayerId(check[1]))).encode()), 200

        elif request.method == 'GET':
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return check[1], 403

            return str(getPlayerId(check[1])), 200

        else:
            return jsonify(code=9, massage='Invalid request method'), 403

    except Exception as e:
        trace_info = format_exc()
        print(trace_info)
        # print(e)
        out_ErrorLog(request, trace_info)
        return jsonify(code=10, massage='Server error'), 500


# 获取summary
@app.route('/api/getSummary', methods=['GET', 'POST'])
def api_getSummary():
    try:
        if request.method == 'POST':  # 如果为POST请求
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return jsonify(code=check[0], massage=check[1]), 403

            return b64encode(str(dict(code=0, massage=getSummary(check[1]))).encode()), 200

        elif request.method == 'GET':
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return check[1], 403

            return str(getSummary(check[1])), 200

        else:
            return jsonify(code=9, massage='Invalid request method'), 403

    except Exception as e:
        trace_info = format_exc()
        print(trace_info)
        # print(e)
        out_ErrorLog(request, trace_info)
        return jsonify(code=10, massage='Server error'), 500


# 获取存档解析字典数据
@app.route('/api/getSave', methods=['GET', 'POST'])
def api_getSave():
    try:
        if request.method == 'POST':
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return jsonify(code=check[0], massage=check[1]), 403

            difficulty = readDifficulty('./difficulty.tsv')
            summary = getSummary(check[1])
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

            return b64encode(str(dict(code=0, massage=saveDict)).encode()), 200

        elif request.method == 'GET':
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return check[1], 403

            difficulty = readDifficulty('./difficulty.tsv')
            summary = getSummary(check[1])
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

            return str(saveDict), 200

        else:
            return jsonify(code=9, massage='Invalid request method'), 403

    except Exception as e:
        trace_info = format_exc()
        print(trace_info)
        # print(e)
        out_ErrorLog(request, trace_info)
        return jsonify(code=10, massage='Server error'), 500


# 获取B19
@app.route('/api/getB19', methods=['GET', 'POST'])
def api_getB19():
    try:
        if request.method == 'POST':  # 如果为POST请求
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return jsonify(code=check[0], massage=check[1]), 403

            difficulty = readDifficulty('./difficulty.tsv')
            summary = getSummary(check[1])
            save = getSave(summary['url'], summary['checksum'])  # 获取存档数据喵

            # 读取并解密然后解析存档数据喵
            saveDict = {
                'record': decrypt(unzipSave(save, 'gameRecord'))
            }
            ParseGameRecord(saveDict, difficulty)

            return b64encode(str(dict(code=0, massage=getB19(saveDict['record']))).encode()), 200

        elif request.method == 'GET':
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return check[1], 403

            difficulty = readDifficulty('./difficulty.tsv')
            summary = getSummary(check[1])
            save = getSave(summary['url'], summary['checksum'])  # 获取存档数据喵

            # 读取并解密然后解析存档数据喵
            saveDict = {
                'record': decrypt(unzipSave(save, 'gameRecord'))
            }
            ParseGameRecord(saveDict, difficulty)

            return getB19(saveDict['record']), 200

        else:
            return jsonify(code=9, massage='Invalid request method'), 403

    except Exception as e:
        trace_info = format_exc()
        print(trace_info)
        # print(e)
        out_ErrorLog(request, trace_info)
        return jsonify(code=10, massage='Server error'), 500


@app.route('/api/getMoney', methods=['GET', 'POST'])
def api_getMoney():
    try:
        if request.method == 'POST':  # 如果为POST请求
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return jsonify(code=check[0], massage=check[1]), 403

            summary = getSummary(check[1])
            save = getSave(summary['url'], summary['checksum'])  # 获取存档数据喵

            # 读取并解密然后解析存档数据喵
            saveDict = {
                'progress': decrypt(unzipSave(save, 'gameProgress'))
            }
            ParseGameProgress(saveDict)

            return b64encode(str(dict(code=0, massage=saveDict['progress']['money'])).encode()), 200

        elif request.method == 'GET':
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return check[1], 403

            summary = getSummary(check[1])
            save = getSave(summary['url'], summary['checksum'])  # 获取存档数据喵

            # 读取并解密然后解析存档数据喵
            saveDict = {
                'progress': decrypt(unzipSave(save, 'gameProgress'))
            }
            ParseGameProgress(saveDict)

            return saveDict['progress']['money'], 200

        else:
            return jsonify(code=9, massage='Invalid request method'), 403

    except Exception as e:
        trace_info = format_exc()
        print(trace_info)
        # print(e)
        out_ErrorLog(request, trace_info)
        return jsonify(code=10, massage='Server error'), 500


# 刷新sessionToken
@app.route('/api/refreshToken', methods=['GET', 'POST'])
def api_refreshToken():
    try:
        if request.method == 'POST':  # 如果为POST请求
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return jsonify(code=check[0], massage=check[1]), 403

            return b64encode(str(dict(code=0, massage=refreshSessionToken(check[1]))).encode()), 200

        elif request.method == 'GET':
            check = check_req(request)  # 检查请求是否合法
            if check[0] != 0:
                return check[1], 403

            return str(refreshSessionToken(check[1])), 200

        else:
            return jsonify(code=9, massage='Invalid request method'), 403

    except Exception as e:
        trace_info = format_exc()
        print(trace_info)
        # print(e)
        out_ErrorLog(request, trace_info)
        return jsonify(code=10, massage='Server error'), 500


# API 介绍页面
@app.route('/', methods=['GET'])
def api_intro():
    return send_from_directory('', 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
