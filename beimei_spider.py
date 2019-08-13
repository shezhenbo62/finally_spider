# -*- coding:utf-8 -*-
import requests
import random
from lxml import etree
import re
import csv


def beimei_spider():
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
        "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    ]
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9',
               'cache-control': 'max-age=0',
               'cookie': 'udid=1D2F84E84E18DC1BDDE5022482B8218D; _ga=GA1.2.844676131.1538184878; cto_lwid=2c94ffe9-1182-47d6-a0b2-aba4f23e79c9; __gads=ID=8d7a061414dc4728:T=1538184879:S=ALNI_MZQS46sn9XWuM-6ao0x5TYsjS0KPw; CC=US; PHPSESSID=2160566025482a7140a9c87b6030d207; rip_detail=; _gid=GA1.2.1948154705.1540436351; manualSelection=cn; langPcCode=cn; lang=cn; enSiteTip=show; TY_SESSION_ID=0a9bf7f6-e737-4bed-b4ee-2347c536b57f; lastRefreshTime=1540460478; _gat=1; _dm_sfa=1; rip=O',
               'referer': 'https://cn.dealmoon.com/',
               'upgrade-isecure-requests': '1',
               'user-agent': random.choice(USER_AGENTS)}
    header = {'accept': 'application/json, text/javascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'content-length': '23',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'cookie': 'udid=1D2F84E84E18DC1BDDE5022482B8218D; _ga=GA1.2.844676131.1538184878; cto_lwid=2c94ffe9-1182-47d6-a0b2-aba4f23e79c9; __gads=ID=8d7a061414dc4728:T=1538184879:S=ALNI_MZQS46sn9XWuM-6ao0x5TYsjS0KPw; _gid=GA1.2.1948154705.1540436351; langPcCode=cn; lang=cn; CC=US; PHPSESSID=bb95df53992be26ab5bf475fa0382a56; rip_detail=; rip=O',
'origin': 'https://cn.dealmoon.com',
'user-agent': random.choice(USER_AGENTS),
'x-requested-with': 'XMLHttpRequest'}
    req = requests.get('https://cn.dealmoon.com/guide', headers=headers).content.decode()
    html = etree.HTML(req)
    li_list = html.xpath("//div[@class='secend_area']/ul/li")
    for li in li_list:
        i = 0
        url = 'https://cn.dealmoon.com' + li.xpath("./a/@href")[0] if len(li.xpath("./a/@href"))>0 else None
        id = url.split('/')[-1]
        post_url = 'https://cn.dealmoon.com/guide/ajax?type=new&id={}&top='.format(id)
        req2 = requests.get(url, headers=headers).content.decode()
        html2 = etree.HTML(req2)
        li_list2 = html2.xpath("//div[@class='dm-sg-cat-res']/ul/li")
        content_list = list()
        for li2 in li_list2:
            item = dict()
            item['title'] = li2.xpath(".//div[@class='content-wrapper']/p[1]/text()")[0] if len(li2.xpath(".//div[@class='content-wrapper']/p[1]/text()")) > 0 else None
            item['introduction'] = li2.xpath(".//div[@class='content-wrapper']/p[2]/text()")[0] if len(li2.xpath(".//div[@class='content-wrapper']/p[2]/text()")) > 0 else None
            item['detail_url'] = 'https://cn.dealmoon.com' + li2.xpath("./a/@href")[0] if len(li2.xpath("./a/@href")) > 0 else None
            item['collection_count'] = re.findall(r'<i class="dm-icon-star-line"></i>(\d+)', req2)[i] if len(re.findall(r'<i class="dm-icon-star-line"></i>(\d+)', req2)) > 0 else None
            item['comment_count'] = re.findall(r'<i class="dm-icon-message"></i>(\d+)', req2)[i] if len(re.findall(r'<i class="dm-icon-message"></i>(\d+)', req2)) > 0 else None
            item['praise_count'] = re.findall(r'<i class="dm-icon-love"></i>(\d+)', req2)[i] if len(
                re.findall(r'<i class="dm-icon-love"></i>(\d+)', req2)) > 0 else None
            i += 1
            content_list.append(item)
            print(item)
        for page_num in range(2,47):
            formdata = {'pageIndex': page_num,
                        'pageSize': 20}
            post_req = requests.post(post_url, data=formdata, headers=header).content.decode()
            a = len(re.findall(r'<p class=\\"title\\".*?>(.*?)</p>', post_req, re.S))//2
            for j in range(a):
                items = dict()
                items['title'] = re.findall(r'<p class=\\"title\\".*?>(.*?)</p>', post_req, re.S)[2*j] if len(re.findall(r'<p class=\\"title\\".*?>(.*?)</p>', post_req, re.S)) > 0 else None
                items['introduction'] = re.findall(r'<p class=\\"content\\">(.*?)</p>', post_req, re.S)[j].replace('\\r','').replace('\\n','') if len(re.findall(r'<p class=\\"content\\">(.*?)</p>', post_req, re.S)) > 0 else None
                items['detail_url'] = 'https://cn.dealmoon.com' + re.findall(r'<a href=\\"(.*?)\\"', post_req, re.S)[j] if len(re.findall(r'<a href=\\"(.*?)\\"', post_req, re.S)) > 0 else None
                items['collection_count'] = re.findall(r'<i class=\\"dm-icon-star-line\\"></i>(\d+)', post_req, re.S)[j] if len(
                    re.findall(r'<i class=\\"dm-icon-star-line\\"></i>(\d+)', post_req, re.S)) > 0 else None
                items['comment_count'] = re.findall(r'<i class=\\"dm-icon-message\\"></i>(\d+)', post_req, re.S)[j] if len(
                    re.findall(r'<i class=\\"dm-icon-message\\"></i>(\d+)', post_req, re.S)) > 0 else None
                items['praise_count'] = re.findall(r'<i class=\\"dm-icon-love\\"></i>(\d+)', post_req, re.S)[j] if len(
                    re.findall(r'<i class=\\"dm-icon-love\\"></i>(\d+)', post_req, re.S)) > 0 else None
                content_list.append(items)
                print(items)
        with open('C:/Users/Administrator/Desktop/beimei.csv', 'a', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'introduction', 'detail_url','praise_count', 'collection_count',
                                                   'comment_count'])
            # writer.writeheader()
            for content in content_list:
                writer.writerow(content)
    return content_list


if __name__ == '__main__':
    content_list = beimei_spider()