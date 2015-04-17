#http_proxy.py
python socket 实现的http(s)代理  
支持的方法:GET,POST,HEAD,CONNECT （其他的方法，没具体看协议的规定，所以没做）    
多进程&&协程&&短连接   


##依赖库(gevent)
[gevent-1.0.1.tar.gz](http://git.oschina.net/chenyanclyz/httpproxy/blob/master/lib/gevent-1.0.1.tar.gz)    
1. 解压 `tar -zxvf xxx.tar.gz`   
2. 编译 `python setup.py build`   
3. 复制编译后的文件到系统环境 `sudo python setup.py install`    


##目录说明
+ bin/ 程序的可执行文件，及使用说明   
+ lib/ 第三方库的安装包   
+ protocol/ http协议的相关文档   

##TODO
连接代理时验证用户名密码
tunnel_fail的信息还不知道该返回什么

##更新日志
http://git.oschina.net/chenyanclyz/httpproxy/blob/master/change_log.md
