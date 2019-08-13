# import pymysql
#
# # 打开数据库连接
# db = pymysql.connect(host='47.107.224.21',user='picture',password='W2sXj6nMFcjiir6Z',db='picture',port=3306)
#
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
#
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")
#
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
#
# print("Database version : %s " % data)
#
# # 关闭数据库连接
# db.close()

# import pandas as pd
#
# pd_name = pd.read_csv('C:/Users/Administrator/Desktop/img_shibie_result.csv',names=['brand_name','img_name','activity'])
# pd_tm = pd.read_csv('C:/Users/Administrator/Desktop/img_huodong.csv',names=['brand_name','url'])
# data = pd.merge(pd_name,pd_tm,how='left',on=['brand_name'])
# data.to_excel('C:/Users/Administrator/Desktop/activity.xls',index=False)

# # 网易考拉品牌爬虫
# from selenium import webdriver
# import csv
#
# driver = webdriver.Chrome()
# url = 'http://www.sasa.com/brand'
# driver.get(url)
# li_list = driver.find_elements_by_xpath("//div[@id='bitemslist']/dl/dd/a")
# print(li_list)
# for li in li_list:
#     item = {}
#     item['brand_name'] = li.find_element_by_xpath("./div").text.strip()
#     item['leibie'] = '美妆'
#     item['website'] = 'sasa'
#     # print(item)
#     with open('C:/Users/Administrator/Desktop/haitao_name.csv','a',encoding='utf-8') as f:
#         writer = csv.DictWriter(f,fieldnames=['brand_name','leibie','website'])
#         writer.writerow(item)
# driver.quit()

# 天猫品牌爬虫
# import requests
# from fake_useragent import UserAgent
# import re
#
# ua = UserAgent()
# headers = {'accept': '*/*',
# 'accept-encoding': 'gzip, deflate, br',
# 'accept-language': 'zh-CN,zh;q=0.9',
# 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
# 'cookie': 'cna=r5cTFAVzS0gCAXFo2mWr3FNi; hng=CN%7Czh-CN%7CCNY%7C156; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; lid=%E5%A5%BD%E7%9A%84%E4%BA%8B%E6%83%85lv; enc=klOKw54k8ButfrUt0DuC6J6aNbSTz8yx9UAA6kkMjWjwChgxck%2BsR06TnFz%2BpivjZsjCR71gfwg3H9zrJ19u1A%3D%3D; UM_distinctid=1661a67e726629-01f85f9dd7c21d-37664109-1fa400-1661a67e7271df; _med=dw:1920&dh:1080&pw:1920&ph:1080&ist:0; _uab_collina=154209327660758908445506; sm4=440300; csa=undefined; uss=""; OZ_1U_2061=vid=vb8e6a76f64b9a.0&ctime=1543566723&ltime=1543566722; cq=ccp%3D1; t=2729faefaec453f12677acb9bf00eeb1; uc3=vt3=F8dByR1X7TGPjuL%2FOxY%3D&id2=UUpjPoFqdvstWg%3D%3D&nk2=2WNpQCKoNcledQ%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=%5Cu597D%5Cu7684%5Cu4E8B%5Cu60C5lv; lgc=%5Cu597D%5Cu7684%5Cu4E8B%5Cu60C5lv; _tb_token_=5631e183638ee; cookie2=16dfe77a977f788f0a278cbc6216135a; tt=food.tmall.com; swfstore=98535; _m_h5_tk=68eb25bbdf31159a07140f2c26613841_1543897709828; _m_h5_tk_enc=b082730613ea74cd6976353a1ca380c7; res=scroll%3A1903*5559-client%3A1903*505-offset%3A1903*5559-screen%3A1920*1080; pnm_cku822=098%23E1hvmvvUvbpvUvCkvvvvvjiPR2M9gjE2R2MO0jEUPmPWtjtRR2M9sjEvPL5h0j3WRphvCvvvphvPvpvhvv2MMQhCvvOvChCvvvmtvpvIvvCvpvvvvvvvvhNjvvmvMvvvBGwvvvUwvvCj1Qvvv99vvhNjvvvmmUyCvvOCvhE20RmivpvUvvCCEr5fgs%2BEvpCW9ayI8CzZHFKzrmphQRA1%2BbeAOHjpT2eARdIAcUmD5d8rVC63D76Xd3w0EZKa6LoNetDto%2FFheBQOVVQ4S4ZAhCkaU6bnDBmOe36AxTwCvvpvvhHh; isg=BE5OEyXBnry1JC0RAahsFQ4QnyTQZxD5a93csniX8dEM2-814FqK2U7dF0cSQwrh',
# 'referer': 'https://list.tmall.com/search_product.htm?spm=a223d.7797701.0.0.691b6d86yHCsHz&cat=54986001&acm=lb-zebra-25393-317299.1003.4.445133&scm=1003.4.lb-zebra-25393-317299.OTHER_14427356591985_445133',
# 'user-agent': ua.random,
# 'x-requested-with': 'XMLHttpRequest'}
#
# url = 'https://list.tmall.com/ajax/allBrandShowForGaiBan.htm?t=0&cat=54986001&sort=s&style=g&active=1&industryCatId=54986001&spm=a223d.7797701.0.0.691b6d86yHCsHz&smAreaId=440300&userIDNum=2228914394&tracknick=%BA%C3%B5%C4%CA%C2%C7%E9lv'
# resp = requests.get(url,headers=headers).text
# brand_name_list = re.findall(r'"title":"(.*?)",',resp)
# print(brand_name_list)
# for i in brand_name_list:
#     with open('C:/Users/Administrator/Desktop/tm.csv', 'a', encoding='utf-8') as f:
#         f.write(i)
#         f.write('\r\n')

