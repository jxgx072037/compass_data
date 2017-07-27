# -*- coding: utf-8 -*-

import web
import sqlite3
from pub import kws

urls = (
    '/','index'
)

render = web.template.render('templates/')

db = web.database(dbn='sqlite', db ='search.db')

class index:
    def GET(self):
        data = db.select('SEARCH')
        return render.index(data, kws)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
