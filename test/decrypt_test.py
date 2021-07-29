from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import requests,json
from hashlib import md5
import base64

def create(info):
    keys = b'asdzxc123suitang'
    iv = b'123asdzxcsuitang'
    aes_obj = AES.new(key=keys,mode=AES.MODE_CBC, iv=iv)
    pad_data = pad(info, 16)
    ret = aes_obj.encrypt(pad_data)
    return binascii.b2a_hex(ret).decode()

def decrypt(miwen):
    print('密文是：', miwen)
    key = b'asdzxc123suitang'
    iv = b'123asdzxcsuitang'
    aes_decry = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    ret = aes_decry.decrypt(binascii.a2b_hex(miwen))
    decry_data = unpad(ret, 16).decode()
    print('明文是：', decry_data)

def myself_test_aes():
    key = b'zhexiazikebuyong'
    iv = b'testivbixuguding'
    mingwen = b'zheshiyitiaomingwenxinxi'
    aes_obj = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    pad_data = pad(mingwen, 16)
    encry_data = aes_obj.encrypt(pad_data)
    print('密文：', binascii.b2a_hex(encry_data).decode())
    # ---------------------------------------------------------------------------------
    # a = binascii.a2b_hex(encry_data)
    decry_data = aes_obj.decrypt(encry_data)
    unpad_data = unpad(decry_data, 16)
    print('明文：', unpad_data.decode())


class ZlktSpider():
    def __init__(self):
        url = 'https://www.zlkt.net/'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        sess = requests.Session()
        sess.get(url=url, headers=self.header)
        self.header['Cookie'], self.header['X-Xsrftoken'] = self.handle_cookie(sess.cookies.get_dict())

    def handle_cookie(self, cookie_dict):
        cookie = ''
        for k, v in cookie_dict.items():
            cookie = cookie + str(k) + '=' + str(v) + ';'
        base64_token = cookie_dict['_xsrf'].split('|')[0]
        token = base64.b64decode(base64_token).decode()
        return cookie, token

    def login(self, username, password):
        url = 'https://www.zlkt.net/signin/do'
        param = {
            'Email': username,
            'Password': password,
        }
        ret = requests.post(url=url, headers=self.header, data=param)
        try:
            ret.json()
            print('登录知了课堂成功！')
        except:
            print('登录知了课堂失败！')
            raise Exception

    def shizhan(self):
        url = 'https://www.zlkt.net/training/jscrack/aes01/login?CourseId=1&BarId=11'
        param = {
            'username': 'zhiliao',
            'password': self.shizhan1_make_encry_data('111111')
        }
        resp = requests.post(url=url, headers=self.header, data=param)
        print(resp.text)

    def shizhan1_make_encry_data(self, psword):
        key = b'ABC34FG91JKL58NO'
        aes_obj = AES.new(key=key, mode=AES.MODE_ECB)
        pad_data = pad(psword.encode(), 16)
        ecrypted_data = aes_obj.encrypt(pad_data)
        return binascii.b2a_hex(ecrypted_data).decode()

    def make_encry_data1(self, info):
        key = b'ABC34FG91JKL58NO'
        iv = b'fajklsfjsdow1238'
        aes_obj = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        pad_data = pad(info.encode(), 16)
        ecrypted_data = aes_obj.encrypt(pad_data)
        return binascii.b2a_hex(ecrypted_data).decode()

    def make_encry_data2(self, info):
        key = b'ABC34FG91JKL58NO'
        iv = b'fajklsfjsdow1238'
        aes_obj = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        pad_data = pad(info.encode(), 16)
        ecrypted_data = aes_obj.encrypt(pad_data)
        aes_data = binascii.b2a_hex(ecrypted_data)
        md5_data = md5(aes_data)
        return md5_data.hexdigest()

    def shizhan2(self):
        pwd1 = self.make_encry_data1('wanghu123')
        pwd2 = self.make_encry_data2('wanghu123')
        url = 'https://www.zlkt.net/training/jscrack/aes02/register?CourseId=1&BarId=12'
        param = {
            'username': '18683108304',
            'password1': pwd1,
            'password2': pwd2,
        }
        resp = requests.post(url=url, headers=self.header, data=param)
        print(resp.text)

if __name__ == "__main__":
    usrname = 'lyfshiwoer@163.com'
    psword = '19980207abc'
    obj = md5()
    obj.update(psword.encode())
    psword = obj.hexdigest()
    spider = ZlktSpider()
    spider.login(usrname, psword)
    spider.shizhan()
    spider.shizhan2()