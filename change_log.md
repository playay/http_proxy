

###1.1 (2017-11-26)      
时隔两三年，已经不是在校生了。从一个工作两年的工程师的角度来看，这工程质量实在是不行啊。好在功能还是能用的。在Ubuntu 服务器上安装了一遍，更新了文档，更新了依赖库的版本，让程序可用。再过两三个月过春节，那时候准备重构下，让它从“程序”进化成“工程”吧（写了三年java，其实并不知道python的工程怎么样算是好的实践额。）   

为了ipad 能正常上网，又搞起了 http 代理。。最早是为了什么来着？好像是大学生创建项目，为了在外网能爬校内的网站。。

###1.0
+ 支持CONNECT方法（支持https等）
+ 按协议规定，替换对应的报文头信息

###0.6
+ 实现多进程！！！
+ 修复response为空时，不退出接收的死循环，gevent一直切换回来，导致的cpu使用率100%的bug（腾讯首页就有这种response,可能是想长连接）

###0.5
+ 使用单进程单线程的gevent提高性能
+ 可怕的腾讯首页。。

###0.4
+ 支持HEAD请求   
+ 确认支持204,206,303,307,413,414,500,501,505响应   
+ 已经能正常浏览http网页（常见的还有CONNECT方法未支持，应该是在https中用到；连着多打开几个可怕的门户网站首页:内存11M，（cpu单核100%，因为有长连接，recv()到的是空的，gevent会一直切换回来等待接收到数据））

###0.3
+ 修改请求的接收方式，支持post请求
+ 确认支持201,503,404,301,302响应

###0.2 
+ 正确完善http响应报文已接收完的判断方式，已经能正常代理响应为200,304的get和post请求。   
+ 连接接目标主机失败（原因是类似目标网站的服务器压根没开。。之类的），返回自定义的错误信息   
+ 200的通过Content-Length, Transfer-Encoding判断。都没有的默认Transfer-Encoding。   
+ 304的是not modify，直接返回报文头   
+ 404的响应也行，只是在收完报文头就直接返回了，还没有管它收完了没，正常的404报文如果够短的话是没问题的。   

###0.1.1
+ 增加http响应报文已接收完的判断方式，至少校内办公可用了   


###0.1
+ 实现基本功能，能解析get和post请求，并转发请求报文给目标主机，收到响应报文后转回给请求方   
+ 主线程接收请求，把分配的socket传给代理线程；代理线程转发请求报文和响应报文   
+ 性能极烂！！请求一多（只是打开一个大网页）cpu占用率就爆满。原因是，来一个请求，分配一个socket时，每个socket都启动一个新线程。而且判断响应报文是否接收完整的方式不对，会在接收响应报文时无限循环   
+ 不知如何判断http响应报文已接收完   

