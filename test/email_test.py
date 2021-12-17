# encoding: utf-8
"""
@project = Py_learing
@file = email_test
@author= wanghu
@create_time = 2021/11/29 14:56
"""
import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp.qiye.aliyun.com'
# mail_host = 'smtp.qq.com'
mail_user = 'bwai@cninct.com'
# mail_pass = 'queirsmpdhkabgif'
mail_pass = 'St123456'
sender = 'bwai@cninct.com'
receivers = ['lyfshiwoer@163.com']

test_text = '''
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/html">
<head>
</head>
<body>
<table>
<tr>
    <td>名称</td>
    <td>来源</td>
    <td>链接</td>
    <td>负责人</td>
    <td>奖项名</td>
</td>
</table>
</body>
</html>
'''



#设置email信息
#邮件内容设置
message = MIMEText(test_text, 'HTML', 'utf-8')
#邮件主题
message['Subject'] = 'title'
#发送方信息
message['From'] = sender
#接受方信息
message['To'] = receivers[0]
try:
    smtpObj = smtplib.SMTP()
    #连接到服务器
    smtpObj.connect(mail_host, 25)
    #登录到服务器
    smtpObj.login(mail_user, mail_pass)
    #发送
    smtpObj.sendmail(
        sender, receivers, message.as_string())
    #退出
    smtpObj.quit()
    print('send email success')
except smtplib.SMTPException as e:
    print('error', e) #打印错误

