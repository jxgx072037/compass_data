# -*- coding: utf-8 -*-

import web
import sqlite3
from pub import kws
from pub import date

urls = (
    '/','index'
)

render = web.template.render('templates/')

db = web.database(dbn='sqlite', db ='search.db')

class index:
    def GET(self):
        data = db.select('SEARCH_KW', order = 'SEARCH_NUM DESC')
        return render.index(data, kws, date)

    def POST(self):
            search_word = web.input(id ='search') #存页面的搜索关键词
            condition = r'KEYWORD like "%' + search_word.keyword + r'%"'
            data = db.select('SEARCH_KW', where = condition, order = 'SEARCH_NUM DESC')
            count = db.query('select count(*) as count from SEARCH_KW where '+condition+'order by SEARCH_NUM DESC')[0]['count']
            return render.index(data, kws, date, count, search_word)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