# 屈层氏品牌爬虫
# import requests
# from fake_useragent import UserAgent
# from lxml import etree
# import pandas as pd
#
# ua = UserAgent()
# headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'accept-encoding': 'gzip, deflate, br',
# 'accept-language': 'zh-CN,zh;q=0.9',
# 'cache-control': 'max-age=0',
# 'cookie': 'JSESSIONID=505D5872818D23DB73804848B25FBC93.whkpfa08; lang=zt; deliveryRegion=hk; gaUserId=769a914b-db57-4bd2-aa5c-1dbefbd51891; _ga=GA1.3.39669124.1543907965; _gid=GA1.3.825010517.1543907965; QueueITAccepted-SDFrts345E-V3_watsonprdhk=EventId%3Dwatsonprdhk%26QueueId%3D2dba8bfc-2540-4c51-ab62-90e6ab6c1b9a%26RedirectType%3Dsafetynet%26IssueTime%3D1543907965%26Hash%3D8a51b8930f1a11b390d1f2df60ad5d8ff462487549ab7e649be5debddf83cef7; _dy_csc_ses=t; _dy_c_exps=; _dycnst=dg; Hm_lvt_1ca6603f12694b02f66a742bf721814a=1543907968; _dyid=792634012696156904; _dyjsession=3aebfd61ed40b6cecedc3689670d3f56; _dy_geo=CN.AS.CN_30.CN_30_Shenzhen; _dy_df_geo=China..Shenzhen; _dy_c_att_exps=; _dy_cs_purchase=true; _hjIncludedInSample=1; _hjShownFeedbackMessage=true; showPopupOnMyBacketPage=null; _gat_UA-24603442-2=1; _gat=1; _dy_toffset=0; _dy_ses_load_seq=64863%3A1543908931092; _dy_soct=300515.472675.1543908931*291344.454706.1543908931; _dycst=dk.w.c.ws.frv5.tos.ah.; _dyus_8769633=89%7C12%7C0%7C0%7C0%7C0.0.1543907969176.1543908931368.962.0%7C337%7C49%7C11%7C118%7C33%7C0%7C0%7C0%7C0%7C0%7C0%7C33%7C0%7C0%7C0%7C0%7C0%7C33%7C0%7C0%7C0%7C0%7C0; Hm_lpvt_1ca6603f12694b02f66a742bf721814a=1543908934',
# 'referer': 'https://www.watsons.com.hk/All-Category/c/040000?categoryCode=040000',
# 'upgrade-insecure-requests': '1',
# 'user-agent': ua.random}
#
# url = 'https://www.watsons.com.hk/All-Category/c/060000'
# resp = requests.get(url,headers=headers).content.decode()
# html = etree.HTML(resp)
# div_list = html.xpath("//div[@class='all-brand-list']/div")
# content_list = []
# for div in div_list:
#     brand_name = div.xpath("./a/text()")
#     content_list.append(brand_name)
# print(content_list)
# pd_name = pd.DataFrame(content_list)
# pd_name.to_excel("C:/Users/Administrator/Desktop/watson_muying.xls")


