#coding:utf-8
#qpy:2
#qpy:console

import logging

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                #format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                #datefmt='%a, %d %b %Y %H:%M:%S',
                #filename='myapp.log',
                #filemode='w'
                )
                
import sys
import time
import socket
import thread
import urllib2


'''解析http请求头,返回（host, port, method, uri）'''
def paser_request_headers(request_headers):

    lines = request_headers.strip().split('\r\n')
    
    '''解析请求类型'''
    line0 = lines[0].split(' ')
    method = line0[0]
    uri = line0[1]
    #logging.debug(str(line0))
    
    '''解析其他header'''
    headers = {}
    for i in range(1,len(lines)):
        line= lines[i].split(':')
        key = line.pop(0)
        value = ''.join(line)
        headers[key] = value
        
    #logging.info(str(headers))
    '''处理目标主机和端口'''
    target_host_and_port = headers['Host'].strip().split(':')
    if len(target_host_and_port)==1:
        target_host = target_host_and_port[0]
        target_port = 80
    else:
        target_host = target_host_and_port[0]
        target_port = int(target_host_and_port[1].strip())
        
    return target_host, target_port, method, uri
    
    
    
def get_response(host, port, request):
    c = socket.socket()
    try:
        c.connect((host, port))
        c.send(request)
        response = ''
        while 1:
            buf = c.recv(1024)
            response = response + buf
            if not buf:
                break    
        logging.debug(response)
    except Exception, e:
        c.close()
        return str(type(e))+' '+str(e)+' err'
    c.close()
    
    return response


def proxyer(ss):
    logging.debug(ss)
    '''接收http请求'''
    request = ''
    while 1:
        buf = ss.recv(1024)
        request = request + buf
        if '\r\n\r\n' in request:
            break
    if not request:
        logging.warning('request empty,close this task')
        ss.close()
        return
    logging.debug('request length: '+str(len(request)))
    logging.debug('\n'+request)
    
    '''解析http请求，得到目标主机和端口''' 
    target_host, target_port, method, uri = paser_request_headers(request)
    if not target_host or not target_port or not method.upper() in ['GET','POST']:
        logging.warning('paser request waring('+
        target_host+':'+str(target_port)+' '+method
        +'): ,close this task')
        ss.close()
        return
    logging.info(target_host+':'+str(target_port)+' '+method+' '+uri)
        
    '''获取目标主机的http应答'''
    response = get_response(target_host, target_port, request)
    if not response or response.endswith(' err'):
        logging.warning('reponse err,close this task')
        logging.warning(response)
        ss.close()
        return
    logging.info(uri+' response length: '+str(len(response)))
    '''返回http应答'''
    ss.send(response)
    #ss.close()

    
def start():
    #address = ('127.0.0.1',int(sys.argv[1]))
    address = ('127.0.0.1',31500)
    s = socket.socket()
    s.bind(address)
    s.listen(100)
    while 1:
        ss, add = s.accept()
        thread.start_new_thread(proxyer, (ss,))
       
if __name__ == '__main__':
   start()
