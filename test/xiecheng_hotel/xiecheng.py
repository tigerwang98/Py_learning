# encoding: utf-8
"""
@project = Py_learing
@file = xiecheng
@author= wanghu
@create_time = 2021/8/11 10:53
"""
import requests
import json
from urllib.parse import quote

def send_requests(user_options):
    url = 'https://m.ctrip.com/restapi/soa2/21881/json/HotelSearch?testab=682e30fae039d465a543ad7ec870f8b0a0d16bff99ee5c1b065e742d4506dcd4'
    param = 'countryId=1&city=28&checkin=2021/08/11&checkout=2021/08/12&optionId=28&optionType=City&directSearch=0&display=%E6%88%90%E9%83%BD&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&'

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

def get_hotel_list():
    url = 'https://m.ctrip.com/restapi/soa2/21881/json/HotelSearch?testab=fd9273a6f1154ebacfd6819ce5ca28519d32cc3d08f7d1c7b7dad42e82932916'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
    }
    param_payload = {
    "meta": {
    "fgt": "",
    "hotelId": "",
    "priceToleranceData": "",
    "priceToleranceDataValidationCode": "",
    "mpRoom": [],
    "hotelUniqueKey": "",
    "shoppingid": "",
    "minPrice": "",
    "minCurr": ""
  },
  "seqid": "d28ec2694bf1424bbc63f1d0ca76d084",
  "deduplication": [
    70433815,
    5279480,
    35911530,
    56464188,
    446107,
    2997815,
    926121,
    70989400,
    78226490,
    67690163,
    916768,
    1014915,
    63603826
  ],
  "filterCondition": {
    "star": [],
    "rate": "",
    "rateCount": [],
    "priceRange": {
      "lowPrice": 0,
      "highPrice": -1
    },
    "priceType": "",
    "breakfast": [],
    "payType": [],
    "bedType": [],
    "bookPolicy": [],
    "bookable": [],
    "discount": [],
    "zone": [],
    "landmark": [],
    "metro": [],
    "airportTrainstation": [],
    "location": [],
    "cityId": [],
    "amenty": [],
    "promotion": [],
    "category": [],
    "feature": [],
    "brand": [],
    "popularFilters": [],
    "hotArea": [],
    "ctripService": [],
    "priceQuickFilters": [],
    "applicablePeople": []
  },
  "searchCondition": {
    "sortType": "1",
    "adult": 1,
    "child": 0,
    "age": "",
    "pageNo": 2,
    "optionType": "City",
    "optionId": "28",
    "lat": 0,
    "destination": "",
    "keyword": "",
    "cityName": quote("成都"),
    "lng": 0,
    "cityId": 28,
    "checkIn": "2021-08-12",
    "checkOut": "2021-08-13",
    "roomNum": 1,
    "mapType": "gd",
    "travelPurpose": 0,
    "countryId": 1,
    "url": "https://hotels.ctrip.com/hotels/list?countryId=1&city=28&checkin=2021/08/12&checkout=2021/08/13&optionId=28&optionType=City&directSearch=0&display=%E6%88%90%E9%83%BD&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&",
    "pageSize": 10,
    "timeOffset": 28800,
    "radius": 0,
    "directSearch": 0,
    "signInHotelId": 0,
    "signInType": 0,
    "hotelIdList": []
  },
  "queryTag": "NORMAL",
  "genk": 'true',
  "genKeyParam": {
    "a": 0,
    "b": "2021-08-12",
    "c": "2021-08-13",
    "d": "zh-cn",
    "e": 2
  },
  "webpSupport": 'true',
  "platform": "online",
  "pageID": "102002",
  "head": {
    "Version": "",
    "userRegion": "CN",
    "Locale": "zh-CN",
    "LocaleController": "zh-CN",
    "TimeZone": "8",
    "Currency": "CNY",
    "PageId": "102002",
    "webpSupport": 'true',
    "userIP": "",
    "P": "48624437009",
    "ticket": "",
    "clientID": "1622600246995.1w3iih6",
    "group": "ctrip",
    "Frontend": {
      "vid": "1622600246995.1w3iih6",
      "sessionID": 13,
      "pvid": 99
    },
    "Union": {
      "AllianceID": "",
      "SID": "",
      "Ouid": ""
    },
    "HotelExtension": {
      "group": "CTRIP",
      "hasAidInUrl": 'false',
      "Qid": "683597696579",
      "WebpSupport": 'true',
      "hotelUuidKey": "pfZxSXEqdxHlrDcrhoenMEtTWnQiQDe3QiGY7AeP8WBNWMHYd7EgmjHoyhaEAYk7YQMKDqeztekdEmljQ5WQmKtnyl9jHYGOWl1JU6r8Oysbw01r1oKffK9BYGAIFYgUJoNvmzwTnjpawqLvg7jk7Wb9izlehYTkv5cRmDrn4jG9wZTvtZjbvN6i5sJ3YqnI5oE6li0bI5OY34yXcjlHvzme7sYGnjD9yFMvfXvLZJ7YZgWsBx3trtFvdpvkFY9Lw4MjDBeGcik7Yo8whXRX1YTYQvLFJgAy11KB8WHzRZYDpx1pRD7RqSv9ceh9YZHikpYlSWHkRsoRBYhdIaNrF5rMbRaLrsTR1Ym7iSAJaOeHBE7DKLFwHziZ1RspjDrlXYFZJXzyDrU6YLAWz7vL3xNaemFYbbKfoELfKb3wq7itlRP6j0rfSYN9JLMyNr35jhbeBDjmoKnsjGLwAAKSFWDqEbSjTHeSpxB4j1rXGEsPWmPelHj4gYBmj58wTmIcOj0Ymfxooxnoef4YOfiB1iZQihOj3byTwkbwQYpAJcprFhEHAwOMEnLYnqw6DE8zJdBYBtwa5RfTe05iPYQkxdHvXbxBfRMlwmAY9AjLlypaJcfjXnyq1wopWSZWMBWc5iqmiLOvGFj8YP6yGTr9Zw3MJHkymgJUFwMsY1mRLpYtaEFowXXxU8jsSR4pjZ4jFAJLaRLtjhnI30WzY3oen1JAaycPRZQw3SYNoYDmw4BW1AW5HYtSELQwFSv1dvTLJZNJG8E8mwkYSNIo6WcUJ7bjakwXsvscjhnW7dWaseZYT0Y73iz9vQFRt3wmFygAWPNeDbvT3EkAWHwLTRqNyQYh9jqqxm6yTUR5UwgFynZW8Tet8vfZWQNJl7ws4yDfe3Y8geFZx7hrfZRhPwXsYfPj9Ay3ZJ5zjA7ytTYSNvXpjNljG3jQPrpNvPdE0Y9URdPwAhIgFE1MjUkWnSWh5WD3YG6Y7QYTqR6FY9oWONY0bY67YDUj0deXhEkDWlFempwHTebOjf6YGAypXESqjqAE76rbzjDfwk7yZorsbw9XKbYt5Rk4Wz0WXpWbGWqZ"
    }
  }
}
    res = requests.post(url=url, headers=header, data=json.dumps(param_payload))
    print(res.text)

if __name__ == '__main__':
    # login()
    get_hotel_list()