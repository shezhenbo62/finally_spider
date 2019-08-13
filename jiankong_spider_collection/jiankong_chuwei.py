# -*- coding: utf-8 -*-
import requests
import os
import time,re,json,csv
from fake_useragent import UserAgent
from lxml import etree
from urllib import parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

words_base = ['特惠','折','减','新品','上新','狂欢','发售','活动','开抢','特卖','赠','联名','礼遇','优惠','开门红','低价','sale']
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


def parse_Page(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ds-content ds-lbimg']/p")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'SUPOR_sn'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./a/img/@src')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = parse.urljoin('https://shop.suning.com/30000176/index.html',img_url)
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
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'SUPOR_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./dt/img/@original')[0]
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


def parse_Page2(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content c374409']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'siemens_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./div/@style')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'siemens_jd'
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


def parse_Page4(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'siemens_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page5(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content c618877']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'midea_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./div/@style')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            if 'url' in img_url:
                img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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
    datas = html_lxml.xpath("//div[@class='jImgNodeArea_dm']/dl")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'midea_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./dt/a/img/@original')[0]
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
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'midea_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page8(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='components-box']/div[position()<5]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ROBAM_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('.//img/@src')[0]
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
    datas = html_lxml.xpath("//a[@class='jsib abs aMUEN-T9F8']")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ROBAM_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath('./@style')[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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
    datas = html_lxml.xpath("//div[@class='jImgNodeArea_dm ']/dl")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ROBAM_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath('./dt/a/img/@original')[0]
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


def parse_Page11(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ROBAM_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page12(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='delaybox banner-slidewrap']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Haier_gw'
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


def parse_Page13(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='crazy_contentzxxEH']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Haier_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./div/div/a/img/@data-ks-lazyload")[0]
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
    datas = html_lxml.xpath("//div[@class='ma_slider']/div/a")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Haier_jd'
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


def parse_Page15(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox focusBox2']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Haier_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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
    datas = html_lxml.xpath("//div[@class='EJ']/ul/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Panasonic_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Panasonic_jd'
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


def parse_Page18(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='PP']/ul/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'donlim_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'donlim_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./dt/img/@original")[0]
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


def parse_Page20(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sf-custom']//img")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'donlim_sn'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@lazy-src")
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
    datas = html_lxml.xpath("//div[@id='ImageList']/ul/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'aca_gw'
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


def parse_Page22(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'aca_jd'
    datas = re.findall(r'pictureList":\[{"url":"(.*?)",',html)[:5]
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


def parse_Page23(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='mbody']/div/a[position()<4]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'hauswirt_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@style")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'hauswirt_jd'
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


def parse_Page25(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'hauswirt_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page26(html, headers):
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
    brand_name = 'joyoung_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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
    datas = html_lxml.xpath("//div[@class='jImgNodeArea']/dl/dt")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'joyoung_jd'
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


def parse_Page28(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'joyoung_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page29(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='lb_bd']/li")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'galanz_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/@style")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'galanz_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page31(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='ks-switchable-content']/a")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'LG_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@style")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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
    datas = html_lxml.xpath("//table[@id='__01']/tbody/tr")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'LG_sn'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./td/img/@lazy-src")[0]
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
    datas = html_lxml.xpath("//ul[@class='macontent']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'sanyo_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'sanyo_jd'
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


def parse_Page35(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'sanyo_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page36(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']//tbody/tr[position()<3]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'kitchenaid_tm'
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


def parse_Page37(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'kitchenaid_jd'
    datas = re.findall(r'src=\\"(.*?)\\"',html)[:3]
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


def parse_Page38(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='slide-content']/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'moen_tm'
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


def parse_Page39(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'moen_jd'
    datas = re.findall(r'src=\\"(.*?)\\"',html)[:2]
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


def parse_Page40(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'moen_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page41(html, headers):
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
    brand_name = 'moen_gm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath(".//img/@src")[0]
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


def parse_Page42(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ace_tm'
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


def parse_Page43(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ace_jd'
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


def parse_Page44(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='slider-large']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'delonghi_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./div/a/@style")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@layoutId='11376813']//img")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'delonghi_sn'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./@lazy-src")
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
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[position()<3]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'yourui_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath(".//a/preceding-sibling::div/@style")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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
    datas = html_lxml.xpath("//div[@layoutid='11684933']/div/div[1]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'yourui_sn'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath(".//img/@lazy-src")[0]
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
    datas = html_lxml.xpath("//ul[@class='macontent']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'braun_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'braun_jd'
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


def parse_Page50(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sf-sortbox sf-noDrag sf-autoWidth JS-pageLayout']/div[2]/div/div[1]/div/div/div/div/div/img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'braun_sn'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./@lazy-src")[0]
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
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'gaggia_tm'
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


def parse_Page52(html, headers):
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
    brand_name = 'philips_tm'
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


def parse_Page53(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'philips_sn'
    datas = re.findall(r"src: '(.*?)',", focus_data)
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:' + data
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
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'hamiltonbeach_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./div/div/span/div/@style")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = 'https:'+re.findall(r'url\((.*?)\)',img_url)[0]
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


def parse_Page55(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'hamiltonbeach_jd'
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


def parse_Page56(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'cuisinart_jd'
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


def parse_Page57(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div[2]/div/div/div/div[position()<5]//img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'MORPHYRICHARDS_tm'
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
    datas = html_lxml.xpath("//ul[@class='sx_content_sys clearfix']/li/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'bonavita_tm'
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


def parse_Page59(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/span/div/div/div/div/div/div/@style")[-2:]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'eupa_tm'
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


def parse_Page60(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'sanM_jd'
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


def parse_Page61(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'vitamix_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page62(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'blendtec_jd'
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


def parse_Page63(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'zojirushi_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page64(html, headers):
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
    brand_name = 'bear_jd'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath(".//img/@original")[0]
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


def parse_Page65(html, headers):
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
    brand_name = 'leecom_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'RussellHobbs_jd'
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


def parse_Page67(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'wmf_jd'
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


def parse_Page68(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='banner-content']/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'tonze_jd'
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


def parse_Page69(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'rabbittomato_jd'
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


def parse_Page70(html, headers):
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
    brand_name = 'jomalonelondon_jd'
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


def parse_Page71(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]/div/div/div/div[1]/div[3]/div/div/div/div/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'chahua_tm'
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


def parse_Page72(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='xx_inner']/@style")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'reflower_tm'
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


def parse_Page73(html, headers):
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
    brand_name = 'flowerplus_tm'
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


def parse_Page74(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='banners']/div[1]/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'purcotton_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/img/@src")[0]
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


def parse_Page75(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='main']/div/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'youdiao_tm'
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


def parse_Page76(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='Lb_show']/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Manito_gw'
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


def parse_Page77(html, headers):
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
    brand_name = 'yanxuan_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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
    datas = html_lxml.xpath("//ul[@class='player']/li/a/@style|//div[@id='shop18830392657']//div[@class='wd_self_rel working']/table/tr/td/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'gelatopique_tm'
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


def parse_Page79(html, headers):
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
    brand_name = 'hyx_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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
    datas = html_lxml.xpath("//ul[@id='flashview_1448']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'luolai_gw'
    for data in datas:
        # 图片链接
        try:
            img_url = data.xpath("./a/img/@src")[0]
        except Exception as e:
            print(brand_name,'图片元素定位为空，请及时查看修改')
        # 图片名字
        else:
            img_url = parse.urljoin('http://www.luolai.cn/',img_url)
            filename = brand_name + "__" + img_url.split("/")[-1].split("?")[0]
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
    datas = html_lxml.xpath("//div[@id='shop21161748919']/div/div/span/div/div/table/tbody/tr/td/img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'lovo_tm'
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


def parse_Page82(html, headers):
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
    brand_name = 'Mendale_kl'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@src")[0]
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


def parse_Page83(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[1]//div[@class='junehtml abs t-na-resize']/table/tbody/tr/td/img")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Ventry_tm'
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


def parse_Page84(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='sx_content_sys clearfix']/li/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'yuanmeng_tm'
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


def parse_Page85(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Umbra_jd'
    datas = re.findall(r'url":"(.*?)"',html)
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


def parse_Page86(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop18381709163']/div/div/span/div/div/div/div/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'zens_tm'
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


def parse_Page87(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'otbhome_jd'
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


def parse_Page88(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='hb']/li/a/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'beladesign_tm'
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


def parse_Page89(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@id='bxSlider_banner']/li")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Nitori_gw'
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


def parse_Page90(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='scroller']/dl/dd")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'urbanoutfitters_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./a/img/@data-ks-lazyload")[0]
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


def parse_Page91(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop21156620742']/div/div/span/div/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'ziinlife_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./img/@data-ks-lazyload")[0]
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


def parse_Page92(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop19899636184']/div/div/span/div/div/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'mzgf_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./img/@data-ks-lazyload")[0]
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


def parse_Page93(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='bd']/div/div/div/div[2]/div/div/span/div/@style|//div[@id='bd']/div/div/div/div[1]/div/div/span/div/div/div[3]/div/div/div/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'fnji_tm'
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


def parse_Page94(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='contentdis']/li/@style")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'kens_tm'
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


def parse_Page95(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'frosch_jd'
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


def parse_Page96(html, headers):
    html_lxml = etree.HTML(html)
    focus_data = html_lxml.xpath("//div[@class='focusBox']/@focus-data")[0]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'tide_sn'
    datas = re.findall(r"src: '(.*?)',",focus_data)
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


def parse_Page97(html, headers):
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
    brand_name = 'liby_jd'
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


def parse_Page98(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'bilang_jd'
    datas = re.findall(r'src=\\"(.*?)\\"',html)
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


def parse_Page99(html, headers):
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
    brand_name = 'jinfang_jd'
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


def parse_Page100(html, headers):
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
    brand_name = 'bio-D_jd'
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


def parse_Page101(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'B&B_jd'
    datas = re.findall(r'url":"(.*?)"',html)
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


def parse_Page102(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop21074250556']/div/div/span/div/div/div")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'peacock_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./img/@data-ks-lazyload")[0]
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


def parse_Page103(html, headers):
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
    brand_name = 'fuguang_jd'
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


def parse_Page104(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'tafuco_jd'
    datas = re.findall(r'url":"(.*?)"',html)
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


def parse_Page105(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'JoyFlower_jd'
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


def parse_Page106(html, headers):
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
    brand_name = 'zhihome_jd'
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


def parse_Page107(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='116959812']/div/div/div/div/div/div/div/a[4]")
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Ecover_jd'
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


def parse_Page108(html, headers):
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'AlmaWin_jd'
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


def parse_Page109(html, headers):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@id='shop21165383770']/div/div/span/div/div/div/table/tbody/tr/td")[:3]
    # 创建保存图片文件夹
    file = 'D:/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = 'Charlie_tm'
    for data in datas:
        # 图片链接
        try:
            img_url = 'https:'+data.xpath("./img/@data-ks-lazyload")[0]
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
    # # SUPOR/苏泊尔 苏宁
    # html = get_Page('https://shop.suning.com/30000176/index.html',headers,'SUPOR_sn')
    # parse_Page(html,headers)
    # # SUPOR/苏泊尔 京东
    # html1 = get_Page('https://mall.jd.com/index-1000001228.html', headers, 'SUPOR_jd')
    # parse_Page1(html1, headers)
    # # siemens/西门子 天猫
    # html2 = get_Page('https://siemens-home.tmall.com/', headers, 'siemens_tm')
    # parse_Page2(html2, headers)
    # # siemens/西门子 京东
    # html3 = get_Page('https://zt-jshop.jd.com/service.html?callback=jQuery3648007&functionId=getModData&body=%5B%7B%22type%22%3A%22module%22%2C%22moduleId%22%3A-288%2C%22moduleData%22%3A%22%7B%5C%22lunboGoodsGroup%5C%22%3A%7B%5C%22materialCode%5C%22%3A%5C%22zTl7f3OLQR2ZDkP%5C%22%2C%5C%22moduleCreate%5C%22%3A1%2C%5C%22bi%5C%22%3A0%2C%5C%22type%5C%22%3A%5C%222%5C%22%2C%5C%22showNum%5C%22%3A%5C%226%5C%22%7D%2C%5C%22moduleMarginBottom%5C%22%3A%5B%5D%2C%5C%22template%5C%22%3A%7B%5C%22type%5C%22%3A1%2C%5C%22templateId%5C%22%3A-256%7D%7D%22%7D%5D&source=jshopact&platformId=1&_=1543804017183', headers, 'siemens_jd')
    # parse_Page3(html3, headers)
    # # siemens/西门子 苏宁
    # html4 = get_Page('https://shop.suning.com/30000095/index.html', headers, 'siemens_sn')
    # parse_Page4(html4, headers)
    # # midea/美的 官网
    # html5 = get_Page1('https://www.midea.cn/?mtag=30007.15.3', headers,'midea_gw')
    # # midea/美的 天猫
    # html6 = get_Page('https://midea.tmall.com/', headers, 'midea_tm')
    # parse_Page5(html6, headers)
    # # midea/美的 京东
    # html7 = get_Page('https://mall.jd.com/index-1000001281.html', headers, 'midea_jd')
    # parse_Page6(html7, headers)
    # # midea/美的 苏宁
    # html8 = get_Page('https://shop.suning.com/30000221', headers, 'midea_sn')
    # parse_Page7(html8, headers)
    # # ROBAM/老板 官网
    # html9 = get_Page('https://www.shoprobam.com/', headers, 'ROBAM_gw')
    # parse_Page8(html9, headers)
    # # ROBAM/老板 天猫
    # html10 = get_Page('https://robam.tmall.com/', headers, 'ROBAM_tm')
    # parse_Page9(html10, headers)
    # # ROBAM/老板 京东
    # html11 = get_Page('https://mall.jd.com/index-1000001402.html', headers, 'ROBAM_jd')
    # parse_Page10(html11, headers)
    # # ROBAM/老板 苏宁
    # html12 = get_Page('https://robam.suning.com/', headers, 'ROBAM_sn')
    # parse_Page11(html12, headers)
    # # Haier/海尔 官网
    # html13 = get_Page('http://www.ehaier.com/', headers, 'Haier_gw')
    # parse_Page12(html13, headers)
    # # Haier/海尔 天猫
    # html14 = get_Page('https://haier.tmall.com/', headers, 'Haier_tm')
    # parse_Page13(html14, headers)
    # # Haier/海尔 京东
    # html15 = get_Page('https://mall.jd.com/index-1000001782.html', headers, 'Haier_jd')
    # parse_Page14(html15, headers)
    # # Haier/海尔 苏宁
    # html16 = get_Page('https://shop.suning.com/30000162', headers, 'Haier_sn')
    # parse_Page15(html16, headers)
    # # Panasonic/松下 天猫
    # html17 = get_Page('https://panasonic.tmall.com/', headers, 'Panasonic_tm')
    # parse_Page16(html17, headers)
    # # Panasonic/松下 京东
    # html18 = get_Page('https://zt-jshop.jd.com/service.html?callback=jQuery5678570&functionId=getModData&body=%5B%7B%22type%22%3A%22module%22%2C%22moduleId%22%3A-288%2C%22moduleData%22%3A%22%7B%5C%22lunboGoodsGroup%5C%22%3A%7B%5C%22materialCode%5C%22%3A%5C%22uLzWgcmTViBIQ%5C%22%2C%5C%22moduleCreate%5C%22%3A2%2C%5C%22bi%5C%22%3A0%2C%5C%22type%5C%22%3A%5C%222%5C%22%2C%5C%22showNum%5C%22%3A%5C%228%5C%22%7D%2C%5C%22moduleMarginBottom%5C%22%3A%5B%5D%2C%5C%22template%5C%22%3A%7B%5C%22type%5C%22%3A1%2C%5C%22templateId%5C%22%3A-256%7D%7D%22%7D%5D&source=jshopact&platformId=1&_=1543818706168', headers, 'Panasonic_jd')
    # parse_Page17(html18, headers)
    # # Donlim/东菱 天猫
    # html19 = get_Page('https://donlimdq.tmall.com/', headers, 'donlim_tm')
    # parse_Page18(html19, headers)
    # # Donlim/东菱 京东
    # html20 = get_Page('https://mall.jd.com/index-1000001316.html', headers, 'donlim_jd')
    # parse_Page19(html20, headers)
    # # Donlim/东菱 苏宁
    # html21 = get_Page('https://shop.suning.com/30000055', headers, 'donlim_sn')
    # parse_Page20(html21, headers)
    # # aca/北美电器 官网
    # html22 = get_Page('http://www.acachina.com/', headers, 'aca_gw')
    # parse_Page21(html22, headers)
    # # aca/北美电器 京东
    # html23 = get_Page('https://mall.jd.com/index-1000002429.html', headers, 'aca_jd')
    # parse_Page22(html23, headers)
    # # hauswirt/海氏 天猫
    # html24 = get_Page('https://hauswirt.tmall.com/', headers, 'hauswirt_tm')
    # parse_Page23(html24, headers)
    # # hauswirt/海氏 京东
    # html25 = get_Page('https://mall.jd.com/index-1000001232.html', headers, 'hauswirt_jd')
    # parse_Page24(html25, headers)
    # # hauswirt/海氏 苏宁
    # html26 = get_Page('https://shop.suning.com/30001278', headers, 'hauswirt_sn')
    # parse_Page25(html26, headers)
    # # joyoung/九阳 天猫
    # html27 = get_Page('https://joyoungtp.tmall.com/', headers, 'joyoung_tm')
    # parse_Page26(html27, headers)
    # # joyoung/九阳 京东
    # html28 = get_Page('https://mall.jd.com/index-1000001465.html', headers, 'joyoung_jd')
    # parse_Page27(html28, headers)
    # # joyoung/九阳 苏宁
    # html29 = get_Page('https://shop.suning.com/30000130', headers, 'joyoung_sn')
    # parse_Page28(html29, headers)
    # # galanz/格兰仕 天猫
    # html30 = get_Page('https://galanz.tmall.com/', headers, 'galanz_tm')
    # parse_Page29(html30, headers)
    # # galanz/格兰仕 苏宁
    # html31 = get_Page('https://shop.suning.com/30000182/index.html', headers, 'galanz_sn')
    # parse_Page30(html31, headers)
    # # LG 天猫
    # html32 = get_Page('https://lg.tmall.com/', headers, 'LG_tm')
    # parse_Page31(html32, headers)
    # # LG 苏宁
    # html33 = get_Page('https://shop.suning.com/30001357', headers, 'LG_sn')
    # parse_Page32(html33, headers)
    # # sanyo/三洋 天猫
    # html34 = get_Page('https://sanyo.tmall.com/', headers, 'sanyo_tm')
    # parse_Page33(html34, headers)
    # # sanyo/三洋 京东
    # html35 = get_Page('https://zt-jshop.jd.com/service.html?callback=jQuery5856824&functionId=getModData&body=%5B%7B%22type%22%3A%22module%22%2C%22moduleId%22%3A-288%2C%22moduleData%22%3A%22%7B%5C%22lunboGoodsGroup%5C%22%3A%7B%5C%22materialCode%5C%22%3A%5C%227r8EtOTKxv%5C%22%2C%5C%22moduleCreate%5C%22%3A2%2C%5C%22bi%5C%22%3A0%2C%5C%22type%5C%22%3A%5C%222%5C%22%2C%5C%22showNum%5C%22%3A4%7D%2C%5C%22moduleMarginBottom%5C%22%3A%5B%5D%2C%5C%22template%5C%22%3A%7B%5C%22type%5C%22%3A1%2C%5C%22templateId%5C%22%3A-256%7D%7D%22%7D%5D&source=jshopact&platformId=1&_=1543829562066', headers, 'sanyo_jd')
    # parse_Page34(html35, headers)
    # # sanyo/三洋 苏宁
    # html36 = get_Page('https://shop.suning.com/30000047', headers, 'sanyo_sn')
    # parse_Page35(html36, headers)
    # # kitchenaid/凯膳怡 天猫
    # html37 = get_Page('https://kitchenaid.tmall.com/', headers, 'kitchenaid_tm')
    # parse_Page36(html37, headers)
    # # kitchenaid/凯膳怡 京东
    # html38 = get_Page('https://kitchenaid.jd.com/', headers, 'kitchenaid_jd')
    # parse_Page37(html38, headers)
    # # moen/摩恩 天猫
    # html39 = get_Page('https://moen.tmall.com/', headers, 'moen_tm')
    # parse_Page38(html39, headers)
    # # moen/摩恩 京东
    # html40 = get_Page('https://mall.jd.com/index-1000001614.html', headers, 'moen_jd')
    # parse_Page39(html40, headers)
    # # moen/摩恩 苏宁
    # html41 = get_Page('https://shop.suning.com/70081866', headers, 'moen_sn')
    # parse_Page40(html41, headers)
    # # moen/摩恩 国美
    # html42 = get_Page('https://mall.gome.com.cn/80013326/', headers, 'moen_gm')
    # parse_Page41(html42, headers)
    # # ace/爱思 天猫
    # html43 = get_Page('https://acexb.tmall.com/', headers, 'ace_tm')
    # parse_Page42(html43, headers)
    # # ace/爱思 京东
    # # https://mall.jd.com/index-57177.html
    # html44 = get_Page('https://zt-jshop.jd.com/service.html?callback=jQuery3017727&functionId=getModData&body=%5B%7B%22type%22%3A%22module%22%2C%22moduleId%22%3A-288%2C%22moduleData%22%3A%22%7B%5C%22lunboGoodsGroup%5C%22%3A%7B%5C%22materialCode%5C%22%3A%5C%220pwJW5gy8eAU%5C%22%2C%5C%22moduleCreate%5C%22%3A2%2C%5C%22bi%5C%22%3A0%2C%5C%22type%5C%22%3A%5C%222%5C%22%2C%5C%22showNum%5C%22%3A4%7D%2C%5C%22moduleMarginBottom%5C%22%3A%5B%5D%2C%5C%22template%5C%22%3A%7B%5C%22type%5C%22%3A1%2C%5C%22templateId%5C%22%3A-256%7D%7D%22%7D%5D&source=jshopact&platformId=1&_=1543894830071', headers, 'ace_jd')
    # parse_Page43(html44, headers)
    # # delonghi/德龙 天猫
    # html45 = get_Page('https://delonghi.tmall.com/', headers, 'delonghi_tm')
    # parse_Page44(html45, headers)
    # # delonghi/德龙 苏宁
    # html46 = get_Page('https://shop.suning.com/30000468', headers, 'delonghi_sn')
    # parse_Page45(html46, headers)
    # # yourui/优瑞 天猫
    # html47 = get_Page('https://youruidq.tmall.com/', headers, 'yourui_tm')
    # parse_Page46(html47, headers)
    # # yourui/优瑞 苏宁
    # html48 = get_Page('https://shop.suning.com/30001433', headers, 'yourui_sn')
    # parse_Page47(html48, headers)
    # # braun/博朗 天猫
    # html49 = get_Page('https://braun.tmall.com/', headers, 'braun_tm')
    # parse_Page48(html49, headers)
    # # braun/博朗 京东
    # html50 = get_Page('https://mall.jd.com/index-1000002836.html', headers, 'braun_jd')
    # parse_Page49(html50, headers)
    # # braun/博朗 苏宁
    # html51 = get_Page('https://shop.suning.com/30000141', headers, 'braun_sn')
    # parse_Page50(html51, headers)
    # # gaggia/加吉亚 天猫
    # html52 = get_Page('https://gaggia.tmall.com/', headers, 'gaggia_tm')
    # parse_Page51(html52, headers)
    # # philips/飞利浦 天猫
    # html53 = get_Page('https://philipschina.tmall.com/', headers, 'philips_tm')
    # parse_Page52(html53, headers)
    # # philips/飞利浦 苏宁
    # html54 = get_Page('https://shop.suning.com/30000180/index.html', headers, 'philips_sn')
    # parse_Page53(html54, headers)
    # # hamiltonbeach/汉美驰 天猫
    # html55 = get_Page('https://hamiltonbeach.tmall.com/', headers, 'hamiltonbeach_tm')
    # parse_Page54(html55, headers)
    # # hamiltonbeach/汉美驰 京东
    # html56 = get_Page('https://mall.jd.com/index-1000007424.html', headers, 'hamiltonbeach_jd')
    # parse_Page55(html56, headers)
    # # cuisinart/美膳雅 京东
    # html57 = get_Page('https://mall.jd.com/index-1000105300.html', headers, 'cuisinart_jd')
    # parse_Page56(html57, headers)
    # # MORPHYRICHARDS/摩飞 天猫
    # html58 = get_Page('https://mofeidianqicfdq.tmall.com/', headers, 'MORPHYRICHARDS_tm')
    # parse_Page57(html58, headers)
    # # bonavita 天猫
    # html59 = get_Page('https://bonavita.tmall.com/?spm=a1z10.3-b-s.1997427721.d4918089.31073598ud6Mc4', headers, 'bonavita_tm')
    # parse_Page58(html59, headers)
    # # eupa/灿坤 天猫
    # html60 = get_Page('https://cankun.tmall.com/', headers,'eupa_tm')
    # parse_Page59(html60, headers)
    # # sanM 京东
    # html61 = get_Page('https://3m.jd.com/', headers, 'sanM_jd')
    # parse_Page60(html61, headers)
    # # vitamix/维他密斯 苏宁
    # html62 = get_Page('http://shop.suning.com/30001147/index.html', headers, 'vitamix_sn')
    # parse_Page61(html62, headers)
    # # blendtec 京东
    # html63 = get_Page('https://mall.jd.com/index-1000079370.html', headers, 'blendtec_jd')
    # parse_Page62(html63, headers)
    # # zojirushi/象印 苏宁
    # html64 = get_Page('https://shop.suning.com/30001001/index.html', headers, 'zojirushi_sn')
    # parse_Page63(html64, headers)
    # # bear/小熊 京东
    # html65 = get_Page('https://mall.jd.com/index-1000002467.html', headers, 'bear_jd')
    # parse_Page64(html65, headers)
    # # leecom/日创 天猫
    # html66 = get_Page('https://leecom.tmall.com/', headers, 'leecom_tm')
    # parse_Page65(html66, headers)
    # # RussellHobbs/领豪 京东
    # html67 = get_Page('https://mall.jd.com/index-1000094647.html', headers, 'RussellHobbs_jd')
    # parse_Page66(html67, headers)
    # # wmf/福腾宝 京东
    # # https://mall.jd.com/index-208564.html
    # html68 = get_Page('https://zt-jshop.jd.com/service.html?callback=jQuery1999000&functionId=getModData&body=%5B%7B%22type%22%3A%22module%22%2C%22moduleId%22%3A-288%2C%22moduleData%22%3A%22%7B%5C%22lunboGoodsGroup%5C%22%3A%7B%5C%22materialCode%5C%22%3A%5C%22Lv3nypmqh7BY4%5C%22%2C%5C%22moduleCreate%5C%22%3A2%2C%5C%22bi%5C%22%3A0%2C%5C%22type%5C%22%3A%5C%222%5C%22%2C%5C%22showNum%5C%22%3A4%7D%2C%5C%22moduleMarginBottom%5C%22%3A%5B%5D%2C%5C%22template%5C%22%3A%7B%5C%22type%5C%22%3A1%2C%5C%22templateId%5C%22%3A-256%7D%7D%22%7D%5D&source=jshopact&platformId=1&_=1544062064930', headers, 'wmf_jd')
    # parse_Page67(html68, headers)
    # # tonze/天际 京东
    # html69 = get_Page('https://mall.jd.com/index-1000001345.html',headers, 'tonze_jd')
    # parse_Page68(html69, headers)
    # # rabbittomato/兔子西红柿 京东
    # html70 = get_Page('https://mall.jd.com/index-827761.html', headers, 'rabbittomato_jd')
    # parse_Page69(html70, headers)
    # # jomalonelondon/祖玛珑 京东
    # html71 = get_Page('https://mall.jd.com/index-1000002742.html', headers, 'jomalonelondon_jd')
    # parse_Page70(html71, headers)
    # # chahua/茶花 天猫
    # html72 = get_Page('https://fjchahua.tmall.com/', headers, 'chahua_tm')
    # parse_Page71(html72, headers)
    # # reflower/花点时间 天猫
    # html73 = get_Page('https://reflower.tmall.com/', headers, 'reflower_tm')
    # parse_Page72(html73, headers)
    # # flowerplus/花加 天猫
    # html74 = get_Page('https://flowerplus.tmall.com/', headers, 'flowerplus_tm')
    # parse_Page73(html74, headers)
    # # purcotton/全棉时代 官网
    # html75 = get_Page('https://www.purcotton.com/', headers, 'purcotton_gw')
    # parse_Page74(html75, headers)
    # # beast/野兽派 官网
    # html76 = get_Page1('http://www.thebeastshop.com/', headers,'beast')
    # # youdiao/优调 天猫
    # html77 = get_Page('https://youdiaojj.tmall.com/', headers, 'youdiao_tm')
    # parse_Page75(html77, headers)
    # # Manito/曼尼陀 官网
    # html78 = get_Page('http://www.manitosilk.com.cn/', headers, 'Manito_gw')
    # parse_Page76(html78, headers)
    # # yanxuan/网易严选 天猫
    # html79 = get_Page('https://wangyiyanxuan.tmall.com/', headers, 'yanxuan_tm')
    # parse_Page77(html79, headers)
    # # gelatopique 天猫
    # html80 = get_Page('https://gelatopique.tmall.com/', headers, 'gelatopique_tm')
    # parse_Page78(html80, headers)
    # # hyx/恒源祥 天猫
    # html81 = get_Page('https://hyxjf.tmall.com/', headers, 'hyx_tm')
    # parse_Page79(html81, headers)
    # luolai/罗莱家纺 官网
    html82 = get_Page('http://www.luolai.cn/', headers, 'luolai_gw')
    parse_Page80(html82, headers)
    # lovo 天猫
    html83 = get_Page('https://lovo.tmall.com/', headers, 'lovo_tm')
    parse_Page81(html83, headers)
    # Mendale/梦洁家纺 网易考拉
    html84 = get_Page('https://mall.kaola.com/20515?zn=result&zp=page1-0&ri=Mendale%2F%E6%A2%A6%E6%B4%81%E5%AE%B6%E7%BA%BA&rp=search', headers, 'Mendale_kl')
    parse_Page82(html84, headers)
    # Mercury/水星家纺 网易考拉
    html85 = get_Page1('https://www.kaola.com/search.html?zn=top&key=Mercury%252F%25E6%25B0%25B4%25E6%2598%259F%25E5%25AE%25B6%25E7%25BA%25BA&searchRefer=searchbutton&oldQuery=Mercury%252F%25E6%25B0%25B4%25E6%2598%259F%25E5%25AE%25B6%25E7%25BA%25BA&timestamp=1544082696828',headers,'Mercury_kl')
    # Ventry 天猫
    html86 = get_Page('https://ventry.tmall.hk/', headers, 'Ventry_tm')
    parse_Page83(html86, headers)
    # yuanmeng/远梦 天猫
    html87 = get_Page('https://yuanmeng.tmall.com/', headers, 'yuanmeng_tm')
    parse_Page84(html87, headers)
    # Umbra 京东
    html88 = get_Page('https://mall.jd.com/index-693869.html', headers, 'Umbra_jd')
    parse_Page85(html88, headers)
    # zens/哲品家居 天猫
    html89 = get_Page('https://zens.tmall.com/index.htm?spm=a1z10.3-b-s.w5002-18381709145.2.4b763a125vuYbv', headers, 'zens_tm')
    parse_Page86(html89, headers)
    # otbhome 京东
    html90 = get_Page('https://mall.jd.com/index-610144.html', headers, 'otbhome_jd')
    parse_Page87(html90, headers)
    # beladesign 天猫
    html91 = get_Page('https://beladesign.tmall.com/', headers, 'beladesign_tm')
    parse_Page88(html91, headers)
    # Nitori/尼达利 官网
    html92 = get_Page('https://www.nitori-net.cn/', headers, 'Nitori_gw')
    parse_Page89(html92, headers)
    # urbanoutfitters 天猫
    html93 = get_Page('https://urbanoutfitters.tmall.hk/', headers, 'urbanoutfitters_tm')
    parse_Page90(html93, headers)
    # ziinlife/吱音 天猫
    html94 = get_Page('https://ziinlife.tmall.com/', headers, 'ziinlife_tm')
    parse_Page91(html94, headers)
    # norhor 天猫
    html95 = get_Page1('https://norhor.tmall.com/', headers,'norhor_tm')
    # mzgf/木智工坊 天猫
    html96 = get_Page('https://mzgf.tmall.com/', headers, 'mzgf_tm')
    parse_Page92(html96, headers)
    # fnji/梵几 天猫
    html97 = get_Page('https://fanjijiaju.tmall.com/', headers, 'fnji_tm')
    parse_Page93(html97, headers)
    # kens 天猫
    html98 = get_Page('https://kens.tmall.com/', headers, 'kens_tm')
    parse_Page94(html98, headers)
    # frosch/菲洛施 京东
    html99 = get_Page('https://mall.jd.com/index-1000102203.html', headers, 'frosch_jd')
    parse_Page95(html99, headers)
    # tide/汰渍 苏宁
    html100 = get_Page('https://shop.suning.com/30000355/index.html', headers, 'tide_sn')
    parse_Page96(html100, headers)
    # liby/立白 京东
    html101 = get_Page('https://mall.jd.com/index-1000001759.html', headers, 'liby_jd')
    parse_Page97(html101, headers)
    # bilang/碧浪 京东
    html102 = get_Page('https://mall.jd.com/index-1000007387.html', headers, 'bilang_jd')
    parse_Page98(html102, headers)
    # jinfang/金纺 京东
    html103 = get_Page('https://mall.jd.com/index-1000001832.html', headers, 'jinfang_jd')
    parse_Page99(html103, headers)
    # bio-D 京东
    html104 = get_Page('https://mall.jd.com/index-1000085316.html', headers, 'bio-D_jd')
    parse_Page100(html104, headers)
    # B&B/保宁 京东
    html105 = get_Page('https://mall.jd.com/index-1000005213.html', headers, 'B&B_jd')
    parse_Page101(html105, headers)
    # peacock/孔雀 天猫
    html106 = get_Page('https://peacock.tmall.com/', headers, 'peacock_tm')
    parse_Page102(html106, headers)
    # fuguang/富光 京东
    html107 = get_Page('https://mall.jd.com/index-1000001660.html', headers, 'fuguang_jd')
    parse_Page103(html107, headers)
    # tafuco/泰福高 京东
    html108 = get_Page('https://mall.jd.com/index-1000001710.html', headers, 'tafuco_jd')
    parse_Page104(html108, headers)
    # JoyFlower 京东
    html109 = get_Page('https://mall.jd.com/index-86884.html#', headers, 'JoyFlower_jd')
    parse_Page105(html109, headers)
    # zhihome/智庭 京东
    html110 = get_Page('https://mall.jd.com/index-45046.html', headers, 'zhihome_jd')
    parse_Page106(html110, headers)
    # Ecover 京东
    html111 = get_Page('https://mall.jd.com/index-1000008281.html', headers, 'Ecover_jd')
    parse_Page107(html111, headers)
    # AlmaWin 京东
    html112 = get_Page('https://mall.jd.com/index-772123.html', headers, 'AlmaWin_jd')
    parse_Page108(html112, headers)
    # Charlie’s Soap/查利 天猫
    html113 = get_Page('https://chalixihu.tmall.com/', headers, 'Charlie_tm')
    parse_Page109(html113, headers)


if __name__ == '__main__':
    main()