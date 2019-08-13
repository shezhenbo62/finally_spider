# -*- coding: utf-8 -*-
import requests
import os
import time
from fake_useragent import UserAgent
from lxml import etree
import re
from urllib import parse
from meizhuang import savepicture
import csv
import json


basedir = os.path.dirname(__file__)
file = basedir + '/meizhuang'
if os.path.exists(file):
    os.chdir(file)
else:
    os.mkdir(file)
    os.chdir(file)

words_base = ['狂欢', '发售', '折', '减', 'sale', 'OFF', '新品', '上新', '限量', '活动', '特卖', '特惠', '赠', '联名', '礼遇', '优惠', '免费',
              '开门红', '低价', '送', '降', '献礼', '全新', '预售', '立省', '钜惠', '秒杀', '领券', '上市', '礼赞', '半价']

def decorator(func):
    def inner(url, html, headers, brandname):
        try:
            datas = func(url, html, headers, brandname)
            if datas == []:
                with open(file+"/muying_Error.csv",'a',encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([brandname, url])
        except:
            with open(file+"/muying_Error.csv", 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([brandname, url])
    return inner


def get_Page1(url, headers, brand_name):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for word in words_base:
            if word in response.text:
                with open(file+"/huodong.csv", 'a', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([brand_name, url, "活动类型：%s" %word])
                    print(brand_name + " " + url + "品牌在做活动" + "活动类型：%s" % word)
                break
        return response.text, url
    return None

def get_Page(url, headers, brand_name):
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            with open(file + "/img_huodong.csv", 'a',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([brand_name, url])
            print(brand_name + " " + url)
            return response.text, url
    except:
        with open(file + "/muying_Error.csv", 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name, url])
    return None,None


def get_Page_locc(url, ua, brand_name):
    formdata = {'functionId': 'getModData',
                'body': json.dumps([{"type":"module","moduleId":-288,"moduleData":"{\"lunboGoodsGroup\":{\"materialCode\":\"FGLu5z0jPxQ1S2U\",\"moduleCreate\":2,\"bi\":0,\"type\":\"2\",\"showNum\":\"4\"},\"moduleMarginBottom\":[],\"template\":{\"type\":1,\"templateId\":-256}}"}]),
                'source': 'jshopact',
                'platformId': '1'}
    headers = {'accept': '*/*',
                'accept-encoding': 'gzip, @decoratordeflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'content-length': '492',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': 'shshshfpa=6776cfe5-3dcb-a849-8490-9e72806fdd35-1535945241; pinId=5Ux_jKaGlGNiUsqGcz67ULV9-x-f3wj7; cn=0; ipLocation=%u5317%u4EAC; shshshfpb=08e7eb8224927ca3eeda6255336854e51ab6f40ec97c208f45b8caa191; user-key=b491b6a5-7b07-421b-9e35-b17ea7721979; mt_xid=V2_52007VwMSVV1aW14YQRtsBDdRFwVcCFdGG0keCxliCxVXQQtUDkhVHlwAb1YUUQpZU1IZeRpdBW4fElFBWFdLH0kSXgFsABdiX2hSahxNH18CYAETVW1YV1wY; ipLoc-djd=1-72-2799-0; PCSYCityID=1607; shshshfp=f3856d1c446473cfa8f6188a6ba4dd62; __jdc=122270672; __jdv=122270672|direct|-|none|-|1545796044706; __jdu=1161385693; 3AB9D23F7A4B3C9B=SRSFDKQAME6KEG2ETDPUPL6BZJ7BJJ5Y7EVSPDF56SLIWBYNKSUIRLGALVVOJOVTIQ4R6C5MOUIQQVZEIONHJ26DPQ; __jda=122270672.1161385693.1535945240.1545796045.1545810732.286; shshshsID=2acf6494db58fd5176530a0a333f597d_4_1545811855968; __jdb=122270672.4.1161385693|286.1545810732',
                'origin': 'https://mall.jd.com',
                'referer': 'https://mall.jd.com/index-1000002984.html',
                'user-agent': ua.random}
    response = requests.post(url, headers=headers, data=formdata, verify=False)
    if response.status_code == 200:
        with open(file + "/img_huodong.csv", 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name, 'https://mall.jd.com/index-1000002984.html'])
        print(brand_name, url)
        return response.text, url


@decorator
def parse_Page1(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop17819418289']/div/div/span/div/table/tbody/tr/td/div/div/div/div[1]/ul/li/a/ss")
    item = {}
    count = 1
    brand_name = 'aesop-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@data-ks-lazyload')[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page2(html, headers, response):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='col-md-12']/div/div/div/div/img")
    item = {}
    count = 1
    brand_name = 'Acqua Di Parma-gw'
    for data in datas:
    # 图片链接
        try:
            img_url = data.xpath('./@src')[0]
            # if img_url:
            #     img_url = "https://stussymmlm.tmall.com/" + img_url
        except Exception as e :
            print(brand_name, "图片元素定位为空，请及时查看修改")
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page3(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='hero-block__hero']//img")
    item = {}
    count = 1
    brand_name = 'Aerin-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@data-src')[0]
            if img_url:
                img_url = "https://www.esteelauder.com.cn" + img_url
        except Exception as e :
            print(brand_name,"图片元素定位为空，请及时查看修改")
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page4(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//figure[@class='hidden_mobile mb20 pt20']/a/img")
    item = {}
    count = 1
    brand_name = 'Aanastasia Beverly Hills-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@src')[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page5(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='slide-content']/li/a/img")
    item = {}
    count = 1
    brand_name = 'aastore-tm'
    for data in datas:
        # 图片链接
        try:
            img_url =data.xpath('./@data-ks-lazyload')[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page6(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='shuimo_con']//img")
    item = {}
    count = 1
    brand_name = 'Benefit-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@data-ks-lazyload')[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page7(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='node-18146']/div/div/div/div/div/section/div[2]/div/article/@style")
    item = {}
    count = 1
    brand_name = 'Bobbi Brown-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'/(.*?).jpg', data).group()
            if img_url:
                img_url = "https://www.bobbibrown.com.cn" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page8(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='b-slider']/div/div/a/img")
    item = {}
    count = 1
    brand_name = 'burberry-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@data-ks-lazyload')[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page9(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='big-hero-image-background']/picture/img")
    item = {}
    count = 1
    brand_name = 'bulgari'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@src')[0]
            # if img_url:
            #     img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page10(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div[1]/div/div/img")[0:2]
    item = {}
    count = 1
    brand_name = 'byterry-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@data-ks-lazyload')[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page11(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='content287364828']/li/a/@style")
    item = {}
    count = 1
    brand_name = 'caudalie-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'//(.*?).png', data).group()
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page12(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//*[@id='22960169']/div/div/div[2]/div/div/div/img")
    item = {}
    count = 1
    brand_name = 'Chanel-jd'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@original')[0]
            if img_url:
                img_url = "http:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page13(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='zq_pictures']/a/img")
    item = {}
    count = 1
    brand_name = 'ctbeaute-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@src')[0]
            # if img_url:
            #     img_url = "http:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page14(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='contentcarousel_asset_body']//img")
    item = {}
    count = 1
    brand_name = 'Clarisonic-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@data-src')[0]
            # if img_url:
            #     img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page15(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='zq_pictures']/a/img")
    item = {}
    count = 1
    brand_name = 'Charlotte Tilbury clarins'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@src')[0]
            if img_url:
                img_url = "http://www.charlottetilburychina.com/" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page16(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='customCarousel']/ul/li/div/a/div/div/img")
    item = {}
    count = 1
    brand_name = 'clarins-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@src')[0]
            # if img_url:
            #     img_url = "http://www.charlottetilburychina.com/" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page17(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='content']/li/a/@style")
    item = {}
    count = 1
    brand_name = 'clinique-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'//(.*?).jpg',data).group()
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page18(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='swiper-wrapper']/div/a/img")
    item = {}
    count = 1
    brand_name = 'Decorte-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@data-lg-img")[0]
            # if img_url:
            #     img_url = "https://clinique.tmall.com/" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page19(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='slick-track']//img")
    item = {}
    count = 1
    brand_name = 'Dior-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@src")[0]
            # if img_url:
            #     img_url = "https://clinique.tmall.com/" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page20(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jbannerImg']/div/dl/dt/img")
    item = {}
    count = 1
    brand_name = 'Diptyque-jd'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@original")[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page21(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div[1]/div/div/a/img")
    item = {}
    count = 1
    brand_name = 'Dr.Jart-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@data-ks-lazyload")[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page22(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div/div/div/img")
    item = {}
    count = 1
    brand_name = 'Dr.Sebagh-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@data-ks-lazyload")[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page23(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div/div/div/div/a[1]/div/@style")
    item = {}
    count = 1
    brand_name = 'Embryolisse-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'//(.*?).jpg', data).group()
            if img_url:
                img_url = "http:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page24(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div[1]/div/div/div/div/div[4]/div/div[1]/ul//img")
    item = {}
    count = 1
    brand_name = 'Elizabeth Arden-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@data-ks-lazyload")[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page25(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='ks-switchable-content']/li/a/@style")
    item = {}
    count = 1
    brand_name = 'Estee Lauder-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'//(.*?).jpg', data).group()
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page26(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop17852520210']/div/div/div/div/div[1]/table/tr/td/div/@style")
    item = {}
    count = 1
    brand_name = 'First Aid Beauty-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'//(.*?).jpg',data).group()
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page27(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div/div/div/div/div[32]/div/@style")
    item = {}
    count = 1
    brand_name = 'Foreo-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'//(.*?).jpg', data).group()
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page28(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='image_hold']//img")
    item = {}
    count = 1
    brand_name = 'Giorgio Armani-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@data-srcset")[0]
            # if img_url:
            #     img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page29(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']//img")
    item = {}
    count = 1
    brand_name = 'Guerlain-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@data-ks-lazyload")[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page30(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt/img")
    item = {}
    count = 1
    brand_name = 'Gucci-jd'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@original")[0]
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page31(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='crazy_content8bdjmw37aeim']//img")
    item = {}
    count = 1
    brand_name = 'Hourglass-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@data-ks-lazyload")[0]
            if img_url:
                img_url = "http:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page32(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@id='homepage-slides']/li/a//img")
    item = {}
    count = 1
    brand_name = 'Huda Beauty-gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@srcset")[0]
            # if img_url:
            #     img_url = "http:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page33(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='ks-switchable-content']/li/a/@style")
    item = {}
    count = 1
    brand_name = 'GIVENCHY-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'//(.*?).jpg',data).group()
            if img_url:
                img_url = "http:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page34(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div/div/div/div/div[8]/div/@style")
    item = {}
    count = 1
    brand_name = 'GELLE FRERES-tm'
    for data in datas:
        # 图片链接
        try:
            img_url = re.search(r'//(.*?).jpg', data).group()
            if img_url:
                img_url = "https:" + img_url
        except Exception as e:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page35(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//*[@id='1145498443']/@module-data")[0]
    item = {}
    count = 1
    brand_name = 'Alpha Hydrox-tm'
    a = parse.unquote(datas)
    try:
        img_url = re.search(r'url\((.*?.jpg)\)', a).group(1).replace("\\", "")
        # if img_url:
        #     img_url = "http:" + img_url
    except Exception as e:
        print(brand_name, "图片元素定位为空，请及时查看修改")
    else:
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", " ").replace("!q90", "")
        # 验证码图片文件名
        savepicture.save(img_url, headers, filename, brand_name, count)
    count += 1
    return [datas]

@decorator
def parse_Page36(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='wd-cont-carousel']//img")
    item = {}
    count = 1
    brand_name = 'Eve Lom-tm'
    for data in datas:
        # 图片链接
        try:
            # img_url = data
            img_url = data.xpath("./@data-ks-lazyload")[0]
            # img_url = data.xpath("./@original")[0]
            # img_url = re.search(r'//(.*?).jpg', data).group()
            if img_url:
                img_url = "https:" + img_url
        except Exception as a:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
        # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", " ").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page37(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//*[@class ='carousel-inner']/div/div[2]/div")
    item = {}
    count = 1
    brand_name = 'cartier-gw'
    for data in datas:
        # 图片链接
        try:
            # img_url = data
            img_url = data.xpath("./@data-original-url")[0]
            # img_url = data.xpath("./@original")[0]
            # img_url = re.search(r'//(.*?).jpg', data).group()
            if img_url:
                img_url = "https://www.cartier.cn/" + img_url
        except Exception as a:
            print(brand_name, "图片元素定位为空，请及时查看修改")
        else:
        # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", " ").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

@decorator
def parse_Page38(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content']/div")
    count = 1
    brand_name = 'HR_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page39(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='horz-carousel carousel']/li")
    count = 1
    brand_name = 'Lamer_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https://www.lamer.com.cn'+data.xpath('./div/div/div/a/img/@src')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page40(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl")
    count = 1
    brand_name = 'la prairie_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./dt/img/@original')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "").split('!')[0]
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page41(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='slide']")
    count = 1
    brand_name = 'LE LABO_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./a/div/img/@src')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")+'.jpg'
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page42(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='ks-switchable-content']/li")
    count = 1
    brand_name = 'MAC_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page43(url, html, headers, brand_name):
    count = 1
    brand_name = 'Marc Jacobs_jd'
    # 图片链接
    datas = re.findall(r'"url":"(.*?)"', html)
    for img_url in datas:
        try:
            img_url = "https:"+img_url
        except Exception as e:
            print(brand_name, '图片元素定位为空，请及时查看修改')
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1]
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page44(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='content_lsm_shiyan']/li")
    count = 1
    brand_name = 'Nars_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./a/@style')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\);',img_url)[0]
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page45(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li//img")
    count = 1
    brand_name = 'NuFace_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./@data-ks-lazyload')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page46(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='hero-carousel__slide js-hero-carousel__slide']")
    count = 1
    brand_name = 'Origins_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https://www.origins.com.cn'+data.xpath('.//a/img/@src')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page47(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='sx_carousel_content clearfix']/li")
    count = 1
    brand_name = 'Omorovicza_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page48(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:3]
    count = 1
    brand_name = 'Paul&Joe_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./@data-ks-lazyload')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page49(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='8675e0dcafdc026e50f29bcf299c88dd']/div")
    count = 1
    brand_name = 'Paulas Choice_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./a/img/@src')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page50(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']/span/div[position()<3]")
    count = 1
    brand_name = 'Perricone MD_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./div/div/img/@data-ks-lazyload')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page51(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='clearfix position_1']/li")
    count = 1
    brand_name = 'Sisley_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./a/img/@src')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page52(url, html, headers, brand_name):
    count = 1
    brand_name = 'Tom Ford_jd'
    datas = re.findall(r'img title=\\".*?\\" src=\\"(.*?)\\"', html)
    # 图片链接
    try:
        img_url = "https:" + datas[0]
    except Exception as e:
        print(brand_name,'图片元素定位为空，请及时查看修改')
    # 图片名字
    else:
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        savepicture.save(img_url, headers, filename, brand_name, count)
    count += 1
    return datas

