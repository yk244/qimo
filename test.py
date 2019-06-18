import base64
import requests
import re
import config

def get_point(index):

    index = index.split(',')
    loc = {
        '1': '43,45',
        '2': '106,45',
        '3': '167,45',
        '4': '259,45',
        '5': '42,120',
        '6': '106,120',
        '7': '167,120',
        '8': '259,120',
    }
    answer = []
    for t in index:
        answer.append(loc[t])
    return ','.join(answer)
# 首先做好伪装,伪装成浏览器
# 实例化一个session
session = requests.Session()  # 自动的处理cookie
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36'
}
# 伪装成浏览器
session.headers.update(headers)
# 访问登陆界面
cookie_url = 'https://kyfw.12306.cn/otn/login.html/conf'
session.get(cookie_url)
# 下载验证码
response = session.get('https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&1541760606034&callback=jQuery19106311375523623572_1541759333476&_=1541759333479')
img_base64 = re.findall(r'"image":"(.*?)"', response.text)[0]
img_byte = base64.b64decode(img_base64)
with open('test.jpg', 'wb') as f:
    f.write(img_byte)

check_captcha = 'https://kyfw.12306.cn/passport/captcha/captcha-check?callback=jQuery19106311375523623572_1541759333476&rand=sjrand&login_site=E&_=1541759333484'
answer = get_point(input('请输入正确的序号:'))
response = session.get(check_captcha, params={'answer': answer})
code = re.findall(r'"result_code":"(.*?)"', response.text)[0]
if code == '4':
    print("验证码验证成功")
    # 验证用户名与密码
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    Form_Data = {
        'username': config.username,
        'password': config.password,
        'appid': 'otn',
        'answer': answer
    }
    response = session.post(login_url, data=Form_Data)
    res = response.json()
    if res['result_code'] == 0:
        print('用户名密码验证正确')
        uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        response = session.post(uamtk_url, data={'appid': 'otn'})
        res = response.json()
        if res['result_code'] == 0:
            print('获取token成功')
            check_token_url = 'https://kyfw.12306.cn/otn/uamauthclient'
            response = session.post(check_token_url, data={'tk': res['newapptk']})
            res = response.json()
            if res['result_code'] == 0:
                print('验证token通过')
                print('登陆成功')
    else:
        print('用户名或密码错误')
else:
    print('验证码错误')
