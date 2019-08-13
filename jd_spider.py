import requests
from lxml import etree
import time
import csv
import random


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


# 定义函数抓取每页前30条商品信息
def crow_first(n, keyword):
    # 构造每一页的url变化
    url = 'https://search.jd.com/Search?keyword='+keyword+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page=' + str(
        2 * n - 1)
    head = {'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/s_new.php?keyword=%E8%8A%B1%E7%8E%8B%E8%87%AA%E8%90%A5&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=3&s=61&click=0',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E8%8A%B1%E7%8E%8B%E8%87%AA%E8%90%A5&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=3&s=61&click=0',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'shshshfpa=6776cfe5-3dcb-a849-8490-9e72806fdd35-1535945241; shshshfpb=08e7eb8224927ca3eeda6255336854e51ab6f40ec97c208f45b8caa191; xtest=9997.cf6b6759; qrsc=3; pinId=5Ux_jKaGlGNiUsqGcz67ULV9-x-f3wj7; user-key=24de112c-366f-4105-9ec3-3f84112b26f1; ipLoc-djd=1-72-2799-0; cn=0; PCSYCityID=1607; __jdu=1161385693; ipLocation=%u5317%u4EAC; areaId=1; unpl=V2_ZzNtbUBTSkJwCxJVfhkPAGIEFV9KBEZBIgASUH8ZXwQzUUFbclRCFXwURlRnGF8UZwUZXUpcQhBFCEdkeylVAGQLF1hyVkJvdVxGBCkQXAJlA0VYEVAUQXI4RVRLGWwFZwQSX0tTRB13OHZTSxxVBGAFE1lygsibrIzAgMW5bAJiBBdYQ1ZAJXQ4R2Qtd1wEZgITXEFQRBY4CEZTextVAWALEG1DZ0A%3d; __jdv=122270672|p.yiqifa.com|t_1_842944|tuiguang|358f42e041b446639b4ef9e55120ecb7|1541150343942; __jdc=122270672; rkv=V0000; mt_xid=V2_52007VwMSVV1aW14YQRtsDDJRRwVZUFZGG0gbVBliAxMGQVBbCB1VEVsAMlZAV1kKVltPeRpdBW4fElJBWVVLHkESWQFsAxZiX2hSahxNGVQAZQESV21YV1wY; 3AB9D23F7A4B3C9B=SRSFDKQAME6KEG2ETDPUPL6BZJ7BJJ5Y7EVSPDF56SLIWBYNKSUIRLGALVVOJOVTIQ4R6C5MOUIQQVZEIONHJ26DPQ; _gcl_au=1.1.534209513.1541472817; __jda=122270672.1161385693.1535945240.1541467695.1541475086.151; shshshfp=f3856d1c446473cfa8f6188a6ba4dd62; __jdb=122270672.2.1161385693|151.1541475086; shshshsID=ec17ab5a213c2154b51c4fff3bd7bb65_2_1541475322728',
            'user-agent': random.choice(USER_AGENTS)
            }
    r = requests.get(url, headers=head)
    # 指定编码方式，不然会出现乱码
    r.encoding = 'utf-8'
    html1 = etree.HTML(r.text)
    # 定位到每一个商品标签li
    datas = html1.xpath('//li[contains(@class,"gl-item")]')
    # 将抓取的结果保存到本地CSV文件中
    with open('JD_Phone.csv', 'a', newline='', encoding='utf-8')as f:
        write = csv.writer(f)
        for data in datas:
            p_price = data.xpath('div/div[@class="p-price"]/strong/i/text()')
            p_comment = data.xpath('div/div[5]/strong/a/text()')
            p_name = data.xpath('div/div[@class="p-name p-name-type-2"]/a/em')
            # 这个if判断用来处理那些价格可以动态切换的商品，比如上文提到的小米MIX2，他们的价格位置在属性中放了一个最低价
            if len(p_price) == 0:
                p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')
                # xpath('string(.)')用来解析混夹在几个标签中的文本
            write.writerow([p_name[0].xpath('string(.)'), p_price[0], p_comment[0]])
    f.close()