# # cultbeauty美妆优惠信息爬虫
# import requests
# from fake_useragent import UserAgent
# from lxml import etree
# import csv
#
# ua = UserAgent()
# headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding': 'gzip, deflate,br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'cache-control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Cookie': '_gcl_au=1.1.2082953080.1544686901; _vwo_uuid_v2=D987D0DE5CE10EA9935E24C4E78546F72|f4b58bf254c667c875d02e99b3b6735a; rmStore=amid:35269; cbar_uid=6383990116485; SLIBeacon=s0ohpgg74p15446869039900ekb25oe; SLIBeacon_926549584=s0ohpgg74p15446869039900ekb25oe; _ga=GA1.3.1028523145.1544686904; cbar_static={}; csrf=f96cb956f4aa9f; tsid=jqenhjpi-230a6d6faca8e3; msid=201901020357148def8395245f7825cf14393959777b43; _gid=GA1.3.1497177824.1546401439; cbar_cart_checksum=0.00; stc111573=env:1546416892%7C20190202081452%7C20190102084452%7C1%7C1013747:20200102081452|uid:1544686902178.673208193.8630552.111573.993368017.1:20200102081452|srchist:1013747%3A1546416892%3A20190202081452:20200102081452|tsa:1546416892612.1076345402.579764.6865079632747668.3:20190102084452; _gat_UA-4554279-3=1; _dc_gtm_UA-4554279-3=1; _dc_gtm_UA-4554279-5=1; cbar_lvt=1546416893; cbar_sess=4; cbar_sess_pv=2; _cmkcke=%7B%22i%22%3A%7B%22v%22%3A%22r.1546416892926%22%2C%22vpg%22%3A11%7D%2C%22cg_325%22%3A%7B%22c%22%3A2%2C%22ir%22%3A%22y%22%2C%22ir_dt%22%3A1546401441448%2C%22cl%22%3A%22y%22%2C%22cl_dt%22%3A1546401442687%7D%7D; _gat_UA-4554279-5=1; bm_sv=362F3985DEE64058BDB012ACE721D85A~GnrZn62p5GUWD9pzbxZ3P3pd4TRf+0RmmQBxDeNP+P9DworJ1a1R1qrD00GUZj4z8i+D0r3ro7tJJfFf9i7uqBa9kYZ1k6usMwRtUt/ATiWx/CWenxvS/yUiSg/dPmisVBn1WBqPkyCIqaP5ftuuxhD60kCf8bJWlZZ67NdZctQ=; _gat_baritracker=1; ak_bmsc=7482CFBEB2E7BB4BA1AA9BF1149505A217236ED560030000FA722C5CEE6D7B7A~plk6DPT1YSV7ms85FQPFwfGwJISfVbqlojzzfwKT0Ldsw7DQZhGWK9MUEgx3Z4zj3sBlJfUfdprsR17oVNaOZIDCaKGeSplGsSrFpb0EiPiXNpQwdDjKja+5gaV062mHthNuBx15YF0iltNS1RfCDq7B08Ldyz9ukwExBg5k2OFfwBc1fLBl4mzc0jqdqO3IbmSjuliOZ6O1e+MssWe66mnkK2qkIC1/sGI6Ojy7Unx7IchUmLx0bmw+fh08pkYeUu',
# 'Referer': 'https://www.cultbeauty.co.uk/',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': ua.random}
#
# url = 'https://www.cultbeauty.co.uk/sale.html?q=sale'
# resp = requests.get(url,headers=headers).text
# html = etree.HTML(resp)
# li_list = html.xpath("//div[@class='refineListItem brand']/div[2]/div")
# print(li_list)
# for li in li_list:
#     item = {}
#     item['brand_name'] = li.xpath("./label/text()")[1]
#     item['act'] = 'sale降价'
#     item['website'] = 'https://www.cultbeauty.co.uk/sale.html?q=sale&brand='+li.xpath("./label/input/@value")[0]
#     print(item)
#     with open('C:/Users/Administrator/Desktop/haitao_name.csv','a',encoding='utf-8') as f:
#         writer = csv.DictWriter(f,fieldnames=['brand_name','act','website'])
#         writer.writerow(item)


