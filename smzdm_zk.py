import requests
from lxml import etree
import csv
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def smzdm_spider(url):
    # ua = UserAgent()
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
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Cookie': '__ckguid=S1P4KbP9RQcVrjKyr1Prg85; device_id=190185334915360587719799791550891678880167b22ccbd859b00861; _ga=GA1.2.1362746504.1536058774; smzdm_user_source=290A6B9BD2004EFF0CDF19F56BABB3C4; smzdm_user_view=A3E5B03FB4535CE701C4FBEC37A2E231; ss_ab=ss38; s_his=%E9%A5%BC%E5%B9%B2%2C%E6%89%8B%E6%9C%BA; wt3_eid=%3B999768690672041%7C2153605880700031209%232154034424300230414; _gid=GA1.2.733334609.1540780824; PHPSESSID=fd4507518cbceaf8fa46e42da642af7d; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1540798579,1540862395,1540867436,1540870048; zdm_qd=%7B%22referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dru86SQ1Z_3MiUxLrI8WHHMKbVlIvZZFtUC67cqbwOJu%26ck%3D6734.1.101.371.172.371.172.129%26shh%3Dwww.baidu.com%26sht%3Dbaiduhome_pg%26wd%3D%26eqid%3De0ff2c3b000163ad000000065bd7cf9a%22%7D; __jsluid=d026d6448c120e2e84a1a1787ffbc9f0; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1540870192',
               'Referer':'https://www.smzdm.com/',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': random.choice(USER_AGENTS)}
    resp = requests.get(url, headers=headers, verify=False).content.decode()
    html = etree.HTML(resp)
    li_list = html.xpath("//ul[@id='feed-main-list']/li")
    content_list = list()
    for li in li_list:
        item = dict()
        item['title'] = li.xpath(".//h5[@class='feed-block-title']/a/text()")[1].strip() if len(li.xpath(".//h5[@class='feed-block-title']/a/text()"))>0 else None
        # a = item['title'].split(" ")[0]
        # print(a)
        item['introduction'] = li.xpath(".//div[@class='feed-block-descripe']/text()")[0].strip() if len(li.xpath(".//div[@class='feed-block-descripe']/text()"))>0 else None
        item['activity'] = li.xpath(".//h5[@class='feed-block-title']/a/span[2]/text()")[0] if len(li.xpath(".//h5[@class='feed-block-title']/a/span[2]/text()"))>0 else None
        item['detial_url'] = li.xpath(".//h5[@class='feed-block-title']/a/@href")[0] if len(li.xpath(".//h5[@class='feed-block-title']/a/@href"))>0 else None
        item['buy_url'] = li.xpath(".//div[@class='z-feed-foot-r']/div/div/a/@href")[0] if len(li.xpath(".//div[@class='z-feed-foot-r']/div/div/a/@href"))>0 else None
        item['source'] = li.xpath(".//div[@class='z-feed-foot-r']/span/a/text()")[0] if len(li.xpath(".//div[@class='z-feed-foot-r']/span/a/text()"))>0 else None
        item['publish_time'] = li.xpath(".//div[@class='z-feed-foot-r']/span/text()")[0].strip() if len(li.xpath(".//div[@class='z-feed-foot-r']/span/text()"))>0 else None
        item['collection_count'] = li.xpath(".//div[@class='z-feed-foot-l']/a[1]/span/text()")[0] if len(li.xpath(".//div[@class='z-feed-foot-l']/a[1]/span/text()"))>0 else None
        item['comment_count'] = li.xpath(".//div[@class='z-feed-foot-l']/a[2]/text()")[1] if len(li.xpath(".//div[@class='z-feed-foot-l']/a[2]/text()"))>0 else None
        content_list.append(item)
    # 翻页
    next_url = html.xpath("//a[text()='下一页']/@href")[0] if len(html.xpath("//a[text()='下一页']/@href"))>0 else None
    return content_list, next_url


def save_content_list(content_list):
    with open('C:/Users/Administrator/Desktop/smzdmdd.csv', 'a', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'introduction', 'activity','detial_url', 'buy_url', 'source', 'publish_time',
                                               'collection_count', 'comment_count'])
        # writer.writeheader()
        for content in content_list:
            writer.writerow(content)


if __name__ == '__main__':
    url = 'https://fashion.smzdm.com/' # 时尚运动
    # url = 'https://home.smzdm.com/' # 家居生活
    # url = 'https://3c.smzdm.com/' # 3C家电
    content_list, next_url = smzdm_spider(url)
    save_content_list(content_list)
    print('第1页保存成功')
    i = 2
    while next_url is not None:
        content_list, next_url = smzdm_spider(next_url)
        save_content_list(content_list)
        print('第%s页保存成功' % i)
        i += 1