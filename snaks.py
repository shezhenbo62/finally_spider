#!/usr/bin/python3
# _*_ coding:utf-8 _*_
import requests
import os
import urllib
import re,csv
import time
from fake_useragent import UserAgent
from lxml import etree

words_base = ['狂欢','发售','折','减','sale','OFF','新品','上新','限量','活动','特卖','特惠','赠','联名','礼遇','优惠','免费',
              '开门红','低价','送','降','献礼','全新','预售','立省','钜惠','秒杀','领券','上市','礼赞','半价','旦','年货']

basedir = os.path.dirname(__file__)

# 装饰器
def decorator(func):
    def inner(url, html, headers, brandname):
        try:
            datas = func(url, html, headers, brandname)
            if datas == []:
                with open(basedir+"/snaks_Error.csv",'a',encoding='utf-8') as f:
                    writer= csv.writer(f)
                    writer.writerow([brandname, url])
        except:
            with open(basedir+"/snaks_Error.csv", 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([brandname, url])
    return inner

def get_Page(url,headers,brand_name):
    try:
        response = requests.get(url,headers=headers,timeout=10)
        if response.status_code == 200:
            for word in words_base:
                if word in response.text:
                    with open(basedir+"/temp/Img.csv",'a',encoding='utf-8') as f:
                        writer= csv.writer(f)
                        writer.writerow([brand_name, '零食', url])
                    print(brand_name,url,"品牌在做活动"+"活动类型：%s"%word)
                    break
            return response.text,url
        return None,url
    except:
        return None,url

def get_Page1(url,headers,brand_name):
    try:
        response = requests.get(url,headers=headers,timeout=10)
        if response.status_code == 200:
            for word in words_base:
                if word in response.text:
                    with open(basedir+"/temp/Noimg.csv",'a',encoding='utf-8') as f:
                        writer= csv.writer(f)
                        writer.writerow([brand_name, '零食', url, "活动类型：%s"%word])
                    print(brand_name,url,"品牌在做活动"+"活动类型：%s"%word)
                    break
            return response.text
        return None
    except:
        with open(basedir + "/snaks_Error.csv", 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name, url])

def get_Page2(url,uri,headers,brand_name,datas):
    response = requests.post(uri,headers=headers,data=datas)
    if response.status_code == 200:
        for word in words_base:
            if word in response.text:
                with open(basedir+"/temp/Img.csv",'a',encoding='utf-8') as f:
                    writer= csv.writer(f)
                    writer.writerow([brand_name, '零食', url])
                print(brand_name,url,"品牌在做活动"+"活动类型：%s"%word)
                break
        return response.text,url
    return None

