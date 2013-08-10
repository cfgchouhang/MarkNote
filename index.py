#!/usr/bin/env python
from flask import request,redirect,url_for
from flask import redirect,render_template
from sqlalchemy.sql.expression import func
from sqlalchemy import desc
from init import app
from query import Query
from dbset import MarkNote,Tag,Relate
from feature import add_new,add_page

qu = Query()
global isdesc
isdesc = True

@app.route("/")
@app.route("/marknote/")
def redir():
    global isdesc
    isdesc = 1
    return redirect("/marknote/time/1")

@app.route("/marknote/check_desc/<int:page>")
def check_desc(page):
    global isdesc
    if isdesc:
        isdesc = False
    else:
        isdesc = True
    return redirect("/marknote/time/"+str(page))

@app.route("/marknote/<orderby>/<int:page>")
def index(orderby,page):
    data = get_data(orderby,page)
    print(qu.count(MarkNote))
    
    pinterval = page-((page-1)%5)
    return render_template('index.html',data=data,orderby=orderby,\
                           pinterval=pinterval,page=page)

@app.route("/marknote/load_data",methods=["GET"])
def load_data():
    offset = request.args.get("offset")
    orderby = request.args.get("orderby")
    print(int(offset),orderby)
    if orderby == "random":
        return render_template("load.html",data="")
    data = get_data(orderby,int(offset))
    return render_template("load.html",data=data)

def get_data(orderby="time",page=1):
    global isdesc
    if orderby=="time":
        if isdesc:
            order = desc(MarkNote.time)
        else:
            order = MarkNote.time
    elif orderby=="title":
        isdesc = False
        order = MarkNote.title
    elif orderby=="tag":
        isdesc = False
        pass
    elif orderby=="random":
        isdesc = False
        order = func.random()
    else:
        isdesc = True
        order = desc(MarkNote.time)
    return qu.query(MarkNote,order,num=10,offset=(page-1)*10)

if __name__=='__main__':
    app.debug = True
    app.run(host='127.0.0.1')

