# encoding: utf-8
# !/usr/bin/env python
import time
from http import cookiejar

import requests
from bs4 import BeautifulSoup

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}


# 使用登录cookie信息
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    print(session.cookies)
    session.cookies.load(ignore_discard=True)
except Exception as e:
    print("还没有cookie信息", e)


def get_xsrf():
    response = session.get(
        "https://www.zhihu.com", headers=headers, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
    return xsrf


def get_captcha():
    """
    把验证码图片保存到当前目录，手动识别验证码
    :return:
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("验证码：")
    return captcha


def login(email, password):
    login_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf(),
        "captcha": get_captcha(),
        'captcha_type': 'en',
        'remember_me': 'true'}
    # print(session.cookies)
    response = session.post(login_url, data=data, headers=headers)
    login_code = response.json()
    print(login_code['msg'])
    # print(session.cookies)
    r = session.get("https://www.zhihu.com/settings/profile", headers=headers)
    print(r.status_code)
    with open("xx.html", "wb") as f:
        f.write(r.content)


if __name__ == '__main__':
    email = '@qq.com'
    password = ''
    login(email, password)
    json_str = ""
