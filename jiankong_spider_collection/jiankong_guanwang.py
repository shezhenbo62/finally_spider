# -*- coding: utf-8 -*-
import requests
import os
import time,re,json,csv
from fake_useragent import UserAgent
from lxml import etree
from urllib import parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

words_base = ['OFF','优惠','特惠','折','减','新品','上新','狂欢','发售','活动','开抢','特卖','赠','联名','礼遇','sale']
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
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        with open("C:/Users/Administrator/Desktop/img_huodong.csv", 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name, url])
        print(brand_name, url)
        return response.text


def get_Page1(url,headers,brand_name):
    response = requests.get(url,headers=headers,verify=False)
    if response.status_code == 200:
        for word in words_base:
            if word in response.text:
                with open("C:/Users/Administrator/Desktop/huodong.csv",'a',encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([brand_name,url, "活动类型：%s" % word])
                print(brand_name,url,"品牌在做活动，"+"活动类型：%s"%word)
                break
        return response.text

# carihome品牌
def get_page_carihome(url,headers,brand_name):
    response = requests.get(url,headers=headers,verify=False)
    if response.status_code == 200:
        with open("C:/Users/Administrator/Desktop/img_huodong.csv",'a',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name,'https://mall.jd.com/index-731748.html'])
        print(url + "品牌在做活动")
        return response.text


