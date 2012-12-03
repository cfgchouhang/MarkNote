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
    return redirect('/marknote/time')

@app.route("/marknote/<order>")
def main(order):
    if order == 'time':
        a = desc(MarkNote.time)
    elif order == 'title':
        a = MarkNote.title
    elif order == 'random':
        #a = func.rand() for mysql
        a = func.random()
    else:
        a = MarkNote.time
    data = qu.query(MarkNote,a,num=20)
    return render_template('main.html',data=data)
    
if __name__=='__main__':
    app.debug = True
    app.run(host='192.168.1.2')
