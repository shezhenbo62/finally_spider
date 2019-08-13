import requests
from lxml import etree
import threading
from queue import Queue

class BiliSpider:
    def __init__(self):
        self.url_temp = 'https://api.bilibili.com/x/v1/dm/list.so?oid=42760487'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        self.content_queue = Queue()

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        content_list = html.xpath('//i/d/text()')
        self.content_queue.put(content_list)

    def save_content_list(self):
        content_list = self.content_queue.get()
        for content in content_list:
            with open('bilibili_danmu.txt', 'a', encoding='utf-8') as f:
                f.write(content)
                f.write('\n')
                print('保存成功')
        self.content_queue.task_done()

    def run(self):
        # 发送请求,获取响应
        html_str = self.parse_url(self.url_temp)
        # 提取数据
        self.get_content_list(html_str)
        # 保存
        t1 = threading.Thread(target=self.save_content_list)
        t1.setDaemon(True)
        t1.start()
        t1.join()
        print('主线程结束')


if __name__ == '__main__':
    bili = BiliSpider()
    bili.run()