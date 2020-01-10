#爬seebug文章，落地到本地。第一层：seebug，第二层：文章目录，第三层：各个文章的源码，结果保存为txt。
import re,requests,os,traceback

def kongisheng(title):  #将空格转换成-
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  
    new_title = re.sub(rstr, "-", title)  
    return new_title

def down():
    try:
        url = 'https://paper.seebug.org'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}
        res = requests.get(url=url,headers=headers,timeout=10)
        ret = re.findall('''<a href="(.+)/"><i
      class="fa fa-angle-right"></i>(.+)</a>''',res.text)   #匹配目录
        os.mkdir('d://seebug')  #创建主文件

        for i in range(0,len(ret)):    #访问不同目录读取页数
            er ='d://seebug//{}'.format(ret[i][1])
            os.mkdir(er)   #创建目录
            step = '{}{}'.format(url,ret[i][0])
            res1 = requests.get(url=step,headers=headers,timeout=10) #访问目录
            ret1 = re.findall(r'<span class="page-number">Page 1 of (.+)</span>',res1.text) #获取页数
            
            for x in range(1,int(ret1[0])+1):   #匹配页数进行读取子目录
                step1 = step+'/?page={}'.format(x)
                res2 = requests.get(url=step1,headers=headers,timeout=10)   #访问不同页码
                ret2 = re.findall('''<h5 class="post-title"><a href="(.+)/">(.+)</a>''',res2.text)    #获取子目录

                for y in range(0,len(ret2)):    #访问子目录获取内容
                    step2 = '{}{}'.format(url,ret2[y][0])
                    res3 =  requests.get(url=step2,headers=headers,timeout=10)    #获取内容
                    with open('d://seebug//{}//{}.txt'.format(kongisheng(ret[i][1]),kongisheng(ret2[y][1])),'w',encoding='utf-8') as f:
                        f.write(res3.text)
                        print('已经爬取'+kongisheng(ret[i][1])+'目录下的'+kongisheng(ret2[y][1])+'文档')
                        
    except Exception as e:
        print('traceback1.print_exc:'.traceback.print_exc())    #显示详细报错信息

down()