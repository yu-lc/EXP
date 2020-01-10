# phpstudy后门
## 简介
早期被人植入的供应链后门，可通过特定方式触发
## 影响版本
目前已知受影响的phpstudy版本
phpstudy 2016版php-5.4
phpstudy 2018版php-5.2.17
phpstudy 2018版php-5.4.45
## 漏洞复现
bp抓包修改请求包的Accept-Encoding和Accept-Charset参数即可利用
## py代码执行结果
![Image text](https://github.com/yu-lc/EXP/blob/master/phpstudy/phpstudy%E5%90%8E%E9%97%A8/1.png)
