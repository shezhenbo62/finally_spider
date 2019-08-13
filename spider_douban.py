import requests
import json

class DouBan:
    def __init__(self):
        self.american_url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count=18&loc_id=108288'
        # self.england_url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?start=0&count=18&loc_id=108288'
        # self.chinese_url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?start=0&count=18&loc_id=108288'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                        'Referer': 'https://m.douban.com/tv/american'}

    def parme(self):
        response = requests.get(self.american_url, headers=self.headers)
        return json.loads(response.content.decode('utf-8'))

    def get_url(self, html_dict):
        page_num = html_dict['total']
        count = page_num // 18 + 1
        return [self.american_url.format(18*i) for i in range(count)]

    def resq_url(self, url):
        response = requests.get(url, headers=self.headers)
        return json.loads(response.content.decode('utf-8'))

    def save_html(self, html_str):
        with open('douban.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(html_str, ensure_ascii=False))
            f.write('\n')

    def run(self):
        html_dict = self.parme()
        url_list = self.get_url(html_dict)

        for url in url_list:
            html_str = self.resq_url(url)

            self.save_html(html_str)
            print('已经成功爬取豆瓣')


if __name__ == '__main__':
    douban = DouBan()
    douban.run()