<div align="center">
<h1>Phi-CloudAction-python</h1>
使用python实现的phigros云端数据操作喵<br>
注意本项目已经猫化了喵，带有大量喵元素喵，介意者勿用喵！<br><br>

[![Github仓库喵](https://img.shields.io/badge/github-Phi--CA--py-red?style=for-the-badge&logo=Github)](https://github.com/wms26/Phi-CloudAction-python)

<img src="https://counter.seku.su/cmoe?name=phi-cloud-py&theme=r34" title="喵喵喵~"/><br>

[![Phi-LocalAction-python](https://img.shields.io/badge/Github-LocalAction(本地数据操作)-red?style=for-the-badge&logo=Github)](https://github.com/wms26/Phi-LocalAction-python)

[![PhigrosLibrary](https://img.shields.io/badge/文酱-Phigros_Library-blue?style=for-the-badge&logo=Github)](https://github.com/7aGiven/PhigrosLibrary)
[![phi-plugin](https://img.shields.io/badge/废酱-phi--plugin-blue?style=for-the-badge&logo=github)](https://github.com/Catrong/phi-plugin)
[![Phigros_Resource](https://img.shields.io/badge/文酱-Phigros__Resource-blue?style=for-the-badge&logo=Github)](https://github.com/7aGiven/Phigros_Resource)

</div>

# 近期繁忙，本项目将会暂时停止更新喵（

## 声明喵：

**本项目仅作为学习参考用喵，请勿用作违法用途喵！(虽然我也想不到能做什么违法的事情就是了喵)**

**编写本项目所需的资料和资源均源于互联网收集喵(所以本人就是一个废物喵，什么都要依靠互联网喵(bushi))**

**本项目的初衷仅仅是为了供学习参考使用喵，本人从未想过要破坏音游圈的游戏平衡喵！**

**请勿尝试滥用本项目！已加检测，请不要试图做出任何商业行为！否则统一纳入黑名单！(此条声明可能与GPLv3许可证存在冲突，请以README.md中本声明为准！)**

**对于本项目本喵拥有最终解释权！请不要做出让任何一个音游玩家都会十分反感的事情！**

**如果你认为本项目不应该存在或者有其他问题，可以提交Issues或者发送邮件到qianqi26@616.sb，我时不时会去查看邮箱**

**Emmm...对于本项目有建议或者问题的请提交Issue谢谢喵~(提Issue方便往后其他有相同问题的人不会再问一遍喵)**

## 环境准备喵！

1. 编写本项目时使用的是 **python3.11.8** 的喵，不能完全保证其他版本会不会出现问题喵，推荐使用 **python>=3.9** 来运行喵~(后面换成3.11.8滴喵！)

2. 云端数据获取需要phigros的云端sessionToken，获取sessionToken的方法可以参考[**Mivik的bot说明文档**](https://mivik.moe/pgr-bot-help/)里面喵！也可以用本喵用pyinstaller打包好的[**GetSession**](https://github.com/wms26/Phi-CloudAction-python/releases/tag/QR-GST_v1.0)扫码登录来获取喵！也可以使用文酱的tomato部署的[**Phi-Login**](https://www.tomato-aoarasi.com/phi-login/)喵!

3. 获取存档打歌记录数据的过程会计算每首歌每个难度的rks喵，所以需要难度定数文件`difficulty.tsv`喵，本项目仓库里面已经有了喵，但不一定是最新的，获取最新的难度定数文件可以用[文酱](https://github.com/7aGiven)的项目[Phigros_Resource](https://github.com/7aGiven/Phigros_Resource)哦喵！

## 使用喵！

### 安装喵!

1. 查看[Releases](https://github.com/wms26/Phi-CloudAction-python/releases)喵
2. 查找最新版本的 `.whl` 文件喵
3. 复制链接并使用以下命令安装喵：
```bash
pip install <whl_url>
```

### 初始化喵!

```bash
python -m phi_cloud_action
```
会把``info``目录和``example``目录拷贝到运行目录下喵

### 各函数功能使用方法喵：

看``example``目录下的文件吧喵,用上了主要功能，看注释也许都能理解怎么用了罢喵~

## 未来计划功能喵！

- [x] **云端操作喵[CloudAction.py]**(已模块化喵)(注释较为完整喵)
  - [x] ~~获取玩家昵称喵~~
  - [x] ~~获取玩家summary并解析喵~~
  - [x] ~~刷新玩家sessionToken喵~~
  - [x] ~~获取玩家云存档喵~~
  - [x] ~~修改玩家云端昵称喵~~(但Phigros仅在登录Taptap时会同步一次昵称好像喵)
  - [x] ~~修改玩家summary喵~~(但只能看没有任何用喵)
  - [x] ~~获取存档时进行md5校验喵~~
  - [ ] ~~上传云存档~~(不计划实现)


- [x] **存档操作喵[Structure/*.py]**(已模块化喵)(注释较为完整喵)
  - [x] ~~云存档解密喵~~
  - [x] ~~根据云存档解析所有内容喵~~
  - [x] ~~根据解析内容构建云存档喵~~
  - [x] ~~结构化解析存档喵~~
  - [x] ~~支持旧版云存档喵~~(`gameKey`最低支持到`\x02`的文件头，`gameProgress`最低`\x03`喵)


- [ ] **其他喵：**
  - [x] ~~获取本地SessionToken喵~~(点[**这里**](https://github.com/wms26/Phi-CloudAction-python/releases/tag/GST_v1.1)来下载喵)
  - [x] ~~计算b19喵！~~
  - [x] ~~将各功能模块化喵~~(更方便使用喵)
  - [x] ~~存档历史记录~~(使用示例已经在`example.py`里面了喵，会检查存档是否有新记录喵，存在新记录时会进行保存存档和其他信息喵。往后可能会用上喵)
  - [x] ~~taptap扫码授权获取sessionToken~~(已经发在release中了喵，在[**这里**](https://github.com/wms26/Phi-CloudAction-python/releases/tag/QR-GST_v1.0)喵)
  - [ ] WebGUI(可视化存档信息喵，感觉也没用喵，先咕咕咕吧喵)
  - [ ] Bot(还是咕咕咕，预计可能开新仓库来写喵！)

## 喵喵喵~

此项目云端操作的思路源于[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)喵(本文档前面也留了链接喵)(快说“谢谢文酱！”)

喵！小小宣传一下[废酱](https://github.com/Catrong)的项目[Phi-Plugin](https://github.com/catrong/phi-plugin)，是一个适用于`Yunzai-Bot V3`的`Phigros`辅助插件喵！(本文档前面也留了链接喵)

介于本喵懒惰的性格和本项目的特殊性喵，本项目也许应该可能大概会在未来也可能在现在某个时间突然停更或者消失喵(bushi)

(小声BB：我也不知道我为什么要写云端数据操作的python实现喵，就当是消遣吧喵。想专门搞这方面的大佬还是移步到[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)吧喵)

(快去给[文酱](https://github.com/7aGiven)和[废酱](https://github.com/Catrong)的项目点star喵！)

## 更新日志喵：

### 2025/01/12(x1.4.2)：
1. 修复了写出的存档json数据在修改后，gameRecord中难度顺序更改导致成绩错误的问题
2. 修复了example.py中未计算等效rks的问题

### 2025/01/11(v1.4.1)：
1. 修改了部分注释以及函数注释 (请注意DataType.py里面的注释部分是AI生成后来修改的，可能描述不太规范)
2. 为Bits数据类型添加了长度限制 (emm可能有的人不太懂所以还是看代码吧，新增了_Bits类)
3. 基于Bits新增的功能上，修改了部分结构类的类型注释，防止在编辑存档时超出了有效Bit单位长度 (好吧可能越描述越糊了x)
4. 修改了下README.md

### 2025/01/05(v1.4.0)：
1. 重写大量代码，删除了之前发癫时添加的异步代码，修改了解析存档的逻辑，采用结构化解析方式，相关请看PhiCloudLib/Structure/
2. 修改了logger.py，在定义了日志输出编码为utf-8的同时也为全局错误捕获输出提供了支持
3. 修改部分旧函数名，稍微统一了一下函数命名与变量命名
4. 重写了函数注释，统一了注释格式
5. 优化了项目喵化时的语句逻辑，仅在句尾喵~

### 2025/01/01：
1. 更新一下难度文件，证明还活着
2. 最近事情比较多可能很难更新什么东西了

### 2024/10/03：
1. 总是看着右下角那个语言组成有那0.6%的Batchfile，所以为了看着舒服清理了一些无用文件（诶嘿~）

### 2024/09/28：
1. 文酱恢复更新[Phigros_Resource](https://github.com/7aGiven/Phigros_Resource)啦！

### 2024/08/31(v1.3.2)：
1. 鸽游在3.9.0更新了gameKey的结构，新增了两个键
2. 更新了3.9.0的定数文件(其实之前一直都有在更新，每次提交时都会把最新的定数提交上来)
3. 其他小更改

### 2024/08/24(v1.3.1)：
1. 新增了修改玩家昵称的函数
2. 鸽游更新了gameProgress的结构，新增了一个键
3. 其他小更改

### 2024/08/11(PhiQRCodeGetSession_v1.0)：
1. 新增了taptap扫码登录授权的方式获取sessionToken）
2. 更新了下README

### 2024/07/22：
1. 才发现上次更新不小心把`GPL`许可证整没了（

### 2024/07/20(v1.3.0)：
1. 重写全部代码，全部统一改为异步处理(虽然代码跟原来的大差不差)
2. 更正了一些函数的命名方式
3. 修改了一些代码结构，现在要请求云端数据推荐使用异步with
4. 代码将使用logging库输出(我还加上了colorlog库，带颜色的哦~)

### 2024/05/01(v1.2.6)：
1. 整理代码，对于新加的功能可能并没有过多去写注释，后面再补咕咕咕...
2. 增加了存档历史记录的功能，可用于绘制rks曲线图或者单曲成绩的曲线图之类的。
3. 给README.md增加了更新日志！
4. 为项目增加了`GNU GPLv3`许可证

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