# # perfumesclub美妆优惠信息爬虫
# import requests
# from fake_useragent import UserAgent
# from lxml import etree
# import csv
#
# ua = UserAgent()
# headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding': 'gzip, deflate,br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'cache-control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Cookie': 'bfd_tmd=4e22aa0debd9fbb98cad857e5e00736e.18077590.1544687610000; bfd_tma=4e22aa0debd9fbb98cad857e5e00736e.63467069.1544687610000; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167a68e6c44b7-0eba77686e0bdf-37664109-2073600-167a68e6c46322%22%2C%22%24device_id%22%3A%22167a68e6c44b7-0eba77686e0bdf-37664109-2073600-167a68e6c46322%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _uuid=EDDCFA67-48BD-4425-81AE-5A1FD8794037; _wtag=3.4.10813.4883.61910; CACHED_FRONT_FORM_KEY=x0yAc77oEOSJXFCg; bfd_sid=6b96f5029fb041fa06d6209326a5576b; bfd_tmc=4e22aa0debd9fbb98cad857e5e00736e.70401106.1546409824000; Hm_lvt_e7cc43bd698ffd9fa610ff64a984eb13=1544687611,1546409825; frontend=ac5fq49698brifo5v9gquana91; cart_item_count=0; Hm_lpvt_e7cc43bd698ffd9fa610ff64a984eb13=1546410101',
# 'Referer': 'https://www.perfumesclub.cn/?wtag=3.4.10813.4883.61910',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': ua.random}
#
# url = 'https://www.perfumesclub.cn/pt_catalog/brands'
# resp = requests.get(url,headers=headers).text
# html = etree.HTML(resp)
# li_list = html.xpath("//div[@id='a-z']//ul/li")
# print(li_list)
# for li in li_list:
#     item = {}
#     item['brand_name'] = li.xpath("./a/text()")[0].strip()
#     item['act'] = '最高80%OFF'
#     item['website'] = li.xpath("./a/@href")[0]
#     print(item)
#     with open('C:/Users/Administrator/Desktop/haitao_name.csv','a',encoding='utf-8') as f:
#         writer = csv.DictWriter(f,fieldnames=['brand_name','act','website'])
#         writer.writerow(item)

# # D88用户足迹数据爬虫
# import requests
# import json
# from fake_useragent import UserAgent
# import pandas as pd
#
# ua = UserAgent()
# headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding': 'gzip, deflate',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Cache-Control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Cookie': '943V1Q_think_language=zh-CN; PHPSESSID=nk8ugc9iu013nsf2pbe95lucj0',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': ua.random}
#
# url = 'http://192.168.2.52/index.php?s=/Portal/index/test.html'
# resp = requests.get(url,headers=headers).json()
# print(resp)
# content_list = []
# for i in resp['data']:
#     user_id = i['user_id']
#     for j in i['collection_list']:
#         user_type = 'collection'
#         weight = 4
#         collection_object_id = j['object_id']
#         collection_title = j['title']
#         content_list.append([user_id,user_type,weight,collection_object_id,collection_title])
#     for a in i['views_list']:
#         user_type = 'views'
#         weight = 1
#         views_object_id = a['object_id']
#         views_title = a['title']
#         content_list.append([user_id,user_type,weight,views_object_id,views_title])
#     for b in i['buy_list']:
#         user_type = 'buy'
#         weight = 2
#         buy_object_id = b['object_id']
#         buy_title = b['title']
#         content_list.append([user_id,user_type,weight, buy_object_id, buy_title])
#     for c in i['comments_list']:
#         user_type = 'comments'
#         weight = 3
#         comments_object_id = c['object_id']
#         comments_title = c['title']
#         content_list.append([user_id,user_type,weight, comments_object_id, comments_title])
#     if i['share_list']:
#         for d in i['share_list']:
#             user_type = 'share'
#             weight = 5
#             share_object_id = d['object_id']
#             share_title = d['title']
#             content_list.append([user_id,user_type,weight, share_object_id, share_title])
#
# data = pd.DataFrame(content_list)
# data.to_excel('C:/Users/Administrator/Desktop/user.xls',index=False,header=['user_id','action_type','weight','info_id','title'])

