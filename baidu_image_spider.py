#!/usr/bin/python3
# _*_ coding:utf-8 _*_
from fake_useragent import UserAgent
import requests
from lxml import etree
import re,json,os
import time,pymysql
import queue
from requests.packages.urllib3.exceptions import InsecureRequestWarning

ua = UserAgent()
headers = {
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'user-agent':ua.random,
            # 'Cookie': 'winWH=%5E6_1920x943; BDIMGISLOGIN=0; BDqhfp=Acqua%2BDi%2BParma%26%260-10-1undefined%26%260%26%261; BAIDUID=E9310D73962A48054C7B8F15419E1864:FG=1; BIDUPSID=E9310D73962A48054C7B8F15419E1864; PSTM=1535941588; MCITY=-%3A; BDUSS=U5HTU1TWHAyb2NaNHl-SEZoSUNDZUw1RDBYNzJGT2ludFFDRkxhQXNtNVl5a3RjQVFBQUFBJCQAAAAAAAAAAAEAAAAJTXMM0sB2aU4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFg9JFxYPSRcd; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; delPer=0; PSINO=6; BDRCVFR[4r8LXJfwh-6]=I67x6TjHwwYf0; H_PS_PSSID=; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; firstShowTip=1; cleanHistoryStatus=0; userFrom=null; indexPageSugList=%5B%22Median%22%2C%22Median%20%E9%BA%A6%E8%BF%AA%E5%AE%89%22%2C%22Acqua%20Di%20Parma%22%2C%22Acqua%20Di%20Parma%2F%E5%B8%95%E5%B0%94%E7%8E%9B%E4%B9%8B%E6%B0%B4%22%2C%22Aesop%22%2C%22Aesop%2F%E4%BC%8A%E7%B4%A2%22%2C%22lancome%22%2C%22ysl%22%2C%22mac%22%5D',
            'X-Requested-With': 'XMLHttpRequest'}

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# q队列用于储存图片信息
q = queue.Queue()


def get_proxy():
    return requests.get('http://119.23.203.63:6066/get/').content


# 获取网页（文本信息）
def parse(url):
    proxy = get_proxy()
    response = requests.get(url,headers=headers,proxies={"http": "http://{}".format(proxy)},timeout=10)
    return response.text


# 解析网页
def get_info(html, brand):
    # 利用re正则匹配图片信息
    img_urls = re.findall(r'"thumbURL":"(.*?)"',html)
    for img_url in img_urls:
        img_name = brand + '_' + img_url.split("/")[-1]
        sql_url = '/images/' + img_name
        cate_id = 1
        brand_name = brand
        create_time = time.time()
        # 将图片的上述信息加入到queue队列中
        q.put([img_name, brand_name, sql_url, img_url, cate_id, create_time])


# 对下一页发起get请求
def parse_next(brand, page):
    url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30'.format(brand,brand,page)
    proxy = get_proxy()
    response = requests.get(url,headers=headers,proxies={"http": "http://{}".format(proxy)},timeout=10)
    return response


# 抓取图片数据
def get_content(json_html,brand,count):
    try:
        json_html = json.loads(json_html.text)
    except Exception as f:
        print('数据类型异常，忽略该条数据')
    else:
        infos = json_html['data']
        for info in infos:
            proxy = get_proxy()
            try:
                img_url = info['thumbURL']
            except Exception as e:
                print(info)
            else:
                img_name = brand + '_' + img_url.split("/")[-1]
                sql_url = '/images/' + img_name
                creat_time = time.time()
                cate_id = 1
                brand_name = brand
                q.put([img_name, brand_name, sql_url, img_url, cate_id, creat_time])
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
    return count


