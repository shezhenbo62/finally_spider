from selenium import webdriver
import time

class BiliSpider:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.start_url = 'https://www.bilibili.com/v/dance/otaku#/'

    def get_content_list(self):
        div_list = self.driver.find_elements_by_xpath("//div[@class='l-item']")
        content_list = []
        for div in div_list:
            item = {}
            item['title'] = div.find_element_by_xpath(".//div[@class='r']/a").text
            item['img'] = div.find_element_by_xpath(".//div[@class='lazy-img']/img").get_attribute('src')
            item['detail'] = div.find_element_by_xpath(".//div[@class='v-desc']").text
            item['upinfo'] = div.find_element_by_xpath(".//div[@class='up-info']/a").text
            print(item)
            content_list.append(item)
        next_url = self.driver.find_elements_by_xpath("//button[@class='nav-btn iconfont icon-arrowdown3']")
        next_url = next_url[0] if len(next_url)>0 else None
        return content_list,next_url

    def save_content_list(self,content_list):
        pass

    def run(self):
        # start_url
        # 发起请求,获取响应
        self.driver.get(self.start_url)
        # 提取数据
        content_list,next_url = self.get_content_list()
        # 保存
        self.save_content_list(content_list)
        while next_url is not None:
            next_url.click()
            time.sleep(2)
            content_list, next_url = self.get_content_list()
            self.save_content_list(content_list)


if __name__ == '__main__':
    bili = BiliSpider()
    bili.run()

