from selenium import webdriver
import string
import zipfile
import time
import json
import re
import pymongo
from fake_useragent import UserAgent

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HU6889T40CE4668D"
proxyPass = "6252BEF79EEE8C81"

MONGO_URL = 'localhost'
MONGO_DB = 'd88_info'
MONGO_TABLE = 'qiaokeli'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
ua = UserAgent()


class Suning(object):
    # 初始化时，传递要查询的关键词
    def __init__(self, keyword):
        self.keyword = keyword

    def suning(self):
        option = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        option.add_argument('user-agent="{}"'.format(ua.random))
        # option.add_argument("--start-maximized")
        # option.add_argument('--headless')
        # option.add_extension(proxy_auth_plugin_path)
        # option.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(chrome_options=option)
        driver.get('http://jd.com')

        search_input = driver.find_element_by_id('key')
        search_input.send_keys(keyword)
        time.sleep(2)
        search_btn = driver.find_element_by_class_name('button')
        search_btn.click()
        time.sleep(2)
        # file_handle = open('%s.json' % self.keyword, 'w', encoding='utf-8')
        for x in range(1,23):
            # 将滚动条移动到页面的底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            print('正在爬取第%s页数据......' % x)
            shops = driver.find_elements_by_xpath("//ul[@class='gl-warp clearfix']/li")
            goods_url_list = []
            for shop in shops:
                item = {}
                item['title'] = shop.find_element_by_xpath(".//div[@class='p-name p-name-type-2']/a/em/descendant-or-self::*").text
                item['goods_url'] = shop.find_element_by_xpath(".//div[@class='p-name p-name-type-2']/a").get_attribute('href')
                item['activity'] = shop.find_element_by_xpath(".//div[@class='p-icons']/descendant-or-self::*").text
                item['price'] = shop.find_element_by_xpath(".//div[@class='p-price']/strong/descendant-or-self::*").text
                item['comment_count'] = shop.find_element_by_xpath(".//div[@class='p-commit']/strong/a").text
                goods_url_list.append(item['goods_url'])
                try:
                    item['shop_name'] = shop.find_element_by_xpath(".//div[@class='p-shop']/span/a").text
                except Exception as e:
                    self.save_mongodb(item)
                else:
                    self.save_mongodb(item)

            next = driver.find_element_by_class_name('pn-next')
            # next=driver.find_element_by_link_text('下一页')
            # self.create_proxy_auth_extension(proxy_host=proxyHost,
            #                                  proxy_port=proxyPort,
            #                                  proxy_username=proxyUser,
            #                                  proxy_password=proxyPass)
            next.click()
            time.sleep(3)

        driver.quit()

    def create_proxy_auth_extension(self, proxy_host, proxy_port,
                                    proxy_username, proxy_password,
                                    scheme='http', plugin_path=None):
        if plugin_path is None:
            plugin_path = r'D:/{}_{}@http-dyn.abuyun.com_9020.zip'.format(proxy_username, proxy_password)

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Abuyun Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                    },
                    bypassList: ["foobar.com"]
                }
              };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )

        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path

    def save_mongodb(self,result):
        try:
            if db[MONGO_TABLE].insert(result):
                print('存储到mongodb成功', result)
        except Exception:
            print('存储到mongodb失败', result)


if __name__ == '__main__':
    keyword = input('请输入查询关键词：')
    sn = Suning(keyword)
    # proxy_auth_plugin_path = sn.create_proxy_auth_extension(
    #     proxy_host=proxyHost,
    #     proxy_port=proxyPort,
    #     proxy_username=proxyUser,
    #     proxy_password=proxyPass)
    sn.suning()