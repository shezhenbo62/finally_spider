#!/usr/bin/python3
# _*_ coding:utf-8 _*_
from fake_useragent import UserAgent
import requests
from lxml import etree
import re,json,csv,os
import time,pymysql
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

# q队列用于储存图片信息，maxsize为20
q = queue.Queue(20)


def get_proxy():
    return requests.get('http://119.23.203.63:6066/get/').content


# 获取网页（文本信息）
def fetch(url):
    proxy = get_proxy()
    response = requests.get(url,headers=headers,proxies={"http": "http://{}".format(proxy)},timeout=10)
    return response.text


# 解析网页
def parser(html,url):
    # 利用lxml将获取到的文本解析成HTML
    soup = etree.HTML(html)
    next = soup.xpath("//div[@id='list']/@next-cursor")[0] if len(soup.xpath("//div[@id='list']/@next-cursor"))>0 else None
    uid = soup.xpath("//span[@id='username']/@data-uid")[0] if len(soup.xpath("//span[@id='username']/@data-uid"))>0 else None
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
def parse_next(next,uid):
    url = 'https://www.veryins.com/user/bareminerals?next='+next+'&uid='+uid+'&rg=79a7de060d56c4d4a259ecce65bbfd1c'
    data = {'next': next,
            'uid': uid,
            'rg': '79a7de060d56c4d4a259ecce65bbfd1c'}
    proxy = get_proxy()
    response = requests.post(url,data=data,headers=headers,proxies={"http": "http://{}".format(proxy)},timeout=10)
    return response


# 抓取图片数据
def get_content(json_html,url,count):
    json_html = json.loads(json_html.text)
    json_next = json_html['user']['media']['page_info']['end_cursor']
    has_next_page = json_html['user']['media']['page_info']['has_next_page']
    infos = json_html['user']['media']['nodes']
    for info in infos:
        proxy = get_proxy()
        img_url = info['thumbnail_src']
        img_name = url.split("/")[-1]+'_'+img_url.split("/")[-1].split("?")[0]
        sql_url = '/images/' + img_name
        creat_time = time.time()
        cate_id = 1
        brand_name = url.split("/")[-1]
        q.put([img_name,brand_name,sql_url,img_url,cate_id,creat_time])
        if q.full():
            img_info = q.get()
            # 使用 execute()  方法执行 SQL
            sql = '''
            insert into vae_image(title,keywords,thumb,d88_desc,article_cate_id,create_time)
            values(%s,%s,%s,%s,%s,%s)
            '''
            cursor.execute(sql,img_info)
            db.commit()
            try:
                response = requests.get(img_info[3], headers=headers, proxies={"http": "http://{}".format(proxy)},timeout=10, verify=False)
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
        sql1 = '''
        insert into vae_image(title,keywords,thumb,d88_desc,article_cate_id,create_time)
        values(%s,%s,%s,%s,%s,%s)
        '''
        cursor.execute(sql1, img_info1)
        db.commit()
        try:
            response = requests.get(img_info1[3], headers=headers, proxies={"http": "http://{}".format(proxy)},timeout=10, verify=False)
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
    return json_next,has_next_page,count


if __name__ == '__main__':
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

    # 将q队列中的数据存入mysql数据库
    # 打开数据库连接
    db = pymysql.connect(host='localhost',user='D88Photo',password='2012Dibaba',db='D88Photo',port=3306)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    file = '/www/wwwroot/d88-photo/vaeThink/public/images'
    # file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    for url in urls:
        html = fetch(url)
        next, uid = parser(html, url)
        json_html = parse_next(next, uid)
        if json_html.status_code == 200:
            json_next, has_next_page, count = get_content(json_html, url, count)
            i = 2
            while has_next_page:
                print("爬取%s品牌第%d页成功" % (url.split("/")[-1], i))
                json_html = parse_next(json_next, uid)
                if json_html.status_code == 200:
                    json_next, has_next_page, count = get_content(json_html, url, count)
                    i += 1

    # 关闭数据库连接
    db.close()

    t2 = time.time() # 结束时间
    print('总共耗时：%s' % (t2 - t1))
    print('#' * 50)