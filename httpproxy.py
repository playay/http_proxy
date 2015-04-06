#coding:utf-8
#qpy:2
#qpy:console

import logging

logging.basicConfig(level=logging.DEBUG,
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


'''解析http响应报文头'''
def parser_response_header(response_header):
    Transfer_Encoding = False
    Content_Length = 0
    status_code = 0
    lines = response_header.strip().split('\r\n')
    status_code = int(lines[0].split(' ')[1])
    
    headers = {}
    for i in range(1,len(lines)):
        line= lines[i].split(':')
        key = line.pop(0)
        value = ''.join(line)
        headers[key] = value
    #logging.debug(str(headers))
    
    return status_code, headers


'''解析http请求头,返回（host, port, method, uri）'''
def parser_request_headers(request_headers):

    lines = request_headers.strip().split('\r\n')
    
    '''解析请求方法和uri'''
    line0 = lines[0].split(' ')
    method = line0[0]
    uri = line0[1]
    logging.debug(str(line0))
    
    '''解析其他header'''
    headers = {}
    for i in range(1,len(lines)):
        line= lines[i].split(':')
        key = line.pop(0)
        value = ''.join(line)
        headers[key] = value
    logging.debug(str(headers))

    '''处理目标主机和端口'''
    target_host_and_port = headers['Host'].strip().split(':')
    if len(target_host_and_port)==1:
        target_host = target_host_and_port[0]
        target_port = 80
    else:
        target_host = target_host_and_port[0]
        target_port = int(target_host_and_port[1].strip())
        
    return target_host, target_port, method, uri
    
'''获取目标主机的http应答, 并转发应答包'''      
def do_proxy(host, port, request, ss):
    c = socket.socket()
    try:
        c.connect((host, port))
    except Exception, e:
        logging.warning(str(type(e))+' '+str(e)+' err')
        c.close()
        ss.send(str(type(e))+' '+str(e)+' err')
        ss.close()
        return
    try:   
        c.send(request)
        response = ''
        got_header = False
        header_length = 0
        headers = {}
        while 1:
            buf = c.recv(4096)
            response = response + buf
            if not got_header and '\r\n\r\n' in response:
                got_header = True
                response_header = response.split('\r\n\r\n')[0] + '\r\n\r\n'
                header_length = len(response_header)
                logging.debug(response_header)
                status_code, headers = parser_response_header(response_header)
                print status_code
            #既没Content_Length也没Transfer_Encoding的
            #可能是304之类的
            if got_header and status_code in [304,404]:
                print 'buf len '+ str(len(buf))
                #logging.debug(response)
                break
            if 'Content-Length' in headers:
                if int(headers['Content-Length'].strip()) == len(response)-header_length:
                    break
            if 'Transfer-Encoding' in headers:
                if not buf:
                    logging.debug('not buf')
                    break 
            if not buf:
                logging.debug('not buf')
                break         
        #logging.debug(response)
        logging.info('response len '+ str(len(response)))
    except Exception, e:
        logging.warning(str(type(e))+' '+str(e)+' err')
    c.close()
    if response:
        ss.send(response)
    ss.close()


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
    target_host, target_port, method, uri = parser_request_headers(request)
    if not target_host or not target_port or not method.upper() in ['GET','POST']:
        logging.warning('parser request waring('+
        target_host+':'+str(target_port)+' '+method
        +'): ,close this task')
        ss.close()
        return
    logging.info(target_host+':'+str(target_port)+' '+method+' '+uri)
    
    '''获取目标主机的http应答, 并转发应答包'''
    do_proxy(target_host, target_port, request, ss)
    
def start():
    address = ('127.0.0.1',int(sys.argv[1]))
    #address = ('127.0.0.1',31500)
    s = socket.socket()
    s.bind(address)
    s.listen(100)
    while 1:
        ss, add = s.accept()
        thread.start_new_thread(proxyer, (ss,))
       
if __name__ == '__main__':
   start()
