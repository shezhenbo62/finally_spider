import pandas as pd
import pymysql
import os

basedir = os.path.dirname(__file__)
file = basedir + '/meizhuang'

def run():
    # 图片识别及信息整合
    pd_name = pd.read_csv(file + "/img_shibie_result.csv", names=['brand_name', 'img_name', 'act'])
    # pd_name['brand_name'].replace("__","_",inplace=True,regex=True)
    pd_name = pd_name.groupby(['brand_name']).sum()
    pd_tm = pd.read_csv(file + '/img_huodong.csv', names=['brand_name', 'url'])
    pd_tm = pd_tm.drop_duplicates(['brand_name'])
    data = pd.merge(pd_name, pd_tm, on=['brand_name'], how='inner')
    data.to_csv(file + '/meizhuang.csv', index=False)

    # db = pymysql.connect(host='localhost', user='root', password='123', db='img', port=3306)
    # # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    pd_a = pd.read_csv(file + "/meizhuang.csv", names=['brand_name', 'img_name', 'act', 'url'], skiprows=[0])
    pd_b = pd.read_csv(file + "/huodong.csv", names=['brand_name', 'url', 'act'])
    info = pd.concat([pd_a, pd_b], sort=False)
    info = info.fillna("null")
    info.to_csv(file + '/meizhuang_result.csv',index=False)

    # a = info.values.tolist()
    # for i in a:
    #     # 使用 execute()  方法执行 SQL
    #     sql = '''
    #     insert into muying(brand_name,img_name,act,url)
    #     values(%s,%s,%s,%s)
    #     '''
    #     cursor.execute(sql, i)
    #     db.commit()
    # db.close()

if __name__ == '__main__':
    run()
