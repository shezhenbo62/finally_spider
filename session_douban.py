import requests

# 1.实例一个session类
session = requests.session()
post_url = 'https://www.douban.com/accounts/login'
post_data = {'form_email': '15102768455', 'form_password': 'bo15927774523'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

# 2.使用session发送post请求,并保存cookie
session.post(post_url, data=post_data, headers=headers)

# 3.使用session保存登录后才能访问的页面
url = 'https://www.douban.com/people/146704130/'
r = session.get(url, headers=headers)
content_html = r.content.decode('utf-8')
with open('douban.html', 'w', encoding='utf-8') as f:
    f.write(content_html)