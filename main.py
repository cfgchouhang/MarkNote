#!/usr/bin/env python
from flask import redirect,render_template
from sqlalchemy.sql.expression import func
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
        a = MarkNote.time
    elif order == 'title':
        a = MarkNote.title
    elif order == 'random':
        #a = func.rand()
        a = func.random()
    else:
        a = MarkNote.time
    data = qu.query(a,num=20)
    return render_template('main.html',data=data)
    
if __name__=='__main__':
    app.debug = True
    app.run(host='192.168.1.2')
