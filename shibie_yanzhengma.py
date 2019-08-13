# # -*- coding: utf-8 -*-
# import requests
# import os
# import time
# from lxml import etree
#
#
# def get_Page(url,headers):
#     response = requests.get(url,headers=headers)
#     if response.status_code == 200:
#         # print(response.text)
#         return response.text
#     return None
#
#
# def parse_Page(html, headers):
#     html_lxml = etree.HTML(html)
#     datas = html_lxml.xpath("//ul[@class='slideshow slides']/li")
#     item= {}
#     # 创建保存验证码文件夹
#     file = 'D:/yanzhengma'
#     if os.path.exists(file):
#         os.chdir(file)
#     else:
#         os.mkdir(file)
#         os.chdir(file)
#     count = 0
#     brand_name = '娇兰'
#     for data in datas:
#         # 图片链接
#         img_url = data.xpath('.//img/@src')[0]
#         # 图片名字
#         filename = brand_name + data.xpath('.//img/@src')[0].split("/")[-1]
#         # 验证码图片文件名
#         response = requests.get(img_url,headers=headers)
#         if response.status_code == 200:
#             image = response.content
#             with open(filename,'wb') as f:
#                 f.write(image)
#                 count += 1
#                 print('保存第{}张验证码成功'.format(count))
#                 time.sleep(1)
#
#
# def main():
#     url = 'http://www.guerlain.com.cn/'
#     headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
#     html = get_Page(url,headers)
#     parse_Page(html,headers)
#
#
# if __name__ == '__main__':
#     main()



from aip import AipOcr
import os
import csv
import hashlib
import pymongo
from PIL import Image
import shutil


i = 0
j = 0
APP_ID = '14734850'
API_KEY = 'TmKdrcRh6lu9AyMsOi13kwau'
SECRET_KEY = 'mbhD3UT5OWwzqAhzF6MY9u4by9dnc6D5'
words_base = ['狂欢','发售','折','减','sale','OFF','新品','上新','限量','活动','特卖','特惠','赠','联名','礼遇','优惠','免费',
              '开门红','低价','送','降','献礼','全新','预售','立省','钜惠','秒杀','领券','上市','礼赞','半价','福利','买','旦',
              '免息','全场','礼赞','满']

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 配置数据库信息
mongo_client=pymongo.MongoClient('localhost',27017)
db=mongo_client['FOR_MD5']
my_collection=db['md5美妆']

# 读取图片
file_path = 'D:/yanzhengma'
# file_path = 'C:/Users/Administrator/Desktop/ImageOCR/yanzhengma'
filenames = os.listdir(file_path)
# print(filenames)
for filename in filenames:
    # 将路径与文件名结合起来就是每个文件的完整路径
    info = os.path.join(file_path,filename)
    with open(info, 'rb') as fp:
        # 获取文件夹的路径
        image = fp.read()
        # 调用通用文字识别, 图片参数为本地图片
        result = client.basicGeneral(image)
        # 定义参数变量
        options = {
                'detect_direction' : 'true',
                'language_type' : 'CHN_ENG',
        }
        # 调用通用文字识别接口
        result = client.basicGeneral(image,options)
        content_list = []
        # print(result)
        if result['words_result_num'] == 0:
            print(filename + ':' + '----')
            i += 1
        else:
            for i in range(len(result['words_result'])):
                content_list.append(result['words_result'][i]['words'])
                j += 1
            content_list = ','.join(content_list)
            # print(filename + ' : ' + content_list)
            for k in words_base:
                if k in content_list:
                    md5 = hashlib.md5(content_list.encode('utf-8')).hexdigest()
                    url_find = {'md5': md5}
                    # 判断网页MD5是否存在数据库中
                    if my_collection.find_one(url_find):
                        old_md5 = my_collection.find_one(url_find)['md5']
                        if md5 == old_md5:
                            print('MD5一致')
                        # else:
                        #     print('MD5不一致')
                        #     my_collection.update(url_find, {'$set': {"md5": md5}})
                        #     with open("C:/Users/Administrator/Desktop/img_shibie_result.csv", "a",
                        #               encoding="utf-8") as f:
                        #         writer = csv.writer(f)
                        #         writer.writerow([filename.split("__")[0], filename, content_list])
                    else:
                        print(filename + ' : 添加数据-----'+content_list)
                        info = {'md5': md5}
                        my_collection.insert(info)
                        with open("C:/Users/Administrator/Desktop/img_shibie_result.csv", "a", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow([filename.split("__")[0], filename, content_list])
                    break

print('共识别图片{}张'.format(i+j))
print('未识别出文本{}张'.format(i))
print('已识别出文本{}张'.format(j))

# from PIL import Image
#
# filepath = 'D:\CHOW TAI FOOK__GANEN_1920_01.jpg'
# image = Image.open(filepath)
# # 传入L将图片转化为灰度图像
# image = image.convert('L')
# # 传入1将图片进行二值化处理
# image = image.convert('1')
# image.show()