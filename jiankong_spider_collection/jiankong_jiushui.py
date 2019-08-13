# -*- coding: utf-8 -*-
import requests
import os
import time,re,json,csv
from fake_useragent import UserAgent
from urllib import parse
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning

words_base = ['特惠','折','减','新品','上新','狂欢','发售','活动','开抢','特卖','赠','联名','礼遇','优惠','sale']
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HO31L31645P86F8D"
proxyPass = "AA00DFD49A7B401B"

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


def get_Page(url,headers,brand_name):
    response = requests.get(url,headers=headers,verify=False)
    if response.status_code == 200:
        with open("C:/Users/Administrator/Desktop/img_huodong.csv",'a',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name,url])
        print(brand_name,url)
        return response.text


def get_Page1(url,headers,brand_name):
    response = requests.get(url,headers=headers,verify=False)
    if response.status_code == 200:
        for word in words_base:
            if word in response.text:
                with open("C:/Users/Administrator/Desktop/huodong.csv",'a',encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([brand_name,url, "活动类型：%s" % word])
                print(url + "品牌在做活动，"+"活动类型：%s"%word)
                break
        return response.text


def get_Page_itoen(url,ua,brand_name):
    formdata = {'functionId': 'getModData',
'body': json.dumps([{"type":"module","moduleId":-288,"moduleData":"{\"lunboGoodsGroup\":{\"materialCode\":\"1JBv3wFlKadGzWyM\",\"moduleCreate\":2,\"bi\":0,\"type\":\"2\",\"showNum\":\"2\"},\"moduleMarginBottom\":[],\"template\":{\"type\":1,\"templateId\":\"-99888\"}}"}]),
'source': 'jshopact',
'platformId': '1'}
    headers = {'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'content-length': '507',
'content-type': 'application/x-www-form-urlencoded',
'cookie': 'shshshfpa=6776cfe5-3dcb-a849-8490-9e72806fdd35-1535945241; pinId=5Ux_jKaGlGNiUsqGcz67ULV9-x-f3wj7; cn=0; ipLocation=%u5317%u4EAC; shshshfpb=08e7eb8224927ca3eeda6255336854e51ab6f40ec97c208f45b8caa191; __jdv=122270672|baidu|-|organic|not set|1544499432339; user-key=b491b6a5-7b07-421b-9e35-b17ea7721979; PCSYCityID=1607; mt_xid=V2_52007VwMSVV1aW14YQRtsBDdRFwVcCFdGG0keCxliCxVXQQtUDkhVHlwAb1YUUQpZU1IZeRpdBW4fElFBWFdLH0kSXgFsABdiX2hSahxNH18CYAETVW1YV1wY; __jdu=1161385693; 3AB9D23F7A4B3C9B=SRSFDKQAME6KEG2ETDPUPL6BZJ7BJJ5Y7EVSPDF56SLIWBYNKSUIRLGALVVOJOVTIQ4R6C5MOUIQQVZEIONHJ26DPQ; _gcl_au=1.1.1087481521.1545295518; shshshfp=f3856d1c446473cfa8f6188a6ba4dd62; __jda=122270672.1161385693.1535945240.1545295094.1545355654.277; __jdc=122270672; shshshsID=db63b06c52176f8dc1bd3f99968dbb15_2_1545355670341; __jdb=122270672.2.1161385693|277.1545355654',
'origin': 'https://mall.jd.com',
'referer': 'https://mall.jd.com/index-1000133222.html',
'user-agent': ua.random}
    response = requests.post(url,headers=headers,data=formdata,verify=False)
    if response.status_code == 200:
        with open("C:/Users/Administrator/Desktop/img_huodong.csv",'a',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name,'https://mall.jd.com/index-1000133222.html'])
        print(brand_name,url)
        return response.text


