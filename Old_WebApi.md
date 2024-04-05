Web_example_old.py是一个POST请求调用示例喵，GET请求不用使用RSA喵

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