from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import requests
from hashlib import md5

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

def shizhan():
    url = 'https://www.zlkt.net/training/jscrack/aes01/login?CourseId=1&BarId=11'
    header = {
        'Cookie': 'zhiliao_website=bcbb089c6f27e1da40e6610a93b5bc29; _xsrf=OUxhdWFPWmYwZDdYWWsyRjhRUUhQaDMyR0VYdnZSMXA=|1622771040703842616|50cbb1d9f072ea11b4792dd7ba010db05ccbd2c494f76053d7f71da6ba6678dd',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Xsrftoken': '9LauaOZf0d7XYk2F8QQHPh32GEXvvR1p',
    }
    param = {
        'username': 'zhiliao',
        'password': make_encry_data1('123456')
    }
    resp = requests.post(url=url, headers=header, data=param).json()
    print(resp)

def make_encry_data1(info):
    key = b'ABC34FG91JKL58NO'
    iv = b'fajklsfjsdow1238'
    aes_obj = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    pad_data = pad(info.encode(), 16)
    ecrypted_data = aes_obj.encrypt(pad_data)
    return binascii.b2a_hex(ecrypted_data).decode()

def make_encry_data2(info):
    key = b'ABC34FG91JKL58NO'
    iv = b'fajklsfjsdow1238'
    aes_obj = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    pad_data = pad(info.encode(), 16)
    ecrypted_data = aes_obj.encrypt(pad_data)
    aes_data = binascii.b2a_hex(ecrypted_data)
    md5_data = md5(aes_data)
    # print(md5_data.hexdigest())
    return md5_data.hexdigest()

def shizhan2():
    pwd1 = make_encry_data1('wanghu123')
    # print('*'*30)
    pwd2 = make_encry_data2('wanghu123')
    url = 'https://www.zlkt.net/training/jscrack/aes02/register?CourseId=1&BarId=12'
    header = {
        'Cookie': 'zhiliao_website=bcbb089c6f27e1da40e6610a93b5bc29; _xsrf=ZGptU2hROHFvNTdodUNrTXZ2dEN2bmhIVnBheDhuN2w=|1622775124298538551|2884370d23383930dcb2d6bc5e7ea5c98680c156349d924330d0dd8a43a5cef8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'X-Xsrftoken': 'djmShQ8qo57huCkMvvtCvnhHVpax8n7l',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    param = {
        'username': '18683108304',
        'password1': pwd1,
        'password2': pwd2,
    }
    resp = requests.post(url=url, headers=header, data=param)
    print(resp.text)

if __name__ == "__main__":
    # info = b'test AES shifou keyong'
    # encrypt_data = create(info)
    # decrypt(encrypt_data)
    # myself_test_aes()
    shizhan2()
    # a = make_encry_data1('123456')
    # print(a)