import requests

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HU6889T40CE4668D"
proxyPass = "6252BEF79EEE8C81"

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

url_list = ['http://www.helenarubinstein.cn/','https://www.lancome.com.cn/','https://www.dior.cn/zh_cn','http://www.guerlain.com.cn/','https://www.givenchy.com','https://www.chanel.cn/zh_CN/','http://www.hermes.cn','http://www.yuesai.com/','http://www.chantecaille.com.tw/','https://asia.christianlouboutin.com','http://www.admin286.com/','http://www.gellefreres.com/','https://www.whoo.com.cn/','http://www.sum37.cn/','http://www.hera.com/cn/zh/','http://www.ohui.com.cn/','http://www.coreana.cn/','https://www.esteelauder.com.cn/','https://china.elizabetharden.com/','https://www.lamer.com.cn','https://cn.fresh.com','https://www.lorealparis.com.cn/','https://www.clarins.com.cn/','http://www.larocheposay.com.cn','https://cn.caudalie.com/','https://www.loccitane.cn/','http://www.eau-thermale-avene.cn/','https://www.yslbeautycn.com/','http://www.sulwhasoo.com/cn/zh/','http://www.lidezi.com/','https://www.innisfree.cn/','https://www.maccosmetics.com.cn/','https://www.clinique.com.cn/','http://www.kiehls.com.cn/','https://www.origins.com.cn/','https://www.benefitcosmetics.com/cn/zh-hans','https://www.skii.com.cn/sc/index.aspx','https://www.cledepeau-beaute.com.cn/','http://sekkisei.kose.com.cn/','http://www.hadalabo.com.cn/','http://www.giorgioarmanibeauty.cn/','https://www.jomalone.com.cn/']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
for url in url_list:
    response = requests.get(url,headers=headers,proxies=proxies,verify=False)
    try:
        last_modified = response.headers['Last-Modified']
    except Exception as e:
        print(url)
        with open('no_time_url.txt', 'a', encoding='utf-8') as f:
            f.write(url)
            f.write('","')
    else:
        print(last_modified)
        with open('last_modify.txt', 'a', encoding='utf-8') as f:
            f.write(last_modified)
            f.write('","')
        with open('yes_url.txt', 'a', encoding='utf-8') as f:
            f.write(url)
            f.write('","')