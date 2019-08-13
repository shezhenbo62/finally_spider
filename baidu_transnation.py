import requests
import json
import sys

class BaiduTrans:
    def __init__(self, trans_content):
        self.content = trans_content
        self.url_temp = 'http://fanyi.baidu.com/langdetect'
        self.url_trans = 'http://fanyi.baidu.com/basetrans'
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}

    def langdetect(self, url, data):
        response = requests.post(url, data=data, headers=self.headers)
        return json.loads(response.content.decode('utf-8'))

    def get_trans_result(self, trans_dict):
        trans_result = trans_dict['trans'][0]['dst']
        print('result is:'+trans_result)

    def run(self):
        # 1.获取语言类型
        langdetect_data = {'query': self.content}
        lang = self.langdetect(self.url_temp, langdetect_data)['lan']
        # 2.准备post请求的数据
        if lang == 'zh':
            trans_data = {'query': trans_content, 'from': 'zh', 'to': 'en'}
        else:
            trans_data = {'query': trans_content, 'from': 'en', 'to': 'zh'}
        # 3.发送请求,获取响应
        trans_dict = self.langdetect(self.url_trans, trans_data)
        # 4.提取翻译的结果
        self.get_trans_result(trans_dict)


if __name__ == '__main__':
    # trans_content = 'Who are you'
    trans_content = sys.argv[1]
    baidutrans = BaiduTrans(trans_content)
    baidutrans.run()