# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from os.path import dirname, abspath, join, getsize  # 对路径的一些操作以及获取文件大小
from subprocess import Popen, PIPE  # 运行adb指令用的
from sys import exit as exti  # emm我也不知道为啥要这样子做（
from json import loads  # 用来解析.userdata喵
from sys import argv  # 获取传入的参数喵

# ---------------------- 定义赋值区 ----------------------

local_path = dirname(abspath(__file__))  # 获取当前脚本的绝对路径喵
adb_path = join(local_path, 'adb\\adb.exe')  # 将此模块绝对路径和adb路径拼接为adb的绝对路径喵，adb安卓调试桥的路径喵
userdata_minsize = 1 * 1024  # 正确userdata大小的最小阈值喵(乘1024是因为os库获取到的以字节为单位喵)
userdata_name = '.userdata'  # userdata文件的文件名
userdata_path = f'/sdcard/Android/data/com.PigeonGames.Phigros/files/{userdata_name}'  # userdata在手机中的路径
userdata_out = join(local_path, '.userdata')  # 拼接userdata文件输出路径


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
    print('[Info]注意喵！获取phigros的sessionToken需要先获取.userdata喵！')
    print('[Info]注意喵！获取.userdata需要使用adb调试喵！')
    print('[Info]请先在手机上进入"开发者模式"喵！打开"USB调试"后用数据线将手机连接到电脑喵(平板也一样喵！)')
    print('[Info]如果在手机上弹出USB调试确认喵，请点击同意喵！')
    adbCheck()  # 检查adb是否正确连接
    print(f'[Info]正在提取手机Phigros的userdata喵，路径喵："{userdata_path}"')
    print(runCmd(f'{adb_path} pull {userdata_path} {userdata_out}'))
    data_size = getsize(userdata_out)  # 获取提取出来的.userdata文件大小
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


# ----------------------- 运行区 -----------------------

if len(argv) >= 2 and argv[1].lower() == 'noget':  # 我也不知道为什么要留一个用来跳过提取userdata的参数喵(也许会有人用吧喵)
    userdata_path = './.userdata'
elif len(argv) >= 2 and argv[1].lower() == 'fuckadb':
    fuck_adb()  # 关掉adb
    exti(1)
else:
    userdata_path = get_userdata()  # "企图"获取userdata喵，保存为.userdata文件喵
    fuck_adb()  # 关掉adb
with open(userdata_path, mode='r', encoding='utf-8') as file:  # 打开.userdata喵
    data = loads(file.read())  # 读取并解析.userdata喵
    print(f'[Info]你的sessionToken喵：{data["sessionToken"]}')  # 输出sessionToken喵
