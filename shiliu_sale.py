# _*_ coding:utf-8 _*_
from fake_useragent import UserAgent
import requests
from multiprocessing import Pool
from lxml import etree
import re,json,csv
import time,random,pymongo
from requests.packages.urllib3.exceptions import InsecureRequestWarning

ua = UserAgent()
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

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_parse(url):
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Cookie': 'imei=961961cb-450a-405d-82ef-a6d45adcac2f; vendor=STYLE-shiliupu',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': ua.random}
    response = requests.get(url,headers=header,proxies=proxies,verify=False)
    if response.status_code == 200:
        resp = response.json()
        cate_sec = resp['cate_sec']
        content_list = []
        for cate in cate_sec:
            bottom_list = cate['bottom_items']
            for bottom in bottom_list:
                item = {}
                item['category'] = bottom['title']
                if bottom['target_rule']['info_flow_rule'] is not None:
                    item['filter'] = bottom['target_rule']['info_flow_rule']['query_conds_v3']['filter']
                    content_list.append(item)
        return content_list


def parse(url,content_list):
    header = {'Accept-Encoding': 'gzip',
              'scenesubid': '0',
              'vendor': 'STYLE-shiliupu',
              'content-type': 'application/json',
              'User-Agent':ua.random,
              'Content-Length': '1256',
              'Connection': 'Keep-Alive'}
    info_list = []
    for content in content_list:
        datas = json.dumps({"filter":content['filter'],"page":{"limit":12,"page":"pn:1;l:12"},"sort":[]})
        try:
            response = requests.post(url, data=datas, headers=header, proxies=proxies, verify=False)
        except Exception as e:
            print(e)
        else:
            if response.status_code == 200:
                resp = response.json()
                skus_list = resp['skus']
                for skus in skus_list:
                    content['descrpt'] = skus['brand']['descrpt']
                    content['brand_name'] = skus['brand']['name']
                    content['jianjie'] = skus['name']
                    content['price'] = skus['price2']['value_display']
                    save_content_list(content)
                    # info_list.append(content)
                time.sleep(0.3)
        for i in range(1,10):
            next_datas = json.dumps({"filter":content['filter'],"page":{"page":"o:{};l:12".format(12*i),"limit":12},"sort":[]})
            try:
                response2 = requests.post(url, data=next_datas, headers=header, proxies=proxies, verify=False)
            except Exception as e:
                print(e)
            else:
                if response2.status_code == 200:
                    resp = response2.json()
                    skus_list = resp['skus']
                    for skus in skus_list:
                        content['descrpt'] = skus['brand']['descrpt']
                        content['brand_name'] = skus['brand']['name']
                        content['jianjie'] = skus['name']
                        content['price'] = skus['price2']['value_display']
                        save_content_list(content)
                        # info_list.append(content)
                    time.sleep(0.3)
    # return info_list


def save_content_list(result):
    with open('C:/Users/Administrator/Desktop/info1.csv', 'a',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['category','filter','descrpt','brand_name','jianjie','price'])
        # writer.writeheader()
        writer.writerow(result)
        print('保存成功',result)


if __name__ == '__main__':
    content_list = get_parse('https://api.ilovelook.cn/api/conds/list/cate?code=shiliupu&shop_code=shiliupu')
    parse('https://api.ilovelook.cn/api/search/v3/goods?code=shiliupu&shop_code=shiliupu&is_input_by_hands=false&is_history=false&is_recommend=false&is_hot=false&search_source=Feed&search_location=&session_id=',content_list)
