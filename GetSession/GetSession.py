# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from GetPgrUserdata import get_userdata, runCmd, fuck_adb  # 用来获取userdata文件喵
from os.path import join, dirname, abspath
from sys import exit as exti
from json import loads  # 用来解析.userdata喵
from sys import argv  # 获取传入的参数喵

# ----------------------- 运行区 -----------------------

if len(argv) >= 2 and argv[1].lower() == 'noget':  # 我也不知道为什么要留一个用来跳过提取userdata的参数喵(也许会有人用吧喵)
    userdata_path = './.userdata'
elif len(argv) >= 2 and argv[1].lower() == 'fuckadb':
    fuck_adb()
    exti(1)
else:
    userdata_path = get_userdata()  # "企图"获取userdata喵，保存为.userdata文件喵
    fuck_adb()
with open(userdata_path, mode='r', encoding='utf-8') as file:  # 打开.userdata喵
    data = loads(file.read())  # 读取并解析.userdata喵
    print(f'[Info]你的sessionToken喵：{data["sessionToken"]}')  # 输出sessionToken喵
