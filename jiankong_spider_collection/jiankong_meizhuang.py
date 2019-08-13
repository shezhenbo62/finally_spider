# -*- coding: utf-8 -*-
import requests
import os,sys
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
    term_id = 4
    response = requests.get(url,headers=headers,verify=False)
    if response.status_code == 200:
        with open("C:/Users/Administrator/Desktop/img_huodong.csv",'a',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([term_id,brand_name,url])
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


def get_Page_locc(url,ua,brand_name):
    term_id = 4
    formdata = {'functionId': 'getModData',
'body': json.dumps([{"type":"module","moduleId":-288,"moduleData":"{\"lunboGoodsGroup\":{\"materialCode\":\"FGLu5z0jPxQ1S2U\",\"moduleCreate\":2,\"bi\":0,\"type\":\"2\",\"showNum\":\"4\"},\"moduleMarginBottom\":[],\"template\":{\"type\":1,\"templateId\":-256}}"}]),
'source': 'jshopact',
'platformId': '1'}
    headers = {'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'content-length': '492',
'content-type': 'application/x-www-form-urlencoded',
'cookie': 'shshshfpa=6776cfe5-3dcb-a849-8490-9e72806fdd35-1535945241; pinId=5Ux_jKaGlGNiUsqGcz67ULV9-x-f3wj7; cn=0; ipLocation=%u5317%u4EAC; shshshfpb=08e7eb8224927ca3eeda6255336854e51ab6f40ec97c208f45b8caa191; user-key=b491b6a5-7b07-421b-9e35-b17ea7721979; mt_xid=V2_52007VwMSVV1aW14YQRtsBDdRFwVcCFdGG0keCxliCxVXQQtUDkhVHlwAb1YUUQpZU1IZeRpdBW4fElFBWFdLH0kSXgFsABdiX2hSahxNH18CYAETVW1YV1wY; ipLoc-djd=1-72-2799-0; PCSYCityID=1607; shshshfp=f3856d1c446473cfa8f6188a6ba4dd62; __jdc=122270672; __jdv=122270672|direct|-|none|-|1545796044706; __jdu=1161385693; 3AB9D23F7A4B3C9B=SRSFDKQAME6KEG2ETDPUPL6BZJ7BJJ5Y7EVSPDF56SLIWBYNKSUIRLGALVVOJOVTIQ4R6C5MOUIQQVZEIONHJ26DPQ; __jda=122270672.1161385693.1535945240.1545796045.1545810732.286; shshshsID=2acf6494db58fd5176530a0a333f597d_4_1545811855968; __jdb=122270672.4.1161385693|286.1545810732',
'origin': 'https://mall.jd.com',
'referer': 'https://mall.jd.com/index-1000002984.html',
'user-agent': ua.random}
    response = requests.post(url,headers=headers,data=formdata,verify=False)
    if response.status_code == 200:
        with open("C:/Users/Administrator/Desktop/img_huodong.csv",'a',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([term_id,brand_name,'https://mall.jd.com/index-1000002984.html'])
        print(brand_name,url)
        return response.text


def parse_Page(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'HR_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
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
    datas = html_lxml.xpath("//ul[@class='horz-carousel carousel']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Lamer_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https://www.lamer.com.cn'+data.xpath('./div/div/div/a/img/@src')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1]
            response = requests.get(img_url,headers=headers,verify=False)
            if response.status_code == 200:
                time.sleep(1)
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
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'la prairie_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./dt/img/@original')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1].split('!')[0]
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
    datas = html_lxml.xpath("//div[@class='slide']")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'LE LABO_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./a/div/img/@src')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            filename = brand_name + "__" + img_url.split("/")[-1]+'.jpg'
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
    datas = html_lxml.xpath("//ul[@class='ks-switchable-content']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'MAC_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Marc Jacobs_jd'
    # 图片链接
    img_url_list = re.findall(r'"url":"(.*?)"', html)
    for img_url in img_url_list:
        img_url = "https:"+img_url
        # 图片名字
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


def parse_Page6(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='content_lsm_shiyan']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
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


def parse_Page7(html, headers):
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
    brand_name = 'NuFace_tm'
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


def parse_Page8(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='hero-carousel__slide js-hero-carousel__slide']")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Origins_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https://www.origins.com.cn'+data.xpath('.//a/img/@src')[0]
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
    datas = html_lxml.xpath("//div[@id='bd']/div[2]/div/div/@module-data")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Omorovicza_tm'
    for data in datas:
        data = parse.unquote(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0].replace('\\','')
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
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Paul&Joe_tm'
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


def parse_Page11(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='8675e0dcafdc026e50f29bcf299c88dd']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Paulas Choice_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./a/img/@src')[0]
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
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']/span/div[position()<3]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Perricone MD_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./div/div/img/@data-ks-lazyload')[0]
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


def parse_Page13(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='clearfix position_1']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Sisley_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./a/img/@src')[0]
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Tom Ford_jd'
    # 图片链接
    try:
        img_url = "https:"+re.findall(r'img title=\\".*?\\" src=\\"(.*?)\\"',html)[0]
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
    brand_name = 'Too cool for school_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = "https:"+data.xpath("./@data-ks-lazyload")[0]
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
    datas = re.findall(r'src=\\"(.*?)\\"',html)[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Ultrasun_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = "https:"+data
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


def parse_Page17(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='swiper-container common-swiper e-swiper-kv']/div[1]/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
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
    datas = html_lxml.xpath("//div[@class='zq_pictures']/a")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Zoeva_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http://www.zoevachina.com/'+data.xpath("./img/@src")[0]
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
    datas = html_lxml.xpath("//div[@class='kv']/ul/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Ahava_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/img/@src")[0]
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
    datas = html_lxml.xpath("//ul[@class='UIslider-content']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Laneige_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http://www.laneige.com'+data.xpath(".//img/@data-web")[0]
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
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:5]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Sulwhasoo_tm'
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


def parse_Page22(html, headers):
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
    brand_name = 'Hera_tm'
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
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
    datas = html_lxml.xpath("//div[@class='zq_pictures']/a")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Darphin_gw'
    for data in datas[1:-1]:
        # 图片链接
        try:
            img_url = 'http://www.darphinchina.com/'+data.xpath("./img/@src")[0]
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
    datas = html_lxml.xpath("//ul[@id='video-homepage-slider']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Fresh_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath(".//img/@src")[0]
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
    brand_name = 'Kora_tm'
    for data in datas:
        data = parse.unquote(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0].replace('\\','')
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'LOCCITANE'
    # 图片链接
    img_url_list = re.findall(r'"picUrl" : "(.*?)"', html)
    for img_url in img_url_list:
        img_url = "https:"+img_url
        # 图片名字
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
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='swiper-container e-swiper-kv']/div[1]/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
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


def parse_Page29(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'HAIRMAX_jd'
    datas = re.findall(r'url":"(.*?)"',html)[:3]
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


def parse_Page30(html, headers):
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
    brand_name = 'realtechniques_tm'
    for data in datas:
        data = parse.unquote(data)
        # print(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0].replace('\\','')
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


def parse_Page31(html, headers):
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
    brand_name = 'uriage_tm'
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


def parse_Page32(html, headers):
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
    brand_name = 'jmsolution_tm'
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


def parse_Page33(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='home-carousel']/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'lorealparis_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/img/@src")[0]
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


def parse_Page34(html, headers):
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
    brand_name = 'lorealparis_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./img/@original")[0]
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


def parse_Page35(html, headers):
    html_lxml = etree.HTML(html)
    # datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img/parent::div/@style")[:2]
    datas = html_lxml.xpath("//ul[@class='macontent']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ahc_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath(".//img/@data-ks-lazyload")[0]
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


def parse_Page36(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
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


def parse_Page37(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//td/div[1]/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Unny_tm'
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


def parse_Page38(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[position()<3]/div/div/span/div/div/div/table/tbody/tr/td/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Revlon_tm'
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


def parse_Page39(html, headers):
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
    brand_name = 'bblaboratories_tm'
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


def parse_Page40(html, headers):
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
    brand_name = 'spatreatment_tm'
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


def parse_Page41(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='banner']/div/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'naturerepublic_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http://www.naturerepublic.cn'+data.xpath(".//img/@src")[0]
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


def parse_Page42(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[3]//img")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'naturerepublic_tm'
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


def parse_Page43(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[3]/div/div/span/div/div/div/div/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'domecare_tm'
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


def parse_Page44(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div[4]/div/div/@module-data")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'rosette_tm'
    for data in datas:
        data = parse.unquote(data)
        # print(data)
        # 图片链接
        try:
            img_url = 'https:'+re.findall(r'background:url\((.*?)\)',data)[-1].replace('\\','')
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


def parse_Page45(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
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


def parse_Page46(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='content_lsm_shiyan']/li/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'utena_tm'
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


def parse_Page47(html, headers):
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
    brand_name = 'mariobadescu_tm'
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


def parse_Page48(html, headers):
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
    brand_name = 'aekyungage20s_tm'
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


def parse_Page49(html, headers):
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
    brand_name = 'paparecipe_tm'
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


def parse_Page50(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img/parent::div/@style")[:1]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'purevivi_tm'
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


def parse_Page51(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='tianmao123']//img")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'kose_tm'
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


def parse_Page52(html, headers):
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
    brand_name = 'shangpree_tm'
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


def parse_Page53(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//span/div/div/div/div/a/div/@style")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'bourjois_tm'
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


def parse_Page54(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt/img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Farmacy_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@original")[0]
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


def parse_Page55(html, headers):
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
    brand_name = 'sentianyaozhuang_tm'
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


def parse_Page56(html, headers):
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
    brand_name = 'qualityfirst_tm'
    for data in datas:
        data = parse.unquote(data)
        # print(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0].replace('\\','')
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


def parse_Page57(html, headers):
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
    brand_name = 'ettusais_tm'
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


def parse_Page58(html, headers):
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
    brand_name = 'kumano_tm'
    for data in datas:
        data = parse.unquote(data)
        # print(data)
        # 图片链接
        try:
            img_url = re.findall(r'"shopBgImg":"(.*?)"',data)[0].replace('\\','')
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


def parse_Page59(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//a/@style")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Orbis_tm'
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


def parse_Page60(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt/img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'daiso_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@original")[0]
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


def parse_Page61(html, headers):
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
    brand_name = 'cerave_tm'
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


def parse_Page62(html, headers):
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
    brand_name = 'growgorgeous_tm'
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


def parse_Page63(html, headers):
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
    brand_name = 'moroccanoil_tm'
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


def parse_Page64(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//a/@style")[:4]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'lush_tm'
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


def parse_Page65(html, headers):
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
    brand_name = 'Avalon_tm'
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


def parse_Page66(html, headers):
    datas = re.findall(r';background:url\((.*?)\)',html)[-1:]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Batiste_tm'
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


def parse_Page67(html, headers):
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
    brand_name = 'manentail_tm'
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


def parse_Page68(html, headers):
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
    brand_name = 'ruiyanrungao_tm'
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


def parse_Page69(html, headers):
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
    brand_name = 'aussie_tm'
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


def parse_Page70(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div[4]/div/div/@module-data")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'tamanohada_tm'
    for data in datas:
        data = parse.unquote(data)
        # print(data)
        # 图片链接
        try:
            img_url = re.findall(r'background:url\((.*?)\)',data)[0].replace('\\','')
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


def parse_Page71(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
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


def parse_Page72(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content c514546']/div/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Amore_tm'
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


def parse_Page73(html, headers):
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
    brand_name = 'oubeiqing_tm'
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


def parse_Page74(html, headers):
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
    brand_name = 'niurushijian_tm'
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


def parse_Page75(html, headers):
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
    brand_name = 'sesderma_tm'
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


def parse_Page76(html, headers):
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
    brand_name = 'lion_tm'
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


def parse_Page77(html, headers):
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
    brand_name = 'beautybuffet_tm'
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


def parse_Page78(html, headers):
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
    brand_name = 'venuslab_tm'
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


def parse_Page79(html, headers):
    datas = re.findall(r'src=\\"(.*?)\\"',html)[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'swisse_jd'
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


def parse_Page80(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//img")[:1]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'marvis_jd'
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


def parse_Page81(html, headers):
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
    brand_name = 'Ora2_jd'
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


def parse_Page82(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='userDefinedArea']/div/img")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'crest_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'http:'+data.xpath("./@original")[0]
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
    # HR/赫莲娜
    html = get_Page('https://helenarubinstein.tmall.com/',headers,'HR_tm')
    parse_Page(html,headers)
    # Jo Malone London/祖·玛珑
    html1 = get_Page1('https://www.jomalone.com.cn/', headers,'Jo Malone London_gw')
    # Lamer/海蓝之谜
    html2 = get_Page('https://www.lamer.com.cn/',headers,'Lamer_gw')
    parse_Page1(html2,headers)
    # la prairie/莱珀妮
    html3 = get_Page('https://mall.jd.com/index-1000119661.html',headers,'la prairie_jd')
    parse_Page2(html3,headers)
    # Laura Mercier/罗拉玛斯亚
    html4 = get_Page1('https://search.jd.com/Search?keyword=Laura%20Mercier&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%8E%B1%E7%8F%80%E5%A6%AE&stock=1&wtype=1&click=1',headers,'Laura Mercier')
    # LE LABO
    headers1 = {'User-Agent': ua.random,
               'cookie': '__cfduid=d4dff2295de80eecbbd990529577142221539057647; acdc_vat=false; _ga=GA1.2.1835578554.1539057650; acdc_region=HK; ACDC_LOCALE=EN; acdc_currency=EUR; AWSALB=t71oZEHcjB550TWfoI4jVe4wj5kboRFHaiztxZW9rwE69sdP8lBN6ILgzEhkQC7IRcF5/D7ggHmic9vehkw6Pv+C9GFEUS5mZPJ5eQfDq0eyYKbJnsUwS4kiKECK; acdc_disclaimer=true; _gid=GA1.2.214871939.1543220959; csrfToken=6a4221d3-6e2f-4a97-86b5-26f6cee0036c'}
    html5 = get_Page('https://www.lelabofragrances.com/',headers1,'LE LABO_gw')
    parse_Page3(html5,headers)
    # M.A.C/魅可
    html6 = get_Page('https://mac.tmall.com/',headers,'MAC_tm')
    parse_Page4(html6,headers)
    # Marc Jacobs/马克雅可布
    # https://mall.jd.com/index-1000005205.html
    html7 = get_Page('https://mall.jd.com/index-1000005205.html',headers,'Marc Jacobs_jd')
    parse_Page5(html7,headers)
    # Nars 
    html8 = get_Page('https://nars.tmall.com/',headers, 'Nars_tm')
    parse_Page6(html8, headers)
    # Natasha Denona 
    html9 = get_Page1('https://cn.feelunique.com/search/result?q=Natasha%20Denona', headers,'Natasha Denona')
    # NuFace 
    html10 = get_Page('https://nuface.tmall.hk',headers, 'NuFace_tm')
    parse_Page7(html10, headers)
    # NYX Professional Makeup 
    html11 = get_Page1('https://cn.feelunique.com/search/result?q=NYX%20Professional%20Makeup', headers,'NYX')
    # Origins/悦木之源 
    html11 = get_Page('https://www.origins.com.cn',headers, 'Origins_gw')
    parse_Page8(html11, headers)
    # Omorovicza/欧微泉萨
    html12 = get_Page('https://omorovicza.tmall.hk/', headers, 'Omorovicza_tm')
    parse_Page9(html12, headers)
    # Paul&Joe
    html13 = get_Page('https://pauljoe.tmall.hk/', headers, 'Paul&Joe_tm')
    parse_Page10(html13, headers)
    # Paula's Choice/宝拉珍选
    html14 = get_Page('http://www.paulaschoice.hk/', headers, 'Paulas Choice_gw')
    parse_Page11(html14, headers)
    # Perricone MD
    html15 = get_Page('https://pmdus.tmall.hk/', headers, 'Perricone MD_tm')
    parse_Page12(html15, headers)
    # Peterthomasroth/彼得罗夫
    html16 = get_Page1('https://www.sephora.cn/brand/peterthomasroth-342', headers,'Peterthomasroth')
    # RMK
    html17 = get_Page1('https://www.kaola.com/brand/1886.html?', headers,'RMK')
    # Sarah Chapman
    html18 = get_Page1('https://cn.feelunique.com/search/result?q=Sarah%20Chapman', headers,'Sarah Chapman')
    # Sisley/希思黎
    html19 = get_Page('http://www.sisley.com.cn/', headers, 'Sisley_gw')
    parse_Page13(html19, headers)
    # Stila/诗狄娜
    html20 = get_Page1('https://www.kaola.com/brand/6673.html', headers,'Stila')
    # SUQQU
    html21 = get_Page1('https://www.kaola.com/brand/2736.html', headers,'SUQQU')
    # Tom Ford
    html22 = get_Page('https://mall.jd.com/index-1000085081.html', headers, 'Tom Ford_jd')
    parse_Page14(html22, headers)
    # Too cool for school
    html23 = get_Page('https://toocoolforschoolhzp.tmall.com/', headers, 'Too cool for school_tm')
    parse_Page15(html23, headers)
    # Ultrasun/U佳
    html24 = get_Page('https://mall.jd.com/index-1000107810.html', headers, 'Ultrasun_jd')
    parse_Page16(html24, headers)
    # Urban Decay/衰败城市
    html25 = get_Page1('https://www.kaola.com/brand/6469.html', headers,'Urban Decay')
    # Yves Saint laurent/YSL/圣罗兰
    html26 = get_Page('https://www.yslbeautycn.com/', headers, 'YSL_gw')
    parse_Page17(html26, headers)
    # Zoeva
    html27 = get_Page('http://www.zoevachina.com/', headers, 'Zoeva_gw')
    parse_Page18(html27, headers)
    # Ahava
    html28 = get_Page('https://www.ahavachina.cn/', headers, 'Ahava_gw')
    parse_Page19(html28, headers)
    # Algenist奥杰尼
    html29 = get_Page1('https://www.sephora.cn/search/?k=algenist%E5%A5%A5%E6%9D%B0%E5%B0%BC', headers,'Algenist')
    # Laneige/兰芝
    html30 = get_Page('http://www.laneige.com/cn/zh/main.html', headers, 'Laneige_gw')
    parse_Page20(html30, headers)
    # Becca
    html31 = get_Page1('https://www.kaola.com/brand/14708.html', headers,'Becca')
    # Sulwhasoo/雪花秀
    html32 = get_Page('https://sulwhasoo.tmall.com/', headers, 'Sulwhasoo_tm')
    parse_Page21(html32, headers)
    # Hera/赫妍
    html33 = get_Page('https://hera.tmall.com/', headers, 'Hera_tm')
    parse_Page22(html33, headers)
    # IOPE/艾诺碧
    html34 = get_Page('http://www.iope.com/cn/zh/skincare_makeup.html', headers, 'IOPE_gw')
    parse_Page23(html34, headers)
    # Darphin/朵梵
    html35 = get_Page('http://www.darphinchina.com/', headers, 'Darphin_gw')
    parse_Page24(html35, headers)
    # Fenty Beauty
    html36 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Fenty%2520Beauty&searchRefer=searchbutton&oldQuery=Drunk%2520Elephant&timestamp=1543199764333', headers,'Fenty Beauty')
    # Fresh
    html37 = get_Page('http://cn.fresh.com/', headers, 'Fresh_gw')
    parse_Page25(html37, headers)
    # Kora
    html38 = get_Page('https://koraorganics.tmall.hk/', headers, 'Kora_tm')
    parse_Page26(html38, headers)
    # Lancome/兰蔻
    html40 = get_Page('https://www.lancome.com.cn/', headers, 'Lancome_gw')
    parse_Page28(html40, headers)
    # HAIRMAX 京东
    html41 = get_Page('https://mall.jd.com/index-1000103004.html', headers, 'HAIRMAX_jd')
    parse_Page29(html41, headers)
    # realtechniques 天猫
    html42 = get_Page('https://realtechniques.tmall.hk/', headers, 'realtechniques_tm')
    parse_Page30(html42, headers)
    # uriage 天猫
    html43 = get_Page('https://yiquan.tmall.com/', headers, 'uriage_tm')
    parse_Page31(html43, headers)
    # jmsolution 天猫
    html44 = get_Page('https://jmsolution.tmall.hk/', headers, 'jmsolution_tm')
    parse_Page32(html44, headers)
    # lorealparis 官网
    html45 = get_Page('https://www.lorealparis.com.cn/', headers, 'lorealparis_gw')
    parse_Page33(html45, headers)
    # lorealparis 京东
    html46 = get_Page('https://mall.jd.com/index-1000002662.html', headers, 'lorealparis_jd')
    parse_Page34(html46, headers)
    # Elegance/雅莉格丝 考拉
    html47 = get_Page1('https://www.kaola.com/search.html?zn=top&key=%25E9%259B%2585%25E8%258E%2589%25E6%25A0%25BC%25E4%25B8%259D&searchRefer=searchbutton&oldQuery=HAIRMAX&timestamp=1544753505586', headers,'Elegance')
    # ahc 天猫
    html48 = get_Page('https://ahchzp.tmall.com/', headers, 'ahc_tm')
    parse_Page35(html48, headers)
    # maybelline/美宝莲 京东
    html49 = get_Page('https://mall.jd.com/index-1000002522.html', headers, 'maybelline_jd')
    parse_Page36(html49, headers)
    # Unny 天猫
    html50 = get_Page('https://unnyclub.tmall.hk/', headers, 'Unny_tm')
    parse_Page37(html50, headers)
    # VIDIVICI 考拉
    html51 = get_Page1('https://www.kaola.com/search.html?zn=top&key=VIDIVICI&searchRefer=searchbutton&oldQuery=Unny&timestamp=1544754723451', headers, 'VIDIVICI_kl')
    # PDC/古法 考拉
    html52 = get_Page1('https://www.kaola.com/search.html?zn=top&key=PDC&searchRefer=searchbutton&oldQuery=VIDIVICI&timestamp=1544754793802',headers, 'PDC_kl')
    # SPC 考拉
    html53 = get_Page1('https://www.kaola.com/search.html?zn=top&key=SPC&searchRefer=searchbutton&oldQuery=SPC&timestamp=1544754863578', headers, 'SPC_kl')
    # Revlon/露华浓 天猫
    html54 = get_Page('https://revlon.tmall.hk/', headers, 'Revlon_tm')
    parse_Page38(html54, headers)
    # bblaboratories 天猫
    html55 = get_Page('https://bblaboratories.tmall.hk/', headers, 'bblaboratories_tm')
    parse_Page39(html55, headers)
    # spatreatment 天猫
    html56 = get_Page('https://spatreatment.tmall.hk/', headers, 'spatreatment_tm')
    parse_Page40(html56, headers)
    # naturerepublic/自然共和国 官网
    html57 = get_Page('http://www.naturerepublic.cn/', headers, 'naturerepublic_gw')
    parse_Page41(html57, headers)
    # naturerepublic/自然共和国 天猫
    html58 = get_Page('https://naturerepublic.tmall.com/', headers, 'naturerepublic_tm')
    parse_Page42(html58, headers)
    # domecare 天猫
    html59 = get_Page('https://domecare.tmall.com/?spm=a220o.1000855.1997427721.d4918089.652a6e7fl0nKuG', headers, 'domecare_tm')
    parse_Page43(html59, headers)
    # Rosette 天猫
    html60 = get_Page('https://rosette.tmall.hk/', headers, 'rosette_tm')
    parse_Page44(html60, headers)
    # # Rohto/乐敦 京东
    # html61 = get_Page_rohto('https://zt-jshop.jd.com/service.html', ua,'rohto_jd')
    # parse_Page45(html61, headers)
    # utena/佑天兰 天猫
    html62 = get_Page('https://utenahzp.tmall.com/', headers,'utena_tm')
    parse_Page46(html62, headers)
    # # mariobadescu 天猫
    html63 = get_Page('https://mariobadescu.tmall.hk/', headers, 'mariobadescu_tm')
    parse_Page47(html63, headers)
    # # aekyungage20s 天猫
    html64 = get_Page('https://aekyungage20s.tmall.com/', headers, 'aekyungage20s_tm')
    parse_Page48(html64, headers)
    # # paparecipe 天猫
    html65 = get_Page('https://paparecipehzp.tmall.com/', headers, 'paparecipe_tm')
    parse_Page49(html65, headers)
    # # purevivi 天猫
    html66 = get_Page('https://purevivi.tmall.com/', headers, 'purevivi_tm')
    parse_Page50(html66, headers)
    # # kose 天猫
    html67 = get_Page('https://kose.tmall.com/', headers, 'kose_tm')
    parse_Page51(html67, headers)
    # # Shangpree/香蒲丽 天猫
    html68 = get_Page('https://shangpree.tmall.hk/', headers, 'shangpree_tm')
    parse_Page52(html68, headers)
    # # Bourjois/妙巴黎 天猫
    html69 = get_Page('https://miaobali.tmall.com/', headers, 'bourjois_tm')
    parse_Page53(html69, headers)
    # # Farmacy 京东
    html70 = get_Page('https://mall.jd.hk/index-780421.html', headers, 'Farmacy_jd')
    parse_Page54(html70, headers)
    # # sentianyaozhuang/森田药妆 天猫
    html71 = get_Page('https://sentianyaozhuang.tmall.com', headers, 'sentianyaozhuang_tm')
    parse_Page55(html71, headers)
    # # Amino mason 考拉
    html72 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Amino%2520mason&searchRefer=searchbutton&oldQuery=%25E6%25A3%25AE%25E7%2594%25B0%25E8%258D%25AF%25E5%25A6%2586&timestamp=1544758190706', headers, 'Amino mason_kl')
    # Creer Beaute/凡尔赛 sasa
    html73 = get_Page1('http://www.sasa.com/search-Creer%20Beaute.html', headers, 'Creer Beaute_sasa')
    # qualityfirst 天猫
    html74 = get_Page('https://qualityfirst.tmall.hk/', headers, 'qualityfirst_tm')
    parse_Page56(html74, headers)
    # ettusais 天猫
    html75 = get_Page('https://ettusais.tmall.hk', headers, 'ettusais_tm')
    parse_Page57(html75, headers)
    # kumano 天猫
    html76 = get_Page('https://kumano.tmall.hk/', headers, 'kumano_tm')
    parse_Page58(html76, headers)
    # Orbis/奥蜜思 天猫
    html77 = get_Page('https://orbis.tmall.com/', headers, 'Orbis_tm')
    parse_Page59(html77, headers)
    # Orbis/奥蜜思 官网
    html78 = get_Page1('http://www.orbis.com.cn/', headers, 'Orbis_gw')
    # matsu yama/松山油脂 考拉
    html79 = get_Page1('https://www.kaola.com/search.html?zn=top&key=%25E6%259D%25BE%25E5%25B1%25B1%25E6%25B2%25B9%25E8%2584%2582&searchRefer=searchbutton&oldQuery=%25E5%25A5%25A5%25E8%259C%259C%25E6%2580%259D&timestamp=1544758851001', headers, 'matsu yama_kl')
    # daiso/大创 京东
    html80 = get_Page('https://mall.jd.com/index-667323.html', headers, 'daiso_jd')
    parse_Page60(html80, headers)
    # cerave 天猫
    html81 = get_Page('https://cerave.tmall.com', headers, 'cerave_tm')
    parse_Page61(html81, headers)
    # growgorgeous 天猫
    html82 = get_Page('https://growgorgeous.tmall.hk/', headers, 'growgorgeous_tm')
    parse_Page62(html82, headers)
    # The body shop 考拉
    html83 = get_Page1('https://www.kaola.com/search.html?changeContent=isSelfProduct&key=The%2520body%2520shop&pageNo=1&type=0&pageSize=60&isStock=false&isSelfProduct=true&isDesc=true&brandId=1247&proIds=&isSearch=0&isPromote=false&isTaxFree=false&factoryStoreTag=-1&backCategory=&country=&headCategoryId=&needBrandDirect=true&searchRefer=searchbutton&referFrom=searchbutton&referPosition=&timestamp=1544759789121&lowerPrice=-1&upperPrice=-1&searchType=synonym&#topTab', headers, 'The body shop_kl')
    # moroccanoil 天猫
    html84 = get_Page('https://moroccanoil.tmall.hk/', headers, 'moroccanoil_tm')
    parse_Page63(html84, headers)
    # lush 天猫
    html85 = get_Page('https://lush.tmall.hk/', headers, 'lush_tm')
    parse_Page64(html85, headers)
    # YANAGIYA/柳屋 天猫
    html86 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Yanagiya&searchRefer=searchbutton&oldQuery=Lush&timestamp=1544772191484', headers, 'YANAGIYA_tm')
    # Avalon/阿瓦隆 天猫
    html87 = get_Page('https://avalonorganics.tmall.hk', headers, 'Avalon_tm')
    parse_Page65(html87, headers)
    # Batiste/碧缇丝 天猫
    html88 = get_Page('https://batiste.tmall.com/', headers, 'Batiste_tm')
    parse_Page66(html88, headers)
    # Mane'n tail 天猫
    html89 = get_Page('https://manentail-hk.tmall.hk', headers, 'manentail_tm')
    parse_Page67(html89, headers)
    # ruiyanrungao 天猫
    html90 = get_Page('https://ruiyanrungao.tmall.com', headers, 'ruiyanrungao_tm')
    parse_Page68(html90, headers)
    # aussie 天猫
    html91 = get_Page('https://aussie.tmall.com', headers, 'aussie_tm')
    parse_Page69(html91, headers)
    # tamanohada 天猫
    html92 = get_Page('https://tamanohada.tmall.hk', headers, 'tamanohada_tm')
    parse_Page70(html92, headers)
    # Moist Diane/黛丝恩 京东
    html93 = get_Page('https://mall.jd.com/index-719938.html', headers, 'Moist Diane_jd')
    parse_Page71(html93, headers)
    # Milbon/玫丽盼 考拉
    html94 = get_Page1('https://www.kaola.com/search.html?changeContent=isSelfProduct&key=%25E7%258E%25AB%25E4%25B8%25BD%25E7%259B%25BC&pageNo=1&type=0&pageSize=60&isStock=false&isSelfProduct=true&isDesc=true&brandId=&proIds=&isSearch=0&isPromote=false&isTaxFree=false&factoryStoreTag=-1&backCategory=&country=&headCategoryId=&needBrandDirect=true&searchRefer=searchbutton&referFrom=searchbutton&referPosition=&timestamp=1544773035844&lowerPrice=-1&upperPrice=-1&searchType=synonym&#topTab', headers, 'milbon_kl')
    # # Amore/爱茉莉 天猫
    html95 = get_Page('https://amorepacific.tmall.hk', headers, 'Amore_tm')
    parse_Page72(html95, headers)
    # # Loretta 考拉
    html96 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Loretta&searchRefer=searchbutton&oldQuery=%25E7%2588%25B1%25E8%258C%2589%25E8%258E%2589&timestamp=1544773220252', headers, 'Loretta_kl')
    # # oubeiqing 天猫
    html96 = get_Page('https://oubeiqing.tmall.com/', headers, 'oubeiqing_tm')
    parse_Page73(html96, headers)
    # # niurushijian 天猫
    html97 = get_Page('https://niurushijian.tmall.com', headers, 'niurushijian_tm')
    parse_Page74(html97, headers)
    # # sesderma 天猫
    html98 = get_Page('https://sesderma.tmall.hk', headers, 'sesderma_tm')
    parse_Page75(html98, headers)
    # # Deonatulle 考拉
    html99 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Deonatulle&searchRefer=searchbutton&oldQuery=Sesderma&timestamp=1544773643503', headers, 'Deonatulle_kl')
    # # lion/狮王 天猫
    html100 = get_Page('https://lion.tmall.com', headers, 'lion_tm')
    parse_Page76(html100, headers)
    # # beautybuffet 天猫
    html101 = get_Page('https://beautybuffet.tmall.hk', headers, 'beautybuffet_tm')
    parse_Page77(html101, headers)
    # # venuslab 天猫
    html102 = get_Page('https://venuslab.tmall.hk', headers, 'venuslab_tm')
    parse_Page78(html102, headers)
    # # swisse 京东
    html103 = get_Page('https://mall.jd.hk/index-1000074146.html', headers, 'swisse_jd')
    parse_Page79(html103, headers)
    # # marvis 天猫
    html104 = get_Page('https://marvis.tmall.com', headers, 'marvis_jd')
    parse_Page80(html104, headers)
    # # Propolinse 考拉
    html105 = get_Page1('https://www.kaola.com/search.html?zn=top&key=pROPOLINSE&searchRefer=searchbutton&oldQuery=Marvis&timestamp=1544775121235', headers, 'Propolinse_kl')
    # # Ora2/皓乐齿 京东
    html106 = get_Page('https://mall.jd.com/index-1000002454.html', headers, 'Ora2_jd')
    parse_Page81(html106, headers)
    # # crest/佳洁士 京东
    html107 = get_Page('https://mall.jd.com/index-1000003795.html', headers, 'crest_jd')
    parse_Page82(html107, headers)


if __name__ == '__main__':
    main()