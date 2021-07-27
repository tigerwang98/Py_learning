# _*_ coding:utf-8 _*_
import json
import time
import random
import base64
import datetime
from Crypto.Cipher import DES3


class Des(object):
    def pad(self, s):
        return s + (DES3.block_size - len(s) % DES3.block_size) * chr(DES3.block_size - len(s) % DES3.block_size)

    def unpad(self, s):
        return s[0:-ord(s[-1])]

    def encrypt(self, text, key):
        text = self.pad(text)
        iv = datetime.datetime.now().strftime('%Y%m%d').encode()
        cryptor = DES3.new(key, DES3.MODE_CBC, iv)
        x = len(text) % 8
        if x != 0: text = text + '\0' * (8 - x)
        self.ciphertext = cryptor.encrypt(text.encode('utf-8'))
        return base64.standard_b64encode(self.ciphertext).decode("utf-8")

    def decrypt(self, text, key):
        iv = datetime.datetime.now().strftime('%Y%m%d').encode()
        cryptor = DES3.new(key, DES3.MODE_CBC, iv)
        de_text = base64.standard_b64decode(text)
        plain_text = cryptor.decrypt(de_text)
        out = self.unpad(plain_text.decode('utf-8'))
        return out

    def make_requestvertificationtoken(self):
        str = ""
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H',
               'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        for i in range(24):
            str += arr[round(random.random() * (len(arr) - 1))]
        return str

    def make_ciphertext(self):
        timestamp = str(int(time.time() * 1000))
        salt = self.make_requestvertificationtoken()
        iv = datetime.datetime.now().strftime('%Y%m%d')
        enc = self.encrypt(timestamp, salt)
        strs = salt + iv + enc
        result = []
        for i in strs:
            result.append(bin(ord(i))[2:])
            result.append(' ')
        return ''.join(result[:-1])


if __name__ == "__main__":
    a = Des()
    text = '123abcD!'
    key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5GVku07yXCndaMS1evPIPyWwhbdWMVRqL4qg4OsKbzyTGmV4YkG8H0hwwrFLuPhqC5tL136aaizuL/lN5DRRbePct6syILOLLCBJ5J5rQyGr00l1zQvdNKYp4tT5EFlqw8tlPkibcsd5Ecc8sTYa77HxNeIa6DRuObC5H9t85ALJyDVZC3Y4ES/u61Q7LDnB3kG9MnXJsJiQxm1pLkE7Zfxy29d5JaXbbfwhCDSjE4+dUQoq2MVIt2qVjZSo5Hd/bAFGU1Lmc7GkFeLiLjNTOfECF52ms/dks92Wx/glfRuK4h/fcxtGB4Q2VXu5k68e/2uojs6jnFsMKVe+FVUDkQIDAQAB"
    t = a.encrypt(text, key)
    b = a.decrypt(t, key)
    print(b)