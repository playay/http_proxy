##你可能会这样试用...
1. `python http_proxy.py 8888` 运行代理，监听8888端口   
2. `ps -aux | grep http_proxy` 可以看到创建了与cpu核心数一样个数的进程   
3. `ls` 看到http_proxy.py的相同路径下生成了个`pid`文件； `cat pid` pid文件中保存着，创建的进程的进程号   
4. `ab -n 5000 -c 128 -Xlocalhost:8888 http://www.qq.com/` 用`apache2-utils`的ab工具进行压力测试    
5. `python stop.py` 关闭代理   
   
##其他
stop.py 通过相同路径下的pid文件中的进程号，关闭进程   
count.py 是协助输出调试信息的   
