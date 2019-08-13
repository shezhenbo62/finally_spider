import requests
import random
from lxml import etree
import pymongo
from multiprocessing import Pool


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
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Cookie': 'gid=fb27be5985814151857f4c300a090e26; yka_gid=78126e76-cb70-bb97-a201-c4533a2c7154; yka_tid=14538524-c304-b838-b7ab-4988780c199a; yka_ph=%7B%20%27value%27%3A%20%2700000000000000000000000000101%27%2C%27lastdate%27%3A%20%271541088000000%27%7D; yka_srchost=brand.yoka.com; Hm_lvt_a641a94f2a28291909af4213f237173a=1540973640,1541129928; Hm_lpvt_a641a94f2a28291909af4213f237173a=1541130305',
           'User-Agent': random.choice(USER_AGENTS)}
# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HO31L31645P86F8D"
proxyPass = "AA00DFD49A7B401B"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


def yoka_brand():
    resp = requests.get('http://brand.yoka.com/brandlist.htm#A', headers=headers, proxies=proxies).content.decode()
    html = etree.HTML(resp)
    li_list = html.xpath("//div[@class='m-letter-box']/div[2]/div/ul/li")
    for li in li_list:
        item = dict()
        item['brand_name'] = li.xpath("./a/text()")[0].strip().replace('\r','').replace('\n','').replace(' ','')
        item['brand_url'] = 'http://brand.yoka.com' + li.xpath("./a/@href")[0]
        try:
            resp2 = requests.get(item['brand_url'], headers=headers, proxies=proxies).content.decode()
        except Exception as f:
            save_content_list(item)
        else:
            html2 = etree.HTML(resp2)
            item['website'] = html2.xpath("//div[@class='brandProfile']/p/a/@href")[0] if len(html2.xpath("//div[@class='brandProfile']/p/a/@href"))>0 else None
            if len(html2.xpath("//dl[@class='brandStory']/dd/a/@href")):
                item['story_url'] = 'http://brand.yoka.com' + html2.xpath("//dl[@class='brandStory']/dd/a/@href")[0]
                resp3 = requests.get(item['story_url'], headers=headers, proxies=proxies).content.decode()
                html3 = etree.HTML(resp3)
                item['country'] = html3.xpath("//ul[@class='brand-outline']/li[3]/text()")[0] if len(html3.xpath("//ul[@class='brand-outline']/li[3]/text()"))>0 else None
                try:
                    data = html3.xpath("//div[@class='m-story']")[0]
                except Exception as e:
                    save_content_list(item)
                else:
                    item['brand_story'] = data.xpath("string(.)").strip().replace('\r','').replace('\n','')
                    save_content_list(item)
            else:
                save_content_list(item)


def save_content_list(result):
    MONGO_URL = 'localhost'
    MONGO_DB = 'brand'
    MONGO_TABLE = 'yoka_brand'
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到mongodb成功', result)
    except Exception:
        print('存储到mongodb失败', result)


if __name__ == '__main__':
    yoka_brand()
    # p = Pool(processes=5)
    # p.apply_async(yoka_brand, args=())
    # p.close()
    # p.join()