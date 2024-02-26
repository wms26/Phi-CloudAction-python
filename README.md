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

4. 获取存档打歌记录数据的过程会计算每首歌每个难度的rks喵，所以需要难度定数文件`difficulty.tsv`喵，本项目仓库里面已经有了喵，但不一定是最新的，获取最新的难度定数文件可以用[文酱](https://github.com/7aGiven)的项目[Phigros_Resource](https://github.com/7aGiven/Phigros_Resource)哦喵！

## 使用喵！

### 安装pycryptodome库和requests库喵：

直接运行喵：(用`pip`也可以的亚子喵(?))

```
pip3 install pycryptodome requests
```

或者如果想要一点仪式感也可以运行喵：

```
pip3 install -r PhiCloudLib/requirement.txt
```

### 各函数功能使用方法喵：

看`example.py`吧喵，里面写了一个示例，几乎用上了所有功能，看注释理论上都能理解怎么用了罢~

## 未来计划功能喵！

- [x] **存档获取喵[CloudAction]**(已模块化喵)(注释较为完整喵)
  - [x] 通过sessionToken获取云存档喵
  - [x] 防呆措施喵(bushi)
  - [x] 下载存档时进行md5校验喵


- [x] **存档解析喵[ParseGameSave]**(已模块化喵)(注释较为完整喵)
  - [x] 解析输出所有内容喵


- [ ] **其他喵：**
    - [x] 获取本地SessionToken喵(点[**这里**](https://github.com/wms26/Phi-CloudAction-python/releases/tag/GST_v1.0)来下载喵)
    - [x] 获取summary和玩家昵称喵
    - [x] 计算b19喵！
    - [x] 将各功能模块化喵(更方便使用喵)

## 喵喵喵~

此项目云端操作的思路源于[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)喵(本文档前面也留了链接喵)

喵！小小宣传一下[废酱](https://github.com/Catrong)的项目[Phi-Plugin](https://github.com/catrong/phi-plugin)，是一个适用于`Yunzai-Bot V3`的`Phigros`辅助插件喵！(本文档前面也留了链接喵)

介于本喵懒惰的性格喵，本项目也许应该可能大概会在未来也可能在现在某个时间突然停更或者消失喵(bushi)

(小声BB：我也不知道我为什么要写云端数据操作的python实现喵，就当是消遣吧喵。想专门搞这方面的大佬还是移步到[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)吧喵)

(快去给[文酱](https://github.com/7aGiven)和[废酱](https://github.com/Catrong)的项目点star喵！)