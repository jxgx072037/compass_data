import sqlite3

database = sqlite3.connect('search.db')
db = database.cursor()

db.execute('''select KEYWORD from SEARCH;''')

kws = []  # 关键词列表
for item in db.fetchall():
    kws.append(list(item)[0])

kws = list(set(kws)) #去重