@decorator
def parse_kelaimei_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_dongyuansp_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='panelsdiv']//tbody/tr/td/div/@style")[1:2]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_dongyuansp_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_maotouying_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo jgabs']/div/div/div/@style")[-1:]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_maotouying_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_dage_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xinhuayuan_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Meiji_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:2]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_jililian_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo']//tbody//img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_jililian_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:5]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Bahlsen_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:2]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_zhudisi_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@module-title='tmTopBanner']/@module-data")
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    datas = re.findall('"shopBgImg":"(.*?)"',request.unquote(datas[0]))
    datas = [x.replace("\\","") for x in datas]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_zhudisi_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_ovaltine_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo']//tbody//img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_ovaltine_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:4]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_yifutang_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']/span/div/img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_yifutang_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_kernes_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_wondelful_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sk imgbg']/@style")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_feiluolun_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='abs sn-simple-logo']/img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_COSTCO_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li/a/img/@data-ks-lazyload")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_callebaut_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_callebaut_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_canute_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='sj-contentCJjMahog']/li/img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_canute_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_guoyuanyi_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='abs sn-simple-logo']/img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_guoyuanyi_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Brookfarm_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='sj-contentpAAmyDpr']/li/a/img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_glico_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo']/img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_glico_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_glico_JD1(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:3]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_bibigo_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_sanyang_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo']//tbody//img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_sanyang_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_haitai_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo']/a/img/@data-ks-lazyload")
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?png',x).group() for x in datas if x != ""]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_ORION_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li//img/@data-ks-lazyload")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_ORION_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[1:2]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_nongfushanquan_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li/a/img/@data-ks-lazyload")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_nongfushanquan_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_huangzu_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='footer-more-trigger sn-simple-logo']//img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_cocoalandlot100_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_daxidi_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo']/img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_daxidi_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:2]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_sinoonunion_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']/span/div/div/div/div/@style")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_sinoonunion_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_daojicao_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/div/@style")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Nestle_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='sx_carousel_content clearfix']/li/img/@data-ks-lazyload")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Nestle_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[-5:]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_illy_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='scroller-content']/li/a/@style")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_illy_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_UCC_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='scroller-content']/li/a/@style")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_UCC_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_g7coffee_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/@style")[1:2]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_g7coffee_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Super_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:-1]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_kelloggs_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:4]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_kelloggs_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_OLDTOWNWHITE_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = ['https:'+re.search('\s<img.*?"(//img.*?jpg)',x).group(1) for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_aikcheong_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo']/img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_aikcheong_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_lavazza_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/@style")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_lavazza_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[1:2]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Evian_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li/a/img/@data-ks-lazyload")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Evian_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_jason_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_jason_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Alicafe_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/div/@style")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Alicafe_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:3]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_fameseen_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_fameseen_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[0:3]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_agf_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[0:3]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_SABAVA_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:2]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_SABAVA_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_cephei_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:2]
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?png',x).group() for x in datas if x != "" and '.png' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_cephei_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_DANACSTORY_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:2]
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?png',x).group() for x in datas if x != "" and '.png' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_DANACSTORY_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:3]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_quannan_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_lidashi_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_lidashi_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_QUAKER_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_QUAKER_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_starbucks_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:4]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_starbucks_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0]
    datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_BINGGRAE_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_gandimuchang_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_gandimuchang_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_lakungayo_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/@style")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_JellyBelly_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_JellyBelly_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:2]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_hersheys_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//a/@style")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_hersheys_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:5]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Brookfarm_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Pepsi_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/@style")[1:2]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_Pepsi_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xijie_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xijie_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_bluediamond_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//ul[@class='macontent']/li/a/img/@data-ks-lazyload")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_sagocoffee_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_sagocoffee_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_HAHNE_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//li/div/@style")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_blink_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/div/@style")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_goldkili_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_juxiangyuan_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@module-title='tmCutPic']/@module-data")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    from urllib import request
    datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_juxiangyuan_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_bbhmf_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_bbhmf_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_TanHueVien_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_senyong_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']/span/div/a/@style")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:2]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_senyong_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:2]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_thaiaochi_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='h-posters']//td/div/@style")[1:2]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_damazhan_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_hanmeihe_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_wangwang_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='item']//img/@data-ks-lazyload")[0:2]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_wangwang_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_wrigley_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_lotus_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:2]
    # datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_zhudisi_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@module-title='tmCutPic']/@module-data")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    from urllib import request
    datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_zhudisi_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_gangrong_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sn-simple-logo']//img/@data-ks-lazyload")[0:2]
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = ['https:'+re.search('"designer_image_url":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_shudaoxiang_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@module-title='tmTopBanner']/@module-data")
    # datas = [re.findall('//.*?jpg',x) for x in datas if x != "" and '.jpg' in x][1]
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    from urllib import request
    datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_shudaoxiang_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:2]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_qiaqia_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_ganyuan_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_yushiyuan_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_yushiyuan_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:4]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_mdlz_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='haibao']/a/@style")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_mdlz_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_yake_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//li[@class='imd4bg']/div/@style")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_yake_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:4]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_chunguang_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//tbody//div/@style")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_chunguang_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_laojiekou_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_laojiekou_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_fujiya_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_fujiya_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_perfetti_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/div/@style")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_haoxiangni_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='item']//img/@data-ks-lazyload")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_haoxiangni_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:1]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_boli_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@module-title='tmTopBanner']/@module-data")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    # datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    from urllib import request
    datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_boli_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:2]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_piaolingdashu_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_piaolingdashu_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_shiweixian_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='xx_inner']/@style")[-2:]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?png',x).group() for x in datas if x != "" and '.png' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_nanguo_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:4]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_nanguo_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_youyou_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='sx_one sn-simple-logo sx_abs']/div/@style")[1:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_youyou_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopHeadImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_tenwow_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@module-title='tmTopBanner']/@module-data")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    # datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    from urllib import request
    datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_tenwow_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_lidl_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_lidl_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:1]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xizhilang_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xizhilang_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_puji_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_dabaitu_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:2]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xinbianjie_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xinbianjie_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xiyumeinong_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_xiyumeinong_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_maidehao_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[1:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_maidehao_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:1]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_unclepop_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd']//img/@src")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:1]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_zhanshi_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@module-title='tmTopBanner']/@module-data")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    # datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:1]
    from urllib import request
    datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_zhanshi_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")
    datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x][0]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x][0:2]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_huanglaowu_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//div[@class='mgzxzs_zybj']/@style")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_huanglaowu_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_jiujiuya_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_madajie_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_madajie_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[2:3]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_ziranpai_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_ziranpai_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_delis_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='item']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_delis_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//img[@class='J_imgLazyload']/@original")[1:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_kebike_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:2]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_wrigley_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_wrigley_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_huangfeihong_TM(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//div[@class='skin-box-bd clear-fix']//img/@data-ks-lazyload")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

@decorator
def parse_huangfeihong_JD(url, html, headers, brandname):
    html_lxml = etree.HTML(html)
    datas = html_lxml.xpath("//script[@class='J_data']/text()")[0:1]
    # datas = [re.findall('//img.*?jpg',x) for x in datas if x != "" and '.jpg' in x]
    datas = ['https:'+re.search('//img.*?jpg',x).group() for x in datas if x != "" and '.jpg' in x]
    # from urllib import request
    # datas = [re.search('"shopBgImg":"(.*?)"',request.unquote(datas[0])).group(1).replace("\\","")]
    # datas = [request.unquote(datas[0])]
    print(datas)
    item= {}
    # 创建保存图片文件夹
    file = basedir + '/yanzhengma'
    if os.path.exists(file):
        os.chdir(file)
    else:
        os.mkdir(file)
        os.chdir(file)
    count = 0
    brand_name = brandname + '__'
    for data in datas:
        # 图片链接
        img_url = data
        # 图片名字
        filename = brand_name + data.split("/")[-1].split("?")[0]
        # 验证码图片文件名
        response = requests.get(img_url, headers=headers)
        if response.status_code == 200:
            image = response.content
            try:
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
            except Exception as e:
                filename = brand_name + str(count) + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(image)
                    count += 1
                    print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
    return datas