# import queue
#
# q = queue.Queue(3)
#
# for i in range(8):
#     q.put(i)
#     print('=======%d'%i)
#     if q.full():
#         a = q.get()
#         print('*******', a)
#
# while not q.empty():
#     print(q.get())

# import pandas as pd
#
# beauty_name = pd.read_excel("C:/Users/Administrator/Desktop/D88品牌库最终_本地.xlsx",sheet_name=[0],usecols=[1])
# brand_list = beauty_name[0]['品牌'].values.tolist()
# content_list = []
# for brand in brand_list:
#     brand_name = brand.split("/")[0]
#     content_list.append(brand_name)
# print(content_list)

# import pandas as pd
# import requests
# from lxml import etree
# from urllib import parse
#
# urls = ['http://www.shihuo.cn/digital/list?scene=%E6%89%8B%E6%9C%BA%E9%80%9A%E8%AE%AF#qk=category',
#         'http://www.shihuo.cn/digital/list?scene=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6#qk=category',
#         'http://www.shihuo.cn/digital/list?scene=%E7%94%B5%E8%84%91%E4%B8%BB%E6%9C%BA#qk=category',
#         'http://www.shihuo.cn/digital/list?scene=%E7%94%B5%E8%84%91%E5%A4%96%E8%AE%BE#qk=category',
#         'http://www.shihuo.cn/digital/list?scene=%E8%80%B3%E6%9C%BA%E9%9F%B3%E5%93%8D#qk=category',
#         'http://www.shihuo.cn/digital/list?scene=%E6%91%84%E5%BD%B1%E6%91%84%E5%83%8F#qk=category',
#         'http://www.shihuo.cn/digital/list?scene=%E6%99%BA%E8%83%BD%E7%A9%BF%E6%88%B4#qk=category']
#
# headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding': 'gzip, deflate',
# 'Accept-Language': 'h-CN,zh;q=0.9',
# 'Cache-Control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Cookie': '_cnzz_CV30020080=buzi_cookie%7C4fb6a6c4.db1c.0293.a293.745b8e5d154c%7C-1; _shcid=jzZRt1VUPFK5Xf9SmMJa; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221684b47fc95b6f-07ddfdd90df508-37664109-2073600-1684b47fc9729c%22%2C%22%24device_id%22%3A%221684b47fc95b6f-07ddfdd90df508-37664109-2073600-1684b47fc9729c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _dacevid3=4fb6a6c4.db1c.0293.a293.745b8e5d154c; _cnzz_CV30020080=buzi_cookie%7C4fb6a6c4.db1c.0293.a293.745b8e5d154c%7C-1; UM_distinctid=1684b47fcdf484-04a986b2f27963-37664109-1fa400-1684b47fce0202; CNZZDATA30089914=cnzz_eid%3D124261727-1547448989-%26ntime%3D1547448989; __dacevst=76fedfae.ad7b040b|1547454252042',
# 'Host': 'www.shihuo.cn',
# 'Referer': 'http://www.shihuo.cn/digital',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
#
# content_list = []
# for url in urls:
#     response = requests.get(url,headers=headers)
#     if response.status_code == 200:
#         resp = response.text
#         html = etree.HTML(resp)
#         li_list = html.xpath("//li[@class='clearfix brands']/span[2]/a")
#         for li in li_list:
#             name = li.xpath("./text()")[0]
#             category = url.split('=')[1].split('#')[0]
#             category = parse.unquote(category)
#             content_list.append([name,category])
# print(content_list)
# pd_name = pd.DataFrame(content_list,columns=['brand_name','category'])
# a = pd_name.drop_duplicates('brand_name','first')
# a.to_excel("C:/Users/Administrator/Desktop/识货品牌.xls",index=False,header=['品牌名','类别'])


