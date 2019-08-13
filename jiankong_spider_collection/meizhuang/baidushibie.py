from aip import AipOcr
import os
import csv, hashlib
import pymongo

def run():
    i = 0
    j = 0
    APP_ID = '11030410'
    API_KEY = 'nFL4SLu5GjpM2K1aGQZPKidO'
    SECRET_KEY = 'QZpXrgt6XLFcC8IfzVQViWcORLVHzc28'
    words_base = ['狂欢', '发售', '折', '减', 'sale', 'OFF', '新品', '上新', '限量', '活动', '特卖', '特惠', '赠', '联名', '礼遇', '优惠', '免费',
                  '开门红', '低价', '送', '降', '献礼', '全新', '预售', '立省', '钜惠', '秒杀', '领券', '上市', '礼赞', '半价']

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 配置数据库信息
    mongo_client = pymongo.MongoClient('localhost', 27017)
    db = mongo_client['FOR_MD5']
    my_collection = db['md5美妆1']

    # 读取图片
    basedir = os.path.dirname(__file__)
    file = basedir + '/meizhuang'
    filenames = os.listdir(file)
    for filename in filenames:
        try:
            # 将路径与文件名结合起来就是每个文件的完整路径
            info = os.path.join(file, filename)
            with open(info, 'rb') as fp:
                # 获取文件夹的路径
                image = fp.read()
                # 调用通用文字识别, 图片参数为本地图片
                result = client.basicGeneral(image)
                # 定义参数变量
                options = {
                        'detect_direction': 'true',
                        'language_type': 'CHN_ENG',
                }
                # 调用通用文字识别接口
                result = client.basicGeneral(image, options)
                content_list = []
                # print(result)
                if result['words_result_num'] == 0:
                    print(filename + ':' + '----')
                    i += 1
                else:
                    for i in range(len(result['words_result'])):
                        content_list.append(result['words_result'][i]['words'])
                        j += 1
                    content_list = ','.join(content_list)
                    # print(filename + ' : ' + content_list)
                    for k in words_base:
                        if k in content_list:
                            md5 = hashlib.md5(content_list.encode('utf-8')).hexdigest()
                            url_find = {'md5': md5}
                            # 判断网页MD5是否存在数据库中
                            if my_collection.find_one(url_find):
                                old_md5 = my_collection.find_one(url_find)['md5']
                                if md5 == old_md5:
                                    print('MD5一致')
                                else:
                                    print('MD5不一致')
                                    my_collection.update(url_find, {'$set': {"md5": md5}})
                                    with open(file + "/img_shibie_result.csv", "a",
                                              encoding="utf-8") as f:
                                        writer = csv.writer(f)
                                        writer.writerow([filename.split("__")[0], filename, content_list])
                            else:
                                print(filename + ' : 添加数据-----'+content_list)
                                info = {'md5': md5}
                                my_collection.insert(info)
                                with open(file + "/img_shibie_result.csv", "a", encoding="utf-8") as f:
                                    writer = csv.writer(f)
                                    writer.writerow([filename.split("__")[0], filename, content_list])
                            break
        except Exception as a :
            print("have a picture erro!!")

    print('共识别图片{}张'.format(i+j))
    print('未识别出文本{}张'.format(i))
    print('已识别出文本{}张'.format(j))


# def del_image():
#     file_path = 'D:/muying'
#     filenames = os.listdir(file_path)
#     print(filenames)
#     for filename in filenames:
#         filename = file_path + "/" + filename
#         print(filename)
#         os.remove(filename)


if __name__ == "__main__":
    run()