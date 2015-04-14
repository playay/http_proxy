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
import socket
import thread


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
        headers[key] = value.strip()
    #logging.debug(str(headers))
    
    return status_code, headers


'''解析http请求头,返回（host, port, method, uri, headers）'''
def parser_request_headers(request_headers):

    lines = request_headers.strip().split('\r\n')
    
    '''解析请求方法和uri'''
    line0 = lines[0].split(' ')
    method = line0[0].upper()
    uri = line0[1]
    logging.debug(str(line0))
    
    '''解析其他header'''
    headers = {}
    for i in range(1,len(lines)):
        line= lines[i].split(':')
        key = line.pop(0)
        value = ''.join(line)
        headers[key] = value.strip()
    logging.debug(str(headers))

    '''处理目标主机和端口'''
    target_host_and_port = headers['Host'].split(':')
    if len(target_host_and_port)==1:
        target_host = target_host_and_port[0]
        target_port = 80
    else:
        target_host = target_host_and_port[0]
        target_port = int(target_host_and_port[1].strip())
        
    return target_host, target_port, method, uri, headers
    
'''获取目标主机的http应答, 并转发应答包'''      
def do_proxy(host, port, method, uri, request_headers, request, ss):
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
            ss.send(buf)
            if not got_header and '\r\n\r\n' in response:
                got_header = True
                response_header = response.split('\r\n\r\n')[0] + '\r\n\r\n'
                header_length = len(response_header)
                logging.debug(response_header)
                status_code, headers = parser_response_header(response_header)
                logging.debug(str(status_code))

            if got_header:
                '''
                没有内容，直接返回报文头就行
                204 No Content
                304 Not Modified 
                '''
                if method in ['HEAD']:
                    break
                if method in ['GET', 'POST']:
                    if status_code in [304,204]:
                        break
                    '''
                    201 Created 已创建 见过201有Transfer-Encoding属性
                    202 Accepted 请求已接受，但服务端未处理
                    206 Partial Content 新浪有Content-Length,只管正常返回这个部分内容就行了，客户端请求时就只要这部分
                    301 Moved Permanently 永久性转移 百度的301包含 Content-Length
                    302 (303,307这三个表示相同含义)Found 暂时性重定向 百度的302包含 Content-Length
                    404 未找到资源 与200一样，返回一个正常网页
                    413 Request Entity Too Large 请求实体太大
                    414 Request URI Too Long 请求URI太长
                    500 Internal Server Error 内部服务器错误
                    501 Not Implemented 未实现
                    503 服务器问题 与200一样，返回一个正常网页
                    505 HTTP Version Not Supported 不支持的HTTP版本
                    '''
                    if status_code in [200,201,206,301,302,303,307,404,413,414,500,501,503,505]:
                        if 'Transfer-Encoding' in headers:
                            if not buf:
                                logging.debug('not buf in tranfer-encoding')
                                break 
                        if 'Content-Length' in headers:
                            if int(headers['Content-Length']) <= len(response)-header_length:
                                break
                        if not 'Content-Length' in headers and not 'Transfer-Encoding' in headers and not buf:
                            logging.debug('not buf')
                            break 
                    else:#其他响应状态码
                        if 'Transfer-Encoding' in headers:
                            if not buf:
                                logging.debug('not buf in tranfer-encoding')
                                break 
                        if 'Content-Length' in headers:
                            if int(headers['Content-Length']) <= len(response)-header_length:
                                break
                        if not 'Content-Length' in headers and not 'Transfer-Encoding' in headers and not buf:
                            logging.debug('not buf')
                            break 


        #logging.debug(response)
        logging.info(str(status_code)+' response len'+str(len(response)-header_length)+uri)
    except Exception, e:
        logging.warning(str(type(e))+' '+str(e)+' err')
        c.close()
        ss.close()
    c.close()
    ss.close()


def proxyer(ss):
    logging.debug(ss)
    '''接收http请求'''
    request = ''
    got_header = False
    headers = {}
    while 1:
        buf = ss.recv(4096)
        request = request + buf
        if not got_header and '\r\n\r\n' in request:
            got_header = True
            request_header = request.split('\r\n\r\n')[0] + '\r\n\r\n'
            header_length = len(request_header)
            host, port, method, uri, headers = parser_request_headers(request_header)
            if method in ['GET','HEAD']:
                break
        if got_header and method in ['POST']:
            if 'Content-Length' in headers:
                if int(headers['Content-Length']) <= len(request)-header_length:
                    break
            else:
                logging.warning('no Content-Length in POST request,close this task')
                ss.close()
                return
        if not buf:
            break
    if not '\r\n\r\n' in request:
        logging.warning('request err,len = '+str(len(request))+',close this task')
        ss.close()
        return
    logging.debug('request length: '+str(len(request)))
    logging.debug('\n'+request)
    
    if not host or not port or not method in ['HEAD','GET','POST']:
        logging.warning('parser request waring('+
        host+':'+str(port)+' '+method
        +'): ,close this task')
        ss.close()
        return
    logging.info(host+':'+str(port)+' '+method+' '+uri)
    
    '''获取目标主机的http应答, 并转发应答包'''
    do_proxy(host, port, method, uri, headers, request, ss)
    
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