@decorator
def parse_Page53(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'Too cool for school_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = "https:"+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page54(url, html, headers, brand_name):
    datas = re.findall(r'src=\\"(.*?)\\"',html)[:2]
    count = 1
    brand_name = 'Ultrasun_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = "https:"+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page55(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='swiper-container common-swiper e-swiper-kv']/div[1]/div")
    count = 1
    brand_name = 'YSL_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/img/@data-image")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            json_img = json.loads(img_url)
            img_url = json_img['standard']['normal']
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page56(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='zq_pictures']/a")
    count = 1
    brand_name = 'Zoeva_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http://www.zoevachina.com/'+data.xpath("./img/@src")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page57(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='kv']/ul/li")
    count = 1
    brand_name = 'Ahava_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/img/@src")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page58(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='UIslider-content']/li")
    count = 1
    brand_name = 'Laneige_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http://www.laneige.com'+data.xpath(".//img/@data-web")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page59(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='quanping']/@style")
    count = 1
    brand_name = 'Sulwhasoo_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page60(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div/img")
    count = 1
    brand_name = 'Hera_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page61(url, html, headers, brand_name):
    count = 1
    brand_name = 'IOPE_gw'
    datas = re.findall(r'img src="(.*?)" data-src',html)
    for data in datas:
        # 图片链接
        try:
            img_url = 'http://www.iope.com'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page62(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='zq_pictures']/a")
    count = 1
    brand_name = 'Darphin_gw'
    for data in datas[1:-1]:
        # 图片链接
        try:
            img_url = 'http://www.darphinchina.com/'+data.xpath("./img/@src")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page63(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@id='video-homepage-slider']/li")
    count = 1
    brand_name = 'Fresh_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath(".//img/@src")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page64(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'Kora_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page65(url, html, headers, brand_name):
    count = 1
    brand_name = 'LOCCITANE'
    # 图片链接
    datas = re.findall(r'"picUrl" : "(.*?)"', html)
    for img_url in datas:
        try:
            img_url = "https:"+img_url
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        else:
            # 图片名字
            filename = brand_name + "__" + img_url.split("/")[-1]
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page66(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='swiper-container e-swiper-kv']/div[1]/div")
    count = 1
    brand_name = 'Lancome_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/img/@data-image")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            json_img = json.loads(img_url)
            img_url = json_img['standard']['normal']
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page67(url, html, headers, brand_name):
    count = 1
    brand_name = 'HAIRMAX_jd'
    datas = re.findall(r'url":"(.*?)"', html)[:3]
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page68(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li")
    count = 1
    brand_name = 'realtechniques_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath(".//img/@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page69(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'uriage_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page70(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:3]
    count = 1
    brand_name = 'jmsolution_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page71(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='home-carousel']/div/div")
    count = 1
    brand_name = 'lorealparis_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/img/@src")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page72(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt")
    count = 1
    brand_name = 'lorealparis_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./img/@original")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "").split("!")[0]
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page73(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img/parent::div/@style")[:2]
    count = 1
    brand_name = 'ahc_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page74(url, html, headers, brand_name):
    count = 1
    brand_name = 'maybelline_jd'
    datas = re.findall(r'src=\\"(.*?)\\"',html)[:3]
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page75(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li")
    count = 1
    brand_name = 'Unny_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath(".//img/@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page76(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[position()<3]/div/div/span/div/div/div/table/tbody/tr/td/div/@style")
    count = 1
    brand_name = 'Revlon_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page77(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:3]
    count = 1
    brand_name = 'bblaboratories_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page78(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img/parent::div/@style")[:2]
    count = 1
    brand_name = 'spatreatment_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page79(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='banner']/div/div/div")
    count = 1
    brand_name = 'naturerepublic_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http://www.naturerepublic.cn'+data.xpath(".//img/@src")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page80(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[3]//img")[:2]
    count = 1
    brand_name = 'naturerepublic_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page81(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[3]/div/div/span/div/div/div/div/div/@style")
    count = 1
    brand_name = 'domecare_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page82(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop21241554176']/div/div/span/div/div/div/div/div[32]/div/@style")
    count = 1
    brand_name = 'rosette_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page83(url, html, headers, brand_name):
    count = 1
    brand_name = 'rohto_jd'
    datas = re.findall(r'"picUrl" : "(.*?)"',html)
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page84(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='content_lsm_shiyan']/li/a/@style")
    count = 1
    brand_name = 'utena_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page85(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img/parent::div/@style")[:2]
    count = 1
    brand_name = 'mariobadescu_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page86(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'aekyungage20s_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page87(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'paparecipe_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page88(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='sx_content_sys clearfix']/li/div/@style")
    count = 1
    brand_name = 'purevivi_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page89(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='tianmao123']//img")[:2]
    count = 1
    brand_name = 'kose_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page90(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'shangpree_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page91(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//span/div/div/div/div/a/div/@style")[:2]
    count = 1
    brand_name = 'bourjois_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)', data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page92(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt/img")
    count = 1
    brand_name = 'Farmacy_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@original")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "").split("!")[0]
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page93(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'sentianyaozhuang_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page94(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'qualityfirst_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page95(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='slide-content']/li")
    count = 1
    brand_name = 'ettusais_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath(".//img/@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page96(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='main']//a/@style")
    count = 1
    brand_name = 'kumano_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page97(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//a/@style")[:2]
    count = 1
    brand_name = 'Orbis_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page98(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt/img")
    count = 1
    brand_name = 'daiso_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@original")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "").split("!")[0]
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page99(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:4]
    count = 1
    brand_name = 'cerave_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page100(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'growgorgeous_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page101(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'moroccanoil_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page102(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//a/@style")[:4]
    count = 1
    brand_name = 'lush_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page103(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'Avalon_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page104(url, html, headers, brand_name):
    datas = re.findall(r';background:url\((.*?)\)',html)[-1:]
    count = 1
    brand_name = 'Batiste_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page105(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'manentail_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page106(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'ruiyanrungao_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page107(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'aussie_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page108(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//*[@id='shop18412883439']/div/div/span/div/div/div/div/div/div[44]/@style")
    count = 1
    brand_name = 'tamanohada_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page109(url, html, headers, brand_name):
    count = 1
    brand_name = 'Moist Diane_jd'
    datas = re.findall(r'url":"(.*?)"',html)[:2]
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page110(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content c514546']/div/div/@style")
    count = 1
    brand_name = 'Amore_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page111(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='mgzxzs_zybj']/@style")[:2]
    count = 1
    brand_name = 'oubeiqing_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page112(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:3]
    count = 1
    brand_name = 'niurushijian_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page113(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'sesderma_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page114(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'lion_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page115(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'beautybuffet_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page116(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:2]
    count = 1
    brand_name = 'venuslab_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@data-ks-lazyload")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page117(url, html, headers, brand_name):
    datas = re.findall(r'src=\\"(.*?)\\"',html)[:2]
    count = 1
    brand_name = 'swisse_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page118(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//span/div/div/div/div/div/@style")[:2]
    count = 1
    brand_name = 'marvis_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "")
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page119(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt")
    count = 1
    brand_name = 'Ora2_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./img/@original")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "").split("!")[0]
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas


@decorator
def parse_Page120(url, html, headers, brand_name):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='user@decoratordefinedArea']/div/img")[:2]
    count = 1
    brand_name = 'crest_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@original")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].replace("!!", "").replace("!q90", "").split("!")[0]
            # 验证码图片文件名
            savepicture.save(img_url, headers, filename, brand_name, count)
        count += 1
    return datas

def main():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    # United Nude-ht
    brand_name = 'United Nude-ht'
    get_Page1('https://www.farfetch.cn/cn/shopping/women/united-nude/items.aspx?utm_content=United%20Nude', headers, 'United Nude-ht')

    # BareMinerals-kl
    brand_name = 'BareMinerals-kl'
    get_Page1('https://www.kaola.com/brand/9264.html',headers,'BareMinerals-kl')

    # It Cosmetics-ht
    brand_name = 'It Cosmetics-ht'
    get_Page1('https://www.beautylish.com/b/it-cosmetics', headers, 'It Cosmetics-ht')

    # Hermes-kl
    brand_name = 'Hermes-kl'
    get_Page1('https://www.kaola.com/brand/2095.html', headers, 'Hermes-kl')

    # Coverfx-ht
    brand_name = 'Coverfx-ht'
    get_Page1('https://cn.feelunique.com/search/result?q=Cover%20fx', headers, 'Coverfx-ht')

    # Christian Louboutin-kl
    brand_name = 'Christian Louboutin-kl'
    get_Page1('https://www.kaola.com/brand/2363.html', headers, 'Christian Louboutin-kl')

    # Byredo-kl
    brand_name = 'Byredo-kl'
    get_Page1('https://www.kaola.com/brand/7780.html', headers, 'Byredo-kl')

    # Beauty Blender-ht
    brand_name = 'Beauty Blender-ht'
    get_Page1('https://www.sephora.cn/brand/about-beautyblender-443501/', headers, 'Beauty Blender-ht')

    # aesop-tm
    brand_name = 'aesop-tm'
    html, url = get_Page('https://aesopskincare.tmall.hk/', headers, 'aesop-tm')
    parse_Page1(url, html, headers, brand_name)

    # Acqua Di Parma-gw
    brand_name = 'Acqua Di Parma-gw'
    html, url = get_Page('http://www.acquadiparma.cn/', headers, 'Acqua Di Parma-gw')
    parse_Page2(url, html, headers, brand_name)
    #
    # Aerin-gw
    brand_name = 'Aerin-gw'
    html, url = get_Page('https://www.esteelauder.com.cn/', headers, 'Aerin-gw')
    parse_Page3(url, html, headers, brand_name)

    # Aanastasia Beverly Hills-gw
    brand_name = 'Aanastasia Beverly Hills-gw'
    html, url = get_Page('https://www.beautylish.com/', headers, 'Aanastasia Beverly Hills-gw')
    parse_Page4(url, html, headers, brand_name)

    # #aastore
    # # html = get_Page('https://aastore.tmall.hk/', headers,'aastore')
    # # parse_Page5(url, html, headers, brand_name)

    # Benefit-tm
    brand_name = 'Benefit-tm'
    html, url = get_Page('https://benefit.tmall.com/', headers, 'Benefit-tm')
    parse_Page6(url, html, headers, brand_name)

    # Bobbi Brown-gw
    brand_name = 'Bobbi Brown-gw'
    html, url = get_Page('https://www.bobbibrown.com.cn/', headers, 'Bobbi Brown-gw')
    parse_Page7(url, html, headers, brand_name)

    # burberry-tm
    brand_name = 'burberry-tm'
    html, url = get_Page('https://burberry.tmall.com/', headers, 'burberry-tm')
    parse_Page8(url, html, headers, brand_name)

    # bulgari-gw
    brand_name = 'bulgari-gw'
    html, url = get_Page('https://www.bulgari.cn/zh-cn/', headers, 'bulgari-gw')
    parse_Page9(url, html, headers, brand_name)

    # byterry-tm
    brand_name = 'byterry-tm'
    html, url = get_Page('https://byterry.tmall.com/', headers, 'byterry-tm')
    parse_Page10(url, html, headers, brand_name)

    # caudalie-tm
    brand_name = 'caudalie-tm'
    html, url = get_Page('https://caudalie.tmall.com/', headers, 'caudalie-tm')
    parse_Page11(url, html, headers, brand_name)

    # Chanel-jd
    brand_name = 'Chanel-jd'
    html, url = get_Page('https://mall.jd.com/index-1000005182.html', headers, 'Chanel-jd')
    parse_Page12(url, html, headers, brand_name)

    # ctbeaute-gw
    brand_name = 'ctbeaute-gw'
    html, url = get_Page('http://www.ctbeaute.com/', headers, 'ctbeaute-gw')
    parse_Page13(url, html, headers, brand_name)

    # Clarisonic-gw
    brand_name = 'Clarisonic-gw'
    html, url = get_Page('https://www.clarisonic.cn/', headers, 'Clarisonic-gw')
    parse_Page14(url, html, headers, brand_name)

    # # # Charlotte Tilbury
    # # html = get_Page('http://www.charlottetilburychina.com/', headers, 'Charlotte Tilbury')
    # # parse_Page15(url, html, headers, brand_name)

    # clarins-gw
    brand_name = 'clarins-gw'
    html, url = get_Page('https://www.clarins.com.cn/', headers, 'clarins-gw')
    parse_Page16(url, html, headers, brand_name)

    # clinique-tm
    brand_name = 'clinique-tm'
    html, url = get_Page('https://clinique.tmall.com/', headers, 'clinique-tm')
    parse_Page17(url, html, headers, brand_name)

    # Decorte-tm
    brand_name = 'Decorte-tm'
    html, url = get_Page('https://shop.decorte-cosmetics.cn/', headers, 'Decorte-tm')
    parse_Page18(url, html, headers, brand_name)

    # Dior-gw
    brand_name = 'Dior-gw'
    html, url = get_Page('https://www.dior.cn/zh_cn', headers, 'Dior-gw')
    parse_Page19(url, html, headers, brand_name)

    # Diptyque-jd
    brand_name = 'Diptyque-jd'
    html, url = get_Page('https://mall.jd.com/index-1000118674.html', headers, 'Diptyque-jd')
    parse_Page20(url, html, headers, brand_name)

    # Dr.Jart-tm
    brand_name = 'Dr.Jart-tm'
    html, url = get_Page('https://drjart.tmall.com/', headers, 'Dr.Jart-tm')
    parse_Page21(url, html, headers, brand_name)

    # Dr.Sebagh-tm
    brand_name = 'Dr.Sebagh-tm'
    html, url = get_Page('https://drsebagh.tmall.com/', headers, 'Dr.Sebagh-tm')
    parse_Page22(url, html, headers, brand_name)

    # Embryolisse-tm
    brand_name = 'Embryolisse-tm'
    html, url = get_Page('https://embryolisse.tmall.hk/', headers, 'Embryolisse-tm')
    parse_Page23(url, html, headers, brand_name)

    # Elizabeth Arden-tm
    brand_name = 'Elizabeth Arden-tm'
    html, url = get_Page('https://elizabetharden.tmall.com/', headers, 'Elizabeth Arden-tm')
    parse_Page24(url, html, headers, brand_name)

    # Estee Lauder
    brand_name = 'Estee Lauder-tm'
    html, url = get_Page('https://esteelauder.tmall.com/', headers, 'Estee Lauder-tm')
    parse_Page25(url, html, headers, brand_name)

    # First Aid Beauty-tm
    brand_name = 'First Aid Beauty-tm'
    html, url = get_Page('https://firstaidbeauty.tmall.hk/', headers, 'First Aid Beauty-tm')
    parse_Page26(url, html, headers, brand_name)

    # Foreo-tm
    brand_name = 'Foreo-tm'
    html, url = get_Page('https://foreo.tmall.com/', headers, 'Foreo-tm')
    parse_Page27(url, html, headers, brand_name)

    # Giorgio Armani-gw
    brand_name = 'Giorgio Armani-gw'
    html, url = get_Page('https://www.giorgioarmanibeauty.cn/', headers, 'Giorgio Armani-gw')
    parse_Page28(url, html, headers, brand_name)

    # Guerlain-tm
    brand_name = 'Guerlain-tm'
    html, url = get_Page('https://guerlain.tmall.com/', headers, 'Guerlain-tm')
    parse_Page29(url, html, headers, brand_name)

    # Gucci-jd
    brand_name = 'Gucci-jd'
    html, url = get_Page('https://mall.jd.com/index-1000004721.html', headers, 'Gucci-jd')
    parse_Page30(url, html, headers, brand_name)

    # Hourglass-tm
    brand_name = 'Hourglass-tm'
    html, url = get_Page('https://hourglass.tmall.hk/', headers, 'Hourglass-tm')
    parse_Page31(url, html, headers, brand_name)

    # Huda Beauty-gw
    brand_name = 'Huda Beauty-gw'
    html, url = get_Page('https://www.shophudabeauty.com/en_CN/home', headers, 'Huda Beauty-gw')
    parse_Page32(url, html, headers, brand_name)

    # GIVENCHY-tm
    brand_name = 'GIVENCHY-tm'
    html, url = get_Page('https://givenchy.tmall.com', headers, 'GIVENCHY-tm')
    parse_Page33(url, html, headers, brand_name)

    # GELLÉ FRÈRES-tm
    brand_name = 'GELLÉ FRÈRES-tm'
    html, url = get_Page('https://gellefreres.tmall.com/', headers, 'GELLE FRERES-tm')
    parse_Page34(url, html, headers, brand_name)

    # Alpha Hydrox-tm
    brand_name = 'Alpha Hydrox-tm'
    html, url = get_Page('https://alphahydrox.tmall.hk/', headers, 'Alpha Hydrox-tm')
    parse_Page35(url, html, headers, brand_name)

    # Eve Lom-tm
    brand_name = 'Eve Lom-tm'
    html, url = get_Page('https://evelom.tmall.com/', headers, 'Eve Lom-tm')
    parse_Page36(url, html, headers, brand_name)

    # # # cartier-gw
    # # brand_name = 'cartier-gw'
    # # html, url = get_Page('https://www.cartier.cn/', headers, 'cartier-gw')
    # # parse_Page37(url, html, headers, brand_name)

    # HR/赫莲娜
    brand_name = 'HR_tm'
    html, url = get_Page('https://helenarubinstein.tmall.com/', headers, 'HR_tm')
    parse_Page38(html, headers, brand_name, url)

    # Jo Malone London/祖·玛珑
    brand_name = "Jo Malone London_gw"
    get_Page1('https://www.jomalone.com.cn/', headers, 'Jo Malone London_gw')

    # Lamer/海蓝之谜
    brand_name = 'Lamer_gw'
    html, url = get_Page('https://www.lamer.com.cn/', headers, 'Lamer_gw')
    parse_Page39(url, html, headers, brand_name)

    # la prairie/莱珀妮
    brand_name = 'la prairie_jd'
    html, url = get_Page('https://mall.jd.com/index-1000119661.html', headers, 'la prairie_jd')
    parse_Page40(url, html, headers, brand_name)

    # Laura Mercier/罗拉玛斯亚
    brand_name = 'Laura Mercier'
    get_Page1('https://search.jd.com/Search?keyword=Laura%20Mercier&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%8E%B1%E7%8F%80%E5%A6%AE&stock=1&wtype=1&click=1',headers,'Laura Mercier')

    # LE LABO
    headers1 = {'User-Agent': ua.random,
               'cookie': '__cfduid=d4dff2295de80eecbbd990529577142221539057647; acdc_vat=false; _ga=GA1.2.1835578554.1539057650; acdc_region=HK; ACDC_LOCALE=EN; acdc_currency=EUR; AWSALB=t71oZEHcjB550TWfoI4jVe4wj5kboRFHaiztxZW9rwE69sdP8lBN6ILgzEhkQC7IRcF5/D7ggHmic9vehkw6Pv+C9GFEUS5mZPJ5eQfDq0eyYKbJnsUwS4kiKECK; acdc_disclaimer=true; _gid=GA1.2.214871939.1543220959; csrfToken=6a4221d3-6e2f-4a97-86b5-26f6cee0036c'}
    brand_name = 'LE LABO_gw'
    html, url = get_Page('https://www.lelabofragrances.com/',headers1,'LE LABO_gw')
    parse_Page41(url, html, headers, brand_name)

    # M.A.C/魅可
    brand_name = 'Joyourbaby_jd'
    html, url = get_Page('https://mac.tmall.com/',headers,'MAC_tm')
    parse_Page42(url, html, headers, brand_name)

    # Marc Jacobs/马克雅可布
    # https://mall.jd.com/index-1000005205.html
    brand_name = 'Marc Jacobs_jd'
    html, url = get_Page('https://mall.jd.com/index-1000005205.html', headers, 'Marc Jacobs_jd')
    parse_Page43(url, html, headers, brand_name)

    # Nars 
    brand_name = 'Nars_tm'
    html, url = get_Page('https://nars.tmall.com/',headers, 'Nars_tm')
    parse_Page44(url, html, headers, brand_name)

    # Natasha Denona 
    brand_name = 'Natasha Denona'
    get_Page1('https://cn.feelunique.com/search/result?q=Natasha%20Denona', headers,'Natasha Denona')

    # NuFace 
    brand_name = 'NuFace_tm'
    html, url = get_Page('https://nuface.tmall.hk',headers, 'NuFace_tm')
    parse_Page45(url, html, headers, brand_name)

    # NYX Professional Makeup 
    brand_name = 'NYX'
    get_Page1('https://cn.feelunique.com/search/result?q=NYX%20Professional%20Makeup', headers,'NYX')

    # Origins/悦木之源 
    brand_name = 'Origins_gw'
    html, url = get_Page('https://www.origins.com.cn',headers, 'Origins_gw')
    parse_Page46(url, html, headers, brand_name)

    # Omorovicza/欧微泉萨
    brand_name = 'Omorovicza_tm'
    html, url = get_Page('https://omorovicza.tmall.hk/', headers, 'Omorovicza_tm')
    parse_Page47(url, html, headers, brand_name)

    # Paul&Joe
    brand_name = 'Paul&Joe_tm'
    html, url = get_Page('https://pauljoe.tmall.hk/', headers, 'Paul&Joe_tm')
    parse_Page48(url, html, headers, brand_name)

    # Paula's Choice/宝拉珍选
    brand_name = 'Paulas Choice_gw'
    html, url = get_Page('http://www.paulaschoice.hk/', headers, 'Paulas Choice_gw')
    parse_Page49(url, html, headers, brand_name)

    # Perricone MD
    brand_name = 'Perricone MD_tm'
    html, url = get_Page('https://pmdus.tmall.hk/', headers, 'Perricone MD_tm')
    parse_Page50(url, html, headers, brand_name)

    # Peterthomasroth/彼得罗夫
    brand_name = 'Peterthomasroth'
    get_Page1('https://www.sephora.cn/brand/peterthomasroth-342', headers,'Peterthomasroth')

    # RMK
    brand_name = 'RMK_kl'
    get_Page1('https://www.kaola.com/brand/1886.html?', headers,'RMK_kl')

    # Sarah Chapman
    brand_name = 'arah Chapman'
    get_Page1('https://cn.feelunique.com/search/result?q=Sarah%20Chapman', headers,'Sarah Chapman')

    # Sisley/希思黎
    brand_name = 'Sisley_gw'
    html, url = get_Page('http://www.sisley.com.cn/', headers, 'Sisley_gw')
    parse_Page51(url, html, headers, brand_name)

    # Stila/诗狄娜
    brand_name = 'Stila_kl'
    get_Page1('https://www.kaola.com/brand/6673.html', headers, 'Stila_kl')

    # SUQQU
    brand_name = 'SUQQU_kl'
    get_Page1('https://www.kaola.com/brand/2736.html', headers, 'SUQQU_kl')

    # Tom Ford
    brand_name = 'Tom Ford_jd'
    html, url = get_Page('https://mall.jd.com/index-1000085081.html', headers, 'Tom Ford_jd')
    parse_Page52(url, html, headers, brand_name)

    # Too cool for school
    brand_name = 'Too cool for school_tm'
    html, url = get_Page('https://toocoolforschoolhzp.tmall.com/', headers, 'Too cool for school_tm')
    parse_Page53(url, html, headers, brand_name)

    # Ultrasun/U佳
    brand_name = 'Ultrasun_jd'
    html, url = get_Page('https://mall.jd.com/index-1000107810.html', headers, 'Ultrasun_jd')
    parse_Page54(url, html, headers, brand_name)

    # Urban Decay/衰败城市
    brand_name = 'Urban Decay_kl'
    get_Page1('https://www.kaola.com/brand/6469.html', headers, 'Urban Decay_kl')

    # Yves Saint laurent/YSL/圣罗兰
    brand_name = 'YSL_gw'
    html, url = get_Page('https://www.yslbeautycn.com/', headers, 'YSL_gw')
    parse_Page55(url, html, headers, brand_name)

    # Zoeva
    brand_name = 'Zoeva_gw'
    html, url = get_Page('http://www.zoevachina.com/', headers, 'Zoeva_gw')
    parse_Page56(url, html, headers, brand_name)

    # Ahava
    brand_name = 'Ahava_gw'
    html, url = get_Page('https://www.ahavachina.cn/', headers, 'Ahava_gw')
    parse_Page57(url, html, headers, brand_name)

    # Algenist奥杰尼
    brand_name = 'Algenist'
    get_Page1('https://www.sephora.cn/search/?k=algenist%E5%A5%A5%E6%9D%B0%E5%B0%BC', headers,'Algenist')

    # Laneige/兰芝
    brand_name = 'Laneige_gw'
    html, url = get_Page('http://www.laneige.com/cn/zh/main.html', headers, 'Laneige_gw')
    parse_Page58(url, html, headers, brand_name)

    # Becca
    brand_name = 'Becca_kl'
    get_Page1('https://www.kaola.com/brand/14708.html', headers, 'Becca_kl')

    # Sulwhasoo/雪花秀
    brand_name = 'Sulwhasoo_tm'
    html, url = get_Page('https://sulwhasoo.tmall.com/', headers, 'Sulwhasoo_tm')
    parse_Page59(url, html, headers, brand_name)

    # Hera/赫妍
    brand_name = 'Hera_tm'
    html, url = get_Page('https://hera.tmall.com/', headers, 'Hera_tm')
    parse_Page60(url, html, headers, brand_name)

    # IOPE/艾诺碧
    brand_name = 'IOPE_gw'
    html, url = get_Page('http://www.iope.com/cn/zh/skincare_makeup.html', headers, 'IOPE_gw')
    parse_Page61(url, html, headers, brand_name)

    # Darphin/朵梵
    brand_name = 'Joyourbaby_jd'
    html, url = get_Page('http://www.darphinchina.com/', headers, 'Darphin_gw')
    parse_Page62(url, html, headers, brand_name)

    # Fenty Beauty
    brand_name = 'Fenty Beauty_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=Fenty%2520Beauty&searchRefer=searchbutton&oldQuery=Drunk%2520Elephant&timestamp=1543199764333', headers,'Fenty Beauty')

    # Fresh
    brand_name = 'Fresh_gw'
    html, url = get_Page('http://cn.fresh.com/', headers, 'Fresh_gw')
    parse_Page63(url, html, headers, brand_name)

    # Kora
    brand_name = 'Kora_tm'
    html, url = get_Page('https://koraorganics.tmall.hk/', headers, 'Kora_tm')
    parse_Page64(url, html, headers, brand_name)

    # L'OCCITANE/欧舒丹
    # https://mall.jd.com/index-1000002984.html
    brand_name = 'LOCCITANE_jd'
    html, url = get_Page_locc('https://zt-jshop.jd.com/service.html', ua, 'LOCCITANE')
    parse_Page65(url, html, headers, brand_name)

    # Lancome/兰蔻
    brand_name = 'Lancome_gw'
    html, url = get_Page('https://www.lancome.com.cn/', headers, 'Lancome_gw')
    parse_Page66(url, html, headers, brand_name)

    # HAIRMAX 京东
    brand_name = 'HAIRMAX_jd'
    html, url = get_Page('https://mall.jd.com/index-1000103004.html', headers, 'HAIRMAX_jd')
    parse_Page67(url, html, headers, brand_name)

    # realtechniques 天猫
    brand_name = 'realtechniques_tm'
    html, url = get_Page('https://realtechniques.tmall.hk/', headers, 'realtechniques_tm')
    parse_Page68(url, html, headers, brand_name)

    # uriage 天猫
    brand_name = 'uriage_tm'
    html, url = get_Page('https://yiquan.tmall.com/', headers, 'uriage_tm')
    parse_Page69(url, html, headers, brand_name)

    # jmsolution 天猫
    brand_name = 'jmsolution_tm'
    html, url = get_Page('https://jmsolution.tmall.hk/', headers, 'jmsolution_tm')
    parse_Page70(url, html, headers, brand_name)

    # lorealparis 官网
    brand_name = "lorealparis_gw"
    htm = get_Page('https://www.lorealparis.com.cn/', headers, 'lorealparis_gw')
    parse_Page71(url, html, headers, brand_name)

    # lorealparis 京东
    brand_name = 'lorealparis_jd'
    html, url = get_Page('https://mall.jd.com/index-1000002662.html', headers, 'lorealparis_jd')
    parse_Page72(url, html, headers, brand_name)

    # Elegance/雅莉格丝 考拉
    brand_name = 'Elegance_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=%25E9%259B%2585%25E8%258E%2589%25E6%25A0%25BC%25E4%25B8%259D&searchRefer=searchbutton&oldQuery=HAIRMAX&timestamp=1544753505586', headers,'Elegance')

    # ahc 天猫
    brand_name = 'ahc_tm'
    html, url = get_Page('https://ahchzp.tmall.com/', headers, 'ahc_tm')
    parse_Page73(url, html, headers, brand_name)

    # maybelline/美宝莲 京东
    brand_name = 'maybelline_jd'
    html, url = get_Page('https://mall.jd.com/index-1000002522.html', headers, 'maybelline_jd')
    parse_Page74(url, html, headers, brand_name)

    # Unny 天猫
    brand_name = 'Unny_tm'
    html, url = get_Page('https://unnyclub.tmall.hk/', headers, 'Unny_tm')
    parse_Page75(url, html, headers, brand_name)

    # VIDIVICI 考拉
    brand_name = 'VIDIVICI_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=VIDIVICI&searchRefer=searchbutton&oldQuery=Unny&timestamp=1544754723451', headers, 'VIDIVICI_kl')

    # PDC/古法 考拉
    brand_name = 'PDC_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=PDC&searchRefer=searchbutton&oldQuery=VIDIVICI&timestamp=1544754793802',headers, 'PDC_kl')

    # SPC 考拉
    brand_name = 'SPC_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=SPC&searchRefer=searchbutton&oldQuery=SPC&timestamp=1544754863578', headers, 'SPC_kl')

    # Revlon/露华浓 天猫
    brand_name = 'Revlon_tm'
    html, url = get_Page('https://revlon.tmall.hk/', headers, 'Revlon_tm')
    parse_Page76(url, html, headers, brand_name)

    # bblaboratories 天猫
    brand_name = 'bblaboratories_tm'
    html, url = get_Page('https://bblaboratories.tmall.hk/', headers, 'bblaboratories_tm')
    parse_Page77(url, html, headers, brand_name)

    # spatreatment 天猫
    brand_name = 'spatreatment_tm'
    html, url = get_Page('https://spatreatment.tmall.hk/', headers, 'spatreatment_tm')
    parse_Page78(url, html, headers, brand_name)

    # naturerepublic/自然共和国 官网
    brand_name = 'naturerepublic_gw'
    html, url = get_Page('http://www.naturerepublic.cn/', headers, 'naturerepublic_gw')
    parse_Page79(url, html, headers, brand_name)

    # naturerepublic/自然共和国 天猫
    brand_name = 'naturerepublic_tm'
    html, url = get_Page('https://naturerepublic.tmall.com/', headers, 'naturerepublic_tm')
    parse_Page80(url, html, headers, brand_name)

    # domecare 天猫
    brand_name = 'domecare_tm'
    html, url = get_Page('https://domecare.tmall.com/?spm=a220o.1000855.1997427721.d4918089.652a6e7fl0nKuG', headers, 'domecare_tm')
    parse_Page81(url, html, headers, brand_name)

    # Rosette 天猫
    brand_name = 'rosette_tm'
    html, url = get_Page('https://rosette.tmall.hk/', headers, 'rosette_tm')
    parse_Page82(url, html, headers, brand_name)

    # # # Rohto/乐敦 京东
    # # html = get_Page_rohto('https://zt-jshop.jd.com/service.html', ua,'rohto_jd')
    # # parse_Page83(url, html, headers, brand_name)

    # utena/佑天兰 天猫
    brand_name = 'utena_tm'
    html, url = get_Page('https://utenahzp.tmall.com/', headers, 'utena_tm')
    parse_Page84(url, html, headers, brand_name)

    # # mariobadescu 天猫
    brand_name = 'mariobadescu_tm'
    html, url = get_Page('https://mariobadescu.tmall.hk/', headers, 'mariobadescu_tm')
    parse_Page85(url, html, headers, brand_name)

    # # aekyungage20s 天猫
    brand_name = 'aekyungage20s_tm'
    html, url = get_Page('https://aekyungage20s.tmall.com/', headers, 'aekyungage20s_tm')
    parse_Page86(url, html, headers, brand_name)

    # # paparecipe 天猫
    brand_name = 'paparecipe_tm'
    html, url = get_Page('https://paparecipehzp.tmall.com/', headers, 'paparecipe_tm')
    parse_Page87(url, html, headers, brand_name)

    # # purevivi 天猫
    brand_name = 'purevivi_tm'
    html, url = get_Page('https://purevivi.tmall.com/', headers, 'purevivi_tm')
    parse_Page88(url, html, headers, brand_name)

    # # kose 天猫
    brand_name = 'kose_tm'
    html, url = get_Page('https://kose.tmall.com/', headers, 'kose_tm')
    parse_Page89(url, html, headers, brand_name)

    # # Shangpree/香蒲丽 天猫
    brand_name = 'shangpree_tm'
    html, url = get_Page('https://shangpree.tmall.hk/', headers, 'shangpree_tm')
    parse_Page90(url, html, headers, brand_name)

    # # Bourjois/妙巴黎 天猫
    brand_name = 'bourjois_tm'
    html, url = get_Page('https://miaobali.tmall.com/', headers, 'bourjois_tm')
    parse_Page91(url, html, headers, brand_name)

    # # Farmacy 京东
    brand_name = 'Farmacy_jd'
    html, url = get_Page('https://mall.jd.hk/index-780421.html', headers, 'Farmacy_jd')
    parse_Page92(url, html, headers, brand_name)

    # # sentianyaozhuang/森田药妆 天猫
    brand_name = 'sentianyaozhuang_tm'
    html, url = get_Page('https://sentianyaozhuang.tmall.com', headers, 'sentianyaozhuang_tm')
    parse_Page93(url, html, headers, brand_name)

    # # Amino mason 考拉
    brand_name = 'Amino mason_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=Amino%2520mason&searchRefer=searchbutton&oldQuery=%25E6%25A3%25AE%25E7%2594%25B0%25E8%258D%25AF%25E5%25A6%2586&timestamp=1544758190706', headers, 'Amino mason_kl')

    # Creer Beaute/凡尔赛 sasa
    brand_name = 'Creer Beaute_sasa'
    get_Page1('http://www.sasa.com/search-Creer%20Beaute.html', headers, 'Creer Beaute_sasa')

    # qualityfirst 天猫
    brand_name = 'qualityfirst_tm'
    html, url = get_Page('https://qualityfirst.tmall.hk/', headers, 'qualityfirst_tm')
    parse_Page94(url, html, headers, brand_name)

    # ettusais_tm 天猫
    brand_name = 'Joyourbaby_jd'
    html, url = get_Page('https://ettusais.tmall.hk', headers, 'ettusais_tm')
    parse_Page95(url, html, headers, brand_name)

    # kumano 天猫
    brand_name = 'kumano_tm'
    html, url = get_Page('https://kumano.tmall.hk/', headers, 'kumano_tm')
    parse_Page96(url, html, headers, brand_name)

    # Orbis/奥蜜思 天猫
    brand_name = 'Orbis_tm'
    html, url = get_Page('https://orbis.tmall.com/', headers, 'Orbis_tm')
    parse_Page97(url, html, headers, brand_name)

    # Orbis/奥蜜思 官网
    brand_name = 'Orbis_gw'
    get_Page1('http://www.orbis.com.cn/', headers, 'Orbis_gw')

    # matsu yama/松山油脂 考拉
    brand_name = 'matsu yama_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=%25E6%259D%25BE%25E5%25B1%25B1%25E6%25B2%25B9%25E8%2584%2582&searchRefer=searchbutton&oldQuery=%25E5%25A5%25A5%25E8%259C%259C%25E6%2580%259D&timestamp=1544758851001', headers, 'matsu yama_kl')

    # daiso/大创 京东
    brand_name = 'daiso_jd'
    html, url = get_Page('https://mall.jd.com/index-667323.html', headers, 'daiso_jd')
    parse_Page98(url, html, headers, brand_name)

    # cerave 天猫
    brand_name = 'cerave_tm'
    html, url = get_Page('https://cerave.tmall.com', headers, 'cerave_tm')
    parse_Page99(url, html, headers, brand_name)

    # growgorgeous 天猫
    brand_name = 'Joyourbaby_jd'
    html, url = get_Page('https://growgorgeous.tmall.hk/', headers, 'growgorgeous_tm')
    parse_Page100(url, html, headers, brand_name)

    # The body shop 考拉
    brand_name = 'The body shop_kl'
    get_Page1('https://www.kaola.com/search.html?changeContent=isSelfProduct&key=The%2520body%2520shop&pageNo=1&type=0&pageSize=60&isStock=false&isSelfProduct=true&isDesc=true&brandId=1247&proIds=&isSearch=0&isPromote=false&isTaxFree=false&factoryStoreTag=-1&backCategory=&country=&headCategoryId=&needBrandDirect=true&searchRefer=searchbutton&referFrom=searchbutton&referPosition=&timestamp=1544759789121&lowerPrice=-1&upperPrice=-1&searchType=synonym&#topTab', headers, 'The body shop_kl')

    # moroccanoil 天猫
    brand_name = 'moroccanoil_tm'
    html, url = get_Page('https://moroccanoil.tmall.hk/', headers, 'moroccanoil_tm')
    parse_Page101(url, html, headers, brand_name)

    # lush 天猫
    brand_name = 'lush_tm'
    html, url = get_Page('https://lush.tmall.hk/', headers, 'lush_tm')
    parse_Page102(url, html, headers, brand_name)

    # YANAGIYA/柳屋 天猫
    brand_name = 'YANAGIYA_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=Yanagiya&searchRefer=searchbutton&oldQuery=Lush&timestamp=1544772191484', headers, 'YANAGIYA_tm')

    # Avalon/阿瓦隆 天猫
    brand_name = 'Avalon_tm'
    html, url = get_Page('https://avalonorganics.tmall.hk', headers, 'Avalon_tm')
    parse_Page103(url, html, headers, brand_name)

    # Batiste/碧缇丝 天猫
    brand_name = 'Batiste_tm'
    html, url = get_Page('https://batiste.tmall.com/', headers, 'Batiste_tm')
    parse_Page104(url, html, headers, brand_name)

    # Mane'n tail 天猫
    brand_name = 'manentail_tm'
    html, url = get_Page('https://manentail-hk.tmall.hk', headers, 'manentail_tm')
    parse_Page105(url, html, headers, brand_name)

    # ruiyanrungao 天猫
    brand_name = 'ruiyanrungao_tm'
    html, url = get_Page('https://ruiyanrungao.tmall.com', headers, 'ruiyanrungao_tm')
    parse_Page106(url, html, headers, brand_name)

    # aussie 天猫
    brand_name = 'aussie_tm'
    html, url = get_Page('https://aussie.tmall.com', headers, 'aussie_tm')
    parse_Page107(url, html, headers, brand_name)

    # tamanohada 天猫
    brand_name = 'tamanohada_tm'
    html, url = get_Page('https://tamanohada.tmall.hk', headers, 'tamanohada_tm')
    parse_Page108(url, html, headers, brand_name)

    # Moist Diane/黛丝恩 京东
    brand_name = 'Moist Diane_jd'
    html, url = get_Page('https://mall.jd.com/index-719938.html', headers, 'Moist Diane_jd')
    parse_Page109(url, html, headers, brand_name)

    # Milbon/玫丽盼 考拉
    brand_name = 'Milbon_kl'
    get_Page1('https://www.kaola.com/search.html?changeContent=isSelfProduct&key=%25E7%258E%25AB%25E4%25B8%25BD%25E7%259B%25BC&pageNo=1&type=0&pageSize=60&isStock=false&isSelfProduct=true&isDesc=true&brandId=&proIds=&isSearch=0&isPromote=false&isTaxFree=false&factoryStoreTag=-1&backCategory=&country=&headCategoryId=&needBrandDirect=true&searchRefer=searchbutton&referFrom=searchbutton&referPosition=&timestamp=1544773035844&lowerPrice=-1&upperPrice=-1&searchType=synonym&#topTab', headers, 'milbon_kl')

    # # Amore/爱茉莉 天猫
    brand_name = 'Amore_tm'
    html, url = get_Page('https://amorepacific.tmall.hk', headers, 'Amore_tm')
    parse_Page110(url, html, headers, brand_name)

    # # Loretta 考拉
    brand_name = 'Loretta_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=Loretta&searchRefer=searchbutton&oldQuery=%25E7%2588%25B1%25E8%258C%2589%25E8%258E%2589&timestamp=1544773220252', headers, 'Loretta_kl')

    # # oubeiqing 天猫
    brand_name = 'oubeiqing_tm'
    html, url = get_Page('https://oubeiqing.tmall.com/', headers, 'oubeiqing_tm')
    parse_Page111(url, html, headers, brand_name)

    # # niurushijian 天猫
    brand_name = 'niurushijian_tm'
    html, url = get_Page('https://niurushijian.tmall.com', headers, 'niurushijian_tm')
    parse_Page112(url, html, headers, brand_name)

    # # sesderma 天猫
    brand_name = 'sesderma_tm'
    html, url = get_Page('https://sesderma.tmall.hk', headers, 'sesderma_tm')
    parse_Page113(url, html, headers, brand_name)

    # # Deonatulle 考拉
    brand_name = 'Deonatulle_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=Deonatulle&searchRefer=searchbutton&oldQuery=Sesderma&timestamp=1544773643503', headers, 'Deonatulle_kl')

    # # lion/狮王 天猫
    brand_name = 'lion_tm'
    html, url = get_Page('https://lion.tmall.com', headers, 'lion_tm')
    parse_Page114(url, html, headers, brand_name)

    # # beautybuffet 天猫
    brand_name = 'beautybuffet_tm'
    html, url = get_Page('https://beautybuffet.tmall.hk', headers, 'beautybuffet_tm')
    parse_Page115(url, html, headers, brand_name)

    # # venuslab 天猫
    brand_name = 'venuslab_tm'
    html, url = get_Page('https://venuslab.tmall.hk', headers, 'venuslab_tm')
    parse_Page116(url, html, headers, brand_name)

    # # swisse 京东
    brand_name = 'swisse_jd'
    html, url = get_Page('https://mall.jd.hk/index-1000074146.html', headers, 'swisse_jd')
    parse_Page117(url, html, headers, brand_name)

    # # marvis 天猫
    brand_name = 'marvis_tm'
    html, url = get_Page('https://marvis.tmall.com', headers, 'marvis_tm')
    parse_Page118(url, html, headers, brand_name)

    # # Propolinse 考拉
    brand_name = 'Propolinse_kl'
    get_Page1('https://www.kaola.com/search.html?zn=top&key=pROPOLINSE&searchRefer=searchbutton&oldQuery=Marvis&timestamp=1544775121235', headers, 'Propolinse_kl')

    # # Ora2/皓乐齿 京东
    brand_name = 'Ora2_jd'
    html, url = get_Page('https://mall.jd.com/index-1000002454.html', headers, 'Ora2_jd')
    parse_Page119(url, html, headers, brand_name)

    # # crest/佳洁士 京东
    brand_name = 'crest_jd'
    html, url = get_Page('https://mall.jd.com/index-1000003795.html', headers, 'crest_jd')
    parse_Page120(url, html, headers, brand_name)


if __name__ == '__main__':
    main()