# import pandas as pd
# import requests
# from lxml import etree
# from urllib import parse
#
# headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'accept-encoding': 'gzip, deflate, br',
# 'accept-language': 'zh-CN,zh;q=0.9',
# 'cache-control': 'max-age=0',
# 'cookie': 'pcsuv=1547111143083.a.10899959; mobileKeyWordNum=0; PClocation=%u6DF1%u5733; Hm_lvt_b1725235b21cd3427b36febf0e7fa0f9=1547453406; Hm_lpvt_b1725235b21cd3427b36febf0e7fa0f9=1547453406; JSESSIONID=abc6lKvNPSTXs-PCuAlHw; channel=1561; Hm_lvt_e8131f7005d33f838fef5c6351fec97b=1547453417; Hm_lpvt_e8131f7005d33f838fef5c6351fec97b=1547453417; _area_name_tag_=sz; pcuvdata=lastAccessTime=1547453420790|visits=2',
# 'referer': 'https://notebook.pconline.com.cn/',
# 'upgrade-insecure-requests': '1',
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
#
# url = 'https://product.pconline.com.cn/'
# content_list = []
# response = requests.get(url,headers=headers).content.decode('gbk')
# html = etree.HTML(response)
# li_list = html.xpath("//ul[@id='JcatsMenu']/li/a")
# for li in li_list:
#     category = li.xpath("./text()")[0]
#     cate_href = li.xpath("./@href")[0]
#     cate_href = parse.urljoin(url,cate_href)
#     resp = requests.get(cate_href,headers=headers)
#     html1 = etree.HTML(resp.text)
#     a_list = html1.xpath("//div[@id='tab-all']/div/a")
#     for a in a_list:
#         brand_name = a.xpath("./text()")[0]
#         content_list.append([brand_name,category])
# pd_name = pd.DataFrame(content_list,columns=['brand_name','category'])
# b = pd_name.drop_duplicates('brand_name','first')
# b.to_excel("C:/Users/Administrator/Desktop/太平洋品牌.xls",index=False,header=['品牌名','类别'])

# a = ['huawei/华为','apple/苹果','戴尔']
# b = ['华为','苹果','三星']
# for i in b:
#     for j in a:
#         if i in j:
#             print(j)

# import pandas as pd
# a = pd.read_excel("C:/Users/Administrator/Desktop/识货品牌.xls",names=['brand_name','category'])
# b = pd.read_excel("C:/Users/Administrator/Desktop/太平洋品牌.xls",names=['brand_name','category'])
# a_list = a.values.tolist()
# b_list = b.values.tolist()
# c_list = []
# for i in range(len(b_list)):
#     b_name = b_list[i][0]
#     for j in range(len(a_list)):
#         a_name = a_list[j][0]
#         if b_name in a_name:
#             c_list.append(b_list[i])
#             break
# c = pd.DataFrame(c_list,columns=['brand_name','category'])
# d = pd.concat([b,c])
# k = d.drop_duplicates('brand_name',False)
# j = pd.concat([k,a])
# j.to_excel("C:/Users/Administrator/Desktop/电子电脑品牌.xls",index=False)

# import pandas as pd
#
# pd_name = pd.read_csv('C:/Users/Administrator/Desktop/smzdm/zdm.brand_meizhuang.csv', names=['brand', 'img_url'])
# pd_dbb = pd.read_excel("C:/Users/Administrator/Desktop/D88品牌库整理版(2019.2.22).xlsx", sheet_name=[0], usecols=[1], names=['brand_name'])
# a = pd_name['brand'].str.lower()
# e = a.tolist()
# pd_list = []
# for k in e:
#     b_list = []
#     for g in str(k):
#         if not ('\u4e00' <= g <= '\u9fff' or g == '/'):
#             b_list.append(g)
#     pinpaia = ''.join(b_list)
#     pinpaia = pinpaia.strip()
#
#     if pinpaia == '':
#         pinpaia = k
#     pd_list.append([pinpaia])
# pd_pp = pd.DataFrame(pd_list,columns=['brand_name'])
# pd_name['brand_name'] = pd_pp['brand_name']
# pd_name = pd_name.drop(columns=['brand'])
# dbb = pd_dbb[0]['brand_name'].str.lower()
# d = dbb.tolist()
# pp_list = []
# for i in d:
#     a_list = []
#     for j in str(i):
#         if not ('\u4e00' <= j <= '\u9fff' or j == '/'):
#             a_list.append(j)
#     pinpai = ''.join(a_list)
#     pinpai = pinpai.strip()
#
#     if pinpai == '':
#         pinpai = i
#     pp_list.append([pinpai])
# pd_pp = pd.DataFrame(pp_list,columns=['brand_name'])
# result = pd.merge(pd_pp, pd_name, on=['brand_name'], how='left')
# result.to_excel("C:/Users/Administrator/Desktop/result.xls",index=False)

