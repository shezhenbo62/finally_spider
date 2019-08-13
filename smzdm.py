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
               'Connection': 'eep-alive',
               'Cookie': '__ckguid=S1P4KbP9RQcVrjKyr1Prg85; __jsluid=3fde33ad8b5980e12ffcb6ccabff6861; device_id=190185334915360587719799791550891678880167b22ccbd859b00861; _ga=GA1.2.1362746504.1536058774; smzdm_user_source=290A6B9BD2004EFF0CDF19F56BABB3C4; wt3_eid=%3B999768690672041%7C2153605880700031209%232153908068600864152; _gid=GA1.2.1410553732.1540169819; PHPSESSID=240f74772766a6e6df19ebd3d6972c29; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1539917930,1540169818,1540177933,1540282208; zdm_qd=%7B%22referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DBr4SjL36Jb4pU4CISiGOfnLXPFEkY462DDzgDA3uCrq%26ck%3D3106.1.87.386.276.392.272.253%26shh%3Dwww.baidu.com%26sht%3Dbaiduhome_pg%26wd%3D%26eqid%3Db69dd3830000eb4a000000065bced759%22%7D; ad_date=23; bannerCounter=%5B%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%5D; ad_json_feed=%7B%22J_feed_ad1%22%3A%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%2C%22J_feed_ad3%22%3A%7B%22number%22%3A0%2C%22surplus%22%3A1%7D%7D; smzdm_user_view=A3E5B03FB4535CE701C4FBEC37A2E231; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1540283149',
               'Host': 'www.smzdm.com',
               'Referer':'https://test.smzdm.com/',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': random.choice(USER_AGENTS)}
    while True:
        # ipprox = requests.get('http://www.yooongchun.com:9999/?name=yooongchun&password=121561&method=random').content.decode()
        # proxy_host = 'https://' + ipprox
        # proxies = {'https': proxy_host}
        # print(proxies)
        proxie = [{'https': 'https://194.187.216.228:53281'}, {'https': 'https://103.111.54.74:8080'}, {'https': 'https://165.138.225.250:8080'}, {'https': 'https://118.178.227.171:80'}, {'https': 'https://34.240.231.232:3128'}, {'https': 'https://85.133.207.14:56728'}, {'https': 'https://109.105.51.18:53281'}, {'https': 'https://35.224.248.29:3128'}, {'https': 'https://190.12.48.158:52305'}, {'https': 'https://46.16.226.10:8080'}, {'https': 'https://31.182.52.156:3129'}, {'https': 'https://190.104.249.148:8080'}, {'https': 'https://218.60.8.98:3129'}, {'https': 'https://185.85.162.32:76'}]
        proies = random.choice(proxie)
        try:
            req = requests.get(url, headers=headers, proxies=proies, verify=False, timeout=5).content.decode()
        except Exception as e:
            print(e)
            continue
        else:
            # prox_list.append(proxies)
            break
    html = etree.HTML(req)
    li_list = html.xpath("//li[@class='feed-wull-item']")
    content_list = []
    for li in li_list:
        item = {}
        item['title'] = li.xpath("./a/div[@class='fw-title']/text()")[0] if len(li.xpath("./a/div[@class='fw-title']/text()"))>0 else None
        item['introduction'] = li.xpath("./a/div[@class='fw-info']/text()")[0] if len(li.xpath("./a/div[@class='fw-info']/text()"))>0 else None
        item['detail_url'] = li.xpath("./a/@href")[0] if len(li.xpath("./a/@href"))>0 else None
        item['collection_count'] = li.xpath("./a/div[@class='fw-data']/a[1]/span/text()")[0] if len(li.xpath("./a/div[@class='fw-data']/a[1]/span/text()"))>0 else None
        item['comment_count'] = li.xpath("./a/div[@class='fw-data']/a[2]/span/text()")[0] if len(li.xpath("./a/div[@class='fw-data']/a[2]/span/text()"))>0 else None
        content_list.append(item)
    return content_list


if __name__ == '__main__':
    # prox_list = list()
    for i in range(1,100):
        url = 'https://www.smzdm.com/list/p{}'.format(i)
        content_list = smzdm_spider(url)
        with open('smzdm.csv','a',encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'introduction', 'detail_url', 'collection_count', 'comment_count'])
            # writer.writeheader()
            for content in content_list:
                writer.writerow(content)
        print("第%s页爬取完成" % i)
        # print(prox_list)