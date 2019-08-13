# coding:utf-8

# 对现有D88品牌库进行品牌名处理，使品牌名适用于天猫结果搜索
import pandas as pd

pd_tm = pd.read_excel("C:/Users/Administrator/Desktop/D88品牌库整理版(2019.2.27).xlsx",
                      sheet_name=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], usecols=[1, 3], names=['brand_name', 'url'])
category_name = ['美妆', '服饰', '高端服饰', '电子', '母婴', '行李箱包', '厨房家电', '家居', '杂货清洁', '酒水', '零食', '保健']
i = 0
info_list = []
for info in pd_tm.values():
    info['category'] = category_name[i]
    i += 1
    info_list.append(info)
df = pd.concat(info_list, ignore_index=True)
order = ['category', 'brand_name', 'url']
df = df[order]
df = df.dropna(how='all', subset=['url'])
cn_brand_list = []
en_brand_list = []
for brand in df[['category', 'brand_name']].values.tolist():
    # brand = str(brand)
    split_list = []
    if ('\u4e00' <= str(brand[1]) <= '\u9fff' and str(brand[1]).isalpha()):
        cn_brand_list.append([brand[0], brand[1]])
    else:
        for j in str(brand[1]):
            if not ('\u4e00' <= j <= '\u9fff' or j == '/'):
                split_list.append(j)
        merge_str = ''.join(split_list)
        merge_str = merge_str.strip()
        en_brand_list.append([brand[0], merge_str])
all_list = en_brand_list + cn_brand_list
print(all_list)
result = pd.DataFrame(all_list, columns=['category', 'brand_name'])
# result.to_excel("C:/Users/Administrator/Desktop/D88处理过后品牌名.xls", index=False)
result.to_csv("C:/Users/Administrator/Desktop/D88处理过后品牌名.csv", index=False)

