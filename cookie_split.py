import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

cookies = 'll="118275"; bid=_JrAIA7ibIw; __yadk_uid=t4KeK6B7lsdbmMVrU0X7HdH2TA7kDaIJ; _vwo_uuid_v2=D4320E9EBFB63C76345FCECFAE258FE1E|5e08aaa17eef8354c00615fbe67498b0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1528976881%2C%22https%3A%2F%2Fwww.hao123.com%2F%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.1735917058.1523184544.1523686220.1528976883.4; __utmz=30149280.1528976883.4.4.utmcsr=hao123.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _ga=GA1.2.1735917058.1523184544; _gid=GA1.2.1852326111.1528977674; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14670; ap=1; ps=y; __utmt=1; __utmc=30149280; _gat_UA-7019765-1=1; dbcl2="146704130:OGpxnzVCCoE"; ck=lxEM; _pk_id.100001.8cb4=d43629b6c66f1636.1523184543.3.1528978873.1523686219.; __utmb=30149280.18.10.1528976883'
cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}
print(cookies)

url = 'https://www.douban.com/people/146704130/'
r = requests.get(url, headers=headers, cookies=cookies)
content_html = r.content.decode('utf-8')

with open('douban3.html', 'w', encoding='utf-8') as f:
    f.write(content_html)