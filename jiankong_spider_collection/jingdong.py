# _*_ coding:utf-8 _*_
from fake_useragent import UserAgent
import requests
from lxml import etree
import re,json,csv
import time,random,pymongo
import aiohttp
import asyncio
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

ua = UserAgent()
headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'cache-control': 'max-age=0',
           'user-agent':ua.random}

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# table表格用于储存书本信息
table = []


# 获取网页（文本信息）
async def fetch(session, url):
    async with session.get(url,headers=headers) as response:
        return await response.text(encoding='utf-8')


# 解析网页
async def parser(html,url):

    # 利用lxml将获取到的文本解析成HTML
    soup = etree.HTML(html)
    # 获取网页中的畅销书信息
    li_list = soup.xpath("//ul[@class='gl-warp clearfix']/li")[:15]
    content_list = []
    for li in li_list:
        item = {}
        pro_title = li.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()") if len(li.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()"))>0 else None
        item['pro_title'] = ''.join(pro_title)
        # item['brand_name'] = li.xpath(".//font[@class='skcolor_ljg']/text()")[0] if len(li.xpath(".//font[@class='skcolor_ljg']/text()"))>0 else None
        # data = li.xpath("//div[@class='p-icons']")[0]
        # activity = data.xpath("string(.)")
        # shop_name = li.xpath(".//div[@class='p-shop']/span/a/text()")[0] if len(li.xpath(".//div[@class='p-shop']/span/a/text()"))>0 else None
        # shop_url = 'https:'+li.xpath(".//div[@class='p-shop']/span/a/@href")[0] if len(
        #     li.xpath(".//div[@class='p-shop']/span/a/@href")) > 0 else None
        item['pro_pic'] = 'https:'+li.xpath(".//div[@class='p-img']/a/img/@source-data-lazy-img")[0] if len(li.xpath(".//div[@class='p-img']/a/img/@source-data-lazy-img"))>0 else None
        item['pro_website'] = 'https:'+li.xpath(".//div[@class='p-img']/a/@href")[0] if len(li.xpath(".//div[@class='p-img']/a/@href"))>0 else None
        item['pro_price_old'] = li.xpath(".//div[@class='p-price']/strong/i/text()")[0] if len(li.xpath(".//div[@class='p-price']/strong/i/text()"))>0 else None
        # 将每本畅销书的上述信息加入到table中
        # table.append([pro_title,brand_name,pro_pic,pro_website,pro_price_new])
        content_list.append(item)
    content_item = {}
    content_item['pro_list'] = json.dumps(content_list,ensure_ascii=False)
    content_item['brand'] = re.findall(r'keyword=(.*?)&enc=utf-8',url)[0]
    table.append(content_item)

# 处理网页
async def download(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        await parser(html,url)

# 全部网页
# brand_list = ['百雀羚','美康粉黛','兰蔻','玛丽黛佳','大宝','相宜本草']
datas = pd.read_excel('C:/Users/Administrator/Desktop/new_info.xls')
a = datas.loc[datas['source'] == 'jd']
brand_list = a['brand'].values.tolist()
urls = ['https://search.jd.com/Search?keyword=%s&enc=utf-8&spm=2.1.1'%i for i in brand_list]

# 统计该爬虫的消耗时间
print('#' * 50)
t1 = time.time() # 开始时间

# 利用asyncio模块进行异步IO处理
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(download(url)) for url in urls]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)

# 将table转化为pandas中的DataFrame并保存为CSV格式的文件
# df = pd.DataFrame(table, columns=['title','brand_name','activity','shop_name','shop_url'])
# df.to_csv('D:/dangdang.csv',index=False)
for info in table:
    with open('C:/Users/Administrator/Desktop/info1.csv', 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=['pro_list','brand'])
        writer.writerow(info)

print(table)
t2 = time.time() # 结束时间
print('使用aiohttp，总共耗时：%s' % (t2 - t1))
print('#' * 50)