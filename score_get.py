import sqlite3
import re
import csv

database = sqlite3.connect('search.db')
db = database.cursor()

db.execute('''select KEYWORD from SEARCH;''')

kws = []  # 关键词列表
for item in db.fetchall():
    kws.append(list(item)[0])

kws = list(set(kws))

# 提前建好CSV得分文件
csvFile = open('score_search.csv', 'w+', newline='') #newline用来避免空行
writer = csv.writer(csvFile)
writer.writerow(('keyword', 'search_num', 'score'))

#整理每一条搜索关键字数据，增加两个排序参数（按搜索次数和位置）

def item_clean(data_db, data, n):
    for item in data_db:
        item = list(item)[0:-4]
        item.append(n)  #增加按照搜索次数的排序标记

        index = (re.findall('(\d*)$', item[4]))[0]
        item.append(index)  #增加商品位置的排序标记

        #在数据库每条记录后面增加search_order和index_order
        db.execute('''update SEARCH set SEARCH_ORDER = ?, INDEX_ORDER = ? where ID = ?;''',(n , index, item[0]))

        data.append(item)
        n += 1

#计算当前搜索关键字的得分
def item_score(data):
    sum_kw = 0 #当前搜索关键词搜索次数的总和
    for item in data:
        sum_kw += int(item[-3])

    sum_s = 0  #位置排序-次数排序）的平方，乘上搜索次数的概率
    for item in data:
        score_sku = ((int(item[-1])-item[-2])**2)*((int(item[-3]))/sum_kw)
        db.execute('''update SEARCH set SCORE_SKU = ? where ID = ?''', (score_sku, item[0]))
        sum_s += (score_sku)

    n = int(data[-1][-1])  #一个关键词内所有数据条目的数量

    score_list = []
    score_list.append(sum_kw)  #在score_list中增加当前搜索词的总次数
    if n == 1:
        score_kw = (round((sum_s/n)**0.5,2))
    else:
        score_kw = (round((sum_s/(n-1)) ** 0.5,2))
    db.execute('''update SEARCH set SCORE_KW = ? where KEYWORD = ?''', (score_sku, data[0][5]))
    score_list.append(score_kw)
    return score_list

num = 1 #进度计数器

for kw in kws:
    db.execute('''select * from SEARCH where keyword = \'%s\''''%(kw))

    i = 1
    data_kw = [] #用来装一个关键词下的所有SKU数据条目，是一个二维list

    item_clean(db.fetchall(), data_kw, i)

    # kw_score为当前关键字得分的list
    kw_score = []
    if kw != '':
        try:
            kw_score.append(kw)
            kw_score += item_score(data_kw)
            writer.writerow(kw_score)
        except UnicodeEncodeError:
            print (UnicodeEncodeError)

    #打印进度
    if num%50 == 0:
        print ('关键词总得分计算进度%.2f%%，共%d个关键词，已处理%d个'% ((num/len(kws))*100, len(kws), num))
    num += 1

    # if num >=200:
    #     break

csvFile.close()
database.commit()
database.close()

print ("计算完毕")




