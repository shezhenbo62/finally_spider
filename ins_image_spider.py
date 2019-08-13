#!/usr/bin/python3
# _*_ coding:utf-8 _*_
from fake_useragent import UserAgent
import requests
from lxml import etree
import re,json,csv,os
import time,pymysql
import aiohttp
import asyncio
import queue
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HCVG2RG9845P67JD"
proxyPass = "3265A46978ABE31C"

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

ua = UserAgent()
headers = {
           # 'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'Connection': 'close',
           'cache-control': 'max-age=0',
           'user-agent':ua.random}

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# q队列用于储存图片信息，maxsize为1000
q = queue.Queue(1000)


# 获取网页（文本信息）
async def fetch(session, url):
    async with session.get(url,headers=headers,timeout=10) as response:
        return await response.text(encoding='utf-8')


# 解析网页
async def parser(html,url):
    # 利用lxml将获取到的文本解析成HTML
    soup = etree.HTML(html)
    try:
        next = soup.xpath("//div[@id='list']/@next-cursor")[0]
        uid = soup.xpath("//span[@id='username']/@data-uid")[0]
    except Exception as e:
        print(url)
    else:
        # 获取网页中的图片信息
        div_list = soup.xpath("//div[@id='list']/div")
        for div in div_list:
            img_url = div.xpath("./div/div[1]/img[1]/@src")[0]
            img_name = url.split("/")[-1]+'_'+img_url.split("/")[-1].split("?")[0]
            sql_url = '/images/'+img_name
            creat_time = time.time()
            cate_id = 1
            brand_name = url.split("/")[-1]
            # 将图片的上述信息加入到queue队列中
            q.put([img_name,brand_name,sql_url,img_url,cate_id,creat_time])
        return next,uid


# 对下一页发起post请求
async def parse_next(session,next,uid):
    url = 'https://www.veryins.com/user/bareminerals?next='+next+'&uid='+uid+'&rg=79a7de060d56c4d4a259ecce65bbfd1c'
    data = {'next': next,
            'uid': uid,
            'rg': '79a7de060d56c4d4a259ecce65bbfd1c'}
    async with session.post(url,data=data,headers=headers,timeout=10) as response:
        return await response.text(encoding='utf-8')


# 抓取图片数据
async def get_content(json_html,url):
    count = 0
    json_html = json.loads(json_html)
    json_next = json_html['user']['media']['page_info']['end_cursor']
    has_next_page = json_html['user']['media']['page_info']['has_next_page']
    infos = json_html['user']['media']['nodes']
    for info in infos:
        img_url = info['thumbnail_src']
        img_name = url.split("/")[-1]+'_'+img_url.split("/")[-1].split("?")[0]
        sql_url = '/images/' + img_name
        creat_time = time.time()
        cate_id = 1
        brand_name = url.split("/")[-1]
        q.put([img_name,brand_name,sql_url,img_url,cate_id,creat_time])
        if q.full():
            img_info = q.get()
            # # 使用 execute()  方法执行 SQL
            # sql = '''
            # insert into vae_image(title,keywords,thumb,d88_desc,article_cate_id,create_time)
            # values(%s,%s,%s,%s,%s,%s)
            # '''
            # cursor.execute(sql,img_info)
            # db.commit()
            try:
                response = requests.get(img_info[3], headers=headers, verify=False)
            except Exception as e:
                print("**********代理连接错误，正在更换代理**********")
            else:
                if response.status_code == 200:
                    image = response.content
                    try:
                        with open(img_info[0], 'wb') as f:
                            f.write(image)
                            count += 1
                            print('保存品牌{}第{}张图片成功'.format(img_info[0], count))
                    except Exception as e:
                        filename = img_info[0] + str(count) + '.jpg'
                        with open(filename, 'wb') as f:
                            f.write(image)
                            count += 1
                            print('保存品牌{}第{}张图片成功'.format(img_info[0], count))
        while not q.empty():
            img_info1 = q.get()
            # sql1 = '''
            # insert into vae_image(title,keywords,thumb,d88_desc,article_cate_id,create_time)
            # values(%s,%s,%s,%s,%s,%s)
            # '''
            # cursor.execute(sql1, img_info1)
            # db.commit()
            try:
                response = requests.get(img_info1[3], headers=headers, verify=False)
            except Exception as e:
                print("**********代理连接错误，正在更换代理**********")
            else:
                if response.status_code == 200:
                    image = response.content
                    try:
                        with open(img_info1[0], 'wb') as f:
                            f.write(image)
                            count += 1
                            print('保存品牌{}第{}张图片成功'.format(img_info1[0], count))
                    except Exception as e:
                        filename = img_info1[0] + str(count) + '.jpg'
                        with open(filename, 'wb') as f:
                            f.write(image)
                            count += 1
                            print('保存品牌{}第{}张图片成功'.format(img_info1[0], count))
    return json_next,has_next_page


