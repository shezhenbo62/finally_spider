import requests
import pandas as pd
import random
import time,json,csv


data = pd.read_excel(r'D:\fidder\xiaohongshu1.xls').values.tolist()
data = data[8:]
print(data)
for i in range(len(data)//9):
    item = {}
    url = "https://www.xiaohongshu.com" + data[9*i][0].split(" ")[1]
    print(url)
    authorization = data[9*i+5][0].split(" ")[1]
    print(authorization)
    device_id = data[9 * i + 6][0].split(" ")[1]
    print(device_id)
    shieid = data[9*i+7][0].split(" ")[1]
    print(shieid)

    header = {'Authorization': authorization,
              'device_id': device_id,
              'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G955F Build/JLS36C) Resolution/720*1280 Version/5.28.0 Build/5280260 Device/(samsung;SM-G955F) NetType/WiFi',
              'shield': shieid,
              'Host': 'www.xiaohongshu.com',
              'Connection': 'Keep-Alive',
              'Accept-Encoding': 'gzip'}
    try:
        resp = requests.get(url,headers=header,timeout=5,verify=False)
    except Exception as e:
        print(e)
    else:
        if resp.status_code == 200:
            response = resp.content.decode()
            print(response)
            js_html = json.loads(response)
            data_list = js_html['data']['notes']
            for f in data_list:
                item['item_id'] = f['id']
                print(item)
                with open('C:/Users/Administrator/Desktop/xiaohongshu.csv','a',encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=['item_id'])
                    # writer.writeheader()
                    writer.writerow(item)
            time.sleep(0.5)

# import re
#
#
# url = 'width:100%;height:100%;display:block;background-image:url(//gdp.alicdn.com/imgextra/i4/3295545743/O1CN014ox8Ay1sIL5DyTUwA_!!3295545743.jpg);background-repeat:no-repeat;'
# title = re.findall(r'url\((.*?)\)',url)
# # for i in range(0,40,2):
# print(title)
# print(type(title))

# import pandas as pd
# import matplotlib.pyplot as plt
#
# labels='frogs', 'hogs', 'dogs', 'logs'
# sizes=[15, 20, 45, 10]
# colors='yellowgreen','gold','lightskyblue','lightcoral'
# explode=(0, 0.1, 0, 0)
# plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=50)
# plt.axis('equal')
# plt.show()

# import requests
# import re
#
# head = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
# resp = requests.get('https://wq.jd.com/item/view?sku=3166589&price=34.80&fs=1',headers=head).content.decode()
# print(resp)
# title = re.findall(r'"nm\\":\\"(.*?)\\",\\"num',resp)
# print(title)

# from fake_useragent import UserAgent
#
# ua = UserAgent()
# print(ua.random)

# import time
#
# a = time.time()
# b = '%.2f'%a
# print(a)
# print(b)
# print(int(round(a*1000)))


# from aip import AipOcr
# import os
#
#
# i = 0
# j = 0
# APP_ID = '14734850'
# API_KEY = 'TmKdrcRh6lu9AyMsOi13kwau'
# SECRET_KEY = 'mbhD3UT5OWwzqAhzF6MY9u4by9dnc6D5'
#
# client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#
# # 读取图片
# file_path = 'D:/yanzhengma'
# filenames = os.listdir(file_path)
# # print(filenames)
# for filename in filenames:
#     # 将路径与文件名结合起来就是每个文件的完整路径
#     info = os.path.join(file_path,filename)
#     with open(info, 'rb') as fp:
#         # 获取文件夹的路径
#         image = fp.read()
#         # 调用通用文字识别, 图片参数为本地图片
#         result = client.basicGeneral(image)
#         # 定义参数变量
#         options = {
#                 'detect_direction' : 'true',
#                 'language_type' : 'CHN_ENG',
#         }
#         # 调用通用文字识别接口
#         result = client.basicGeneral(image,options)
#         content_list = []
#         # print(result)
#         if result['words_result_num'] == 0:
#             print(filename + ':' + '----')
#             i += 1
#         else:
#             for i in range(len(result['words_result'])):
#                 content_list.append(result['words_result'][i]['words'])
#                 j += 1
#             content_list = ','.join(content_list)
#             print(filename + ' : ' +content_list)
#             j += 1
#
# print('共识别图片{}张'.format(i+j))
# print('未识别出文本{}张'.format(i))
# print('已识别出文本{}张'.format(j))


# import pandas as pd
# import requests
# from fake_useragent import UserAgent
# import random
# import time,json
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
#
# # 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#
# ua = UserAgent()
# headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'accept-encoding': 'gzip, deflate, br',
# 'accept-language': 'zh-CN,zh;q=0.9',
# 'cache-control': 'max-age=0',
# 'cookie': 'cna=r5cTFAVzS0gCAXFo2mWr3FNi; hng=CN%7Czh-CN%7CCNY%7C156; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; lid=%E5%A5%BD%E7%9A%84%E4%BA%8B%E6%83%85lv; enc=klOKw54k8ButfrUt0DuC6J6aNbSTz8yx9UAA6kkMjWjwChgxck%2BsR06TnFz%2BpivjZsjCR71gfwg3H9zrJ19u1A%3D%3D; UM_distinctid=1661a67e726629-01f85f9dd7c21d-37664109-1fa400-1661a67e7271df; _med=dw:1920&dh:1080&pw:1920&ph:1080&ist:0; cq=ccp%3D1; OZ_1U_2061=vid=vb8e6a76f64b9a.0&ctime=1542090817&ltime=1542090718; _uab_collina=154209327660758908445506; t=2729faefaec453f12677acb9bf00eeb1; tracknick=%5Cu597D%5Cu7684%5Cu4E8B%5Cu60C5lv; _tb_token_=318e1e77fef6; cookie2=13239add829854cce619a89e27a9dcde; _m_h5_tk=43f9d7b8b15629f087396a9b453e2a4a_1542860397683; _m_h5_tk_enc=e70845af13ca7a58b4f5cff585c6ae1e; tt=tmall-main; res=scroll%3A1903*3972-client%3A1903*943-offset%3A1903*3972-screen%3A1920*1080; pnm_cku822=098%23E1hvMpvUvbpvUvCkvvvvvjiPR2q9ljYEPFM96jrCPmPysj1hPLFO1jDCPsSZQjrPiQhvCvvv9UUtvpvhvvvvvUyCvvOUvvVvayTivpvUvvmv%2Bzy6mO7tvpvIvvvvvhCvvvvvvUnvphvWS9vv96CvpC29vvm2phCvhhvvvUnvphvppvyCvhQWUDyvCA7QD7zhV8tYE57QD70Oe169QbmDYEQwJhmQ0f0DW3CQog0HsXZpejHbAXcBlLyzOvxrAn3l5FItoX7YeOmAdcnjafmxfXyOvphvC9vhvvCvpvGCvvpvvPMM; isg=BIaGaS_OIWfbe_V5CbAkTYa413zIT8iC02XkGnCvaKmEcyaN2HfjsMYBT-8aW8K5',
# 'referer': 'https://www.tmall.com/',
# 'upgrade-insecure-requests': '1',
# 'user-agent': ua.random}
#
# pinpai_list = pd.read_excel('C:/Users/Administrator/Desktop/海淘网美妆品牌.xls',skiprows=1170).values.tolist()
# print(pinpai_list)
# for pinpai in pinpai_list:
#     proxies = requests.get('http://119.23.203.63:6066/get/').content
#     pinpai_name = str(pinpai[0]).strip()
#     url = 'https://list.tmall.com/search_product.htm?q={}&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton'.format(pinpai_name)
#     try:
#         response = requests.get(url,headers=headers,proxies={"http": "http://{}".format(proxies)},verify=False)
#     except Exception as e:
#         print(e)
#     else:
#         if response.status_code == 200:
#             resp = response.text
#             if '没找到' in resp:
#                 continue
#             elif '官方' in resp:
#                 print(pinpai[0],'在天猫开设有官方旗舰店')
#                 with open('C:/Users/Administrator/Desktop/tm_pinpai.csv','a',encoding='utf-8') as f:
#                     f.write(str(pinpai[0]))
#                     f.write('\r\n')
#             elif '旗舰' in resp:
#                 print(pinpai[0],'在天猫开设有官方旗舰店')
#                 with open('C:/Users/Administrator/Desktop/tm_pinpai.csv','a',encoding='utf-8') as f:
#                     f.write(str(pinpai[0]))
#                     f.write('\r\n')


# # 对活动内容加密并插入到mongodb数据库
# import pandas as pd
# import numpy as np
# import jieba
# import time
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# from scipy.misc import imread
# import pymongo
# import hashlib
# import datetime
#
# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_colwidth', 100)
# pd.set_option('display.expand_frame_rep', False)
#
# # 配置数据库信息
# mongo_client = pymongo.MongoClient('localhost', 27017)
# db = mongo_client['FOR_MD5']
# my_collection = db['md5']
#
# pd_info = pd.read_excel('C:/Users/Administrator/Desktop/每日数据/20190127/total.xls')
# act_list = pd_info['act'].tolist()
# for act in act_list:
#     md5 = hashlib.md5(act.encode('utf-8')).hexdigest()
#     create_date = datetime.datetime.now()
#     my_collection.insert({'md5':md5,'create_date':create_date})

# # 数据md5去重
# pd_total = pd.read_excel('C:/Users/Administrator/Desktop/每日数据/20190127/total.xls')
# # pd_a = pd.read_excel('C:/Users/Administrator/Desktop/每日数据/20190128/total.xls')
# pd_a = pd.read_excel('C:/Users/Administrator/Desktop/meizhuang.xls')
# byte_act = [hashlib.md5(i.encode('utf-8')).hexdigest() for i in pd_a['act']]
# ser_act = pd.Series(byte_act)
# pd_a['md5'] = ser_act
# byte_act_total = [hashlib.md5(i.encode('utf-8')).hexdigest() for i in pd_total['act']]
# info_list = []
# for j in byte_act:
#     if j not in byte_act_total:
#         info_list.append([j])
# b = pd.DataFrame(info_list,columns=['md5'])
# c = pd.merge(b,pd_a,on='md5',how='inner')
# d = c.sort_values(by='type',ascending=True)
# d.to_excel('C:/Users/Administrator/Desktop/2019-1-28美妆折扣信息.xls',index=False)

# #什么值得买折扣数据分析
# startTime = time.time()
# zm = pd.read_excel('D:/数据与书籍备份/什么值得买服装美妆折扣数据.xls')
# zm = zm.dropna(how='all',subset=['标题','简介','活动','详情页链接','购买链接','来源','发布时间'])
# zm = zm.fillna(0)
# zm[['收藏数','评论数']] = zm[['收藏数','评论数']].astype('int')
# zm = zm.reset_index(drop=True)
# # 对标题用jieba分词进行分词
# title = zm['标题'].values.tolist()
# title_s = []
# for i in title:
#     title_cut = jieba.lcut(i)
#     title_s.append(title_cut)
#
# # 导入停用词表
# stopwords = pd.read_csv('D:/stopwords.txt', sep='\t', quoting=3, names=['stopword'])
# stopwords = stopwords.stopword.values.tolist()
#
# # 剔除停用词
# title_clean = []
# for line in title_s:
#     line_clean = []
#     for word in line:
#         if word not in stopwords:
#             line_clean.append(word)
#     title_clean.append(line_clean)
# print(title_clean)
#
# # 对title_clean进行去重
# title_clean_dist = []
# for line in title_clean:
#     line_dist = []
#     for word in line:
#         if word not in line_dist:
#             line_dist.append(word)
#     title_clean_dist.append(line_dist)
# print(title_clean_dist)
#
# # 将title_clean_dist转化为一个list
# allwords_clean_dist = []
# for line in title_clean_dist:
#     for word in line:
#         allwords_clean_dist.append(word)
# df_allwords_clean_dist = pd.DataFrame({'allwords':allwords_clean_dist})
# word_count = df_allwords_clean_dist.allwords.value_counts().reset_index()
# word_count = word_count.drop(index=0).reset_index(drop=True)
# word_count.columns = ['word', 'counts']

# # 词云可视化
# plt.figure(figsize=(20,10))
# pic = imread("C:/Users/Administrator/Desktop/111.jpg")
# w_c = WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',
#                 background_color='white',
#                 mask=pic, max_font_size=60, margin=1)
# wc = w_c.fit_words({x[0]: x[1] for x in word_count.head(100).values})
# # wc.to_file('C:/Users/Administrator/Desktop/wordcloud.png')
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.show()

# # 对每个词汇
# w_s_sum = []
# for w in word_count.word:
#     i = 0
#     s_list = []
#     for t in title_clean_dist:
#         if w in t:
#             s_list.append(zm['收藏数'][i])
#         i+=1
#     w_s_sum.append(sum(s_list))
#
# word_count['w_s_sum'] = w_s_sum
# print(word_count)

# df_w_s_sum = pd.DataFrame({'w_s_sum':w_s_sum})
# df_word_sum = pd.concat([word_count,df_w_s_sum],axis=1,ignore_index=True)
# df_word_sum.columns = ['word','count','w_s_sum']
# print(df_word_sum)
# endTime = time.time()
# print('总计用时：%s' % (endTime-startTime))