def parse_Page(html, headers):
    datas = re.findall(r'"picUrl" : "(.*?)"',html)
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'itoen_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page1(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:4]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'starbucks_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page2(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='scroller-content']/li/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ucc_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page3(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'nongfushanquan_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath(".//img/@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page4(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'rio_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath(".//img/@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page5(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Hey juice_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./img/@original")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page6(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ozeki_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./img/@original")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page7(html, headers):
    datas = re.findall(r'src=\\"(.*?)\\"',html)[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'joybo_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page8(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//span/div/div/div/div/div/@style")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Balleys_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page9(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'kiku_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./img/@original")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def parse_Page10(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='crzyjdzybj']/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'la fiole_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                image = response.content
                try:
                    with open(filename,'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name, count))
                except Exception as e:
                    filename = brand_name + str(count) + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(image)
                        count += 1
                        print('保存品牌{}第{}张图片成功'.format(brand_name,count))


def main():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    # itoen/伊藤园 京东
    html = get_Page_itoen('https://zt-jshop.jd.com/service.html',ua,'itoen_jd')
    parse_Page(html,headers)
    # starbucks/星巴克 天猫
    html1 = get_Page('https://starbucks.tmall.com', headers, 'starbucks_tm')
    parse_Page1(html1, headers)
    # ucc/悠诗诗 天猫
    html2 = get_Page('https://youshishi.tmall.com', headers, 'ucc_tm')
    parse_Page2(html2, headers)
    # nongfushanquan/农夫山泉 天猫
    html3 = get_Page('https://nongfushanquan.tmall.com', headers, 'nongfushanquan_tm')
    parse_Page3(html3, headers)
    # rio/锐澳 天猫
    html4 = get_Page('https://ruiao.tmall.com', headers, 'rio_tm')
    parse_Page4(html4, headers)
    # Hey juice 京东
    html5 = get_Page('https://mall.jd.com/index-165378.html', headers, 'Hey juice_jd')
    parse_Page5(html5, headers)
    # KOOKSOONDANG/麴醇堂 京东
    html6 = get_Page1('https://search.jd.com/Search?keyword=%E9%BA%B4%E9%86%87%E5%A0%82&enc=utf-8&wq=%E9%BA%B4%E9%86%87%E5%A0%82&pvid=6dad5772f1244ef6a5928fe7709facdc', headers, 'KOOKSOONDANG_jd')
    # umepon/白岳 京东
    html7 = get_Page1('https://search.jd.com/Search?keyword=%E7%99%BD%E5%B2%B3&enc=utf-8&wq=%E7%99%BD%E5%B2%B3&pvid=e9ab0aafe7cd48579fb6aab300cecc10',headers, 'umepon_jd')
    # choya/蝶矢俏雅 京东
    html8 = get_Page1('https://search.jd.com/Search?keyword=%E8%9D%B6%E7%9F%A2%E4%BF%8F%E9%9B%85&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&wtype=1&click=1',headers, 'choya_jd')
    # ozeki/大关清酒 京东
    html9 = get_Page('https://mall.jd.com/index-1000090402.html', headers, 'ozeki_jd')
    parse_Page6(html9, headers)
    # joybo/江小白 京东
    html10 = get_Page('https://mall.jd.com/index-1000076282.html', headers, 'joybo_jd')
    parse_Page7(html10, headers)
    # Balleys/百利 天猫
    html11 = get_Page('https://baileys.tmall.com', headers, 'Balleys_tm')
    parse_Page8(html11, headers)
    # kiku/菊正宗 京东
    html12 = get_Page('https://mall.jd.com/index-1000102032.html', headers, 'kiku_jd')
    parse_Page9(html12, headers)
    # feiqian/肥前杜氏 京东
    html13 = get_Page1('https://search.jd.com/Search?keyword=%E8%82%A5%E5%89%8D%E6%9D%9C%E6%B0%8F&enc=utf-8&wq=%E8%82%A5%E5%89%8D%E6%9D%9C%E6%B0%8F&pvid=0b33162bb46e4bd5b0aae403d763c024', headers, 'feiqian_jd')
    # gekkeikan/月桂冠 京东
    html14 = get_Page1('https://search.jd.com/Search?keyword=%E6%9C%88%E6%A1%82%E5%86%A0&enc=utf-8&wq=%E8%BE%9B%E4%B8%B9%E6%B3%A2&pvid=ae080fd806584822b957e9ca68e3aa0f',headers, 'gekkeikan_jd')
    # ribensheng/日本盛 京东
    html15 = get_Page1('https://search.jd.com/Search?keyword=%E6%97%A5%E6%9C%AC%E7%9B%9B&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&ev=exbrand_%E6%97%A5%E6%9C%AC%E7%9B%9B%5E&stock=1&wtype=1&click=1',headers, 'ribensheng_jd')
    # la fiole/菊正宗 京东
    html16 = get_Page('https://mall.jd.com/index-1000113843.html', headers, 'la fiole_jd')
    parse_Page10(html16, headers)
    # choya/蝶矢俏雅 京东
    html17 = get_Page1('https://search.jd.com/Search?keyword=choya&enc=utf-8&suggest=1.rem.0.V00&wq=%E8%8A%99%E5%8D%8E%E7%BD%97%E9%A1%BF&pvid=db85e80eed194aa591dca5f8b5ddb329',headers, 'choya_jd')
    # fangge/芳歌 京东
    html18 = get_Page1('https://search.jd.com/Search?keyword=%E8%8A%B3%E6%AD%8C&enc=utf-8&wq=%E8%8A%B3%E6%AD%8C&pvid=99332c4dac7e48f485d3b6dbf7355fc7',headers, 'fangge_jd')


if __name__ == '__main__':
    main()