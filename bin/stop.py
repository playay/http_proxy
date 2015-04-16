#coding:utf-8

import sys,os

with open(sys.path[0]+'/pid','r') as f:
    pid_list = f.read().split('|')

for pid in pid_list:
    os.system('kill '+pid)

with open(sys.path[0]+'/pid','w') as f:
    f.truncate()
    
print('stop process '+'|'.join(pid_list)+' ok')
