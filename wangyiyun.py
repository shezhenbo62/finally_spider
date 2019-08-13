from selenium import webdriver


class WangyiyunMusic:
    def __init__(self):
        self.start_url = 'https://music.163.com/#/discover/playlist/'
        self.driver = webdriver.Chrome()

    def get_detail_url(self):
        detail_list = self.driver.find_elements_by_xpath("//div[@class='u-cover u-cover-1']")
        href_list = []
        for detail in detail_list:
            href = detail.find_element_by_xpath("./a").get_attribute('href')
            href_list.append(href)
        return href_list

    def get_content_list(self):
        div_list = self.driver.find_elements_by_xpath("//tr[contains(@class,' ')]")
        content_list = []
        # detail = {}
        # detail['title'] = self.driver.find_element_by_xpath("//h2[@class='f-ff2 f-brk']").text
        # detail['author'] = self.driver.find_element_by_xpath("//span[@class='name']/a").text
        # detail['introduce'] = self.driver.find_element_by_xpath("//p[@id='album-desc-more']").text
        # content_list.append(detail)
        for div in div_list:
            item = {}
            item['music_name'] = div.find_element_by_xpath(".//span[@class='txt']/a/b").get_attribute('title')
            item['singer'] = div.find_element_by_xpath(".//div[@class='text']").get_attribute('title')
            print(item)
            content_list.append(item)
        return content_list

    def get_next_url(self):
        next_url = self.driver.find_elements_by_xpath("//div[@class='u-page']")
        next_url_list = []
        for next in next_url:
            n_url = next.find_element_by_xpath("./a[@class='zbtn znxt']").get_attribute('href')
            next_url_list.append(n_url)
        print(next_url_list)
        return next_url_list

    def save_content_list(self,content_list):
        pass

    def run(self):
        self.driver.get(self.start_url)
        self.driver.switch_to.frame('g_iframe')
        next_url = self.get_next_url()
        next_url = next_url[-1]
        while next_url:
            href_list = self.get_detail_url()
            for href in href_list:
                self.driver.get(href)
                self.driver.switch_to.frame('g_iframe')
                content_list = self.get_content_list()
                self.save_content_list(content_list)

            self.driver.get(next_url)
            self.driver.switch_to.frame('g_iframe')
            next_url = self.get_next_url()
            next_url = next_url[-1]


if __name__ == '__main__':
    wangyiyun = WangyiyunMusic()
    wangyiyun.run()