def main():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    brandname = '客唻美_JD'
    html,url = get_Page('https://kelaimei.jd.com/', headers, brandname)
    parse_kelaimei_JD(url, html, headers, brandname)

    brandname = 'TOKYO MILK CHEESE FACTORY_kaola'
    get_Page1('https://mall.kaola.com/3413345?zn=banner&zp=1&ri=TOKYO%20MILK%20CHEESE%20FACTORY&rp=search', headers, brandname)

    brandname = 'Lotus和情_JD'
    get_Page1('https://mall.jd.com/index-1000102764.html', headers, brandname)

    brandname = '东远_TM'
    html,url = get_Page('https://dongyuansp.tmall.com', headers, brandname)
    parse_dongyuansp_TM(url, html, headers, brandname)

    brandname = '东远_JD'
    html,url = get_Page('https://mall.jd.com/index-828884.html', headers, brandname)
    parse_dongyuansp_JD(url, html, headers, brandname)

    brandname = '猫头鹰_TM'
    html,url = get_Page('https://maotouying.tmall.com/', headers, brandname)
    parse_maotouying_TM(url, html, headers, brandname)

    brandname = '猫头鹰_JD'
    html,url = get_Page('https://mall.jd.com/index-1000072461.html', headers, brandname)
    parse_maotouying_JD(url, html, headers, brandname)

    brandname = '大哥_JD'
    html,url = get_Page('https://mall.jd.com/index-694248.html', headers, brandname)
    parse_dage_JD(url, html, headers, brandname)

    brandname = '新华园_JD'
    html,url = get_Page('https://mall.jd.com/index-841659.html', headers, brandname)
    parse_xinhuayuan_JD(url, html, headers, brandname)

    brandname = '明治_JD'
    html,url = get_Page('https://mall.jd.com/index-1000107610.html', headers, brandname)
    parse_Meiji_JD(url, html, headers, brandname)

    brandname = '吉利莲_TM'
    html,url = get_Page('https://jililian.tmall.com/', headers, brandname)
    parse_jililian_TM(url, html, headers, brandname)

    brandname = '吉利莲_JD'
    html,url = get_Page('https://mall.jd.com/index-1000077643.html', headers, brandname)
    parse_jililian_JD(url, html, headers, brandname)

    brandname = '百乐顺_JD'
    html,url = get_Page('https://mall.jd.com/index-1000110142.html', headers, brandname)
    parse_Bahlsen_JD(url, html, headers, brandname)

    brandname = '茱蒂丝_TM'
    html,url = get_Page('https://zhudisi.tmall.com/', headers, brandname)
    parse_zhudisi_TM(url, html, headers, brandname)

    brandname = '茱蒂丝_JD'
    html,url = get_Page('https://mall.jd.com/index-1000107801.html', headers, brandname)
    parse_zhudisi_JD(url, html, headers, brandname)

    brandname = '阿华田_TM'
    html,url = get_Page('https://ovaltine.tmall.com/', headers, brandname)
    parse_ovaltine_TM(url, html, headers, brandname)

    brandname = '阿华田_JD'
    html,url = get_Page('https://mall.jd.com/index-1000073381.html', headers, brandname)
    parse_ovaltine_JD(url, html, headers, brandname)

    brandname = '艺福堂_TM'
    html,url = get_Page('https://yifutang.tmall.com/', headers, brandname)
    parse_yifutang_TM(url, html, headers, brandname)

    brandname = '艺福堂_JD'
    html,url = get_Page('https://mall.jd.com/index-1000015041.html', headers, brandname)
    parse_yifutang_JD(url, html, headers, brandname)

    brandname = '克恩兹_JD'
    html,url = get_Page('https://mall.jd.com/index-1000103421.html', headers, brandname)
    parse_kernes_JD(url, html, headers, brandname)

    brandname = '万多福_JD'
    html,url = get_Page('https://mall.jd.com/index-585334.html', headers, brandname)
    parse_wondelful_JD(url, html, headers, brandname)

    brandname = '费罗伦_TM'
    html,url = get_Page('https://feiluolun.tmall.com/', headers, brandname)
    parse_feiluolun_TM(url, html, headers, brandname)

    brandname = 'COSTCO_TM'
    html,url = get_Page('https://costcowholesale.tmall.com/', headers, brandname)
    parse_COSTCO_TM(url, html, headers, brandname)

    brandname = '嘉利宝_TM'
    html,url = get_Page('https://callebaut.tmall.com/', headers, brandname)
    parse_callebaut_TM(url, html, headers, brandname)

    brandname = '嘉利宝_JD'
    html,url = get_Page('https://mall.jd.com/index-1000100468.html', headers, brandname)
    parse_callebaut_JD(url, html, headers, brandname)

    brandname = '嘉利宝_kaola'
    get_Page1('https://mall.kaola.com/17199343?zn=result&zp=page1-0&ri=%E5%98%89%E5%88%A9%E5%AE%9D&rp=search', headers, brandname)

    brandname = 'canute_TM'
    html,url = get_Page('https://canutesp.tmall.com/', headers, brandname)
    parse_canute_TM(url, html, headers, brandname)

    brandname = 'canute_JD'
    html,url = get_Page('https://mall.jd.com/index-621504.html', headers, brandname)
    parse_canute_JD(url, html, headers, brandname)

    brandname = '郭元益_TM'
    html,url = get_Page('https://guoyuanyi.tmall.com/', headers, brandname)
    parse_guoyuanyi_TM(url, html, headers, brandname)

    brandname = '郭元益_JD'
    html,url = get_Page('https://mall.jd.com/index-695817.html', headers, brandname)
    parse_guoyuanyi_JD(url, html, headers, brandname)

    brandname = 'Brookfarm_TM'
    html,url = get_Page('https://brookfarm.tmall.com/', headers, brandname)
    parse_Brookfarm_TM(url, html, headers, brandname)

    brandname = 'Brookfarm_kaola'
    get_Page1('https://mall.kaola.com/18277904?zn=result&zp=page1-0&ri=Brookfarm&rp=search', headers, brandname)

    brandname = '格力高_TM'
    html,url = get_Page('https://glico.tmall.com/', headers, brandname)
    parse_glico_TM(url, html, headers, brandname)

    brandname = '格力高_JD'
    html,url = get_Page('https://mall.jd.com/index-1000102990.html', headers, brandname)
    parse_glico_JD(url, html, headers, brandname)

    brandname = '格力高_JD1'
    html,url = get_Page('https://mall.jd.com/index-660102.html', headers, brandname)
    parse_glico_JD1(url, html, headers, brandname)

    brandname = '必品阁_JD'
    html,url = get_Page('https://mall.jd.com/index-1000076821.html', headers, brandname)
    parse_bibigo_JD(url, html, headers, brandname)

    brandname = '三养_TM'
    html,url = get_Page('https://sanyangsp.tmall.com/', headers, brandname)
    parse_sanyang_TM(url, html, headers, brandname)

    brandname = '三养_JD'
    html,url = get_Page('https://mall.jd.com/index-1000083941.html', headers, brandname)
    parse_sanyang_JD(url, html, headers, brandname)

    brandname = '海太_TM'
    html,url = get_Page('https://haitai.tmall.com/', headers, brandname)
    parse_haitai_TM(url, html, headers, brandname)

    brandname = 'ORION好丽友_TM'
    html,url = get_Page('https://orion.tmall.com/', headers, brandname)
    parse_ORION_TM(url, html, headers, brandname)

    brandname = 'ORION好丽友_JD'
    html,url = get_Page('https://mall.jd.com/index-1000007923.html', headers, brandname)
    parse_ORION_JD(url, html, headers, brandname)

    brandname = '农夫山泉_TM'
    html,url = get_Page('https://nongfushanquan.tmall.com/', headers, brandname)
    parse_nongfushanquan_TM(url, html, headers, brandname)

    brandname = '农夫山泉_JD'
    html,url = get_Page('https://mall.jd.com/index-1000008814.html', headers, brandname)
    parse_nongfushanquan_JD(url, html, headers, brandname)

    brandname = '皇族_TM'
    html,url = get_Page('https://huangzusp.tmall.com/', headers, brandname)
    parse_huangzu_TM(url, html, headers, brandname)

    brandname = '一百份_TM'
    html,url = get_Page('https://cocoalandlot100.tmall.com', headers, brandname)
    parse_cocoalandlot100_TM(url, html, headers, brandname)

    brandname = '大希地_TM'
    html,url = get_Page('https://daxidi.tmall.com/', headers, brandname)
    parse_daxidi_TM(url, html, headers, brandname)

    brandname = '大希地_JD'
    html,url = get_Page('https://mall.jd.com/index-57837.html', headers, brandname)
    parse_daxidi_JD(url, html, headers, brandname)

    brandname = '星农联合_TM'
    html,url = get_Page('https://sinoonunion.tmall.com/', headers, brandname)
    parse_sinoonunion_TM(url, html, headers, brandname)

    brandname = '星农联合_JD'
    html,url = get_Page('https://mall.jd.com/index-1000102501.html', headers, brandname)
    parse_sinoonunion_JD(url, html, headers, brandname)

    brandname = '星农联合_kaola'
    get_Page1('https://mall.kaola.com/7659?zn=result&zp=page1-0&ri=%E6%98%9F%E5%86%9C%E8%81%94%E5%90%88&rp=search', headers, brandname)

    brandname = '道吉草_TM'
    html,url = get_Page('https://daojicao.tmall.com/', headers, brandname)
    parse_daojicao_TM(url, html, headers, brandname)

    brandname = 'Nestle雀巢_TM'
    html,url = get_Page('https://nestle.tmall.com/', headers, brandname)
    parse_Nestle_TM(url, html, headers, brandname)

    brandname = 'Nestle雀巢_JD'
    html,url = get_Page('https://mall.jd.com/index-1000017162.html', headers, brandname)
    parse_Nestle_JD(url, html, headers, brandname)

    brandname = 'Illy_TM'
    html,url = get_Page('https://illy.tmall.com/', headers, brandname)
    parse_illy_TM(url, html, headers, brandname)

    brandname = 'Illy_JD'
    html,url = get_Page('https://mall.jd.com/index-1000099745.html', headers, brandname)
    parse_illy_JD(url, html, headers, brandname)

    brandname = 'Illy_kaola'
    get_Page1('https://www.kaola.com/brand/1156.html', headers, brandname)

    brandname = 'UCC悠诗诗_TM'
    html,url = get_Page('https://youshishi.tmall.com/', headers, brandname)
    parse_UCC_TM(url, html, headers, brandname)

    brandname = 'UCC悠诗诗_JD'
    html,url = get_Page('https://mall.jd.com/index-1000099565.html', headers, brandname)
    parse_UCC_JD(url, html, headers, brandname)

    brandname = 'g 7 coffee_TM'
    html,url = get_Page('https://g7coffeeyxw.tmall.com/', headers, brandname)
    parse_g7coffee_TM(url, html, headers, brandname)

    brandname = 'g 7 coffee_JD'
    html,url = get_Page('https://mall.jd.com/index-1000098301.html', headers, brandname)
    parse_g7coffee_JD(url, html, headers, brandname)

    brandname = 'Super超级_JD'
    html,url = get_Page('https://mall.jd.com/index-1000081122.html', headers, brandname)
    parse_Super_JD(url, html, headers, brandname)

    brandname = '家乐氏_TM'
    html,url = get_Page('https://kelloggs.tmall.com/', headers, brandname)
    parse_kelloggs_TM(url, html, headers, brandname)

    brandname = '家乐氏_JD'
    html,url = get_Page('https://mall.jd.com/index-1000013642.html', headers, brandname)
    parse_kelloggs_JD(url, html, headers, brandname)

    brandname = '家乐氏_kaola'
    get_Page1('https://www.kaola.com/brand/1898.html', headers, brandname)

    brandname = 'OLDTOWN WHITE旧街场_JD'
    html,url = get_Page('https://mall.jd.com/index-1000078821.html', headers, brandname)
    parse_OLDTOWNWHITE_JD(url, html, headers, brandname)

    brandname = '益昌老街_TM'
    html,url = get_Page('https://aikcheong.tmall.com/', headers, brandname)
    parse_aikcheong_TM(url, html, headers, brandname)

    brandname = '益昌老街_JD'
    html,url = get_Page('https://mall.jd.com/index-1000072402.html', headers, brandname)
    parse_aikcheong_JD(url, html, headers, brandname)

    brandname = 'LAVAZZA拉瓦萨_TM'
    html,url = get_Page('https://lavazza.tmall.com/', headers, brandname)
    parse_lavazza_TM(url, html, headers, brandname)

    brandname = 'LAVAZZA拉瓦萨_JD'
    html,url = get_Page('https://mall.jd.com/index-648998.html', headers, brandname)
    parse_lavazza_JD(url, html, headers, brandname)

    brandname = 'Evian依云_TM'
    html,url = get_Page('https://evian.tmall.com/', headers, brandname)
    parse_Evian_TM(url, html, headers, brandname)

    brandname = 'Evian依云_JD'
    html,url = get_Page('https://mall.jd.com/index-1000092987.html', headers, brandname)
    parse_Evian_JD(url, html, headers, brandname)

    brandname = 'jason捷森_TM'
    html,url = get_Page('https://jasonsp.tmall.com/', headers, brandname)
    parse_jason_TM(url, html, headers, brandname)

    brandname = 'jason捷森_JD'
    html,url = get_Page('https://mall.jd.com/index-694289.html', headers, brandname)
    parse_jason_JD(url, html, headers, brandname)

    brandname = 'Alicafe啡特力_TM'
    html,url = get_Page('https://feiteli.tmall.com/', headers, brandname)
    parse_Alicafe_TM(url, html, headers, brandname)

    brandname = 'Alicafe啡特力_JD'
    html,url = get_Page('https://mall.jd.com/index-1000079376.html', headers, brandname)
    parse_Alicafe_JD(url, html, headers, brandname)

    brandname = 'FameSeen名馨_TM'
    html,url = get_Page('https://fameseen.tmall.com/', headers, brandname)
    parse_fameseen_TM(url, html, headers, brandname)

    brandname = 'FameSeen名馨_JD'
    html,url = get_Page('https://mall.jd.com/index-1000091645.html', headers, brandname)
    parse_fameseen_JD(url, html, headers, brandname)

    brandname = 'agf_JD'
    html,url = get_Page('https://mall.jd.com/index-1000099626.html', headers, brandname)
    parse_agf_JD(url, html, headers, brandname)

    brandname = 'SABAVA沙巴哇_TM'
    html,url = get_Page('https://sabava.tmall.com/', headers, brandname)
    parse_SABAVA_TM(url, html, headers, brandname)

    brandname = 'SABAVA沙巴哇_JD'
    html,url = get_Page('https://mall.jd.com/index-1000077333.html', headers, brandname)
    parse_SABAVA_JD(url, html, headers, brandname)

    brandname = 'CEPHEI奢斐_TM'
    html,url = get_Page('https://cephei.tmall.com/', headers, brandname)
    parse_cephei_TM(url, html, headers, brandname)

    brandname = 'CEPHEI奢斐_JD'
    html,url = get_Page('https://mall.jd.com/index-649228.html', headers, brandname)
    parse_cephei_JD(url, html, headers, brandname)

    brandname = 'DANACSTORY当年故事_TM'
    html,url = get_Page('https://dangniangushi.tmall.com/', headers, brandname)
    parse_DANACSTORY_TM(url, html, headers, brandname)

    brandname = 'DANACSTORY当年故事_JD'
    html,url = get_Page('https://mall.jd.com/index-623153.html', headers, brandname)
    parse_DANACSTORY_JD(url, html, headers, brandname)

    brandname = '全南_JD'
    html,url = get_Page('https://mall.jd.com/index-1000074126.html', headers, brandname)
    parse_quannan_JD(url, html, headers, brandname)

    brandname = '力大狮_TM'
    html,url = get_Page('https://lidashi.tmall.com/', headers, brandname)
    parse_lidashi_TM(url, html, headers, brandname)

    brandname = '力大狮_JD'
    html,url = get_Page('https://mall.jd.com/index-1000093403.html', headers, brandname)
    parse_lidashi_JD(url, html, headers, brandname)

    brandname = 'QUAKER桂格_TM'
    html,url = get_Page('https://guigeshipin.tmall.com/', headers, brandname)
    parse_QUAKER_TM(url, html, headers, brandname)

    brandname = 'QUAKER桂格_JD'
    html,url = get_Page('https://mall.jd.com/index-1000007543.html', headers, brandname)
    parse_QUAKER_JD(url, html, headers, brandname)

    brandname = '日东红茶_kaola'
    get_Page1('https://www.kaola.com/brand/2614.html', headers, brandname)

    brandname = 'starbucks星巴克_TM'
    html,url = get_Page('https://starbucks.tmall.com/', headers, brandname)
    parse_starbucks_TM(url, html, headers, brandname)

    brandname = 'starbucks星巴克_JD'
    html,url = get_Page('https://mall.jd.com/index-1000090906.html', headers, brandname)
    parse_starbucks_JD(url, html, headers, brandname)

    brandname = '宾格瑞_JD'
    html,url = get_Page('https://mall.jd.com/index-1000102189.html', headers, brandname)
    parse_BINGGRAE_JD(url, html, headers, brandname)

    brandname = '甘蒂牧场_TM'
    html,url = get_Page('https://gandimuchang.tmall.com/', headers, brandname)
    parse_gandimuchang_TM(url, html, headers, brandname)

    brandname = '甘蒂牧场_JD'
    html,url = get_Page('https://mall.jd.com/index-1000074607.html', headers, brandname)
    parse_gandimuchang_JD(url, html, headers, brandname)

    brandname = '拉昆lakungayo_TM'
    html,url = get_Page('https://lakungayo.tmall.com/', headers, brandname)
    parse_lakungayo_TM(url, html, headers, brandname)

    brandname = 'Jelly Belly吉力贝_TM'
    html,url = get_Page('https://jellybelly.tmall.com/', headers, brandname)
    parse_JellyBelly_TM(url, html, headers, brandname)

    brandname = 'Jelly Belly吉力贝_JD'
    html,url = get_Page('https://mall.jd.com/index-783207.html', headers, brandname)
    parse_JellyBelly_JD(url, html, headers, brandname)

    brandname = '好时_TM'
    html,url = get_Page('https://hersheys.tmall.com/', headers, brandname)
    parse_hersheys_TM(url, html, headers, brandname)

    brandname = '好时_JD'
    html,url = get_Page('https://mall.jd.com/index-1000075682.html', headers, brandname)
    parse_hersheys_JD(url, html, headers, brandname)

    brandname = 'Brookfarm布鲁克家族_TM'
    html,url = get_Page('https://brookfarm.tmall.com/', headers, brandname)
    parse_Brookfarm_TM(url, html, headers, brandname)

    brandname = 'Brookfarm布鲁克家族_kaola'
    get_Page1('https://mall.kaola.com/18277904?zn=result&zp=page1-0&ri=Brookfarm%2F%E5%B8%83%E9%B2%81%E5%85%8B%E5%AE%B6%E6%97%8F&rp=search', headers, brandname)

    brandname = 'Pepsi百事_TM'
    html,url = get_Page('https://pepsico.tmall.com/', headers, brandname)
    parse_Pepsi_TM(url, html, headers, brandname)

    brandname = 'Pepsi百事_JD'
    html,url = get_Page('https://mall.jd.com/index-1000010481.html', headers, brandname)
    parse_Pepsi_JD(url, html, headers, brandname)

    brandname = '西捷_TM'
    html,url = get_Page('https://xijiesp.tmall.com/', headers, brandname)
    parse_xijie_TM(url, html, headers, brandname)

    brandname = '西捷_JD'
    html,url = get_Page('https://mall.jd.com/index-804107.html', headers, brandname)
    parse_xijie_JD(url, html, headers, brandname)

    brandname = 'BLUE DIAMOND蓝钻_TM'
    html,url = get_Page('https://bluediamond.tmall.com/', headers, brandname)
    parse_bluediamond_TM(url, html, headers, brandname)

    brandname = 'SAGOcoffee_TM'
    html,url = get_Page('https://sagocoffee.tmall.com/', headers, brandname)
    parse_sagocoffee_TM(url, html, headers, brandname)

    brandname = 'SAGOcoffee_JD'
    html,url = get_Page('https://mall.jd.com/index-208892.html', headers, brandname)
    parse_sagocoffee_JD(url, html, headers, brandname)

    brandname = 'HAHNE汉尼_TM'
    html,url = get_Page('https://hanni.tmall.com/', headers, brandname)
    parse_HAHNE_TM(url, html, headers, brandname)

    brandname = 'blink冰力克_TM'
    html,url = get_Page('https://blinksp.tmall.com/', headers, brandname)
    parse_blink_TM(url, html, headers, brandname)

    brandname = 'blink冰力克_kaola'
    get_Page1('https://mall.kaola.com/53955150?ri=brand&from=page1&zn=result&zp=page1-0&position=0&istext=3&srId=e117cd254fe86f24bb7788035db1e3fc', headers, brandname)

    brandname = '金祥麟_JD'
    html,url = get_Page('https://mall.jd.com/index-1000122703.html', headers, brandname)
    parse_goldkili_JD(url, html, headers, brandname)

    brandname = '咀香园饼家_TM'
    html,url = get_Page('https://juxiangyuanshipin.tmall.com/', headers, brandname)
    parse_juxiangyuan_TM(url, html, headers, brandname)

    brandname = '咀香园饼家_JD'
    html,url = get_Page('https://mall.jd.com/index-76615.html', headers, brandname)
    parse_juxiangyuan_JD(url, html, headers, brandname)

    brandname = 'Bobs Red Mill鲍勃红磨坊_TM'
    html,url = get_Page('https://bbhmf.tmall.com/', headers, brandname)
    parse_bbhmf_TM(url, html, headers, brandname)

    brandname = 'Bobs Red Mill鲍勃红磨坊_JD'
    html,url = get_Page('https://mall.jd.com/index-760354.html', headers, brandname)
    parse_bbhmf_JD(url, html, headers, brandname)

    brandname = 'Bobs Red Mill鲍勃红磨坊_JD'
    html,url = get_Page('https://mall.jd.com/index-760354.html', headers, brandname)
    parse_bbhmf_JD(url, html, headers, brandname)

    brandname = 'tan hue vien新华园_JD'
    html,url = get_Page('https://mall.jd.com/index-847443.html', headers, brandname)
    parse_TanHueVien_JD(url, html, headers, brandname)

    brandname = 'Morinaga森永_TM'
    html,url = get_Page('https://senyong.tmall.com/', headers, brandname)
    parse_senyong_TM(url, html, headers, brandname)

    brandname = 'Morinaga森永_JD'
    html,url = get_Page('https://mall.jd.com/index-114434.html', headers, brandname)
    parse_senyong_JD(url, html, headers, brandname)

    brandname = 'Thai Ao Chi泰奥琪_TM'
    html,url = get_Page('https://thaiaochi.tmall.com/', headers, brandname)
    parse_thaiaochi_TM(url, html, headers, brandname)

    brandname = '大马占_TM'
    html,url = get_Page('https://damazhan.tmall.com/', headers, brandname)
    parse_damazhan_TM(url, html, headers, brandname)

    brandname = '韩美禾_JD'
    html,url = get_Page('https://mall.jd.com/index-652441.html', headers, brandname)
    parse_hanmeihe_JD(url, html, headers, brandname)

    brandname = '旺旺_TM'
    html,url = get_Page('https://wangwangshipin.tmall.com/', headers, brandname)
    parse_wangwang_TM(url, html, headers, brandname)

    brandname = '旺旺_JD'
    html,url = get_Page('https://mall.jd.com/index-1000079565.html', headers, brandname)
    parse_wangwang_JD(url, html, headers, brandname)

    brandname = 'SKITTLES彩虹_TM'
    html,url = get_Page('https://wrigley.tmall.com/', headers, brandname)
    parse_wrigley_TM(url, html, headers, brandname)

    brandname = 'lotus和情_JD'
    html,url = get_Page('https://mall.jd.com/index-1000102764.html', headers, brandname)
    parse_lotus_JD(url, html, headers, brandname)

    brandname = 'Julie’s茱蒂丝_TM'
    html,url = get_Page('https://zhudisi.tmall.com/', headers, brandname)
    parse_zhudisi_TM(url, html, headers, brandname)

    brandname = 'Julie’s茱蒂丝_JD'
    html,url = get_Page('https://mall.jd.com/index-1000107801.html', headers, brandname)
    parse_zhudisi_JD(url, html, headers, brandname)

    brandname = 'Kong WENG港荣_TM'
    html,url = get_Page('https://gangrongsp.tmall.com/', headers, brandname)
    parse_gangrong_TM(url, html, headers, brandname)

    brandname = '蜀道香_TM'
    html,url = get_Page('https://shudaoxiang.tmall.com/', headers, brandname)
    parse_shudaoxiang_TM(url, html, headers, brandname)

    brandname = '蜀道香_JD'
    html,url = get_Page('https://mall.jd.com/index-1000010104.html', headers, brandname)
    parse_shudaoxiang_JD(url, html, headers, brandname)

    brandname = 'ChaCheer洽洽_TM'
    html,url = get_Page('https://qiaqia.tmall.com/', headers, brandname)
    parse_qiaqia_TM(url, html, headers, brandname)

    brandname = 'KAM YUEN甘源_TM'
    html,url = get_Page('https://mall.jd.com/index-1000083686.html', headers, brandname)
    parse_ganyuan_TM(url, html, headers, brandname)

    brandname = '御食园_TM'
    html,url = get_Page('https://yushiyuan.tmall.com/', headers, brandname)
    parse_yushiyuan_TM(url, html, headers, brandname)

    brandname = '御食园_JD'
    html,url = get_Page('https://mall.jd.com/index-44644.html', headers, brandname)
    parse_yushiyuan_JD(url, html, headers, brandname)

    brandname = '奥利奥_TM'
    html,url = get_Page('https://mdlz.tmall.com/', headers, brandname)
    parse_mdlz_TM(url, html, headers, brandname)

    brandname = '奥利奥_JD'
    html,url = get_Page('https://mall.jd.com/index-1000100813.html', headers, brandname)
    parse_mdlz_JD(url, html, headers, brandname)

    brandname = '雅客_TM'
    html,url = get_Page('https://yakesp.tmall.com/', headers, brandname)
    parse_yake_TM(url, html, headers, brandname)

    brandname = '雅客_JD'
    html,url = get_Page('https://mall.jd.com/index-1000093244.html', headers, brandname)
    parse_yake_JD(url, html, headers, brandname)

    brandname = '春光_TM'
    html,url = get_Page('https://chunguang.tmall.com', headers, brandname)
    parse_chunguang_TM(url, html, headers, brandname)

    brandname = '春光_JD'
    html,url = get_Page('https://mall.jd.com/index-1000076141.html', headers, brandname)
    parse_chunguang_JD(url, html, headers, brandname)

    brandname = '老街口_TM'
    html,url = get_Page('https://laojiekou.tmall.com/', headers, brandname)
    parse_laojiekou_TM(url, html, headers, brandname)

    brandname = '老街口_JD'
    html,url = get_Page('https://mall.jd.com/index-1000102261.html', headers, brandname)
    parse_laojiekou_JD(url, html, headers, brandname)

    brandname = '不二家_TM'
    html,url = get_Page('https://fujiya.tmall.com/', headers, brandname)
    parse_fujiya_TM(url, html, headers, brandname)

    brandname = '不二家_JD'
    html,url = get_Page('https://mall.jd.com/index-1000088842.html', headers, brandname)
    parse_fujiya_JD(url, html, headers, brandname)

    brandname = '阿尔卑斯_TM'
    html,url = get_Page('https://perfetti.tmall.com/', headers, brandname)
    parse_perfetti_TM(url, html, headers, brandname)

    brandname = '好想你_TM'
    html,url = get_Page('https://haoxiangni.tmall.com/', headers, brandname)
    parse_haoxiangni_TM(url, html, headers, brandname)

    brandname = '好想你_JD'
    html,url = get_Page('https://mall.jd.com/index-36624.html', headers, brandname)
    parse_haoxiangni_JD(url, html, headers, brandname)

    brandname = '波力_TM'
    html,url = get_Page('https://bolisp.tmall.com/', headers, brandname)
    parse_boli_TM(url, html, headers, brandname)

    brandname = '波力_JD'
    html,url = get_Page('https://mall.jd.com/index-1000083662.html', headers, brandname)
    parse_boli_JD(url, html, headers, brandname)

    brandname = '飘零大叔_TM'
    html,url = get_Page('https://piaolingdashu.tmall.com/', headers, brandname)
    parse_piaolingdashu_TM(url, html, headers, brandname)

    brandname = '飘零大叔_JD'
    html,url = get_Page('https://mall.jd.com/index-1000089638.html', headers, brandname)
    parse_piaolingdashu_JD(url, html, headers, brandname)

    brandname = '食为先_TM'
    html,url = get_Page('https://shiweixian.tmall.com/', headers, brandname)
    parse_shiweixian_TM(url, html, headers, brandname)

    brandname = '南国_TM'
    html,url = get_Page('https://nanguo.tmall.com/', headers, brandname)
    parse_nanguo_TM(url, html, headers, brandname)

    brandname = '南国_JD'
    html,url = get_Page('https://mall.jd.com/index-1000105597.html', headers, brandname)
    parse_nanguo_JD(url, html, headers, brandname)

    brandname = '有友_TM'
    html,url = get_Page('https://youyoushipin.tmall.com/', headers, brandname)
    parse_youyou_TM(url, html, headers, brandname)

    brandname = '有友_JD'
    html,url = get_Page('https://mall.jd.com/index-1000078273.html', headers, brandname)
    parse_youyou_JD(url, html, headers, brandname)

    brandname = 'Ten Wow天喔_TM'
    html,url = get_Page('https://tenwow.tmall.com/', headers, brandname)
    parse_tenwow_TM(url, html, headers, brandname)

    brandname = 'Ten Wow天喔_JD'
    html,url = get_Page('https://mall.jd.com/index-1000080344.html', headers, brandname)
    parse_tenwow_JD(url, html, headers, brandname)

    brandname = 'Lidl历德_TM'
    html,url = get_Page('https://lidl.tmall.hk/', headers, brandname)
    parse_lidl_TM(url, html, headers, brandname)

    brandname = 'Lidl历德_JD'
    html,url = get_Page('https://mall.jd.hk/index-676582.html', headers, brandname)
    parse_lidl_JD(url, html, headers, brandname)

    brandname = 'Lidl历德_kaola'
    get_Page1('https://mall.kaola.com/17453672?zn=banner&zp=1&ri=%E5%8E%86%E5%BE%B7&rp=search', headers, brandname)

    brandname = '喜之郎_TM'
    html,url = get_Page('https://xizhilangsp.tmall.com/', headers, brandname)
    parse_xizhilang_TM(url, html, headers, brandname)

    brandname = '喜之郎_JD'
    html,url = get_Page('https://mall.jd.com/index-1000100238.html', headers, brandname)
    parse_xizhilang_JD(url, html, headers, brandname)

    brandname = '葡记_JD'
    html,url = get_Page('https://mall.jd.com/index-1000090501.html', headers, brandname)
    parse_puji_JD(url, html, headers, brandname)

    brandname = '大白兔_JD'
    html,url = get_Page('https://mall.jd.com/index-1000111642.html', headers, brandname)
    parse_dabaitu_JD(url, html, headers, brandname)

    brandname = 'New boundaries新边界_TM'
    html,url = get_Page('https://xinbianjie.tmall.com/', headers, brandname)
    parse_xinbianjie_TM(url, html, headers, brandname)

    brandname = 'New boundaries新边界_JD'
    get_Page1('https://mall.jd.com/index-1000089592.html', headers, brandname)

    brandname = '西域美农_TM'
    html,url = get_Page('https://xiyumeinong.tmall.com/', headers, brandname)
    parse_xiyumeinong_TM(url, html, headers, brandname)

    brandname = '西域美农_JD'
    html,url = get_Page('https://mall.jd.com/index-1000007573.html', headers, brandname)
    parse_xiyumeinong_JD(url, html, headers, brandname)

    brandname = '麦德好_TM'
    html,url = get_Page('https://maidehao.tmall.com/', headers, brandname)
    parse_maidehao_TM(url, html, headers, brandname)

    brandname = '麦德好_JD'
    html,url = get_Page('https://mall.jd.com/index-1000101401.html', headers, brandname)
    parse_maidehao_JD(url, html, headers, brandname)

    brandname = 'UNCLE POP米老头_TM'
    html,url = get_Page('https://unclepop.tmall.com/', headers, brandname)
    parse_unclepop_TM(url, html, headers, brandname)

    brandname = '詹氏_TM'
    html,url = get_Page('https://zhanshishipin.tmall.com/', headers, brandname)
    parse_zhanshi_TM(url, html, headers, brandname)

    brandname = '詹氏_JD'
    html,url = get_Page('https://mall.jd.com/index-20881.html', headers, brandname)
    parse_zhanshi_JD(url, html, headers, brandname)

    brandname = '黄老五_TM'
    html,url = get_Page('https://huanglaowu.tmall.com/', headers, brandname)
    parse_huanglaowu_TM(url, html, headers, brandname)

    brandname = '黄老五_JD'
    html,url = get_Page('https://mall.jd.com/index-1000074722.html', headers, brandname)
    parse_huanglaowu_JD(url, html, headers, brandname)

    brandname = '久久丫_TM'
    html,url = get_Page('https://jiujiuya.tmall.com/', headers, brandname)
    parse_jiujiuya_TM(url, html, headers, brandname)

    brandname = '马大姐_TM'
    html,url = get_Page('https://madajiesp.tmall.com/', headers, brandname)
    parse_madajie_TM(url, html, headers, brandname)

    brandname = '马大姐_JD'
    html,url = get_Page('https://mall.jd.com/index-40213.html', headers, brandname)
    parse_madajie_JD(url, html, headers, brandname)

    brandname = 'NATURAL IS BEST自然派_TM'
    html,url = get_Page('https://ziranpai.tmall.com/', headers, brandname)
    parse_ziranpai_TM(url, html, headers, brandname)

    brandname = 'NATURAL IS BEST自然派_JD'
    html,url = get_Page('https://mall.jd.com/index-1000083823.html', headers, brandname)
    parse_ziranpai_JD(url, html, headers, brandname)

    brandname = 'DELIS煌上煌_TM'
    html,url = get_Page('https://delis.tmall.com/', headers, brandname)
    parse_delis_TM(url, html, headers, brandname)

    brandname = 'DELIS煌上煌_JD'
    html,url = get_Page('https://mall.jd.com/index-67104.html', headers, brandname)
    parse_delis_JD(url, html, headers, brandname)

    brandname = '可比克_JD'
    html,url = get_Page('https://mall.jd.com/index-1000097324.html', headers, brandname)
    parse_kebike_JD(url, html, headers, brandname)

    brandname = 'wrigley箭牌_TM'
    html,url = get_Page('https://wrigley.tmall.com/', headers, brandname)
    parse_wrigley_TM(url, html, headers, brandname)

    brandname = 'wrigley箭牌_JD'
    html,url = get_Page('https://mall.jd.com/index-1000074985.html', headers, brandname)
    parse_wrigley_JD(url, html, headers, brandname)

    brandname = '黄飞红_TM'
    html,url = get_Page('https://huangfeihong.tmall.com/', headers, brandname)
    parse_huangfeihong_TM(url, html, headers, brandname)

    brandname = '黄飞红_JD'
    html,url = get_Page('https://mall.jd.com/index-1000083766.html', headers, brandname)
    parse_huangfeihong_JD(url, html, headers, brandname)

if __name__ == '__main__':
    main()
