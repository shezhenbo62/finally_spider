import pandas as pd
import numpy as np
import time


class CF(object):
    def __init__(self, datas, k=5, n=10):
        self.datas = datas
        # 邻居个数
        self.k = k
        # 推荐个数
        self.n = n
        # 用户对折扣信息的操作行为及权重，浏览：1，点击购买：2，评论：3，收藏：4，分享：5
        # 数据格式{'UserID：用户ID':[{'ObjectID：折扣信息ID':[ActionType：用户操作行为]}]}
        self.userDict = {}
        # 对某折扣信息有过操作行为的用户
        # 数据格式：{'ObjectID：折扣信息ID':[UserID：用户ID]}
        # {'1',[1,2,3..],...}
        self.ItemUser = {}
        # 邻居的信息
        self.neighbors = []
        # 推荐列表
        self.recommendList = []
        self.cost = 0.0
        self.rows = []

    # 将datas转换为userDict和ItemUser
    def setup_data(self):
        term_list = []
        for i in self.datas:
            temp = {i[3]:[float(i[2])/5]}
            if i[0] in self.userDict:
                for k in self.userDict[i[0]]:
                    if i[3] in k:
                        k[i[3]].append(float(i[2])/5)
                for v in self.userDict[i[0]]:
                    for a,b in v.items():
                        term_list.append(a)
                if i[3] not in term_list:
                    self.userDict[i[0]].append(temp)
            else:
                self.userDict[i[0]] = [temp]
            if i[3] in self.ItemUser:
                self.ItemUser[i[3]].append(i[0])
            else:
                term_list = []
                self.ItemUser[i[3]] = [i[0]]
        # print(self.userDict)
        # print(self.ItemUser)

    # 找到某用户的相邻用户
    def getNearestNeighbor(self, userId):
        neighbors = []
        self.neighbors = []
        # 获取userId有过操作行为的折扣信息都有那些用户也有过操作行为
        for i in self.userDict[userId]:
            i = list(i.keys())
            for j in self.ItemUser[i[0]]:
                if (j != userId and j not in neighbors):
                    neighbors.append(j)
        # 计算这些用户与userId的相似度并排序
        for i in neighbors:
            dist = self.getCost(userId, i)
            self.neighbors.append([dist, i])
        # 排序默认是升序，reverse=True表示降序
        self.neighbors.sort(reverse=True)
        self.neighbors = self.neighbors[:self.k]
        # print(self.neighbors)

    # 计算余弦距离
    def getCost(self, userId, l):
        # 获取用户userId和l有过操作行为的折扣信息的并集
        # {'折扣信息ID'：[userId的操作行为权重，l的操作行为权重]}
        user = self.formatuserDict(userId, l)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0])*float(v[0])+float(v[1])*float(v[1])+float(v[2])*float(v[2])+float(v[3])*float(v[3])+float(v[4])*float(v[4])
            y += float(v[5])*float(v[5])+float(v[6])*float(v[6])+float(v[7])*float(v[7])+float(v[8])*float(v[8])+float(v[9])*float(v[9])
            z += float(v[0])*float(v[5])+float(v[1])*float(v[6])+float(v[2])*float(v[7])+float(v[3])*float(v[8])+float(v[4])*float(v[9])
        if (z == 0.0):
            return 0
        return z / np.sqrt(x * y)

    # 格式化userDict数据
    def formatuserDict(self, userId, l):
        user = {}
        for i in self.userDict[userId]:
            a = list(i.keys())
            b = list(i.values())
            array = np.zeros(10,dtype=float)
            for v in b[0]:
                if v == 0.2:
                    array[0] = v
                elif v == 0.4:
                    array[1] = v
                elif v == 0.6:
                    array[2] = v
                elif v == 0.8:
                    array[3] = v
                elif v == 1.0:
                    array[4] = v
            user[a[0]] = array.tolist()  # a折扣信息id, b折扣信息评分
        for j in self.userDict[l]:
            c = list(j.keys())
            d = list(j.values())
            array1 = np.zeros(10, dtype=float)
            for k in d[0]:
                if k == 0.2:
                    array1[5] = k
                elif k == 0.4:
                    array1[6] = k
                elif k == 0.6:
                    array1[7] = k
                elif k == 0.8:
                    array1[8] = k
                elif k == 1.0:
                    array1[9] = k
            if (c[0] not in user):
                user[c[0]] = array1.tolist()
            else:
                for e in d[0]:
                    if e == 0.2:
                        user[c[0]][5] = e
                    elif e == 0.4:
                        user[c[0]][6] = e
                    elif e == 0.6:
                        user[c[0]][7] = e
                    elif e == 0.8:
                        user[c[0]][8] = e
                    elif e == 1.0:
                        user[c[0]][9] = e
        return user

    # 获取推荐列表
    def getrecommendList(self, userId):
        self.recommendList = []
        # 建立推荐字典
        recommendDict = {}
        # 目标用户有过行为操作的折扣信息Id列表
        discount_id = []
        for data in datas:
            if data[0] == userId:
                discount_id.append(data[3])
        for neighbor in self.neighbors:
            infos = self.userDict[neighbor[1]]
            for info in infos:
                k = list(info.keys())[0]
                # 过滤掉目标用户本身有过行为操作的折扣信息Id
                if k not in discount_id:
                    if (k in recommendDict):
                        recommendDict[k] += neighbor[0]
                    else:
                        recommendDict[k] = neighbor[0]
        # 建立推荐列表
        for key in recommendDict:
            self.recommendList.append([recommendDict[key], key])
            self.recommendList.sort(reverse=True)
            self.recommendList = self.recommendList[:self.n]

    # 推荐的准确率
    def getPrecision(self, userId):
        user = [list(i.keys())[0] for i in self.userDict[userId]]
        recommend = [i[1] for i in self.recommendList]
        count = 0.0
        if (len(user) >= len(recommend)):
            for i in recommend:
                if (i in user):
                    count += 1.0
            self.cost = count / len(recommend)
        else:
            for i in user:
                if (i in recommend):
                    count += 1.0
            self.cost = count / len(user)

    def show_recommend_result(self):
        for i in self.recommendList:
            for j in datas:
                if j[3] == i[1]:
                    info_id = i[1]
                    title = j[4]
                    getCost = i[0]
                    self.rows.append([info_id,title,getCost])
                    break

    def run(self, userId):
        # 构建userDict和ItemUser数据集
        self.setup_data()
        # 推荐个数 等于 本身操作的折扣信息条数，用户计算准确率
        self.n = len(self.userDict[userId])
        # self.n = 10
        self.getNearestNeighbor(userId)
        self.getrecommendList(userId)
        # print(self.recommendList)
        self.getPrecision(userId)
        self.show_recommend_result()


if __name__ == '__main__':
    start = time.time()
    # 读取用户历史行为数据
    datas = pd.read_excel('C:/Users/Administrator/Desktop/user.xls').values.tolist()
    cf = CF(datas, k=20)
    # 用户id 29 为joey, 56为佘振波
    cf.run(29)
    # 将推荐列表数据转化成Dataframe数据类型，美化输出
    rows = pd.DataFrame(cf.rows,columns=['discountId', 'title', 'similarityDegree'])
    # 推荐列表数据写入到EXCEL表格
    rows.to_excel('C:/Users/Administrator/Desktop/recommend.xls',index=False)
    print('推荐列表为：')
    print(rows)
    print("处理的数据数量为：%d条" % len(datas))
    # print('推荐的准确率为：%.2f%%' % (cf.cost * 100))
    end = time.time()
    print("推荐需要耗费时间：%fs" % (end-start))