def parse_Page(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='flexslider flexslider-7-25 ']/ul/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Evisu'
    for data in datas:
        # 图片链接
        img_url = data.xpath('.//img/@src')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('.//img/@src')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page1(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='col-1 scroll-icon-ption']/ul/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'PUMA'
    for data in datas:
        # 图片链接
        img_url = "https:"+data.xpath('.//img/@src')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('.//img/@src')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page2(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='scroll-background-image']")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Reebok'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./img/@src')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./img/@src')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page3(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='swiper-wrapper']/div/a/img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'vans'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./@data-src')[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page4(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='gm-abs switchable-content-193']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'CHIARA FERRAGNI'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./a/@style')[0]
        img_url = 'http:'+re.findall(r'url\((.*?)\)',img_url)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page5(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//a/parent::div/@style")[:4]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'cozy steps'
    for data in datas:
        # 图片链接
        img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page6(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Hush Puppies'
    # 图片链接
    img_url = 'http:' + re.findall(r'"picUrl" : "(.*?)"', html)[0]
    # 图片名字
    filename = brand_name + "__" + img_url.split("/")[-1]
    # 验证码图片文件名
    response = requests.get(img_url,headers=headers,verify=False)
    if response.status_code == 200:
        image = response.content
        try:
            with open(filename,'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
        except Exception as e:
            filename = brand_name + str(count) + '.jpg'
            with open(filename, 'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page7(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//a/parent::div/@style")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'bell'
    for data in datas:
        # 图片链接
        img_url = 'http:'+re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page8(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Palladium'
    for data in datas:
        # 图片链接
        img_url = re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page9(html, headers):
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
    brand_name = 'apm monaco'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath('./@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


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
    brand_name = 'CITIZEN'
    for data in datas:
        # 图片链接
        img_url = 'http:'+data.xpath('./@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page11(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='slides']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Longines'
    for data in datas:
        # 图片链接
        img_url = data.xpath('.//picture/source[1]/@srcset')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('.//picture/source[1]/@srcset')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page12(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@id='homepageSlider']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Tissot'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./a/img[1]/@src')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./a/img[1]/@src')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page13(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='slides']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'FIYTA'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./a/img/@src')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./a/img/@src')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page14(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='slides']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'CIGA Design'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./@style')[0]
        img_url = re.findall(r"src='(.*?)'",img_url)[0].replace("1","")
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page15(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='carousel-inner position-box role-position-box']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'casio'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./a/@style')[0]
        img_url = re.findall(r"url\('(.*?)'\)",img_url)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page16(html, headers):
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
    brand_name = 'ISSEY MIYAKE'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath('./@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page17(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@alt='PC(tm)-fin.jpg']|//img[@alt='banner-2']")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'LACOSTE'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath('./@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./@data-ks-lazyload')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page18(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//a[@class='bndw']")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Jonasverus'
    for data in datas:
        # 图片链接
        img_url = 'http://www.jonasverus.com'+data.xpath('./img/@src')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./img/@src')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page19(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Folli Follie'
    # 图片链接
    img_url = 'https:'+re.findall(r'src=\\"(.*?)\\"',html)[0]
    # 图片名字
    filename = brand_name + "__" + img_url.split("/")[-1]
    # 验证码图片文件名
    response = requests.get(img_url,headers=headers,verify=False)
    if response.status_code == 200:
        image = response.content
        try:
            with open(filename,'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
        except Exception as e:
            filename = brand_name + str(count) + '.jpg'
            with open(filename, 'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page20(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='swiper-wrapper']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ENZO'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./@style')[0]
        img_url = 'http://www.enzo-jewelry.com'+re.findall(r"url\('(.*?)'\)",img_url)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page21(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//table[@id='__01']//img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'CHOW TAI FOOK'
    for data in datas:
        # 图片链接
        img_url = data.xpath('./@data-original')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./@data-original')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page22(html, headers):
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
    brand_name = 'LaPerla'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./a/img/@data-ks-lazyload')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page23(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Tory Burch'
    # 图片链接
    img_url = 'https:'+re.findall(r'"picUrl" : "(.*?)"',html)[0]
    # 图片名字
    filename = brand_name + "__" + re.findall(r'"picUrl" : "(.*?)"',html)[0].split("/")[-1]
    # 验证码图片文件名
    response = requests.get(img_url,headers=headers,verify=False)
    if response.status_code == 200:
        image = response.content
        try:
            with open(filename,'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
        except Exception as e:
            filename = brand_name + str(count) + '.jpg'
            with open(filename, 'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page24(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//dl[@class='contsls']/dd")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Urban Outfitter'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./a/img/@data-ks-lazyload')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page25(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@alt='1119PC_01.jpg']")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'yifuli'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath('./@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./@data-ks-lazyload')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page26(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='gm-box abs eff1']/a")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Dazzle'
    for data in datas:
        # 图片链接
        img_url = data.xpath("./@style")[0]
        img_url = 'https:'+re.findall(r"url\((.*?)\)",img_url)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page27(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']//div[@class='main-wrap J_TRegion']/div[2]//div[@class='rel']")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Sandro'
    for data in datas:
        # 图片链接
        img_url = data.xpath("./@style")[0]
        img_url = 'https:'+re.findall(r"url\((.*?)\)",img_url)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page28(html, headers):
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
    brand_name = 'Allsaints'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./a/img/@data-ks-lazyload')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page29(html, headers):
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
    brand_name = 'Icicle'
    for data in datas:
        # 图片链接
        img_url = data.xpath(".//div[@class='zfh']/div/div/a/@style")[0]
        img_url = 'https:'+re.findall(r"url\((.*?)\)",img_url)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page30(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//a[@class='J_TWidget zui s1_d2_pop_0']/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Rain.Cun'
    for data in datas:
        # 图片链接
        img_url = 'https:'+re.findall(r"url\((.*?)\)",data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page31(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'tudor'
    # 图片链接
    img_url = 'https:'+re.findall(r'\[{"url":"(.*?)",',html)[0]
    # 图片名字
    filename = brand_name + "__" + re.findall(r'\[{"url":"(.*?)",',html)[0].split("/")[-1]
    # 验证码图片文件名
    response = requests.get(img_url,headers=headers,verify=False)
    if response.status_code == 200:
        image = response.content
        try:
            with open(filename,'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
        except Exception as e:
            filename = brand_name + str(count) + '.jpg'
            with open(filename, 'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page32(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div//a/parent::div/@style")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Clarks'
    for data in datas:
        # 图片链接
        img_url = 'https:'+re.findall(r"url\((.*?)\)",data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page33(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'INXX'
    img_url_list = re.findall(r'blank\\"><img src=\\"(.*?)\\"',html)
    for img_url in img_url_list:
        # 图片链接
        img_url = 'https:'+img_url
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page34(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Golden Goose'
    # 图片链接
    img_url = 'https:'+re.findall(r'\[{"url":"(.*?)",',html)[0]
    # 图片名字
    filename = brand_name + "__" + img_url.split("/")[-1]
    # 验证码图片文件名
    response = requests.get(img_url,headers=headers,verify=False)
    if response.status_code == 200:
        image = response.content
        try:
            with open(filename,'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
        except Exception as e:
            filename = brand_name + str(count) + '.jpg'
            with open(filename, 'wb') as f:
                f.write(image)
                count += 1
                print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page35(html, headers):
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
    brand_name = 'Asics'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath('./a/img/@data-ks-lazyload')[0]
        # 图片名字
        filename = brand_name + "__" + data.xpath('./a/img/@data-ks-lazyload')[0].split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page36(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop21156236862']/div/div/span/div/div/div/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Volley_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page37(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop17874149457']/div/div/span/div/div/div/a/img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'frontrowshop_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page38(html, headers):
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
    brand_name = 'jnby_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page39(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='rel scroller j-b']/div/div/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'rayban_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page40(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='zui-slide-con zui-con']/div/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'barneysnewyork_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page41(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Toomanyshoes_jd'
    datas = re.findall(r'src=\\"(.*?)\\',html)
    for data in datas:
        # 图片链接
        img_url = 'https:'+data
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page42(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='picCont']/ul/li/a/img/@original")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'jbrand_jd'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page43(html, headers):
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
    brand_name = 'Andersson Bell_jd'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./img/@original")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page44(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Ziiiro_jd'
    datas = re.findall(r'src=\\"(.*?)\\',html)
    for data in datas:
        # 图片链接
        img_url = 'https:'+data
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page45(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[position()<3]//img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'annaya_tm'
    for data in datas:
        # 图片链接
        img_url = data.xpath("./@data-ks-lazyload")[0]
        img_url = parse.urljoin('https://annaya.tmall.com/',img_url)
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page46(html, headers):
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
    brand_name = 'dumbem_jd'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./img/@original")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page47(html, headers):
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
    brand_name = 'DEL CHEN_jd'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./img/@original")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page48(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div")[1:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'unifree_tm'
    for data in datas:
        # 图片链接
        img_url = data.xpath(".//div[@class='um-3']/div/div/div/@style")[0]
        img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


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
    brand_name = 'PHILIP STEIN_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page50(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'CARIHOME_jd'
    datas = re.findall(r'"picUrl" : "(.*?)"',html)
    for data in datas:
        # 图片链接
        img_url = 'https:'+data
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page51(html, headers):
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
    brand_name = 'BASS_kl'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./a/img/@src")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page52(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop19115829388']/div/div/span/div/div/div/div/div/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'venque_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page53(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'WEEKENDER_jd'
    datas = re.findall(r'url":"(.*?)"',html)[:2]
    for data in datas:
        # 图片链接
        img_url = 'https:'+data
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page54(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='contentlist']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'alloy_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page55(html, headers):
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
    brand_name = 'bothyoung_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page56(html, headers):
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
    brand_name = 'Anne Klein_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page57(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'lets diet_jd'
    datas = re.findall(r'url":"(.*?)"',html)[:3]
    for data in datas:
        # 图片链接
        img_url = 'https:'+data
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page58(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop14869619343']/div/div/div/div/div/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'naturalizer_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page59(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='J_TWidget maGong']//img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'shineline_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page60(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'cote&ciel_jd'
    datas = re.findall(r'background:url\((.*?)\)',html)[:2]
    for data in datas:
        # 图片链接
        img_url = 'https:'+data
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page61(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Lancaster Paris_jd'
    datas = re.findall(r'url":"(.*?)"',html)
    for data in datas:
        # 图片链接
        img_url = 'https:'+data
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page62(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop21072089854']/div/div/span/div/div/img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'cat_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page63(html, headers):
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
    brand_name = 'movado_jd'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./img/@original")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page64(html, headers):
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
    brand_name = 'piquadro_jd'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./img/@original")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page65(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='wd-cont-carousel']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'sergiorossi_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page66(html, headers):
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
    brand_name = 'misscuriosity_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page67(html, headers):
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
    brand_name = 'AuroraAlba_jd'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./img/@original")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1].split("!")[0]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page68(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div[1]/div/div/div[position()<4]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ABLE JEANS_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath(".//img/@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page69(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div[1]/div/div/div//div[@class='canvas']/@style")[:2]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'avirex_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page70(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content c385302']/div/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'AliyaStore_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+re.findall(r'url\((.*?)\)',data)[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page71(html, headers):
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
    brand_name = 'alphastyle_tm'
    for data in datas:
        # 图片链接
        img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def parse_Page72(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='cms-html-edit']/li/div/a/img/@data-image")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'adidas_gw'
    for data in datas:
        # 图片链接
        js_data = json.loads(data)
        img_url = js_data['standard']['normal']
        # 图片名字
        filename = brand_name + "__" + img_url.split("/")[-1]
        # 验证码图片文件名
        response = requests.get(img_url,headers=headers,verify=False)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename,'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name,count))


def main():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    # # Evisu
    # html = get_Page('https://www.evisu.com/cn/',headers,'Evisu')
    # parse_Page(html,headers)
    # # nike
    # html1 = get_Page1('https://www.nike.com/cn/zh_cn/', headers,'nike')
    # # puma
    # html2 = get_Page('http://cn.puma.com/?utm_source=baidu&utm_medium=ppc&utm_term=puma%E5%BD%AA%E9%A9%AC&utm_content=B_Core&utm_campaign=core&smtid=538301628z2hfbz1nrcxz8jz0zMTI%3D', headers,'PUMA')
    # parse_Page1(html2, headers)
    # # 锐步
    # html3 = get_Page('https://www.reebok.com.cn/',headers,'Reebok')
    # parse_Page2(html3, headers)
    # # vans
    # html4 = get_Page('https://vans.com.cn/index.php', headers,'vans')
    # parse_Page3(html4, headers)
    # # CHIARA FERRAGNI
    # html5 = get_Page('https://chiaraferragni.tmall.com/view_shop.htm?spm=a220m.1000858.0.0.747543b9twaarZ&shop_id=310409403&rn=12377375e70e54c0b94ee5b3b2858d29', headers,'CHIARA FERRAGNI')
    # parse_Page4(html5, headers)
    # # cozy steps
    # html6 = get_Page('https://cozystepsxl.tmall.com/?spm=a1z10.1-b-s.w15382158-15815521104.3.71674cebQ9oIOr&scene=taobao_shop',headers,'cozy steps')
    # parse_Page5(html6, headers)
    # # 梅丽莎
    # html7 = get_Page1('http://cn.shopbop.com/sale-melissa/br/v=1/19102.htm',headers,'meilisha')
    # # Hush Puppies
    # html8 = get_Page('https://zt-jshop.jd.com/service.html?callback=jQuery2880750&functionId=getModData&body=%5B%7B%22type%22%3A%22module%22%2C%22moduleId%22%3A-288%2C%22moduleData%22%3A%22%7B%5C%22lunboGoodsGroup%5C%22%3A%7B%5C%22materialCode%5C%22%3A%5C%22wz8ogT073sQrBM%5C%22%2C%5C%22moduleCreate%5C%22%3A2%2C%5C%22bi%5C%22%3A0%2C%5C%22type%5C%22%3A%5C%222%5C%22%2C%5C%22showNum%5C%22%3A4%7D%2C%5C%22moduleMarginBottom%5C%22%3A%5B%5D%2C%5C%22template%5C%22%3A%7B%5C%22type%5C%22%3A1%2C%5C%22templateId%5C%22%3A-256%7D%7D%22%7D%5D&source=jshopact&platformId=1&_=1542698519182',headers,'Hush Puppies')
    # parse_Page6(html8, headers)
    # # 百丽
    # html9 = get_Page('https://ebelle.tmall.com/shop/view_shop.htm?user_number_id=167873659&ali_trackid=2%3Amm_26132928_45480038_616698400%3A1542699797_280_1132493648',headers,'bell')
    # parse_Page7(html9, headers)
    # # Palladium
    # html10 = get_Page('http://www.palladium.net.cn/',headers,'Palladium')
    # parse_Page8(html10, headers)
    # # apm monaco
    # html11 = get_Page('https://apmmonaco.tmall.com/view_shop.htm?spm=a220m.1000858.0.0.7701f41dBYlBbS&shop_id=375964680&rn=6c2c978b7c86375f11fd9c9ce88fb2b8', headers,'apm monaco')
    # parse_Page9(html11, headers)
    # # CITIZEN
    # html12 = get_Page('https://citizenwatch.tmall.com/?spm=a1z10.3-b-s.w5001-14529176280.17.53766301bdAmeT&scene=taobao_shop',headers,'CITIZEN')
    # parse_Page10(html12, headers)
    # # 浪琴
    # html13 = get_Page('https://www.longines.cn/longines-new?utm_source=baidu&utm_medium=Brandzone&utm_campaign=Brandzone-PC&utm_content=title&utm_term=LONGINES%E5%AE%98%E7%BD%91',headers,'Longines')
    # parse_Page11(html13, headers)
    # # 天梭
    # html14 = get_Page('https://www.tissotwatches.cn/?utm_source=baidu&utm_medium=cpc&utm_campaign=P_2018%E5%93%81%E7%89%8C_B&utm_content=%E5%93%81%E7%89%8C&utm_term=%E5%A4%A9%E6%A2%ADtissot&mz_ca=2092947&mz_sp=7HNho&mz_sb=1',headers,'Tissot')
    # parse_Page12(html14, headers)
    # # 飞亚达
    # html15 = get_Page('http://www.fiyta.com.cn/',headers,'FIYTA')
    # parse_Page13(html15, headers)
    # # 优立时
    # html16 = get_Page1('https://unizeit.tmall.com/', headers,'youlishi')
    # # DW
    # html17 = get_Page1('https://www.danielwellington.cn/?utm_source=baidu&utm_medium=cpc&utm_campaign=P-CN-Search-Brand-Phrase&utm_content=Daniel%20Wellington%20-%20CHS&utm_term=%E4%B8%B9%E5%B0%BC%E5%B0%94%E6%83%A0%E7%81%B5%E9%A1%BF&e_matchtype=2&e_creative=25133528565&e_adposition=clg1&e_pagenum=1&e_keywordid=82358847344', headers,'dw')
    # # CIGA Design
    # html18 = get_Page('http://www.cigadesign.com/index.php?route=common/home',headers,'CIGA Design')
    # parse_Page14(html18, headers)
    # # 卡西欧
    # html19 = get_Page('https://www.casiostore.com.cn/?source=casio', headers,'casio')
    # parse_Page15(html19, headers)
    # # 三宅一生/ISSEY MIYAKE
    # html20 = get_Page('https://isseymiyake.tmall.com/?spm=a1z10.1-b-s.w5001-14993501014.3.6c247154nOImUK&scene=taobao_shop', headers,'ISSEY MIYAKE')
    # parse_Page16(html20, headers)
    # # 迈克高仕/MICHAEL KORS
    # html21 = get_Page1('https://www.michaelkors.cn/', headers,'MICHAEL KORS')
    # # LACOSTE
    # html22 = get_Page('https://lacoste.tmall.com/?spm=a1z10.3-b-s.w5001-14917971715.3.68b71ca1RRvNbr&scene=taobao_shop', headers,'LACOSTE')
    # parse_Page17(html22, headers)
    # # Jonasverus
    # html23 = get_Page('http://www.jonasverus.com/Index/index',headers,'Jonasverus')
    # parse_Page18(html23, headers)
    # # 潘多拉/ PANDORA
    # html24 = get_Page1('https://cn.pandora.net/zh', headers,'PANDORA')
    # # Folli Follie
    # html25 = get_Page('https://mall.jd.com/index-1000091481.html',headers,'Folli Follie')
    # parse_Page19(html25, headers)
    # # 万宝龙/MONT BLANC
    # html26 = get_Page1('https://www.montblanc.cn/zh-cn/home.html', headers,'MONT BLANC')
    # # ENZO
    # html27 = get_Page('http://www.enzo-jewelry.com/cn/index',headers,'ENZO')
    # parse_Page20(html27, headers)
    # # 周大福/CHOW TAI FOOK
    # html28 = get_Page('https://www.ctfmall.com/', headers,'CHOW TAI FOOK')
    # parse_Page21(html28, headers)
    # # LaPerla
    # html29 = get_Page('https://laperla.tmall.com/', headers,'LaPerla')
    # parse_Page22(html29, headers)
    # # Air Jordan/乔丹
    # headers1 = {'User-Agent': ua.random,
    #             'cookie': '_jzqckmp_v2=1/; _jzqckmp=1/; AnalysisUserId=182.132.32.110.60151542613427637; anonymousId=D58BEE78B6043B5BAB410663DD95A4FC; NIKE_COMMERCE_COUNTRY=CN; NIKE_COMMERCE_LANG_LOCALE=zh_CN; nike_cp=cnns_sz_071516_a_alnul_bz01; guidS=5bc84242-e6b6-4555-922c-6cb3abebf988; guidU=87282c0e-092a-4663-cc78-ceef6db7bf04; neo.swimlane=33; cicIntercept=1; neo.experiments=%7B%22main%22%3A%7B%223333-interceptor-cn%22%3A%22a%22%7D%7D; _gcl_au=1.1.1468974453.1542613436; RES_TRACKINGID=168395306426827; ResonanceSegment=1; _gscu_207448657=36113443ujt7up11; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22D58BEE78B6043B5BAB410663DD95A4FC%22; _smt_uid=5bf269be.3b80ebf6; CONSUMERCHOICE_SESSION=t; CONSUMERCHOICE=cn/zh_cn; geoloc=cc=CN,rc=GD,tp=vhigh,tz=GMT+8,la=23.12,lo=113.25,bw=5000; bm_sz=1DD015878EACDDEF39D7072316A71318~QAAQe0InOyKCe+VmAQAAtRRNNey709bkqmmdo86b6e00+LXsTzt62ZtSXkDY+IGv1b1d+V9xIAOqCdxfDetjvTT1DhYE9Sux2YNpfPUPXAE9vuaaqL+TQ1bN7DDoDfoNW/uTusJOj7ft5TmnJfI99DK8WfuHfkn2Hbvnzy6RXx6w+kB4xrcgQZ1/jF/c; mm_wc_pmt=1; ak_bmsc=73A4BC310786372BEF235A46ADB492A63B27427BFF3B0000AF11F55B820FDD3E~plHEQ0L+4ju+vCyrhUEF9ICcTnseCCU7/4cTU+d+EWVbpJ6D/fMKmKnksADwm3RDERNkiDQiz6L1XlqYxA5CK9T/1IdNNwbbpactaAu8NvetGZQQh+vti/nRYakKMasgx1oaWroni0Vh5gvzGsV610K+ToIinUv/2qMSSpeRfmJ2g3ivy4SxeeSVBgGey79kwvxhA6JkrjeWatYKgBOYkivNwKChn/v8sGVWoRF5WYnCPsXi9v8f5CHIyptzCadtfE; AMCVS_F0935E09512D2C270A490D4D%40AdobeOrg=1; AMCV_F0935E09512D2C270A490D4D%40AdobeOrg=690614123%7CMCIDTS%7C17857%7CMCMID%7C17405002317383258452003464050636633774%7CMCAAMLH-1543392306%7C11%7CMCAAMB-1543392306%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1542794706s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.0; exp.swoosh.user=%7B%22granted%22%3A0%7D; _qzjc=1; _gscbrs_207448657=1; RES_SESSIONID=253079701612334; ppd=landing%20page%7Cnikecom%3Ejordan%3Aland; APID=B018AF709447CF3C5FE9C73571A8785E.sin-328-app-ap-0; CART_SUMMARY=%7B%22profileId%22+%3A%2218645617667%22%2C%22userType%22+%3A%22DEFAULT_USER%22%2C%22securityStatus%22+%3A%220%22%2C%22cartCount%22+%3A0%7D; _abck=D5EEE81FA090A9D4C7E3F6A2CD3EA4E7~0~YAAQe0InOzaGe+VmAQAAonpNNQC5G9z8r0TWs8QYFrlLubTvh/S/a1CiZ31I+6Nc1K+dsYQ1v47WEyicmFmUSloYvd286QkoDB/2ziamrlItl4Fa+rG6z7Tm9OnIymMtY0gV8HhMv340gNQHB1QT7c/sNbZWCfePbc7pOLoMsGujJERrxuPrqwDJthZXbgHFj/wwlEqKmIgTn3YDKwtCW2CdX0go3UdpOOsrIS854r/TEeWPvWPY3oVSLaXpX/02VhjVAJ7dMaT6eItBS24s+/NcYwzdsr36W1mkEoF9GHv0AeqHj/95~-1~-1~-1; utag_main=_st:1542789916367$ses_id:1542788079828%3Bexp-session; s_pers=%20s_dfa%3Dnikecomprod%7C1542789917204%3B%20c58%3Dno%2520value%7C1542789918091%3B; NIKE_CART_SESSION={%22bucket%22:%22jcart%22%2C%22country%22:%22CN%22%2C%22id%22:0%2C%22merged%22:false}; _gscs_207448657=42787506q3nz7o13|pv:4; _qzja=1.2044037218.1542613471759.1542613471759.1542787506973.1542787646574.1542788119084..0.0.7.2; _qzjb=1.1542787506973.4.0.0.0; _qzjto=4.1.0; bm_sv=0C8F4F948D7774A7A3B96637A6ABB1D5~1dS/kzaG0Cr+EYU/WGlSKocOt0t2S00wbrPAhV4bCmry3VkKBMLyuT7hmYgYyFgVwUgknV/qV0GiZNVtqPgLgFm1sgYptxLcF1rUrk4qqJTbv4ARMbSgbO3OuQfq2NPZOEDjtgI/BuEbTRi684hPu2ut7qe/nt7feB8laYU3KoA=; s_sess=%20c51%3Dhorizontal%3B%20prevList2%3D%3B%20s_cc%3Dtrue%3B%20tp%3D9365%3B%20s_ppv%3Dnikecom%25253Ejordan%25253Aland%252C5%252C5%252C478%3B; RT="dm=nike.com&si=728b716a-10c0-42cd-a5ab-0f683199ac59&ss=1542787503059&sl=4&tt=12638&obo=0&sh=1542788118956%3D4%3A0%3A12638%2C1542787646368%3D3%3A0%3A9329%2C1542787536354%3D2%3A0%3A6471%2C1542787506834%3D1%3A0%3A3770&bcn=%2F%2F36fb68c2.akstat.io%2F&r=https%3A%2F%2Fwww.nike.com%2Fcn%2Fzh_cn%2Fc%2Fjordan&ul=1542789274371"'}
    # html30 = get_Page1('https://www.nike.com/cn/zh_cn/c/jordan', headers1,'Jordan')
    # # free people
    # headers2 = {'User-Agent': ua.random,
    #             'cookie': 'SS_AFTERPAY=1; _dy_cs_pinterest=default; SSLB=1; SSSC_A15=513.G6626223343882222845.1|36039.1046629:37328.1099788:37750.1120334:39619.1219143:39855.1228406; urbn_country=CN; urbn_device_type=LARGE; urbn_geo_region=AS-SG; AKA_A2=A; urbn_inventory_pool=INTL_DIRECT; urbn_edgescape_site_id=fp-cn; urbn_tracer=TD0GIG1SIA; urbn_channel=web; urbn_data_center_id=US-NV; ak_bmsc=FE26F62F4D9749D5AFA379583FBF31BBB73CC565015500000613F55B33A03C19~pl3C/Tu/4w/0QjxO/nl30HzN0NV42T8kgx2SaLIuybXWLqzHWoWEfuQIeUFBCu3JCn7ATuEDItm6MsS3FrkhTaYRNZ/KVZBUTe1ANeevylalEuw+JajDNrdgMPSgbQaIb4FcCWWzW/77m8wsJ8FA5421nqYdXpbjp8FgnxyQV4R0J3VdvC8Psl+8lgJblRlTG675sKOz+IWLoI+TFdIL9EXW6op0KLwbvCaRAQsT5D818=; akacd_ss1=3720240645~rv=90~id=f08f5896e25198a78f977782a2fc6f1e; bm_sz=453126717C381F4B15973871BACA158E~QAAQZcU8t4m/PxJnAQAAllJSNQFHePxg/ug7Wdk0ffNsyJG936iGkIMchOuCHC59V0IWDY6deU9q82LGRdsk8RzJmUGhxdHsA2wk8VDwUhqJAunL+l2zBDbwYM4dubN3zc46phu0/aYe5VknmcQ9vA4933jiDbannQOqAuUBp6S678DhzfMZ6Mlmn3sBAR8NLexC; SSID_BE=CABenh1GAAAAAAAGE_Vb_TyAJgYT9VsBAAAAAACyR9ZdBhP1WwDRnHaTAANOGBEABhP1WwEAr5sAA3a-EgAGE_VbAQDDmgABR5oSAAYT9VsBAMeMAANl-A8ABhP1WwEA0JEAAQzIEAAGE_VbAQA; FP_ATTR=other; _ga=GA1.2.675031552.1542787851; _gid=GA1.2.1456074474.1542787851; _abck=99CE3D5DF05CD03B9A51D07A478C45AFB73CC565015500000613F55BF0AE7278~0~slWGF8rTtO7fumxttCX0rL5efBFkhlmWzoe8YWyxutk=~-1~-1; urbn_email_signup_marketing_optin=true; _dy_csc_ses=t; _dy_c_exps=; _dycnst=dg; gbi_sessionId=cjoqwcg0u0000368jf7qpx9z8; gbi_visitorId=cjoqwcg0u0001368jfpib2n5i; _gcl_au=1.1.1518128597.1542788343; _mibhv=anon-1542788343448-8254066910_6190; MGX_P=d2cb2070-235a-422a-9788-61760edf69bf; MGX_U=f6bd5c00-27ab-445c-87fa-c19247f32ce6; MGX_PX=8e7ea38c-d0f6-4e4a-9699-97cf0e6fa11e; MGX_CID=d87dada7-708c-4d85-9db3-ec3e59c8727c; _dy_ses_load_seq=92632%3A1542788361890; _dy_c_att_exps=; _ceg.s=pijb4b; _ceg.u=pijb4b; MGX_VS=2; rkglsid=h-caa2d727eb79e63735afa601673559e6_t-1542788364; _dyid=792634012696156904; _dyjsession=97a6ae1ca1b0745c8423f4c890295095; _dycst=dk.w.c.ws.frv1.frs.; _dy_geo=CN.AS.CN_30.CN_30_Shenzhen; _dy_df_geo=China..Shenzhen; _dyus_8767826=0%7C0%7C0%7C0%7C0%7C0.0.1542788365921.1542788365921.0.0%7C324%7C47%7C10%7C118%7C1%7C0%7C0%7C0%7C0%7C0%7C0%7C1%7C0%7C0%7C0%7C0%7C0%7C1%7C0%7C0%7C0%7C0%7C0; _dy_toffset=-3; _dy_soct=342129.554937.1542788342*279600.430785.1542788361*165298.236606.1542788361*264077.403653.1542788362*277633.427405.1542788365; urbn_site_id=fp-cn; siteId=fp-cn; urbn_language=zh-CN; urbn_currency=CNY; urbn_personalization_context=%5B%5B%22device_type%22%2C%20%22LARGE%22%5D%2C%20%5B%22personalization%22%2C%20%5B%5B%22ab%22%2C%20%5B%5B%22SS_AFTERPAY%22%2C%201%5D%5D%5D%2C%20%5B%22experience%22%2C%20%5B%5B%22image_quality%22%2C%2050%5D%2C%20%5B%22reduced%22%2C%20true%5D%5D%5D%2C%20%5B%22initialized%22%2C%20false%5D%2C%20%5B%22isCallCenterSession%22%2C%20false%5D%2C%20%5B%22isSiteOutsideNorthAmerica%22%2C%20true%5D%2C%20%5B%22isSiteOutsideUSA%22%2C%20true%5D%2C%20%5B%22isViewingInEnglish%22%2C%20false%5D%2C%20%5B%22isViewingRegionalSite%22%2C%20true%5D%2C%20%5B%22loyalty%22%2C%20false%5D%2C%20%5B%22loyaltyPoints%22%2C%20%22%22%5D%2C%20%5B%22siteDown%22%2C%20false%5D%2C%20%5B%22thirdParty%22%2C%20%5B%5B%22dynamicYield%22%2C%20true%5D%2C%20%5B%22googleMaps%22%2C%20true%5D%2C%20%5B%22moduleImages%22%2C%20true%5D%2C%20%5B%22personalizationQs%22%2C%20%22%22%5D%2C%20%5B%22productImages%22%2C%20true%5D%2C%20%5B%22promoBanners%22%2C%20true%5D%2C%20%5B%22tealium%22%2C%20true%5D%5D%5D%2C%20%5B%22userHasAgreedToCookies%22%2C%20false%5D%5D%5D%2C%20%5B%22scope%22%2C%20%22GUEST%22%5D%2C%20%5B%22user_location%22%2C%20%226eadebfeeedce815afc3ce3845d0dff4%22%5D%5D; SSRT_A15=MBf1WwADAA; urbn_auth_payload=%7B%22authToken%22%3A%20%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmcCIsImlhdCI6MTU0Mjc4ODkxNC4zMzYyNjYsImRhdGEiOiJ7XCJjYXJ0SWRcIjogXCJlR0UrVHFBMDIvUzRRd2lIdEFSK2oxVXFPbHNjRkI2dmxkNERaUVUxMWRnLzVJbFJlOUJMVTMvU21ydTdBVE1DNVUrM3JzMnJ4aGptNHBEMzBDY0lCdz09YTYzZDY1NjI4ZmUyOWZiYmVkMTk5ZDVlNTI5MTEzYTU4NzI5NWU1ZDBkMDE5YTdlYzYwYmM1ZGQzZmEzNWYwNlwiLCBcIndlYklkXCI6IFwiMDk3Mzk5MmQtOTQ4My00NzIxLWIwMTgtZDNmNTAwOTdlMjhiXCIsIFwiZWRnZXNjYXBlXCI6IHtcInJlZ2lvbkNvZGVcIjogXCJHRFwifSwgXCJicmFuZElkXCI6IFwiZnBcIiwgXCJkYXRhQ2VudGVySWRcIjogXCJVUy1OVlwiLCBcInNpdGVJZFwiOiBcImZwLXVzXCIsIFwiYW5vbnltb3VzXCI6IHRydWUsIFwic2NvcGVcIjogW1wiR1VFU1RcIl0sIFwiY3JlYXRlZFRpbWVcIjogMTU0Mjc4Nzg0Ni42NjAyNzMsIFwicHJvZmlsZUlkXCI6IFwiYzhqRmpoUE40M1RqaWhSSCtuLzdiRkxHcTQwZXlNeUNOc2Y1dTltYm9hRUFXMmM1ZmZtS3J6NENuUC8rRGVweTVVKzNyczJyeGhqbTRwRDMwQ2NJQnc9PTI5YzI4OGE3Y2MxMjBlYTNhNTEwNDVlMzhlOGY0YjVlZDgwNTQyZDJkYmJkZDQzODEyYTM3MmE2NzQ2NGE2YTlcIiwgXCJ0cmFjZXJcIjogXCJURDBHSUcxU0lBXCIsIFwiZ2VvUmVnaW9uXCI6IFwiQVMtU0dcIiwgXCJzaXRlR3JvdXBcIjogXCJmcFwifSIsImV4cCI6MTU0Mjc4OTUxNC4zMzYyNjZ9.sDWcVc74-ZGXUnGxfzqc-2N5hFgy923FOdtrHgovwoE%22%2C%20%22reauthToken%22%3A%20%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmcCIsImlhdCI6MTU0Mjc4ODkxNC4zMzY2OTEsImRhdGEiOiJ7XCJjcmVhdGVkVGltZVwiOiAxNTQyNzg4OTE0LjMzNjY3NSwgXCJzY29wZVwiOiBbXCJHVUVTVFwiXSwgXCJ0cmFjZXJcIjogXCJURDBHSUcxU0lBXCIsIFwicHJvZmlsZUlkXCI6IFwiYzhqRmpoUE40M1RqaWhSSCtuLzdiRkxHcTQwZXlNeUNOc2Y1dTltYm9hRUFXMmM1ZmZtS3J6NENuUC8rRGVweTVVKzNyczJyeGhqbTRwRDMwQ2NJQnc9PTI5YzI4OGE3Y2MxMjBlYTNhNTEwNDVlMzhlOGY0YjVlZDgwNTQyZDJkYmJkZDQzODEyYTM3MmE2NzQ2NGE2YTlcIn0iLCJleHAiOjE1NTgzNDA5MTQuMzM2NjkxfQ.s2nww24RmMkXJoAqXGkO_cJVtUG-UCsU-2y8PgXL43A%22%2C%20%22expiresIn%22%3A%20600.0%2C%20%22reauthExpiresIn%22%3A%2015552000.0%2C%20%22scope%22%3A%20%22GUEST%22%2C%20%22tracer%22%3A%20%22TD0GIG1SIA%22%2C%20%22dataCenterId%22%3A%20%22US-NV%22%2C%20%22geoRegion%22%3A%20%22AS-SG%22%2C%20%22createdAt%22%3A%201542788914342.4922%2C%20%22authExpiresTime%22%3A%201542789394.3424935%2C%20%22reauthExpiresTime%22%3A%201558340914.342495%7D; _gat_tealium_0=1; urbn_page_visits_count=%7B%22fp-cn%22%3A9%2C%22fp-us%22%3A2%7D; utag_main=v_id:016735525a4e005e9e7ae82e4ad80306e002106600bd0$_sn:1$_ss:0$_st:1542790731730$ses_id:1542787848783%3Bexp-session$_pn:11%3Bexp-session; stc114946=tsa:1542787850976.1433465822.6993742.48816863802125954:20181121085851|env:1%7C20181222081050%7C20181121085851%7C11%7C1044753:20191121082851|uid:1542787850976.419892383.32997465.114946.2086388117:20191121082851|srchist:1044753%3A1%3A20181222081050:20191121082851; bm_sv=83F3377331C8C60B7F320B5A55424B0D~ELqH8F1ah+y0NxoOvv3e97bigcepxt8tWrYd+0jU0bp1w7Jb1q0IeYbcMWTRj8kf9hmWdXTY9SkjkVbDHXfkGmj6Z0y4OBWHbfdM/JIhcf+CwMfP/KuuGkG1smvQUYGwJ2Jwz+ZNbYgYaC/HujyAOOYmFOh2tGKgodqzYg24Xr4=; _px3=ff85607422e34954a61d6fd7f5e69ac882cd9b9b9cd6b7a9edd4d322cbd99b9d:uba141VfGqexE3NfHVQIhuX8ftLkAM+8k/lbcxD5mtjmD9d2BcG7dnROhJxPCu7Avb94DPz+1oFH27tOZF+PxA==:1000:620cNzwoqoZIdDdE1XgN+cVmZxD1YqX3HOBdVh/+SM5j66Kpv2QreOb+dO2BTpDsnP0NiinWWb+DwLLFiVFtSRzH4aU1hkjQCAyjBHvwb3KXTSKBgQfaeIhaLvXUhHBAPn7w/kUNjYKZdi1WRXF88QmiZyF66HqPVd96cVrzjfs=; RT="sl=11&ss=1542787845644&tt=129050&obo=3&bcn=%2F%2F36fb78d7.akstat.io%2F&sh=1542788933619%3D11%3A3%3A129050%2C1542788919724%3D10%3A3%3A125507%2C1542788479742%3D9%3A2%3A125507%2C1542788390017%3D8%3A2%3A102854%2C1542788366384%3D7%3A2%3A79261&dm=freepeople.com&si=fc05963c-a063-48dc-bbad-a3dd44cecec2&ld=1542788933619&r=https%3A%2F%2Fwww.freepeople.com%2Fchina%2F&ul=1542788940915"'}
    # html31 = get_Page1('https://www.freepeople.com/china/', headers2,'free people')
    # # Kate Spade
    # html32 = get_Page1('http://www.katespade.cn/', headers,'Kate Spade')
    # # Tory Burch
    # html33 = get_Page('https://zt-jshop.jd.com/service.html?callback=jQuery9508474&functionId=getModData&body=%5B%7B%22type%22%3A%22module%22%2C%22moduleId%22%3A-288%2C%22moduleData%22%3A%22%7B%5C%22lunboGoodsGroup%5C%22%3A%7B%5C%22materialCode%5C%22%3A%5C%22KyMbuBdorpHV%5C%22%2C%5C%22moduleCreate%5C%22%3A2%2C%5C%22bi%5C%22%3A0%2C%5C%22type%5C%22%3A%5C%222%5C%22%2C%5C%22showNum%5C%22%3A%5C%221%5C%22%7D%2C%5C%22moduleMarginBottom%5C%22%3A%5B%5D%2C%5C%22template%5C%22%3A%7B%5C%22type%5C%22%3A1%2C%5C%22templateId%5C%22%3A-256%7D%7D%22%7D%5D&source=jshopact&platformId=1&_=1542789890224', headers,'Tory Burch')
    # parse_Page23(html33, headers)
    # # MCM
    # html34 = get_Page1('https://cn.mcmworldwide.com/zh_CN/%22holiday%22', headers,'MCM')
    # # Urban Outfitter
    # html35 = get_Page('https://urbanoutfitters.tmall.hk/', headers,'Urban Outfitter')
    # parse_Page24(html35, headers)
    # # Sam Edelman
    # html36 = get_Page1('http://cn.shopbop.com/sam-edelman/br/v=1/9878.htm', headers,'Sam Edelman')
    # # Yuzefi
    # html37 = get_Page1('http://cn.shopbop.com/yuzefi/br/v=1/56769.htm', headers,'Yuzefi')
    # # 伊芙丽
    # html38 = get_Page('https://eifini.tmall.com/view_shop.htm?spm=a220m.1000858.0.0.31201ecebjfmNa&shop_id=63721895&rn=72a669d8a0ccd621dce7220078cc0ffd', headers,'yifuli')
    # parse_Page25(html38, headers)
    # # Ledin 乐町
    # html39 = get_Page1('https://leting.tmall.com/',headers,'Ledin')
    # # Dazzle 地素
    # html40 = get_Page('https://dazzle.tmall.com/view_shop.htm?spm=a220m.1000858.0.0.79a559dbq6cqNr&shop_id=70235107&rn=09a6971b69b5e2f7e002534b82e11ba0', headers,'Dazzle')
    # parse_Page26(html40, headers)
    # # Sandro
    # html41 = get_Page('https://sandro.tmall.com/campaign-10290-42.htm?spm=a211oj.12055667.6271037800.2.76f650113YzpaJ&wx_navbar_transparent=true',headers,'Sandro')
    # parse_Page27(html41, headers)
    # # Maje
    # html42 = get_Page1('https://www.maje.cn/',headers,'Maje')
    # # Immi
    # html43 = get_Page1('https://immifs.tmall.com/', headers,'Immi')
    # # Allsaints
    # html44 = get_Page('https://allsaints.tmall.com/',headers,'Allsaints')
    # parse_Page28(html44, headers)
    # # Icicle 之禾
    # html45 = get_Page('https://icicle.tmall.com/campaign-10290-47.htm?spm=a211oj.12055667.1621939700.5.76f650113YzpaJ&wx_navbar_transparent=true', headers,'Icicle')
    # parse_Page29(html45, headers)
    # # Snidel
    # html46 = get_Page1('https://snidel.tmall.com/',headers,'Snidel')
    # # Rain.Cun 然与纯
    # html47 = get_Page('https://raincun.tmall.com/', headers,'Rain.Cun')
    # parse_Page30(html47, headers)
    # # 帝舵/tudor
    # html48 = get_Page('https://mall.jd.com/index-1000002797.html', headers,'tudor')
    # parse_Page31(html48, headers)
    # # 其乐/Clarks
    # html49 = get_Page('https://clarks.tmall.com/', headers,'Clarks')
    # parse_Page32(html49, headers)
    # # INXX
    # html50 = get_Page('https://mall.jd.com/index-67744.html', headers,'INXX')
    # parse_Page33(html50, headers)
    # # Golden Goose
    # html51 = get_Page('https://mall.jd.com/index-1000093872.html', headers,'Golden Goose')
    # parse_Page34(html51, headers)
    # # 亚瑟士/Asics
    # html52 = get_Page('https://asics.tmall.com/', headers,'Asics')
    # parse_Page35(html52, headers)
    # # Volley 天猫
    # html53 = get_Page('https://volley.tmall.com/', headers, 'Volley_tm')
    # parse_Page36(html53, headers)
    # # frontrowshop/江南布衣 天猫
    # html54 = get_Page('https://frontrowshop.tmall.com/', headers, 'frontrowshop_tm')
    # parse_Page37(html54, headers)
    # # jnby 天猫
    # html55 = get_Page('https://jnby.tmall.com/', headers, 'jnby_tm')
    # parse_Page38(html55, headers)
    # # rayban/雷朋 天猫
    # html56 = get_Page('https://rayban.tmall.com/', headers, 'rayban_tm')
    # parse_Page39(html56, headers)
    # # barneysnewyork 天猫
    # html57 = get_Page('https://barneysnewyork.tmall.hk/', headers, 'barneysnewyork_tm')
    # parse_Page40(html57, headers)
    # # Dsquared2 考拉
    # html58 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Dsquared2&searchRefer=searchbutton&timestamp=1543370017448', headers, 'barneysnewyork_kl')
    # # ARMANI JEANS 考拉
    # html59 = get_Page1(
    #     'https://www.kaola.com/search.html?changeContent=isSelfProduct&key=ARMANI%2520JEANS&pageNo=1&type=0&pageSize=60&isStock=false&isSelfProduct=true&isDesc=true&brandId=&proIds=&isSearch=0&isPromote=false&isTaxFree=false&factoryStoreTag=-1&backCategory=&country=&headCategoryId=&needBrandDirect=true&searchRefer=searchbutton&referFrom=searchbutton&referPosition=&timestamp=1543370122402&lowerPrice=-1&upperPrice=-1&searchType=synonym&#topTab',
    #     headers, 'ARMANI JEANS_kl')
    # # Toomanyshoes 京东
    # html60 = get_Page('https://mall.jd.com/index-817945.html', headers, 'Toomanyshoes_jd')
    # parse_Page41(html60, headers)
    # # NEIL BARRETT
    # html61 = get_Page1('https://www.farfetch.cn/cn/shopping/men/neil-barrett/items.aspx?q=NEIL%2520BARRETT', headers, 'NEIL BARRETT')
    # # jbrand 京东
    # html62 = get_Page('https://mall.jd.com/index-724149.html', headers, 'jbrand_jd')
    # parse_Page42(html62, headers)
    # # Andersson Bell 京东
    # html63 = get_Page('https://mall.jd.com/index-866870.html', headers, 'Andersson Bell_jd')
    # parse_Page43(html63, headers)
    # # Ziiiro 京东
    # html64 = get_Page('https://mall.jd.com/index-1000621.html', headers, 'Ziiiro_jd')
    # parse_Page44(html64, headers)
    # # annaya 天猫
    # html65 = get_Page('https://annaya.tmall.com/', headers, 'annaya_tm')
    # parse_Page45(html65, headers)
    # # dumbem/独本 京东
    # html66 = get_Page('https://mall.jd.com/index-780349.html', headers, 'dumbem_jd')
    # parse_Page46(html66, headers)
    # # B-Low The Belt
    # html67 = get_Page1('http://cn.shopbop.com/s/products?query=B-Low+The+Belt&searchSuggestion=false', headers, 'B-Low The Belt')
    # # DEL CHEN 京东
    # html68 = get_Page('https://mall.jd.com/index-795558.html', headers, 'DEL CHEN_jd')
    # parse_Page47(html68, headers)
    # # unifree 天猫
    # html69 = get_Page('https://unifree.tmall.com/', headers, 'unifree_tm')
    # parse_Page48(html69, headers)
    # # PHILIP STEIN 天猫
    # html70 = get_Page('https://philipstein.tmall.hk/', headers, 'PHILIP STEIN_tm')
    # parse_Page49(html70, headers)
    # # CARIHOME 京东
    # html71 = get_page_carihome('https://zt-jshop.jd.com/service.html?callback=jQuery7709089&functionId=getModData&body=%5B%7B%22type%22%3A%22module%22%2C%22moduleId%22%3A-288%2C%22moduleData%22%3A%22%7B%5C%22lunboGoodsGroup%5C%22%3A%7B%5C%22materialCode%5C%22%3A%5C%227NpVqa18ERljDviY%5C%22%2C%5C%22moduleCreate%5C%22%3A2%2C%5C%22bi%5C%22%3A0%2C%5C%22type%5C%22%3A%5C%222%5C%22%2C%5C%22showNum%5C%22%3A4%7D%2C%5C%22moduleMarginBottom%5C%22%3A%5B%5D%2C%5C%22template%5C%22%3A%7B%5C%22type%5C%22%3A1%2C%5C%22templateId%5C%22%3A-256%7D%7D%22%7D%5D&source=jshopact&platformId=1&_=1544433718093', headers, 'CARIHOME_jd')
    # parse_Page50(html71, headers)
    # # BASS 考拉
    # html72 = get_Page('https://mall.kaola.com/183555?zn=result&zp=page1-2&ri=BASS&rp=search', headers, 'BASS_kl')
    # parse_Page51(html72, headers)
    # # Boyy 考拉
    # html73 = get_Page1('https://www.kaola.com/search.html?changeContent=isSelfProduct&key=Boyy&pageNo=1&type=0&pageSize=60&isStock=false&isSelfProduct=true&isDesc=true&brandId=&proIds=&isSearch=0&isPromote=false&isTaxFree=false&factoryStoreTag=-1&backCategory=&country=&headCategoryId=&needBrandDirect=true&searchRefer=searchbutton&referFrom=searchbutton&referPosition=&timestamp=1544492282353&lowerPrice=-1&upperPrice=-1&searchType=synonym&#topTab', headers, 'Boyy_kl')
    # # venque/范克 天猫
    # html74 = get_Page('https://venquexb.tmall.com/?spm=a1z10.3-b-s.1997427721.d4918089.72346e276f7Xs7', headers, 'venque_tm')
    # parse_Page52(html74, headers)
    # # WEEKENDER 京东
    # html75 = get_Page('https://mall.jd.com/index-29251.html', headers,'WEEKENDER_jd')
    # parse_Page53(html75, headers)
    # # alloy 天猫
    # html76 = get_Page('https://alloy.tmall.com/?spm=a1z10.3-b-s.1997427721.d4918089.57ae37b7kaoD5g', headers, 'alloy_tm')
    # parse_Page54(html76, headers)
    # # Mansur Gavriel 考拉
    # html77 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Mansur%2520Gavriel&searchRefer=searchbutton&oldQuery=ALLOY%252B&timestamp=1543375344052', headers,'Mansur Gavriel_kl')
    # # veja 考拉
    # html78 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Veja&searchRefer=searchbutton&timestamp=1543376545872',headers, 'veja_kl')
    # # bothyoung/宝诗嫣 天猫
    # html79 = get_Page('https://bothyoung.tmall.com/', headers, 'bothyoung_tm')
    # parse_Page55(html79, headers)
    # # BORN CHAMPS 考拉
    # html80 = get_Page1('https://www.kaola.com/brand/8909.html', headers, 'BORN CHAMPS_kl')
    # # Les Petits Joueurs 考拉
    # html81 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Les%2520Petits%2520Joueurs&searchRefer=searchbutton&oldQuery=LARTIGENT&timestamp=1543389588053', headers, 'Les Petits Joueurs_kl')
    # # Anne Klein/安妮克莱因 天猫
    # html82 = get_Page('https://annekleinshoubiao.tmall.com', headers, 'Anne Klein_tm')
    # parse_Page56(html82, headers)
    # # lets diet 京东
    # html83 = get_Page('https://mall.jd.com/index-828294.html', headers, 'lets diet_jd')
    # parse_Page57(html83, headers)
    # # naturalizer 天猫
    # html84 = get_Page('https://naturalizer.tmall.com/', headers, 'naturalizer_tm')
    # parse_Page58(html84, headers)
    # # shineline/忻兰 天猫
    # html85 = get_Page('https://shineline.tmall.com/', headers, 'shineline_tm')
    # parse_Page59(html85, headers)
    # # cote&ciel 京东
    # html86 = get_Page('https://mall.jd.com/index-1000081128.html', headers, 'cote&ciel_jd')
    # parse_Page60(html86, headers)
    # # Philippe Model
    # html87 = get_Page1('https://www.farfetch.cn/cn/shopping/men/philippe-model/items.aspx?utm_source=Baidu&utm_medium=cpc&utm_term=20186840&utm_campaign=BAIDU%3ADesignerN%3AExact%3A%3AM-2&utm_content=Philippe%20Model&pid=Baidu&af_channel=Search&af_keywords=20186840&c=BAIDU%3ADesignerN%3AExact%3A%3AM-2&af_adset_id=Philippe%20Model&is_retargeting=true', headers, 'Philippe Model')
    # # Lancaster Paris 京东
    # html88 = get_Page('https://mall.jd.com/index-1000099717.html', headers, 'Lancaster Paris_jd')
    # parse_Page61(html88, headers)
    # # frye shopbop
    # html89 = get_Page1('http://cn.shopbop.com/frye/br/v=1/2534374302024536.htm?extid=PS_Baidu_CN_frye&cvosrc=ppc.baidu.frye&cvo_campaign=SB_Baidu&Matchtype=exact&ef_id=W2fk3gAAAX80Zg-R:20181130024311:s', headers, 'frye_shopbop')
    # # cat 天猫
    # html90 = get_Page('https://cathuwai.tmall.com', headers, 'cat_tm')
    # parse_Page62(html90, headers)
    # # movado 京东
    # html91 = get_Page('https://mall.jd.com/index-1000016366.html', headers, 'movado_jd')
    # parse_Page63(html91, headers)
    # # piquadro 京东
    # html92 = get_Page('https://mall.jd.com/index-206700.html', headers, 'piquadro_jd')
    # parse_Page64(html92, headers)
    # # sergiorossi 天猫
    # html93 = get_Page('https://sergiorossi.tmall.com', headers, 'sergiorossi_tm')
    # parse_Page65(html93, headers)
    # # misscuriosity 天猫
    # html94 = get_Page('https://misscuriosity.tmall.com/', headers, 'misscuriosity_tm')
    # parse_Page66(html94, headers)
    # # AuroraAlba 京东
    # html95 = get_Page('https://mall.jd.com/index-1000086232.html', headers, 'AuroraAlba_jd')
    # parse_Page67(html95, headers)
    # # ABLE JEANS 天猫
    # html96 = get_Page('https://ablejeans.tmall.com/', headers, 'ABLE JEANS_tm')
    # parse_Page68(html96, headers)
    # avirex 天猫
    html97 = get_Page('https://avirex.tmall.com/', headers, 'avirex_tm')
    parse_Page69(html97, headers)
    # AliyaStore 天猫
    html98 = get_Page('https://shejimaogf.tmall.com/', headers, 'AliyaStore_tm')
    parse_Page70(html98, headers)
    # alphastyle 官网
    html99 = get_Page1('http://www.alphastyle.cn/', headers, 'alphastyle_gw')
    # alphastyle 天猫
    html100 = get_Page('https://alphastyle.tmall.com/', headers, 'alphastyle_tm')
    parse_Page71(html100, headers)
    # adidas 官网
    html101 = get_Page('https://www.adidas.com.cn/', headers, 'adidas_gw')
    parse_Page72(html101, headers)


if __name__ == '__main__':
    main()