# 定义函数抓取每页后30条商品信息
def crow_last(n, keyword):
    # 获取当前的Unix时间戳，并且保留小数点后5位
    a = time.time()
    b = '%.5f' % a
    url = 'https://search.jd.com/s_new.php?keyword='+keyword+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq='+keyword+'&cid2=653&cid3=655&page=' + str(
        2 * n) + '&s=' + str(48 * n - 20) + '&scrolling=y&log_id=' + str(b)
    head = {'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/s_new.php?keyword=%E8%8A%B1%E7%8E%8B%E8%87%AA%E8%90%A5&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=4&s=87&scrolling=y&log_id=1541475701.67096&tpl=1_M&show_items=992315,362110,1248885,862395,7062950,992314,3369865,1222511,2181099,1946989,6481659,1750032,3426300,1551733,1228009,1248890,1938013,1255053,3171024,3399866,1248889,1551735,1689064,3170842,2123169,2208641,1367483,7154390,1946979,1947006',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E8%8A%B1%E7%8E%8B%E8%87%AA%E8%90%A5&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=3&s=61&click=0',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'shshshfpa=6776cfe5-3dcb-a849-8490-9e72806fdd35-1535945241; shshshfpb=08e7eb8224927ca3eeda6255336854e51ab6f40ec97c208f45b8caa191; xtest=9997.cf6b6759; qrsc=3; pinId=5Ux_jKaGlGNiUsqGcz67ULV9-x-f3wj7; user-key=24de112c-366f-4105-9ec3-3f84112b26f1; ipLoc-djd=1-72-2799-0; cn=0; PCSYCityID=1607; __jdu=1161385693; ipLocation=%u5317%u4EAC; areaId=1; unpl=V2_ZzNtbUBTSkJwCxJVfhkPAGIEFV9KBEZBIgASUH8ZXwQzUUFbclRCFXwURlRnGF8UZwUZXUpcQhBFCEdkeylVAGQLF1hyVkJvdVxGBCkQXAJlA0VYEVAUQXI4RVRLGWwFZwQSX0tTRB13OHZTSxxVBGAFE1lygsibrIzAgMW5bAJiBBdYQ1ZAJXQ4R2Qtd1wEZgITXEFQRBY4CEZTextVAWALEG1DZ0A%3d; __jdv=122270672|p.yiqifa.com|t_1_842944|tuiguang|358f42e041b446639b4ef9e55120ecb7|1541150343942; __jdc=122270672; rkv=V0000; mt_xid=V2_52007VwMSVV1aW14YQRtsDDJRRwVZUFZGG0gbVBliAxMGQVBbCB1VEVsAMlZAV1kKVltPeRpdBW4fElJBWVVLHkESWQFsAxZiX2hSahxNGVQAZQESV21YV1wY; 3AB9D23F7A4B3C9B=SRSFDKQAME6KEG2ETDPUPL6BZJ7BJJ5Y7EVSPDF56SLIWBYNKSUIRLGALVVOJOVTIQ4R6C5MOUIQQVZEIONHJ26DPQ; _gcl_au=1.1.534209513.1541472817; __jda=122270672.1161385693.1535945240.1541467695.1541475086.151; shshshfp=f3856d1c446473cfa8f6188a6ba4dd62; __jdb=122270672.2.1161385693|151.1541475086; shshshsID=ec17ab5a213c2154b51c4fff3bd7bb65_2_1541475322728',
            'user-agent': random.choice(USER_AGENTS)
            }
    r = requests.get(url, headers=head)
    r.encoding = 'utf-8'
    html1 = etree.HTML(r.text)
    datas = html1.xpath('//li[contains(@class,"gl-item")]')
    with open('JD_Phone.csv', 'a', newline='', encoding='utf-8')as f:
        write = csv.writer(f)
        for data in datas:
            p_price = data.xpath('div/div[@class="p-price"]/strong/i/text()')
            p_comment = data.xpath('div/div[5]/strong/a/text()')
            p_name = data.xpath('div/div[@class="p-name p-name-type-2"]/a/em')
            if len(p_price) == 0:
                p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')
            write.writerow([p_name[0].xpath('string(.)'), p_price[0], p_comment[0]])
    f.close()


if __name__ == '__main__':
    keyword = input("请输入要爬取的产品名称：")
    for i in range(1, 10):
        # 下面的print函数主要是为了方便查看当前抓到第几页了
        print('***************************************************')
        try:
            print('   First_Page:   ' + str(i))
            crow_first(i, keyword)
            print('   Finish')
        except Exception as e:
            print(e)
        print('------------------')
        try:
            print('   Last_Page:   ' + str(i))
            crow_last(i, keyword)
            print('   Finish')
        except Exception as e:
            print(e)