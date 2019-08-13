# _*_ coding:utf-8 _*_
from fake_useragent import UserAgent
import pandas as pd
import requests
from multiprocessing import Pool
from lxml import etree
import re,csv,json
import time,random,pymongo
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Tmspider():
    def __init__(self):
        # self.start_url = 'https://list.tmall.com/search_product.htm?q={}&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton'
        self.start_url = 'https://list.tmall.com/search_product.htm?q={}&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&xl=lankou_1&from=mallfp..pc_1_suggest'
        self.headers = {'User-Agent': ua.random,
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'max-age=0',
'cookie': 'cna=r5cTFAVzS0gCAXFo2mWr3FNi; hng=CN%7Czh-CN%7CCNY%7C156; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; lid=%E5%A5%BD%E7%9A%84%E4%BA%8B%E6%83%85lv; enc=klOKw54k8ButfrUt0DuC6J6aNbSTz8yx9UAA6kkMjWjwChgxck%2BsR06TnFz%2BpivjZsjCR71gfwg3H9zrJ19u1A%3D%3D; UM_distinctid=1661a67e726629-01f85f9dd7c21d-37664109-1fa400-1661a67e7271df; _med=dw:1920&dh:1080&pw:1920&ph:1080&ist:0; _uab_collina=154209327660758908445506; sm4=440300; uss=""; OZ_1U_2061=vid=vb8e6a76f64b9a.0&ctime=1543566723&ltime=1543566722; cq=ccp%3D1; _m_h5_tk=ef8bc60e2a5044b3e1c64efab556ec09_1545628994697; _m_h5_tk_enc=dfb527562cc438078d91ee37b006aab5; t=2729faefaec453f12677acb9bf00eeb1; uc3=vt3=F8dByRzDqQwxrbB39NU%3D&id2=UUpjPoFqdvstWg%3D%3D&nk2=2WNpQCKoNcledQ%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=%5Cu597D%5Cu7684%5Cu4E8B%5Cu60C5lv; lgc=%5Cu597D%5Cu7684%5Cu4E8B%5Cu60C5lv; _tb_token_=770e5783733e5; cookie2=16646a8bec2048a1014b0a59094159d5; tt=tmall-main; swfstore=219995; res=scroll%3A1903*5850-client%3A1903*943-offset%3A1903*5850-screen%3A1920*1080; pnm_cku822=098%23E1hvUpvUvbpvUvCkvvvvvjiPR259QjtnPLMysjrCPmP9gjYVR2dWtjE2RLqvAjDCiQhvCvvv9UUtvpvhvvvvvvhCvvOvCvvvphvEvpCWhR7LvvakfwLyaX7xfvc6gnFpV1O0747B9Wma%2BoHoDO2yT2eAnhjEKOmD5dUfb5cQD76OdegmDfea6LoNwZ29gW2IVBDsBq2XS4ZAh8yCvv9vvUmsuOLwbIyCvvOUvvVvayTtvpvIvvvvvhCvvvvvvUnvphvWS9vv96CvpC29vvm2phCvhhvvvUnvphvppvGCvvpvvPMM; l=aBthMdfJyFZ7oJBpBMaJeXu4I7076Y5PskFF1MaktTEhNPW0iFgJoKno-VwWj_qC5JFy_K-5F; isg=BNLSjWpv2k4mVSEdZTSoIZJEI5h0S9RIR6nQvpwr-gVwr3KphHHVjTjNG0s2304V',
'referer': 'https://www.tmall.com/',
'upgrade-insecure-requests': '1'}

    def parse(self, url):
        # s.keep_alive = False
        # s.adapters.DEFAULT_RETRIES = 5
        try:
            response = requests.get(url, headers=self.headers, verify=False)
        except Exception as e:
            print(e)
            self.parse(url)
        else:
            return response.content.decode('gbk')

    def get_content_info(self, response):
        html = etree.HTML(response)
        div_list = html.xpath("//div[@class='product  ']")[:15]
        content_list = []
        for div in div_list:
            item = {}
            # item['title'] = div.xpath(".//p[@class='productTitle']/a/")[0]
            goods_url = div.xpath(".//p[@class='productTitle']/a/@href")
            if len(goods_url) == 0:
                goods_url = div.xpath(".//div[@class='productImg-wrap']/a/@href")
            item['pro_website'] = 'https:' + goods_url[0]
            pro_pic = div.xpath(".//div[@class='productImg-wrap']/a/img/@src")
            if len(pro_pic) == 0:
                pro_pic = div.xpath(".//div[@class='productImg-wrap']/a/img/@data-ks-lazyload")
            item['pro_pic'] = 'https'+ pro_pic[0]
            item['pro_price_new'] = div.xpath(".//p[@class='productPrice']/em/text()")[0] if len(div.xpath(".//p[@class='productPrice']/em/text()"))>0 else None
            # item['shop_name'] = div.xpath(".//p[@class='productStatus']/span[3]/@data-nick")[0] if len(div.xpath(".//p[@class='productStatus']/span[3]/@data-nick"))>0 else None
            # if item['shop_name'] is None:
            #     data = div.xpath(".//a[@class='productShop-name']")[0]
            #     item['shop_name'] = data.xpath("string(.)").strip()
            # item['sale_count'] = div.xpath(".//p[@class='productStatus']/span[1]/em/text()")[0] if len(div.xpath(".//p[@class='productStatus']/span[1]/descendant-or-self::*/text()"))>0 else None
            # item['comment_count'] = div.xpath(".//p[@class='productStatus']/span[2]/a/text()")[0] if len(div.xpath(".//p[@class='productStatus']/span[2]/descendant-or-self::*/text()"))>0 else None
            content_list.append(item)
        return content_list

    def get_detail_info(self, detail_rsp, content, info_list):
        html = etree.HTML(detail_rsp)
        content['pro_title'] = html.xpath("//div[@class='tb-detail-hd']/h1/text()")[0].strip() if len(html.xpath("//div[@class='tb-detail-hd']/h1/text()"))>0 else None
        # content['fu_title'] = html.xpath("//div[@class='tb-detail-hd']/p/text()")[0].strip() if len(html.xpath("//div[@class='tb-detail-hd']/p/text()"))>0 else None
        try:
            content['pro_price_old'] = re.findall(r'defaultItemPrice":"(\d+\.\d+)",', detail_rsp)[0]
        except Exception as e:
            print(e)
        finally:
            # print(content)
            info_list.append(content)
            # return info_list

    def run(self):
        datas = pd.read_excel('C:/Users/Administrator/Desktop/new_info.xls')
        a = datas.loc[datas['source'] == 'tm']
        keywords = a['brand'].values.tolist()
        p = Pool(processes=3)
        for keyword in keywords:
            url = self.start_url.format(keyword)
            table = []
            info_list = []
            response = self.parse(url)
            content_list = self.get_content_info(response)
            for content in content_list:
                # time.sleep('%.2f' % random.random())
                detail_rsp = p.apply_async(self.parse, args=(content['pro_website'],))
                detail_rsp = detail_rsp.get()
                self.get_detail_info(str(detail_rsp), content, info_list)
            content_item = {}
            content_item['pro_list'] = json.dumps(info_list,ensure_ascii=False)
            content_item['brand'] = keyword
            print(content_item)
            table.append(content_item)
            for info in table:
                with open('C:/Users/Administrator/Desktop/info1.csv', 'a', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['pro_list', 'brand'])
                    writer.writerow(info)
        p.close()
        p.join()


if __name__ == '__main__':
    ua = UserAgent()
    tmspider = Tmspider()
    tmspider.run()