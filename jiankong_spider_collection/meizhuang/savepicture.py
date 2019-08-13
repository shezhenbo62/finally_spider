import requests

def save(img_url, headers, filename, brand_name, count):
    # 验证码图片文件名
    response = requests.get(img_url, headers=headers)
    if response.status_code == 200:
        image = response.content
        try:
            with open(filename, 'wb') as f:
                f.write(image)
                print('保存品牌{}第{}张验证码成功'.format(brand_name, count))
        except Exception as e:
            filename = brand_name + str(count) + '.jpg'
            with open(filename, 'wb') as f:
                f.write(image)
                print('保存品牌{}第{}张验证码成功'.format(brand_name, count))

if __name__ == '__main__':
    # save()
    pass