if __name__ == '__main__':
    # 全部网页
    brand_list = ['Aesop', 'Acqua Di Parma', 'Aerin', 'Amouage', 'Aanastasia Beverly Hills', 'Alpha Hydrox',
                  'Aromatherapy Associates', 'Bare Minerals', 'Beauty Blender', 'Benefit', 'Bobbi Brown', 'Burberry',
                  'Bvlgari', 'By Terry', 'Byredo', 'Cartier', 'Caudalie', 'Chanel', 'Chantecaille', 'Christian Louboutin',
                  'Clarisonic', 'Charlotte Tilbury', 'Clarin', 'Clinique', 'Cover fx', 'Creed', 'Decorte', 'Dior',
                  'Diptyque', 'Dr.Jart+', 'Dr.Sebagh', 'Ellis Faas', 'Embryolisse', 'Elizabeth Arden', 'Eve Lom',
                  'Estee Lauder', 'First Aid Beauty', 'Foreo', 'Frederic Malle', 'Fragonard', 'Giorgio Armani', 'Glam Glow',
                  'Gucci', 'Guerlain', 'Hermes', 'Hourglass', 'Huda Beauty', 'GIVENCHY', 'GELLÉ FRÈRES', 'It Cosmetics',
                  'HR', 'Jo Malone London', 'Lamer', 'la prairie', 'Laura Mercier', 'LE LABO', 'M.A.C', 'Marc Jacobs',
                  'Morphe', 'Nars', 'Natasha Denona', 'NuFace', 'NYX Professional Makeup', 'Origins', 'Omorovicza',
                  'Paul&Joe', "Paula's Choice", 'Perricone MD', 'Peterthomasroth', 'RMK', 'Sarah Chapman', 'Sisley',
                  'Stila', 'SUQQU', 'Tata Harper', 'The Organic Pharmacy', 'Tom Ford', 'Too cool for school', 'Too Faced',
                  'Trish McEvoy', 'Ultrasun', 'Urban Decay', 'VISEART', 'Yves Saint laurent', 'Zoeva', 'Ahava',
                  'Algenist奥杰尼', 'Amore Pacific', 'Laneige', 'Becca', 'Sulwhasoo', 'Hera', 'IOPE', 'Biossance', 'Bite',
                  'Darphin', 'Drunk Elephant', 'Fenty Beauty ', 'Fresh', 'Kora', "L'OCCITANE", 'Lancome', 'Make up for ever',
                  'Ole Henriksen', 'Pat McGrath', 'Philosophy', 'Shiseido', 'ShuUemura', 'SK-II', 'Sunday riley', 'Tarte',
                  'Tatcha', 'Chloé', 'Atelier Cologne', 'Aveda', 'Bioeffect', 'Belif', 'Clé de Peau Beauté', 'Color Mad',
                  'POLA', 'ReVive', 'WHOO', 'Valmont', 'Erno Laszlo', 'Elixir', 'Albion', 'IPSA', 'HR', 'Fancl',
                  'SEKKISEI', 'Jurlique', 'Lunasol', 'Laduree', 'Refa', 'Ya-man', 'Hitachi', 'Exideal', 'The Beautools',
                  'Koh Gen Do 江原道', 'The Ginza', 'La Roche-Posay', 'TAKAMI', 'Covermark', 'RMK', 'Chicca', 'Elegance',
                  'Canmake', 'Clarisonic', 'Biotherm', 'CLIO', 'Forbelovedone', '百雀羚', '双妹', '相宜本草', '玉泽', '谢馥春',
                  '戴春林', '玛丽黛佳', '毛戈平', 'ADDICTION', 'Zelens', 'Color Pop', '3CE', 'Banilaco', 'Curel', 'Freeplus',
                  'Kate', 'Artis', '大宝', 'Chikuhodo', 'Kanebo', 'Sofina', '肌美精', 'MINON', 'Avène', '完美日记', 'HAIRMAX',
                  'REAL TECHNIQUES', 'URIAGE', 'JMsolution', 'LOREAL 欧莱雅', 'Elégance雅莉格丝', 'AHC', '美宝莲', 'Unny',
                  'VIDIVICI', 'PDC 古法', 'SPC', 'Cure 水润', 'Muji ', 'Revlon 露华浓', 'Bb Laboratories', 'spa treatment',
                  'Revital', 'Nature republic', 'DMC 欣兰', 'Rosette', 'Rohto 乐敦', 'utena 佑天兰', 'Mario Badescu',
                  "AGE 20's 二十岁", 'Papa recipe 爸爸的礼物', 'Purevivi', 'Kose 高丝', 'Shangpree 香蒲丽', 'Bourjois 妙巴黎',
                  'Farmacy', '森田药妆', 'Amino mason', 'Creer Beaute凡尔赛', 'Saborino', 'Quality first皇后的秘密', '艾杜纱',
                  '熊野油脂', 'Orbis 奥蜜思', '松山油脂', 'Flow fushi', '豆腐の盛田屋', 'Daiso 大创', 'Melty wink', 'CeraVe',
                  'Nexcare 3M', 'Grow gorgeous', 'The body shop', 'Moroccanoil', 'Lush', 'Yanagiya 柳屋', 'Avalon 阿瓦隆',
                  'Batiste 碧缇丝', "Mane'n tail", 'Dr.groot', 'Aussie 袋鼠', 'Tamano hada 玉肌', 'Moist Diane 黛丝恩',
                  'Milbon玫丽盼', 'Amore 爱茉莉', 'Loretta', 'Alpecin 阿佩辛', 'KAO', 'COW 牛牌', 'Sesderma', 'Deonatulle',
                  'Lion 狮王', 'Beauty buffet', 'House of rose ', 'Venus Lab', 'Swisse', 'Median 麦迪安', 'Marvis',
                  'pROPOLINSE', 'Ora2', 'G.U.M', 'Crest 佳洁士']

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
    for brand in brand_list:
        url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1546999901926_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word={}'.format(brand)
        html = parse(url)
        get_info(html, brand)
        for i in range(30):
            page = (i+1)*30
            json_html = parse_next(brand, page)
            if json_html.status_code == 200:
                count = get_content(json_html,brand,count)

    # # 关闭数据库连接
    # db.close()

    t2 = time.time() # 结束时间
    print('总共耗时：%s' % (t2 - t1))
    print('#' * 50)