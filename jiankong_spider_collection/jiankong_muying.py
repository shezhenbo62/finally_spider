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


def get_Page_Rafferty(url,ua,brand_name):
    formdata = {'functionId': 'getModData',
'body': json.dumps([{"type":"module","moduleId":-288,"moduleData":"{\"lunboGoodsGroup\":{\"materialCode\":\"J1I7Y56jFH\",\"moduleCreate\":2,\"bi\":0,\"type\":\"2\",\"showNum\":4},\"moduleMarginBottom\":[],\"template\":{\"type\":1,\"templateId\":-99888}}"}]),
'source': 'jshopact',
'platformId': '1'}
    headers = {'accept': '*/*',
'content-type': 'application/x-www-form-urlencoded',
# 'cookie': 'shshshfpa=6776cfe5-3dcb-a849-8490-9e72806fdd35-1535945241; pinId=5Ux_jKaGlGNiUsqGcz67ULV9-x-f3wj7; cn=0; ipLocation=%u5317%u4EAC; ipLoc-djd=1-72-2799-0; shshshfpb=08e7eb8224927ca3eeda6255336854e51ab6f40ec97c208f45b8caa191; __jdv=122270672|baidu|-|organic|not set|1544499432339; user-key=b491b6a5-7b07-421b-9e35-b17ea7721979; PCSYCityID=1607; 3AB9D23F7A4B3C9B=SRSFDKQAME6KEG2ETDPUPL6BZJ7BJJ5Y7EVSPDF56SLIWBYNKSUIRLGALVVOJOVTIQ4R6C5MOUIQQVZEIONHJ26DPQ; _gcl_au=1.1.528096839.1544756625; mt_xid=V2_52007VwMSVV1aW14YQRtsBDdRFwVcCFdGG0keCxliCxVXQQtUDkhVHlwAb1YUUQpZU1IZeRpdBW4fElFBWFdLH0kSXgFsABdiX2hSahxNH18CYAETVW1YV1wY; shshshfp=f3856d1c446473cfa8f6188a6ba4dd62; __jdu=1161385693; __jda=122270672.1161385693.1535945240.1545018696.1545028641.259; __jdc=122270672; shshshsID=652f424f97e1d725e05e387c40eb721a_2_1545028643943; __jdb=122270672.2.1161385693|259.1545028641',
'origin': 'https://mall.jd.com',
'referer': 'https://mall.jd.hk/index-863120.html',
'user-agent': ua.random}
    response = requests.post(url,headers=headers,data=formdata,verify=False)
    if response.status_code == 200:
        with open("C:/Users/Administrator/Desktop/img_huodong.csv",'a',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name,'https://mall.jd.hk/index-863120.html'])
        print(brand_name,url)
        return response.text


