#coding:utf-8

import sys,os

with open(sys.path[0]+'/pid','r') as f:
    pid_list = f.read().split('|')

for pid in pid_list:
    if pid:
        os.system('kill '+pid)
        print('stop process '+pid+' ok')
    else:
        print('nothing to stop')
with open(sys.path[0]+'/pid','w') as f:
    f.truncate()
