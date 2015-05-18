#http_proxy.py
python socket 实现的http代理  
支持的方法:GET,POST,HEAD,CONNECT （其他的方法，没具体看协议的规定，所以没做）    
多进程&&协程&&短连接   

##依赖库(gevent)
[gevent-1.0.1.tar.gz](lib)    
1. 解压 `tar -zxvf xxx.tar.gz`   
2. 编译 `python setup.py build`   
3. 复制编译后的文件到系统环境 `sudo python setup.py install`    


##目录说明
+ bin/ 程序的可执行文件，及使用说明   
+ lib/ 第三方库的安装包   
+ protocol/ http协议的相关文档   

##TODO
+ python3的版本
+ 连接代理时验证用户名密码    
+ tunnel_fail的信息还不知道该返回什么    

##讲在后面
程序部署到阿里云的硅谷主机上，多数网站都能正常访问，但是很奇怪：    
1. `http://www.baidu.com`没有被自动跳转到`https://www.baidu.com`   
2. 访问`某管道`时，浏览器显示我的程序断开了连接，我的程序显示浏览器断开了连接。。（→_→ 猜猜是谁断了谁）    

毕竟http是明文的啊！就算访问的是https的网页，第一条报文`CONNECT`也是明文带着目标主机地址的！！（→_→ 我是这么猜的）   
在本地用ssh端口转发，建一个`本地端口`到`阿里云的代理端口`的隧道，试用一切正常(→_→ 所以我猜的应该是对的吧)    
不纠结、折腾这点了。。    

##更新日志
[change_log.md](change_log.md)
