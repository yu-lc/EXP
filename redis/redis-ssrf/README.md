# redis-ssrf漏洞
## 简介
Weblogic中存在一个SSRF漏洞，利用该漏洞可以发送任意HTTP请求，进而攻击内网中redis、fastcgi等脆弱组件
## 漏洞利用
### 查看uddiexplorer应用（通过错误的不同，即可探测内网状态）

#### 漏洞存在位置

#### 抓包，修改配置
#### 抓包，修改成访问一个可以访问的IP:PORT

可访问的端口将会得到错误，一般是返回status code（如下图），如果访问的非http协议，则会返回did not have a valid SOAP content-type
#### 修改为不存在的端口
将会返回could not connect over HTTP to server

### 注入HTTP头，利用Redis反弹shell
#### 探测内网，发现172.24.0.2:6379可以连通

#### 发送三条redis命令，将弹shell脚本写入/etc/crontab

#### 成功反弹shell

## py脚本执行结果
监听机器成功反弹shell
