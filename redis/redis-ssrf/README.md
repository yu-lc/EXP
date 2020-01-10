# redis-ssrf漏洞
## 简介
Weblogic中存在一个SSRF漏洞，利用该漏洞可以发送任意HTTP请求，进而攻击内网中redis、fastcgi等脆弱组件
## 漏洞利用
### 查看uddiexplorer应用（通过错误的不同，即可探测内网状态）
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/1.png)
#### 漏洞存在位置
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/2.png)
#### 抓包，修改配置
#### 抓包，修改成访问一个可以访问的IP:PORT
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/3.png)
可访问的端口将会得到错误，一般是返回status code（如下图），如果访问的非http协议，则会返回did not have a valid SOAP content-type
#### 修改为不存在的端口,将会返回could not connect over HTTP to server
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/4.png)
### 注入HTTP头，利用Redis反弹shell
#### 探测内网，发现172.24.0.2:6379可以连通
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/5.png)
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/6.png)
#### 发送三条redis命令，将弹shell脚本写入/etc/crontab
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/7.png)
#### 成功反弹shell
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/8.png)
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/9.png)
## py脚本执行结果
### 监听机器成功反弹shell
![Image text](https://github.com/yu-lc/EXP/blob/master/redis/redis-ssrf/img/10.png)
