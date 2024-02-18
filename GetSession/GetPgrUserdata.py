# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from os.path import dirname, abspath, join, getsize
from subprocess import Popen, PIPE
from sys import exit as exti

# ---------------------- 定义赋值区 ----------------------

local_path = dirname(abspath(__file__))  # 获取当前脚本的绝对路径喵
adb_path = join(local_path, 'adb\\adb.exe')  # 将此模块绝对路径和adb路径拼接为adb的绝对路径喵，adb安卓调试桥的路径喵
userdata_minsize = 1 * 1024  # 正确userdata大小的最小阈值喵(乘1024是因为os库获取到的以字节为单位喵)
userdata_name = '.userdata'
userdata_path = f'/sdcard/Android/data/com.PigeonGames.Phigros/files/{userdata_name}'
userdata_out = join(local_path, '.userdata')


def fuck_adb():
    runCmd(join(dirname(abspath(__file__)), 'adb\\adb.exe') + ' kill-server')


def runCmd(cmd, outerr=False, prerr=True):  # 运行命令并进行简单的判断和输出喵
    """运行cmd命令喵，可按需调整返回内容喵\n
    可用参数喵：\n
    cmd：要运行的命令喵\n
    outerr：是否返回错误内容喵\n
    prerr：是否打印错误到控制台喵"""
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)  # 运行命令喵
    out, err = process.communicate()  # 获取运行结果喵
    try:  # 先尝试使用utf-8解码喵(万恶的编码问题啊啊啊啊)
        output = out.decode('utf-8')
        error = err.decode('utf-8')
    except UnicodeDecodeError:  # 解码错误就换个编码再试喵
        output = out.decode('gbk')
        error = err.decode('gbk')
    if error != '':  # 如果错误不为空喵(不为空就是有错误喵)
        if prerr:  # prerr就是PrintError(打印错误)喵
            print("\n[Error]发生了错误喵：")
            print(error)  # 输出错误信息喵
        if outerr:  # outerr就是OutputError(输出错误)喵
            return error  # 返回错误以便进一步进行处理
        else:
            return None
    else:
        return output  # 没错误就输出执行结果喵


def adbCheck():
    """检查设备有没有正确连接adb\n
    doExit：检查到未正确连接是否直接exit(默认为True)"""
    runCmd(adb_path + ' devices', prerr=False)
    output = runCmd(adb_path + ' devices', outerr=True)
    try:
        if output is not None and '\tdevice' not in output:  # 判断关键字是否存在于输出内容中喵，不存在就证明没有连接adb喵
            if 'unauthorized' in output:
                fuck_adb()
                raise Exception('[Error]你没有允许本计算机对手机进行调试喵！')
            elif 'recovery' in output:
                fuck_adb()
                raise Exception('[Error]喵？你怎么在Recovery模式啊喵？请重启到系统先喵！')
            else:
                fuck_adb()
                raise Exception('[Error]没有任何设备连接到adb喵！')
    except Exception as e:
        print(e)
        exti(1)


def get_userdata():
    """使用adb获取phigros的.userdata"""
    adbCheck()
    print(f'[Info]正在提取手机Phigros的userdata喵，路径喵："{userdata_path}"')
    print(runCmd(f'{adb_path} pull {userdata_path} {userdata_out}'))
    data_size = getsize(userdata_out)
    try:
        if data_size <= userdata_minsize:
            print(
                f'[Error]获取到的.userdata大小不足{userdata_minsize / 1024}KB喵！仅有{data_size / 1024}KB喵！(共{data_size}字节喵)')
            fuck_adb()
            raise Exception('[Info]请再试几次喵，如果多次出现次错误请附带日志反馈喵！')
    except Exception as e:
        print(e)
        exti(1)
    print(f'[Info]提取完成喵！路径喵："{userdata_out}"')
    return userdata_out
