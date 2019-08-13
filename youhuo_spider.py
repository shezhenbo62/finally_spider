import requests
from lxml import etree
import csv
import random


def yhspider(url):
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
               'cookie': 'udid=889d5f4e-a7fb-4da9-8858-26940878b2c0; yohobuy_session_cookie=mfP-9eEO-A4dkRreIedB2Q.MyOUOvzZna1UzLsnn6pXVz5xYAwhGbBwZP-T-WTgbUH-7d-V1eEIZhQJV2McBI1Zx2VjKop958LDcbRDFokbgfgOxsJTb9iEsFI-L2YIpv2D5sUOgv4l_zvsLsp2rCnonaCUOmNiUQGhbeMpDpMxx_QaXIrnOGe7fU8QZGmJ5TgLL06yYCXLn_V0gBItajtx.1541058524978.86400000.MwU6RwYJ03f_5eLJyxobzi3UZLjZ1HjX6L9v9Epg5Hk; yohobuy_session=s%3AJnif5ALH7j-VYdlDzsnFW0ykIBwtFTAV.6YO6bHataL%2Fvkh06kmhWBcWUniK0NnN0NZ34f4Zf0kw; _yasvd=562385672; mkt_code=100000000008051; Hm_lvt_65dd99e0435a55177ffda862198ce841=1541058526; __utma=69251608.313830384.1541058526.1541058526.1541058526.1; __utmc=69251608; __utmz=69251608.1541058526.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.313830384.1541058526; _gid=GA1.2.889808035.1541058526; __utmt=1; _pzfxuvpc=1541058525989%7C1062157453108893054%7C10%7C1541059630003%7C1%7C%7C5192942424602170210; _pzfxsvpc=5192942424602170210%7C1541058525989%7C10%7Chttps%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DtwK0e-zuDFZXM5UF3Ddq9rsw3YrPNR6qcyOhf_XoZvvBmsHJ76N1rAPCUCM2nu12vvtl3nkj6a3HhL8ncpru7JMevIfY7dVnoB9YBmJcNm3%26wd%3D%26eqid%3D9c55bc1c00001c45000000065bdaafd9; Hm_lpvt_65dd99e0435a55177ffda862198ce841=1541059630; ajaxreqid=3b882f3b-5ff4-4f3d-b6d1-c7a2f726afc0; docreqid=3b882f3b-5ff4-4f3d-b6d1-c7a2f726afc0; __utmb=69251608.10.10.1541058526',
               'referer': 'https://www.yohobuy.com/shop/stage-1504.html?domain=stage',
               'user-agent': random.choice(USER_AGENTS)}

    resp = requests.get(url, headers=headers).content.decode()
    html = etree.HTML(resp)
    li_list = html.xpath("//div[@class='brands-list']//ul[@class='clearfix']/li")
    content_list = list()
    for li in li_list:
        item = dict()
        item['brand_name'] = li.xpath("./a/span/text()")[0]
        item['detail_url'] = 'https:' + li.xpath("./a/@href")[0]
        item['hot'] = 'Hot' if len(li.xpath("./i/text()"))>0 else None
        try:
            detail_resp = requests.get(item['detail_url'], headers=headers).content.decode()
        except Exception as e:
            print(e)
        else:
            detail_html = etree.HTML(detail_resp)
            genre = detail_html.xpath("//div[@class='sort-container']/ul/li/h3/@title")
            a = '/'
            for i in range(len(genre)):
                a = a + genre[i]
            item['genre'] = a
            print(item)
            content_list.append(item)
    with open('C:/Users/Administrator/Desktop/youhuo.csv', 'a', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f,
                                fieldnames=['brand_name','detail_url','hot','genre'])
        # writer.writeheader()
        for content in content_list:
            writer.writerow(content)
    return content_list


if __name__ == '__main__':
    url = 'https://www.yohobuy.com/boys-brands/'
    yhspider(url)