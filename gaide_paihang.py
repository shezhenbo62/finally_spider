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
header = {'User-Agent': ua.random,
              'Content-Type': 'application/json; charset=UTF-8',
'Connection': 'Keep-Alive',
'Accept-Encoding': 'gzip'}


def parse(url):
    datas = json.dumps({"rootCategoryId": "14606179869901389369"})
    response = requests.post(url, data=datas, headers=header, proxies=proxies, verify=False)
    if response.status_code == 200:
        resp =  response.json()
        info_list = resp['data']['rootCategory']['categories']
        content_list = []
        for info in info_list:
            name = info['name']
            for content in info['categories']:
                item = {}
                item['big_category'] = name
                item['categorys'] = content['categoryId']
                item['s_category'] = content['name']
                content_list.append(item)
        return content_list


def get_detail_info(url,content_list):
    for content in content_list:
        datas = json.dumps({"categoryId": content['categorys'], "rankingId": ""})
        try:
            response = requests.post(url, data=datas, headers=header, proxies=proxies, verify=False)
        except Exception as e:
            print(e)
        else:
            if response.status_code == 200:
                resp = response.json()
                info_list = resp['data']['globalPage']['rankingGlobals']
                for info in info_list:
                    content['country'] = info['brand']['country']
                    content['brand_name'] = info['brand']['name']
                    content['comment'] = info['comment']
                    content['grade'] = info['score']
                    save_content_list(content)
                    # print(content)
                time.sleep(0.2)


def save_content_list(result):
    with open('C:/Users/Administrator/Desktop/info1.csv', 'a',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['big_category','categorys','s_category','country','brand_name','comment','grade'])
        # writer.writeheader()
        writer.writerow(result)
        print('保存成功',result)


if __name__ == '__main__':
    content_list = parse('https://zone.guiderank-app.com/guiderank-web/app/ranking/getRootCategoryById.do?token=&ver=android_3.3.3&role=1&model=MuMu&imei=008796755195077 ')
    get_detail_info('https://zone.guiderank-app.com/guiderank-web/app/ranking/getRankingGlobalPage.do?token=&ver=android_3.3.3&role=1&model=MuMu&imei=008796755195077',content_list)