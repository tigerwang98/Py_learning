import requests
for page in range(1,7):
    start = page if page == 1 else (page - 1) * 45 + 1
    end = page * 45
    url = 'http://jsj.jiaxing.gov.cn/module/jpage/dataproxy.jsp?startrecord=%s&endrecord=%s&perpage=15'%(start, end)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    param = {
        'col': 1,
        'appid': 1,
        'webid': 3197,
        'path': '/',
        'columnid': 1633698,
        'sourceContentType': 3,
        'unitid': 5088170,
        'webname': '嘉兴市住房和城乡建设局',
        'permissiontype': 0
    }
    resp = requests.post(url, headers=header, data=param)
    resp.encoding = 'utf-8'
    # print(resp.text)
    if any(i in resp.text for i in ['事故', '处罚', '违规', '违法', '行政执法', '弄虚作假']):
        print('找到了！', page)
        print(resp.text)
    else:
        print('当前是:%s页'%page)