def parse_Page(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'meadjohnson_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./@data-ks-lazyload')[0]
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
    datas = html_lxml.xpath("//div[@id='bd']/div[2]/div/div/@module-data")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'soondoongi_tm'
    for data in datas:
        data = parse.unquote(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = img_url.replace('\\','')
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
    datas = html_lxml.xpath("//div[@id='bd']/div[2]/div/div/@module-data")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'nestlebaby_tm'
    for data in datas:
        data = parse.unquote(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = img_url.replace('\\','')
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
    datas = html_lxml.xpath("//div[@id='bd']/div[2]/div/div/@module-data")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'mellin_tm'
    for data in datas:
        data = parse.unquote(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = img_url.replace('\\','')
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
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Kabrita_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./img/@original')[0]
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
    brand_name = 'Guigoz_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./img/@original')[0]
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
    datas = re.findall(r'url":"(.*?)"',html)[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Bubs Organic_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data
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
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='con1lv']/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'happy baby_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
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


def parse_Page8(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'goonyishang_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
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
    datas = html_lxml.xpath("//ul[@id='show_pic']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Muumi baby_kl'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath(".//img/@src")[0]
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


def parse_Page10(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'libero_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
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


def parse_Page11(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@id='show_pic']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'BEABA_kl'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath(".//img/@src")[0]
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


def parse_Page12(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='mc']//img")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'nepia_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@original")[0]
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


def parse_Page13(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Nuby_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
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


def parse_Page14(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Dodie_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
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


def parse_Page15(html, headers):
    datas = re.findall(r'url":"(.*?)"',html)[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Natures Way_jd'
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


def parse_Page16(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div[2]/div/div/@module-data")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Healtheries_tm'
    for data in datas:
        data = parse.unquote(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = img_url.replace('\\','')
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


def parse_Page17(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'littlefreddie_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
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


def parse_Page18(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img/parent::div/@style")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'miaogu_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
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


def parse_Page19(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='mgzxzs_zybj']/@style")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'eastwes_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
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


def parse_Page20(html, headers):
    html_lxml = etree.HTML(html)
    data = html_lxml.xpath("//div[@class='MaGong']/div/div/div/@style")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'bellamys_tm'
    # 图片链接
    try:
        img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
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


def parse_Page21(html, headers):
    datas = re.findall(r'url":"(.*?)"',html)[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Ellas kitchen_jd'
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


def parse_Page22(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ostelin_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
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


def parse_Page23(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content c174770']/div/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Childlife_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
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


def parse_Page24(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@id='show_pic']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'engnice_kl'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath(".//img/@src")[0]
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


def parse_Page25(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Lilcritters_tm'
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


def parse_Page26(html, headers):
    datas = re.findall(r'"picUrl" : "(.*?)"',html)
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Raffertys Garden_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data
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


def parse_Page27(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='lb_bd']/li/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'purcotton_tm'
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


def parse_Page28(html, headers):
    datas = re.findall(r'src=\\"(.*?)\\"',html)
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Joyourbaby_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data
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


def main():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    # meadjohnson/美赞臣 天猫
    html = get_Page('https://meadjohnson.tmall.com',headers,'meadjohnson_tm')
    parse_Page(html,headers)
    # soondoongi/顺顺儿 天猫
    html1 = get_Page('https://shunshuner.tmall.com', headers, 'soondoongi_tm')
    parse_Page1(html1, headers)
    # Sudocrem 考拉
    html2 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Sudocrem&searchRefer=searchbutton&oldQuery=%25E8%258B%25B1%25E5%259C%258B%25E5%25AF%25B6%25E5%25AF%25B6&timestamp=1543995104151', headers, 'Sudocrem_kl')
    # nestlebaby/雀巢 天猫
    html3 = get_Page('https://nestlebaby.tmall.hk', headers, 'nestlebaby_tm')
    parse_Page2(html3, headers)
    # Karicare/可瑞康 考拉
    html4 = get_Page1('https://www.kaola.com/category/2620.html?key=&pageSize=60&pageNo=1&sortfield=0&isStock=false&isSelfProduct=false&isPromote=false&isTaxFree=false&factoryStoreTag=-1&isDesc=true&b=1236&proIds=&source=false&country=&needBrandDirect=false&isNavigation=0&lowerPrice=-1&upperPrice=-1&backCategory=&headCategoryId=&changeContent=brandId&#topTab', headers, 'Karicare_kl')
    # mellin 天猫
    html5 = get_Page('https://mellin.tmall.hk', headers, 'mellin_tm')
    parse_Page3(html5, headers)
    # Kabrita/佳贝艾特 京东
    html6 = get_Page('https://mall.jd.com/index-1000002710.html', headers, 'Kabrita_jd')
    parse_Page4(html6, headers)
    # Guigoz/古戈氏 京东
    html7 = get_Page('https://mall.jd.hk/index-1000090221.html', headers, 'Guigoz_jd')
    parse_Page5(html7, headers)
    # Bubs Organic/澳洲贝儿 京东
    html8 = get_Page('https://mall.jd.hk/index-1000100563.html', headers, 'Bubs Organic_jd')
    parse_Page6(html8, headers)
    # happy baby 天猫
    html9 = get_Page('https://happyfamilyinc.tmall.hk', headers, 'happy baby_tm')
    parse_Page7(html9, headers)
    # goonyishang 天猫
    html10 = get_Page('https://goonyishang.tmall.com', headers, 'goonyishang_tm')
    parse_Page8(html10, headers)
    # Muumi baby/姆明一族 考拉
    html11 = get_Page('https://mall.kaola.com/34861232?ri=navigation&from=page1&zn=result&zp=page1-0&position=0&istext=3&srId=d2cc79d06210ccff899d390d6a30ee89', headers, 'Muumi baby_kl')
    parse_Page9(html11, headers)
    # libero 天猫
    html12 = get_Page('https://libero.tmall.com', headers, 'libero_tm')
    parse_Page10(html12, headers)
    # BEABA/碧芭 考拉
    html13 = get_Page('https://mall.kaola.com/50635557?ri=navigation&from=page1&zn=result&zp=page1-0&position=0&istext=3&srId=eba821ed3292fae07fa85ae69795a1be', headers, 'BEABA_kl')
    parse_Page11(html13, headers)
    # nepia/妮飘 京东
    html14 = get_Page('https://mall.jd.com/index-28660.html', headers, 'nepia_jd')
    parse_Page12(html14, headers)
    # Nuby/努比 天猫
    html15 = get_Page('https://nuby.tmall.com', headers, 'Nuby_tm')
    parse_Page13(html15, headers)
    # Dodie/杜迪 天猫
    html16 = get_Page('https://dodie.tmall.com', headers, 'Dodie_tm')
    parse_Page14(html16, headers)
    # Natures Way 京东
    html17 = get_Page('https://mall.jd.com/index-1000084244.html', headers, 'Natures Way_jd')
    parse_Page15(html17, headers)
    # Healtheries 天猫
    html18 = get_Page('https://healtheries.tmall.hk', headers, 'Healtheries_tm')
    parse_Page16(html18, headers)
    # littlefreddie 天猫
    html19 = get_Page('https://littlefreddieglobal.tmall.hk', headers, 'littlefreddie_tm')
    parse_Page17(html19, headers)
    # miaogu/妙谷 天猫
    html20 = get_Page('https://miaogumuying.tmall.com', headers, 'miaogu_tm')
    parse_Page18(html20, headers)
    # eastwes 天猫
    html21 = get_Page('https://eastwes.tmall.com', headers, 'eastwes_tm')
    parse_Page19(html21, headers)
    # bellamys/贝拉米 天猫
    html22 = get_Page('https://bellamyshk.tmall.hk', headers, 'bellamys_tm')
    parse_Page20(html22, headers)
    # Ellas kitchen 京东
    html23 = get_Page('https://mall.jd.hk/index-872768.html', headers, 'Ellas kitchen_jd')
    parse_Page21(html23, headers)
    # ostelin 天猫
    html24 = get_Page('https://ostelin.tmall.hk', headers, 'ostelin_tm')
    parse_Page22(html24, headers)
    # Childlife/童年时光 天猫
    html25 = get_Page('https://child.tmall.hk', headers, 'Childlife_tm')
    parse_Page23(html25, headers)
    # Fruchtbar/福乐蓓 考拉
    html26 = get_Page1('https://www.kaola.com/brand/6129.html', headers, 'Fruchtbar_kl')
    # engnice/英氏 考拉
    html27 = get_Page('https://mall.kaola.com/324403?zn=result&zp=page1-0&ri=engnice&rp=search', headers, 'engnice_kl')
    parse_Page24(html27, headers)
    # Lilcritters/丽贵 天猫
    html28 = get_Page('https://lilcritters.tmall.hk', headers, 'Lilcritters_tm')
    parse_Page25(html28, headers)
    # Herbs of Gold 考拉
    html29 = get_Page1('https://www.kaola.com/brand/3331.html', headers, 'Herbs of Gold_kl')
    # Raffertys Garden 京东
    html30 = get_Page_Rafferty('https://zt-jshop.jd.com/service.html', ua, 'Raffertys Garden_jd')
    parse_Page26(html30, headers)
    # purcotton/全棉时代 天猫
    html31 = get_Page('https://purcotton.tmall.com', headers, 'purcotton_tm')
    parse_Page27(html31, headers)
    # akachan honpo/阿卡佳本铺 考拉
    html32 = get_Page1('https://www.kaola.com/brand/5683.html', headers, 'akachan honpo_kl')
    # Joyourbaby/佳韵宝 京东
    html33 = get_Page('https://mall.jd.com/index-46669.html', headers, 'Joyourbaby_jd')
    parse_Page28(html33, headers)


if __name__ == '__main__':
    main()