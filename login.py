import io
import json
import re

import matplotlib.pyplot as plt
from PIL import Image

import requests

headers = {
    'Referer': 'https://www.luogu.com.cn/auth/login',
    'Origin': 'https://www.luogu.com.cn',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.421.0 Safari/537.36",
    "Accept": "*/*",
    'Connection': 'keep-alive',
    'x-requested-with': 'XMLHttpRequest',
    'x-csrf-token':'',
}

def login():
    name = input("用户名：")
    password = input("密码：")

    s = requests.session()
    r = s.get('https://www.luogu.com.cn/auth/login', headers=headers)
    client_id = r.cookies.get('__client_id')
    csrf_token = re.findall('<meta name="csrf-token" content="(.*?)">', r.text)[0]
    headers['x-csrf-token'] = csrf_token
    print('获取验证码...')
    r = s.get('https://www.luogu.com.cn/api/verify/captcha', headers=headers)
    print("请记住弹出的验证码窗口中的验证码并关闭窗口")
    plt.figure(num='captcha')
    plt.title('Please identify and remember the verification code.')
    plt.imshow(Image.open(io.BytesIO(r.content)))
    plt.axis('off')
    plt.show()
    captcha = input('请输入验证码: ')

    print('正在进行登录...')
    headers['Content-Type'] = 'application/json'
    data = {
        'captcha': captcha,
        'password': password,
        'username': name,
    }
    r = s.post('https://www.luogu.com.cn/api/auth/userPassLogin', headers=headers, data=json.dumps(data))
    print(r.text)
    if ('status' in r.json() and r.json()['status'] == 403):
        print('出现错误: ' + r.json()['errorMessage'])
        print('登录失败!')
        return
    tk = r.json()['syncToken']
    print('Token获取成功!')
    data = {'syncToken': tk}
    r = s.post('https://www.luogu.org/api/auth/syncLogin', headers=headers, data=json.dumps(data))
    cookies_list = r.cookies.get_dict()
    cookies_list['__client_id'] = client_id
    with open("cookie.json", 'w') as f:
        f.write(json.dumps(cookies_list))
    print('登录成功!')
    print('用户名: ' + name)
