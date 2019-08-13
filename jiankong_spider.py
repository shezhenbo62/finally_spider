import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HU6889T40CE4668D"
proxyPass = "6252BEF79EEE8C81"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
  "host" : proxyHost,
  "port" : proxyPort,
  "user" : proxyUser,
  "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}

url_list = ["http://www.helenarubinstein.cn/","http://www.ohui.com.cn/","https://www.esteelauder.com.cn/","https://www.lamer.com.cn","https://www.loccitane.cn/","https://www.innisfree.cn/","https://www.maccosmetics.com.cn/","https://www.clinique.com.cn/","https://www.origins.com.cn/","https://www.benefitcosmetics.com/cn/zh-hans","http://sekkisei.kose.com.cn/","http://www.hadalabo.com.cn/","https://www.jomalone.com.cn/"]
last_time_list = ["Mon, 20 Aug 2018 08:40:49 GMT","Tue, 04 Aug 2009 21:25:02 GMT","Thu, 13 Sep 2018 06:15:47 GMT","Wed, 12 Sep 2018 06:16:27 GMT","Thu, 13 Sep 2018 07:11:02 GMT","Wed, 29 Nov 2017 01:26:34 GMT","Tue, 11 Sep 2018 10:15:07 GMT","Thu, 13 Sep 2018 05:52:09 GMT","Mon, 10 Sep 2018 14:34:32 GMT","Thu, 13 Sep 2018 04:21:58 GMT","Fri, 29 Dec 2017 11:25:06 GMT","Tue, 07 Aug 2018 03:25:48 GMT","Thu, 13 Sep 2018 05:39:03 GMT"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
i = 0
for url in url_list:
    response = requests.get(url, headers=headers, proxies=proxies, verify=False)
    # print(response.headers)
    last_modified = last_time_list[i]
    # last_modified1 = response.headers['Last-Modified']
    print(last_modified)
    rsp = requests.head(url, headers={'If-Modified-Since': last_modified}, verify=False)
    # 网站未更新
    if str(rsp) == '<Response [304]>':
        print('网站页面未更新')
    # 网站更新
    else:
        print(url)
        # 第三方 SMTP 服务
        mail_host = "smtp.163.com"  # 设置服务器
        mail_user = "smart123_it@163.com"  # 用户名
        mail_pass = "szb190688"  # 口令

        sender = 'smart123_it@163.com'
        receivers = ['smart123_it@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        mail_msg = """
        <p>此网站已更新，请及时查看是否在做优惠活动!</p>
        <p><a href='{}'>活动链接</a></p>
        """.format(url)

        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['From'] = Header("smart123_it@163.com", 'utf-8')
        message['To'] = Header("smart123_it@163.com", 'utf-8')

        subject = 'D88 品牌官网活动信息 邮件测试'
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
    i += 1