# 定时框架APScheduler
# from datetime import datetime
# import time
# import os
# from apscheduler.schedulers.background import BlockingScheduler
#
#
# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#
#
# if __name__ == '__main__':
#     scheduler = BlockingScheduler()
#     # 间隔3秒钟执行一次
#     scheduler.add_job(tick, 'cron', day_of_week='mon-fri',hour=14,minute=32,end_date='2019-12-31')
#     # scheduler.add_job(tick, 'cron', second='*/3')
#     # 这里的调度任务是独立的一个线程
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    # try:
    #     # 其他任务是独立的线程执行
    #     while True:
    #         time.sleep(2)
    #         print('sleep!')
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
    #     print('Exit The Job!')

# # 蜜伢母婴品牌爬虫
# import requests
# import pandas as pd
# from fake_useragent import UserAgent
# from lxml import etree
#
#
# def get_proxy():
#     return requests.get('http://119.23.203.63:6066/get/').content
#
#
# def get_page(url):
#     ua = UserAgent()
#     headers = {
#         'Connection': 'keep-alive',
#         'Cache-Control': 'max-age=0',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': ua.random,
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9'
#     }
#     proxy = get_proxy()
#     resp = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)}).content.decode('utf-8')
#     html_lxml = etree.HTML(resp)
#     a_list = html_lxml.xpath("//div[@class='colums']//a")
#     content_list = []
#     for a in a_list:
#         cate_name = a.xpath("./text()")[0]
#         website = a.xpath("./@href")[0]
#         # proxy1 = get_proxy()
#         resp_detial = requests.get(website, headers=headers).content.decode('utf-8')
#         html = etree.HTML(resp_detial)
#         ab_list = html.xpath("//div[@class='kcon k0']/a")
#         for i in ab_list:
#             brand_name = i.xpath("./text()")[0]
#             brand_url = i.xpath("./@href")[0]
#             print(brand_name, cate_name, brand_url)
#             content_list.append([brand_name, cate_name, brand_url])
#     pd_info = pd.DataFrame(content_list, columns=['brand_name', 'cate_name', 'url'])
#     pd_info = pd_info.drop_duplicates('brand_name', 'first')
#     pd_info.to_excel("C:/Users/Administrator/Desktop/miya_brand.xls", index=False)
#
#
# if __name__ == '__main__':
#     url = 'https://www.mia.com/'
#     get_page(url)

# from PIL import Image,ImageFilter
#
# im = Image.open('C:/Users/Administrator/Desktop/URIAGE2019-02-19-11_06_48__.png')
# im2 = im.filter(ImageFilter.BLUR)
# im2.save('C:/Users/Administrator/Desktop/blur.png')

# import requests
# from lxml import etree
# import pandas as pd
# from fake_useragent import UserAgent
#
# ua = UserAgent()
#
# headers = {
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'User-Agent': ua.random,
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Cache-Control': 'max-age=0',
#     'Upgrade-Insecure-Requests': '1',
#     'Connection': 'keep-alive',
#     'Host': 'www.chinasspp.com',
#     # 'Cookie': '__cfduid=d5ccc6eb48dde9a67724868bed28eabe81551684468; UM_distinctid=169479a09297e-04a8c78f32ed5b-37664109-1fa400-169479a092a548; yjs_id=e518fdb7429e032e6d4b643344e53e65; ctrl_time=1; CNZZDATA3998881=cnzz_eid%3D2035586720-1551684110-http%253A%252F%252Fwww.chinasspp.com%252F%26ntime%3D1551684110; ASP.NET_SessionId=mqkjit45epeaxti1bwxi2bb1; CNZZDATA538723=cnzz_eid%3D2111850012-1551679236-%26ntime%3D1551746409; CNZZDATA3858846=cnzz_eid%3D1139572510-1551679420-%26ntime%3D1551748287; Hm_lvt_61a43de5ea58c0258ca306ea55b66eba=1551684471,1551748792; Hm_lpvt_61a43de5ea58c0258ca306ea55b66eba=1551748792'
# }
#
# for i in range(1, 76):
#     url = 'http://www.chinasspp.com/brand/bsearch.aspx?cid=%BC%D2%BE%D3&tid=&area=&lid=&order=1&key=&page={}'.format(i)
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         resp = response.content.decode('gbk')
#         html = etree.HTML(resp)
#         div_list = html.xpath("//div[@class='brand']")
#         content_list = []
#         for div in div_list:
#             brand_name = div.xpath("./a/@title")[0] if len(div.xpath("./a/@title")) > 0 else None
#             logo_url = div.xpath("./a/img/@src")[0] if len(div.xpath("./a/img/@src")) > 0 else None
#             popularity = div.xpath("./p[@class='last']/i/text()")[0]\
#                 if len(div.xpath("./p[@class='last']/i/text()")) > 0 else None
#             content_list.append([brand_name, logo_url, popularity])
#             print(brand_name)
#         pd_brand = pd.DataFrame(content_list, columns=['brand_name', 'logo_url', 'popularity'])
#         pd_brand.to_csv("C:/Users/Administrator/Desktop/家居品牌.csv", index=False, header=None, mode='a')

