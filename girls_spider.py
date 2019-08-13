import requests
import re
import json

class GuokeSpider:
    def __init__(self):
        self.start_url = 'https://www.ugirls.com/Content/'
        self.url_temp = 'https://www.ugirls.com/Content/Page-{}.html'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def parse(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode('utf-8')

    def parse_img(self, url):
        response = requests.get(url, headers=self.headers).content
        return response

    def get_content(self, content):
        html_str = re.findall(r'<img .*?src="(.*?)" alt=".*?" />', content, re.S) # 标题
        return html_str

    def save_content(self, html_str, img_name):
        with open("D:/douyu/youguo/" + img_name, "wb") as f:
            f.write(html_str)
            print("保存成功")

    def get_url_list(self):
        return [self.url_temp.format(i) for i in range(2, 101)]

    def run(self):
        # 发起请求,接收响应
        content = self.parse(self.start_url)
        # 提取数据
        html_str = self.get_content(content)
        # 对图片url发起请求
        for img_url in html_str:
            print(img_url)
            img_comment = self.parse_img(img_url)
        # 保存数据
            img_name = img_url.split("/")[-1]
            self.save_content(img_comment, img_name)
        # 遍历url列表
        url_list = self.get_url_list()
        for url in url_list:
            # 发起请求,接收响应
            response_str = self.parse(url)
            # 提取数据
            title_str = self.get_content(response_str)
            for i in title_str:
                print(i)
                img_comments = self.parse_img(i)
                # 保存数据
                img_name2 = i.split("/")[-1]
                self.save_content(img_comments, img_name2)


if __name__ == '__main__':
    guoke = GuokeSpider()
    guoke.run()