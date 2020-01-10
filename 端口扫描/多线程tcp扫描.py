import socket
from queue import Queue
from IPy import IP
from threading import Thread
import requests
import re
import time

def getDate():   # 创建队列方法
    ip_port = Queue(-1)    # 队列 先进先出FIFO,-1代表长度无限
    ports = [81,80]
    for ip in IP('192.168.150.0/24'):
        for port in ports:
            ip_port.put((str(ip),port))    # 将ip，port传到ip_port中
    return ip_port  # 保存组合后的队列

def portscan(i,ip_port):
    socket.setdefaulttimeout(1)    # 超时跳转到下一个线程
    while not ip_port.empty():    # 如果ip_port有意义
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # 创建套接字  AF_INET（使用IPv4通信）SOCK_STREAM（面向连接）
        ip,port = ip_port.get()    # 取值取下来放入ip和port中
        address = (ip,port)
        time.sleep(1)
        try:
            s.connect(address)   # 主动初始化TCP服务器连接
            print('[+][线程{}]{}: open [{}]'.format(i,address[0],address[1]))
            get_title(str(address[0]),address[1])
        except Exception as e:
            s.close()    # 关闭套接字
            print('[-][线程{}]{}: closed [{}]  error {}: '.format(i,address[0],address[1],e))
        s.close()

def get_title(url_ip,url_port):   # 取web首页title
    url = 'http://{}:{}'.format(url_ip,url_port)
    res = requests.get(url=url,timeout=10)
    ret = re.search(r'<title>(.*)</title>',res.text)   # 取title值
    print(ret.group(0))

def THREAD():   # 多线程
    for i in range(50):   #  线程数50
        t = Thread(target=portscan,args=(i,ip_port))    # target+方法 args+方法里的参数
        threads.append(t)    # 赋值
        t.start()   # 开启线程
    for t in threads:
        t.join()   # 阻塞线程

#if __name__ == "__main__":  # 自己调用自己
ip_port = getDate()   # 将队列方法实例化赋值
threads = []
THREAD()