# from itertools import product
# a = [6518, 6152, 123]
# b = list(range(10))
# arrays = [a, b]
# c = list(product(*arrays))
# a = ['https://cn.pharmacyonline.com.au/queryapi/lists?page={0[1]}&cid={0[0]}&sort=top'.format(i) for i in c]
# print(a)


# import redis
# import random
#
#
# def get_proxy():
#     rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
#     data = rediscli.hgetall('useful_proxy')
#     proxies = ["http://{}".format(proxy.decode()) for proxy in data]
#     return random.choice(proxies)


# # coding:utf-8
#
# import random
# import requests
# import pandas as pd
# import pymongo
#
#
# def read_info():
#     data = pd.read_excel('D:/fidder/request.xls')
#     ua = pd.read_excel('D:/fidder/ua_string.xls')
#     data = data.dropna(how='all')
#     data = data.reset_index()
#     data = data.drop(columns=['index', 'higo2'])
#     return data.values.tolist(), ua.values.tolist()
#
#
# def parse(data, ua_list):
#     num = len(data)//7
#     image_list = []
#     for i in range(num):
#         ua = random.choice(ua_list)[0]
#         headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#                    'Accept-Encoding': 'gzip, deflate',
#                    'Accept-Language': 'zh-CN,zh;q=0.9',
#                    'Cache-Control': 'max-age=0',
#                    'Connection': 'keep-alive',
#                    'Host': 'v.lehe.com',
#                    'Upgrade-Insecure-Requests': '1',
#                    'User-Agent': ua}
#         split_list = data[i * 7][0].split(' ')
#         url = 'http://v.lehe.com'+split_list[1]
#         resp = requests.get(url, headers=headers).json()
#         brand_name = resp.get('data').get('brand_info').get('name')
#         img_list = resp.get('data').get('goods_image')
#         for img in img_list:
#             print(brand_name, img.get('image_original'))
#             image_list.append([brand_name, img.get('image_original')])
#         df = pd.DataFrame(image_list, columns=['brand_name', 'img_url'])
#         df.to_excel("C:/Users/Administrator/Desktop/img_url.xls", index=False)
#
#
# def save_to_mongodb(item):
#     try:
#         if db[MONGO_TABLE].insert(item):
#             print('存储到mongodb成功', item)
#     except Exception:
#         print('存储到mongodb失败', item)
#
#
# if __name__ == '__main__':
#     MONGO_URL = 'localhost'
#     MONGO_DB = 'brand_story'
#     MONGO_TABLE = 'higo'
#     client = pymongo.MongoClient(MONGO_URL)
#     db = client[MONGO_DB]
#     data, ua_list = read_info()
#     parse(data, ua_list)

import datetime

create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(create_time)


# import happybase
#
# con = happybase.Connection()
# table = con.table('kaolainfo')
# # 全局查询
# for key, value in table.scan():
#     print(value)
# # 插入数据
# table.put('muying',{'data:brand': '爱他美', 'data:shop': '网易考拉自营', 'data:title': 'Aptamil 爱他美 德国 配方婴幼儿奶粉'})

# import re
#
# stringA = 'fteru--255.168.1.1%++'
# a = re.findall(r'([0-2][0-9]{2}\.[0-2][0-9]{2}\.\d\.\d)', stringA)
# print(a)
