#http_proxy.py
python socket 实现的http代理   
多进程&&协程   

##依赖库(gevent)
http://git.oschina.net/chenyanclyz/httpproxy/blob/master/lib/gevent-1.0.1.tar.gz    
解压 `tar -zxvf xxx.tar.gz`   
编译 `python setup.py build`   
复制编译后的文件到系统环境 `sudo python setup.py install`    

##目录说明
bin/ 程序的可执行文件，及使用说明   
lib/ 第三方库的安装包   
protocol/ http协议的相关文档   

##TODO
####性能优化
+ 客户端取消请求后，及时结束任务   

####协议支持
+ 尝试Connection  keep-alive   
+ 完善对http请求的各种method的支持（已测试通过：GET,POST,HEAD)   
+ 添加https支持   

##更新日志
http://git.oschina.net/chenyanclyz/httpproxy/blob/master/change_log.md
