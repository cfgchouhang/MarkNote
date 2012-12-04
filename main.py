#!/usr/bin/env python
from flask import redirect,render_template
from sqlalchemy.sql.expression import func
from sqlalchemy import desc
import editpart
from querypart import querypart as qu
from marknote import MarkNote

app = editpart.app
@app.route("/")
@app.route("/marknote/")
def redir():
    return redirect('/marknote/time/1')

@app.route("/marknote/<orderby>/<int:page>")
def main(orderby,page):
    if orderby == 'time':
        order = desc(MarkNote.time)
    elif orderby == 'title':
        order = MarkNote.title
    elif orderby == 'random':
        #a = func.rand() for mysql
        order = func.random()
    else:
        order = MarkNote.time
    data = qu.query(MarkNote,order,num=10,offset=(page-1)*10)
    print qu.count(MarkNote)
    return render_template('main.html',data=data,\
                            page=(page-page%5)+1,orderby=orderby)
    
if __name__=='__main__':
    app.debug = True
    app.run(host='192.168.1.2')
