#!/usr/bin/env python
#coding=utf-8

import csv
import sqlite3

database = sqlite3.connect('search.db')
db = database.cursor()
db.execute('''DROP TABLE SEARCH''')
db.execute('''CREATE TABLE IF NOT EXISTS SEARCH
    (
    ID INT PRIMARY KEY NOT NULL,
    DATE TEXT NOT NULL,
    SKU_ID TEXT NOT NULL,
    SKU_NAME TEXT NOT NULL,
    HOT_TAG TEXT NOT NULL,
    KEYWORD TEXT NOT NULL,
    SEARCH_NUM INT NOT NULL,
    SEARCH_ORDER NULL,
    INDEX_ORDER NULL,
    SCORE_KW NULL,
    SCORE_SKU NULL
    );
    ''')

with open('data.csv', 'r', encoding='utf-8') as csvfile:
    csvReader = csv.reader(csvfile)
    i = 0
    for row in csvReader:
        if i != 0:
            if row[0] != '合计':
                for item in row:
                    item = item.encode('utf-8')
                db.execute(
                    '''INSERT INTO SEARCH (ID, DATE, SKU_ID, SKU_NAME, HOT_TAG, KEYWORD, SEARCH_NUM) VALUES (?,?,?,?,?,?,?);''' \
                    , ((tuple([i]) + tuple(row)))
                )
                i += 1
            else:
                None
        else:
            i += 1

db.execute('''select * from SEARCH order by SEARCH_NUM DESC''')

database.commit()
database.close()