# 翻译爬虫
class Wyfy():
    def fy():
        while 1:
            import urllib.request #打开读取url的模块
            import urllib.parse # 负责解析功能
            import json #返回类型是json格式的 所以我们调用 json模块解析她
            text = input('请输入要翻译的字符（输入0退出）:')
            if text=='0':
                break
            else:
                url=('http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule')
                data={} #post 提交的信息 以字典的方式 from data
                data['i']= text
                data['from']='AUTO'
                data['to']='AUTO'
                data['smartresult']='dict'
                data['client']='fanyideskweb'
                data['salt']='15752056706074'
                data['sign']='867ae0fd4c347c5737417ce63f41cce3'
                data['ts']='1575205670607'
                data['bv']='e2a78ed30c66e16a857c5b6486a1d326'
                data['doctype']='json'
                data['version']='2.1'
                data['keyfrom']='fanyi.web'
                data['action']='FY_BY_CLICKBUTTION'
                data1=urllib.parse.urlencode(data).encode('utf-8')

                response = urllib.request.urlopen(url,data1) #输入url地址
                '''
                response.info() #服务器返回信息
                response.geturl() #得到访问的url地址
                response.getcode() #得到返回状态 如200，404
                '''
                html = response.read().decode('utf-8')
                txt=json.loads(html)
                print('翻译为:%s' %txt['translateResult'][0][0]['tgt'], )
            

Wyfy.fy()