# 处理网页
async def download(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        next,uid = await parser(html,url)
        json_html = await parse_next(session,next,uid)
        json_next,has_next_page = await get_content(json_html,url)
        i = 2
        while has_next_page:
            print("爬取%s品牌第%d页成功" % (url.split("/")[-1], i))
            json_html = await parse_next(session, json_next, uid)
            json_next, has_next_page = await get_content(json_html, url)
            i += 1

# 全部网页
urls = ['https://www.veryins.com/aesopskincare', 'https://www.veryins.com/acquadiparma_official',
        'https://www.veryins.com/amouageofficial', 'https://www.veryins.com/anastasiabeverlyhills',
        'https://www.veryins.com/aromatherapyassociates',
        'https://www.veryins.com/bareminerals', 'https://www.veryins.com/beautyblender', 'https://www.veryins.com/benefitfrance',
        'https://www.veryins.com/bobbibrownthailand', 'https://www.veryins.com/burberry', 'https://www.veryins.com/bulgariofficial',
        'https://www.veryins.com/byterryofficial', 'https://www.veryins.com/officialbyredo', 'https://www.veryins.com/cartier',
        'https://www.veryins.com/cartier', 'https://www.veryins.com/chanelofficial', 'https://www.veryins.com/chantecaille',
        'https://www.veryins.com/louboutinworld', 'https://www.veryins.com/clarisonic', 'https://www.veryins.com/ctilburymakeup',
        'https://www.veryins.com/clarinsofficial', 'https://www.veryins.com/cliniquebrasil', 'https://www.veryins.com/coverfx',
        'https://www.veryins.com/cosmedecortejp', 'https://www.veryins.com/diorparfums', 'https://www.veryins.com/diptyque',
        'https://www.veryins.com/drjart', 'https://www.veryins.com/drsebagh', 'https://www.veryins.com/ellisfaascosmetics',
        'https://www.veryins.com/embryolisse', 'https://www.veryins.com/elizabetharden', 'https://www.veryins.com/eve_lom',
        'https://www.veryins.com/esteelauder', 'https://www.veryins.com/firstaidbeauty', 'https://www.veryins.com/foreo',
        'https://www.veryins.com/fredericmalle', 'https://www.veryins.com/fragonardparfumeurofficiel',
        'https://www.veryins.com/giorgioarmanibellevue', 'https://www.veryins.com/glamglowrussia', 'https://www.veryins.com/gucci',
        'https://www.veryins.com/guerlain', 'https://www.veryins.com/hermes', 'https://www.veryins.com/hourglasscosmetics',
        'https://www.veryins.com/givenchybeauty', 'https://www.veryins.com/gelle_freres', 'https://www.veryins.com/itcosmetics',
        'https://www.veryins.com/hrperfumes', 'https://www.veryins.com/jomalonelondon', 'https://www.veryins.com/lamer',
        'https://www.veryins.com/laprairie', 'https://www.veryins.com/lauramercier', 'https://www.veryins.com/lelabofragrances',
        'https://www.veryins.com/maccosmeticsrussia', 'https://www.veryins.com/marcjacobsfragrances',
        'https://www.veryins.com/morphebrushes', 'https://www.veryins.com/narsobsession', 'https://www.veryins.com/natashadenona',
        'https://www.veryins.com/mynuface', 'https://www.veryins.com/nyxcosmetics_es', 'https://www.veryins.com/origins',
        'https://www.veryins.com/omorovicza', 'https://www.veryins.com/paulandjoe_beaute', 'https://www.veryins.com/paulaschoice',
        'https://www.veryins.com/perriconemd', 'https://www.veryins.com/peterthomasrothofficial', 'https://www.veryins.com/rmkofficial',
        'https://www.veryins.com/skinesis', 'https://www.veryins.com/sisleyparisofficial', 'https://www.veryins.com/stilacanada',
        'https://www.veryins.com/suqqu_official', 'https://www.veryins.com/tataharperskincare'
        ]

# 统计该爬虫的消耗时间
print('#' * 50)
t1 = time.time() # 开始时间

# # 将q队列中的数据存入mysql数据库
# # 打开数据库连接
# db = pymysql.connect(host='192.168.2.223',user='D88Photo',password='2012Dibaba',db='D88Photo',port=3306)
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()

# file = '/www/wwwroot/d88-photo/vaeThink/public/images'
file = 'D:/yanzhengma'
if os.path.exists(file):
    os.chdir(file)
else:
    os.mkdir(file)
    os.chdir(file)

# 利用asyncio模块进行异步IO处理
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(download(url)) for url in urls]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)

# # 关闭数据库连接
# db.close()

# print(table)
t2 = time.time() # 结束时间
print('使用aiohttp，总共耗时：%s' % (t2 - t1))
print('#' * 50)