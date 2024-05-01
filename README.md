<div align="center">
<h1>Phi-CloudAction-python</h1>
使用python实现的phigros云端数据操作喵<br>
注意本项目已经猫化了喵，带有大量喵元素喵，介意者勿用喵！<br><br>

[![Github仓库喵](https://img.shields.io/badge/github-Phi--CA--py-red?style=for-the-badge&logo=Github)](https://github.com/wms26/Phi-CloudAction-python)

<img src="https://counter.seku.su/cmoe?name=phi-cloud-py&theme=r34" title="喵喵喵~"/><br>

[![Phi-LocalAction-python](https://img.shields.io/badge/Github-LocalAction(本地数据操作)-red?style=for-the-badge&logo=Github)](https://github.com/wms26/Phi-LocalAction-python)


[![PhigrosLibrary](https://img.shields.io/badge/文酱-Phigros_Library-blue?style=for-the-badge&logo=Github)](https://github.com/7aGiven/PhigrosLibrary)
[![phi-plugin](https://img.shields.io/badge/废酱-phi--plugin-blue?style=for-the-badge&logo=github)](https://github.com/Catrong/phi-plugin)
[![Phigros_Resource](https://img.shields.io/badge/烧饼-Phigros__Resource-blue?style=for-the-badge&logo=Github)](https://github.com/3035936740/Phigros_Resource)

</div>

# 开学了喵，本项目将会保持极低频率的更新喵（

## 声明喵：

本项目仅作为学习参考用喵，请勿用作违法用途喵！(虽然我也想不到能做什么违法的事情就是了喵)

编写本项目所需的资料和资源均源于互联网收集喵(所以本人就是一个废物喵，什么都要依靠互联网喵(bushi))

本项目的初衷仅仅是为了供学习参考使用喵，本人从未想过要破坏音游圈的游戏平衡喵！

## 环境准备喵！

1. 编写本项目时使用的是 **python3.11.8** 的喵，不能完全保证其他版本会不会出现问题喵，建议使用 **python>=3.9** 来运行喵~(最近换成3.11.8滴喵！)

2. 注意在使用本项目前要先安装`PhiCloudLib/requirement.txt`中的模块喵

3. 云端数据获取需要phigros的云端sessionToken，获取sessionToken的方法可以参考[**Mivik的bot说明文档**](https://mivik.moe/pgr-bot-help/)里面喵！也可以用本喵用pyinstaller打包好的[**GetSession**](https://github.com/wms26/Phi-CloudAction-python/releases/tag/GST_v1.0)来获取喵！

4. 获取存档打歌记录数据的过程会计算每首歌每个难度的rks喵，所以需要难度定数文件`difficulty.tsv`喵，本项目仓库里面已经有了喵，但不一定是最新的，获取最新的难度定数文件可以用[烧饼](https://github.com/3035936740)的项目[Phigros_Resource](https://github.com/3035936740/Phigros_Resource)哦喵！

## 使用喵！

### 安装pycryptodome库和requests库和喵：

直接在命令行运行喵：

```
pip install pycryptodome requests
```

或者如果想要一点仪式感也可以运行喵：

```
pip install -r PhiCloudLib/requirement.txt
```

### 各函数功能使用方法喵：

看`example.py`吧喵，里面写了一个示例，几乎用上了所有功能，看注释理论上都能理解怎么用了罢~

### 关于WebApi喵：

使用WebApi前请先安装Flask库喵：

```
pip install flask
```

看Web_api.py里面就好啦喵，注释不多喵(因为懒喵)，Web_example.py是一个POST请求调用示例喵

注意两个脚本中都提供了一个`reqData_encrypt`选项来决定是否要使用本喵闲着没事搓出来没什么用的“混淆处理”来传输sessionToken，默认是False，就是明文传输(虽然“混淆”后的也差不多算是明文了)

#### POST：
1. 请求各api时都需要将sessionToken经过处理后提交喵，可参考Web_example.py喵，调用了gen_data()进行"混淆处理"后再用gen_base64()输出特殊的base64
2. POST请求返回的数据都是{"code"=xx, "massage"=xxx...}格式喵，code=0就是成功喵，http状态码是200喵，内容在massage里面喵，如果不是0就是出问题了喵，状态码是403喵，一般massage会说大致讲是什么问题喵
3. 当出现未定义的错误时会返回{"code"=10, "massage"="Server error"}喵，状态码是500喵，此时服务端控制台会输出错误关键信息喵，比较具体错误信息会写入到ErrorLog/20xx-xx-xx_error.log里面喵喵

#### GET：
1. GET请求参数用token=xxx...喵，参数的值是sessionToken经过特殊处理的base64编码数据，就是base64编码后去除尾部的等于号喵，在前面用一个数字表示有几个等于号喵(比如编码后尾部有两个等于号喵，删掉后在头部加一个数字2喵喵，没有等于号就加0喵)(直接调用Web_example.py的gen_base64()也是一样的)
2. GET请求返回的数据不像POST请求一样喵，在成功时不返回code喵，http状态码是200喵，直接返回数据喵(比如getPlayerId就只返回一个玩家昵称喵)，当出现错误时则会返回类似"Errorx：xxx..."的内容喵，Error后面会跟code喵，状态码是403喵
3. 当出现未定义错误时返回的数据以及情况与POST一样喵

#### 如果想要找旧的WebApi大致的使用方法的话，请看[旧WebApi文档](./Old_WebApi.md)

> WenApi以及示例并没有进行严格验证，请不要使用在正式环境，并且并没有优化过代码结构，可以说是屎山代码，估计很难懂可能

> **注意：** WebApi仅仅是本喵闲着没事写的，没有什么技术含量，可能存在安全问题，部署到服务器上需谨慎！

## 未来计划功能喵！

- [x] **存档获取喵[CloudAction]**(已模块化喵)(注释较为完整喵)
  - [x] ~~通过sessionToken获取云存档喵~~
  - [x] ~~防呆措施喵~~(bushi)
  - [x] ~~下载存档时进行md5校验喵~~


- [x] **存档解析喵[ParseGameSave]**(已模块化喵)(注释较为完整喵)
  - [x] ~~解析输出所有内容喵~~


- [ ] **其他喵：**
    - [x] ~~获取本地SessionToken喵~~(点[**这里**](https://github.com/wms26/Phi-CloudAction-python/releases/tag/GST_v1.0)来下载喵)
    - [x] ~~获取summary和玩家昵称喵~~
    - [x] ~~计算b19喵！~~
    - [x] ~~将各功能模块化喵~~(更方便使用喵)
    - [x] ~~WebApi~~(没什么用喵，建议别用喵，不能保证安全喵)
    - [x] ~~存档历史记录~~(使用示例已经在`example.py`里面了喵，会检查存档是否有新记录喵，存在新记录时会进行保存存档和其他信息喵。往后可能会用上喵)
    - [ ] WebGUI(可视化存档信息喵，感觉也没用喵，先咕咕咕吧喵)
    - [ ] Bot(还是咕咕咕喵！)

## 喵喵喵~

此项目云端操作的思路源于[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)喵(本文档前面也留了链接喵)

喵！小小宣传一下[废酱](https://github.com/Catrong)的项目[Phi-Plugin](https://github.com/catrong/phi-plugin)，是一个适用于`Yunzai-Bot V3`的`Phigros`辅助插件喵！(本文档前面也留了链接喵)

介于本喵懒惰的性格喵，本项目也许应该可能大概会在未来也可能在现在某个时间突然停更或者消失喵(bushi)

(小声BB：我也不知道我为什么要写云端数据操作的python实现喵，就当是消遣吧喵。想专门搞这方面的大佬还是移步到[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)吧喵)

(快去给[文酱](https://github.com/7aGiven)和[废酱](https://github.com/Catrong)的项目点star喵！)

## 更新日志喵：

### 2024/05/01(v1.2.6)：
1. 整理代码，对于新加的功能可能并没有过多去写注释，后面再补咕咕咕...
2. 增加了存档历史记录的功能，可用于绘制rks曲线图或者单曲成绩的曲线图之类的。
3. 给README.md增加了更新日志！

### 2024/04/05(v1.2.5-v1.2.5b)：
1. 新增了对解析存档时传入数据的类型检查
2. 调换了解析record传参的顺序(感觉之前那个顺序有点不人性化，前后换了个位置顺眼多了)
3. 修复了refreshSessionToken不能使用报错的问题(其实就是一个请求方法不对的问题，把get改成put就不会404了)
4. 修正了部分注释(感觉注释还是有一些容易被误解的地方，本喵是个fw不会写注释，希望还是先看example.py的例子吧，防止误解)
5. 重写了webapi，把加密去掉了，但是提供了一个选项来决定要不要使用本喵闲着没事搓出来没什么用的“混淆处理”进行提交token，默认没有开(旧的用“old”标记了)
6. 更新了README.md并将旧的WebApi文档单独分到Old_WebApi.md中(什么时候才能记得把readme一起改了然后提交上来而不是每次都提交完了才想起来然后改完再提交)
7. 我是傻逼忘记提交Old_WebApi.md了

### 2024/03/30(v1.2.4-v1.2.4a)：
1. 新增了WebApi，可以自行架个小服务器跑Web_api.py(GPT说建议用gunicorn跑，不懂百度)
2. 没有什么好更的了（
3. 好的刚刚忘记把index.html提交上来了，是个十分简单的api介绍页，请结合readme食用

### 2024/03/08(v1.2.3)：
1. 修复了在获取打歌记录时存在旧谱记录或者其他无定数的难度时报错的问题
2. 修复了在获取b19时没有AP过歌时报错的问题(不会吧真的还有人没有AP过嘛)
3. 将序列化反序列化存档全部一致改为字典传址
4. 更新添加修改了一些注释

### 2024/02/29(v1.2.2)：
1. 在example.py中增加了上传存档等功能的示例与逻辑注释

### 2024/02/27(v1.2.1)：
1. 原仓库的作者文酱放弃维护了，之后烧饼接手了这个项目捏，好耶！
2. 修改了CloudAction的一点逻辑代码，也许看起来没有这么*(shi)了？
3. 将GetSession打包用的脚本分为两个脚本(单文件打包和多文件打包)
4. 更新了一下示例脚本example.py
5. 乱七八糟优化了点代码）

### 2024/02/26(v1.2)：
1. 将获取存档和上传存档写了两个调用脚本示例
2. 稍微改了一点东西，无伤大雅

### 2024/02/25(v1.1-v1.1.8)：
1. 增加了三个云端操作：上传存档和上传summary以及刷新sessionToken
2. 将云存档各api接口单独写为一个CloudLib，更方便调用(也更难懂了)
3. 修改了一下反序列化和序列化存档的代码，把几个以二进制表示信息的键展开为列表来表示，便于理解阅读的同时也不影响序列化存档
4. 给getSave增加了验证md5校验值和验证存档大小的代码，在校验失败和存档过小时输出警告并等待5秒
5. 将release里面pyinstaller编译打包的主脚本开源(main.py)
6. 修改了main.py的小部分代码，以适配getSave需要checksum进行md5校验的要求
7. 刚刚更新忘记把pyinstaller编译打包时要用的UPX一起上传了）
8. 把GetSession一起上传了）

### 2024/02/18(v1.0)：
1. 写了大部分功能喵，目前只有存档读取操作是最完善的喵，其他功能请自行琢磨喵
2. 闲着没事把项目大部分内容喵化了（
3. 将另一个本地数据操作的项目Phi-LocalAction-python里面的获取sessionToken独立了出来
4. 添加了README.md和requirement.txt喵！
5. 更新README.md