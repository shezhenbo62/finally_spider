# _*_ coding:utf-8 _*_
from fake_useragent import UserAgent
import requests
from queue import Queue
from lxml import etree
import re,json,csv,datetime
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
           'user-agent': ua.random}

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# 获取网页（文本信息）
async def fetch(session, url):
    async with session.get(url,headers=headers) as response:
        return await response.text(encoding='utf-8')


# 解析网页
async def parser(html,url):
    html_lxml = etree.HTML(html)
    li_list = html_lxml.xpath("//ul[@data-test='product-card-list']/li")
    table = []
    for li in li_list:
        brand_name = li.xpath(".//h3/text()")[0]
        title = li.xpath(".//p/text()")[0]
        link = 'https://www.farfetch.cn' + li.xpath("./a/@href")[0]
        final_price = int(li.xpath("./a/div[2]/div/span[last()]/text()")[0].replace("¥", "").replace(",", ""))
        original_price = int(li.xpath("./a/div[2]/div/span[1]/text()")[0].replace("¥", "").replace(",", ""))
        offers = original_price - final_price
        discount = li.xpath("./a/div[2]/div/span[2]/text()")[0]
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_list = [brand_name, title, link, final_price, original_price, offers, discount, create_time]
        table.append(info_list)
    pd_brand = pd.DataFrame(table, columns=['brand_name', 'title', 'link', 'final_price', 'original_price',
                                            'offers', 'discount', 'create_time'])
    pd_brand.to_csv("C:/Users/Administrator/Desktop/farfetch.csv", index=False, mode='a', header=False)
    next_url = url+html_lxml.xpath("//a[@data-test='page-next']/@href")[0]\
        if len(html_lxml.xpath("//a[@data-test='page-next']/@href")) > 0 else None
    tabindex = html_lxml.xpath("//a[@data-test='page-next']/@tabindex")[0]
    print(tabindex)
    print('已成功爬取该网址：', next_url)
    return next_url, tabindex


# 处理网页
async def download(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        next_url, tabindex = await parser(html, url)
        while tabindex == '0':
            html = await fetch(session, next_url)
            next_url, tabindex = await parser(html, url)


def main():
    # 全部网页
    urls = ['https://www.farfetch.cn/cn/shopping/women/sale/all/items.aspx',
            'https://www.farfetch.cn/cn/shopping/men/sale/all/items.aspx']

    # 统计该爬虫的消耗时间
    print('#' * 50)
    t1 = time.time()  # 开始时间

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(download(url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    t2 = time.time() # 结束时间
    print('使用aiohttp，总共耗时：%s' % (t2 - t1))
    print('#' * 50)


if __name__ == '__main__':
    main()