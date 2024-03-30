<div align="center">
<h1>Phi-CloudAction-python</h1>
使用python实现的phigros云端数据操作喵<br>
注意本项目已经猫化了喵，带有大量喵元素喵，介意者勿用喵！<br><br>

[![Github仓库喵](https://img.shields.io/badge/github-Phi--CA--py-red?style=for-the-badge&logo=Github)](https://github.com/wms26/Phi-CloudAction-python)

<img src="https://counter.seku.su/cmoe?name=phi-cloud-py&theme=r34" title="喵喵喵~"/><br>

[![Phi-LocalAction-python](https://img.shields.io/badge/Github-LocalAction(本地数据操作)-red?style=for-the-badge&logo=Github)](https://github.com/wms26/Phi-LocalAction-python)


[![PhigrosLibrary](https://img.shields.io/badge/文酱-Phigros_Library-blue?style=for-the-badge&logo=Github)](https://github.com/7aGiven/PhigrosLibrary)
[![phi-plugin](https://img.shields.io/badge/废酱-phi--plugin-blue?style=for-the-badge&logo=github)](https://github.com/Catrong/phi-plugin)


[![Phi-CloudAction-pyinstaller_v1.0](https://img.shields.io/badge/Lasest--release-Phi--CloudAction--pyinstaller__v1.0-green?style=for-the-badge&logo=Github)](https://github.com/wms26/Phi-CloudAction-python/releases/download/v1.0-kawaii/Phi-CloudAction-pyinstaller_v1.0.kawaii.exe)
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

### 安装pycryptodome库和requests库和flask库喵：

直接在命令行运行喵：

```
pip install pycryptodome requests flask
```

或者如果想要一点仪式感也可以运行喵：

```
pip install -r PhiCloudLib/requirement.txt
```

### 各函数功能使用方法喵：

看`example.py`吧喵，里面写了一个示例，几乎用上了所有功能，看注释理论上都能理解怎么用了罢~

### 关于WebApi喵：

看Web_api.py里面就好啦喵，注释不多喵(因为懒喵)

Web_example.py是一个POST请求调用示例喵，GET请求不用使用RSA喵

#### POST：
1. 需要/api/bind_key获取RSA公钥喵，注意是可以重复请求获取新的公钥的喵，私钥会在服务器自动与请求IP绑定喵，可以请求一次后重复使用喵(注意这个绑定信息是以变量形式存储的喵，服务端重新启动后会失效喵)
2. 请求各api时都需要将sessionToken经过加密处理后提交喵，可参考Web_example.py喵，注意在加密前还需要调用gen_data()来对sessionToken进行“混淆处理”喵(其实原理很好懂的喵，知道了原理谁都可以解出来喵，所以才要RSA喵，只是一个本喵突发奇想搓出来的对称加密罢了喵)
3. 注意sessionToken是先用gen_data()进行“混淆”喵，然后进行RSA加密喵，然后base64编码才提交的喵
4. POST请求返回的数据都是{"code"=xx, "massage"=xxx...}格式喵，code=0就是成功喵，http状态码是200喵，内容在massage里面喵，如果不是0就是出问题了喵，状态码是403喵，一般massage会说大致讲是什么问题喵
5. 当出现未定义的错误时会返回{"code"=10, "massage"="Server error"}喵，状态码是500喵，此时服务端控制台会输出错误关键信息喵，比较具体错误信息会写入到ErrorLog/20xx-xx-xx_error.log里面喵喵

#### GET：
1. GET请求不使用RSA喵，请求参数用token=xxx...喵，参数的值是sessionToken经过base64编码后去除尾部的等于号喵，在前面用一个数字表示有几个等于号喵(比如编码后尾部有两个等于号喵，删掉后在头部加一个数字2喵喵，没有等于号就加0喵)
2. GET请求返回的数据不像POST请求一样喵，在成功时不返回code喵，http状态码是200喵，直接返回数据喵(比如getPlayerId就只返回一个玩家昵称喵)，当出现错误时则会返回类似"Errorx：xxx..."的内容喵，Error后面会跟code喵，状态码是403喵
3. 当出现未定义错误时返回的数据以及情况与POST一样喵

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
    - [ ] WebGUI(可视化存档信息喵，感觉也没用喵，先咕咕咕吧喵)
    - [ ] Bot(还是咕咕咕喵！)

## 喵喵喵~

此项目云端操作的思路源于[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)喵(本文档前面也留了链接喵)

喵！小小宣传一下[废酱](https://github.com/Catrong)的项目[Phi-Plugin](https://github.com/catrong/phi-plugin)，是一个适用于`Yunzai-Bot V3`的`Phigros`辅助插件喵！(本文档前面也留了链接喵)

介于本喵懒惰的性格喵，本项目也许应该可能大概会在未来也可能在现在某个时间突然停更或者消失喵(bushi)

(小声BB：我也不知道我为什么要写云端数据操作的python实现喵，就当是消遣吧喵。想专门搞这方面的大佬还是移步到[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)吧喵)

(快去给[文酱](https://github.com/7aGiven)和[废酱](https://github.com/Catrong)的项目点star喵！)