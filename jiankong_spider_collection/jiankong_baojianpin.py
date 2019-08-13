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


def get_Page_dezhuang(url,ua,brand_name):
    formdata = {'functionId': 'getModData',
'body': json.dumps([{"type":"module","moduleId":-288,"moduleData":"{\"lunboGoodsGroup\":{\"materialCode\":\"6pDQbG0WTRa\",\"moduleCreate\":2,\"bi\":0,\"type\":\"2\",\"showNum\":4},\"moduleMarginBottom\":[],\"template\":{\"type\":1,\"templateId\":-256}}"}]),
'source': 'jshopact',
'platformId': '1'}
    headers = {'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'content-length': '476',
'content-type': 'application/x-www-form-urlencoded',
'cookie': 'shshshfpa=6776cfe5-3dcb-a849-8490-9e72806fdd35-1535945241; pinId=5Ux_jKaGlGNiUsqGcz67ULV9-x-f3wj7; cn=0; ipLocation=%u5317%u4EAC; shshshfpb=08e7eb8224927ca3eeda6255336854e51ab6f40ec97c208f45b8caa191; user-key=b491b6a5-7b07-421b-9e35-b17ea7721979; mt_xid=V2_52007VwMSVV1aW14YQRtsBDdRFwVcCFdGG0keCxliCxVXQQtUDkhVHlwAb1YUUQpZU1IZeRpdBW4fElFBWFdLH0kSXgFsABdiX2hSahxNH18CYAETVW1YV1wY; ipLoc-djd=1-72-2799-0; PCSYCityID=1607; __jdv=122270672|direct|-|none|-|1545796044706; __jdu=1161385693; 3AB9D23F7A4B3C9B=SRSFDKQAME6KEG2ETDPUPL6BZJ7BJJ5Y7EVSPDF56SLIWBYNKSUIRLGALVVOJOVTIQ4R6C5MOUIQQVZEIONHJ26DPQ; _gcl_au=1.1.1982296530.1545893498; shshshfp=f3856d1c446473cfa8f6188a6ba4dd62; __jda=122270672.1161385693.1535945240.1545893292.1545977485.290; __jdc=122270672; shshshsID=d4669401db48f3338e568b3c2b0b4338_3_1545977590958; __jdb=122270672.4.1161385693|290.1545977485',
'origin': 'https://mall.jd.com',
'referer': 'https://mall.jd.com/index-1000093771.html',
'user-agent': ua.random}
    response = requests.post(url,headers=headers,data=formdata,verify=False)
    if response.status_code == 200:
        with open("C:/Users/Administrator/Desktop/img_huodong.csv",'a',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name,'https://mall.jd.com/index-1000093771.html'])
        print(brand_name,url)
        return response.text


def parse_Page(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//span/div/@style")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'orihiro_tm'
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


def parse_Page1(html, headers):
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
    brand_name = 'orihiro_tm'
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


def parse_Page2(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//span/div/@style")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'isdg_tm'
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


def main():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    # # orihiro/立喜乐 天猫
    # html = get_Page('https://orihiro.tmall.hk',headers,'orihiro_tm')
    # parse_Page(html,headers)
    # # nordic/挪威小鱼 天猫
    # html1 = get_Page('https://nordic.tmall.hk', headers, 'nordic_tm')
    # parse_Page1(html1, headers)
    # # ISDG 天猫
    # html2 = get_Page('https://isdg.tmall.hk', headers, 'isdg_tm')
    # parse_Page2(html2, headers)
    # Optislim 考拉
    html3 = get_Page1('https://search.kaola.com/search.html?zn=top&key=Optislim&searchRefer=searchbutton&oldQuery=%25E6%2596%25AF%25E6%2597%25BA%25E6%25A3%25AE&timestamp=1543976831154&hcAntiCheatSwitch=0&anstipamActiCheatSwitch=1&anstipamActiCheatToken=ee7b2ce7910f4e04ac89bbdae1871d04&anstipamActiCheatValidate=anstipam_acti_default_validate', headers, 'Optislim_kl')


if __name__ == '__main__':
    main()