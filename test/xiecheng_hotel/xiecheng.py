# encoding: utf-8
"""
@project = Py_learing
@file = xiecheng
@author= wanghu
@create_time = 2021/8/11 10:53
"""
import requests

url = 'https://m.ctrip.com/restapi/soa2/21881/json/HotelSearch?testab=682e30fae039d465a543ad7ec870f8b0a0d16bff99ee5c1b065e742d4506dcd4'
param = 'countryId=1&city=28&checkin=2021/08/11&checkout=2021/08/12&optionId=28&optionType=City&directSearch=0&display=%E6%88%90%E9%83%BD&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&'
def send_requests(user_options):

    requests.get()

def login():
    url = 'https://passport.ctrip.com/gateway/api/soa2/12559/userValidateNoRisk'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        # 'referer': 'https://passport.ctrip.com/user/login?BackUrl=https%3A%2F%2Fwww.ctrip.com%2F',
        'content-type': 'application/json; charset=UTF-8',
    }
    param = '''{"AccountHead": {"Platform":"P","Extension":{}},
             "Data": {"accessCode":"7434E3DDCFF0EDA8","strategyCode":"698D04A841768C87","userName":"F8443E828B9645B29F4D3513C716C495","certificateCode":"123456abc",
                      "extendedProperties":[
                          {"key":"LoginName","value":"F8443E828B9645B29F4D3513C716C495"},
                          {"key":"Platform","value":"P"},
                          {"key":"PageId","value":"10320670296"},
                          {"key":"URL","value":"https://passport.ctrip.com/user/login?BackUrl=https%3A%2F%2Fwww.ctrip.com%2F#ctm_ref=c_ph_login_buttom"},
                          {"key":"http_referer","value":"https://www.ctrip.com/"},
                          {"key":"rmsToken","value":"fp=op2hqg-nroife-mz06gz&vid=1622600246995.1w3iih6&pageId=10320670296&r=3018af198eed4547ab2774865789a22a&ip=171.214.176.116&rg=fin&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1670x940&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F92.0.4515.131%20Safari%2F537.36&d=passport.ctrip.com&v=25&kpg=0_0_0_0_934_6_0_0_0_0&adblock=F&cck=F"}
                        ]
                      }
             }'''
    ret = requests.post(url=url, headers=header, data=param)
    print(ret.text)

if __name__ == '__main__':
    login()