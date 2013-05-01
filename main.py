#!/usr/bin/env python
from flask import redirect,render_template
from sqlalchemy.sql.expression import func
from sqlalchemy import desc
import editpart
import urltool as url
from querypart import querypart as qu
from marknote import MarkNote,Tag

global dec
dec = 1
app = editpart.app
request = editpart.request

@app.route("/")
@app.route("/marknote/")
def redir():
    global dec
    dec = 1
    return redirect('/marknote/time/1')

@app.route("/marknote/check_dec/<int:p>")
def checktime(p):
    global dec
    if dec == 0:
        dec = 1
    else :
        dec = 0
    return redirect('/marknote/time/'+str(p))

@app.route("/marknote/<orderby>/<int:page>")
def main(orderby,page):
    '''
    global dec
    if orderby == 'time':
        if dec == 1:
            order = desc(MarkNote.time)
        else:
            order = MarkNote.time
    elif orderby == 'title':
        dec = 0
        order = MarkNote.title
    elif orderby == 'tag':
        dec = 0
        data = qu.query(Tag,Tag.id)
        return render_template('tags_page.html',data=data,\
                                page=page-((page-1)%5),orderby='tag')
    elif orderby == 'random':
        #a = func.rand() for mysql
        order = func.random()
        dec = 0
    else:
        order = desc(MarkNote.time)
        dec = 1
    '''
    data = get_data(orderby,page)
    #data = qu.query(MarkNote,order,num=10,offset=(page-1)*10)
    print qu.count(MarkNote)
    if orderby == "tag":
        return render_template('tags_page.html',data=data,\
                                page=page-((page-1)%5),orderby='tag')
    return render_template('main.html',data=data,\
                            page=page-((page-1)%5),orderby=orderby,curp=page)

@app.route("/marknote/tags/<tag_title>")
def tag_page(tag_title):
    rel = qu.query_bytitle(Tag,tag_title)
    note = []
    for a in rel.relates:
        note += [qu.query_byid(a.marknoteid)]
        print a.title,a.tagid,a.marknoteid
    for a in note:
        print a.title, a.tag
    return render_template('tags.html',data=note)

@app.route("/marknote/search",methods=["GET"])
def search():
    term = request.args.get('search','')
    data = qu.search(term)
    return render_template('search_page.html',data=data)

@app.route("/marknote/get_data",methods=["GET"])
def get_data(orderby="time",page=1):
    global dec
    if orderby == 'time':
        if dec == 1:
            order = desc(MarkNote.time)
        else:
            order = MarkNote.time
    elif orderby == 'title':
        dec = 0
        order = MarkNote.title
    elif orderby == 'tag':
        dec = 0
        return qu.query(Tag,Tag.id)
    elif orderby == 'random':
        #a = func.rand() for mysql
        order = func.random()
        dec = 0
    else:
        order = desc(MarkNote.time)
        dec = 1
    print request.args.get
    return qu.query(MarkNote,order,num=10,offset=(page-1)*10)

@app.route("/marknote/get_test",methods=["GET","POST"])
def get_test():
    if request.method == "GET":
        print request.args.get("orderby")
        print request.args.get("page")
    else:
        print request.form
    return "get success"

if __name__=='__main__':
    #app.debug = True
    #app.run(host='127.0.0.1')
    app.run(host='192.168.1.2')
