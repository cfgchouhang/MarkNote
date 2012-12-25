#!/usr/bin/env python
from flask import redirect,render_template
from sqlalchemy.sql.expression import func
from sqlalchemy import desc
import editpart
from querypart import querypart as qu
from marknote import MarkNote,Tag

global dec
dec = 0
app = editpart.app
@app.route("/")
@app.route("/marknote/")
def redir():
    return redirect('/marknote/time/1')

@app.route("/marknote/<orderby>/<int:page>")
def main(orderby,page):
    global dec
    if orderby == 'time':
        if dec == 0:
            order = desc(MarkNote.time)
            dec = 1
        else:
            order = MarkNote.time
            dec = 0
    elif orderby == 'title':
        dec = 0
        order = MarkNote.title
    elif orderby == 'tag':
        dec = 0
        data = qu.query(Tag,Tag.id,num=10,offset=(page-1)*10)
        return render_template('main_tags.html',data=data,\
                                page=page-((page-1)%5),orderby='tag')
    elif orderby == 'random':
        #a = func.rand() for mysql
        order = func.random()
        dec = 0
    else:
        order = desc(MarkNote.time)
        dec = 1
    data = qu.query(MarkNote,order,num=10,offset=(page-1)*10)
    print qu.count(MarkNote)
    return render_template('main.html',data=data,\
                            page=page-((page-1)%5),orderby=orderby)

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

if __name__=='__main__':
    app.debug = True
    app.run(host='127.0.0.1')
