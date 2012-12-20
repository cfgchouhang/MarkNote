#!/usr/bin/env python
from flask import redirect,render_template
from sqlalchemy.sql.expression import func
from sqlalchemy import desc
import editpart
from querypart import querypart as qu
from marknote import MarkNote,Tag

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
    elif orderby == 'tag':
        data = qu.query(Tag,Tag.id,num=10,offset=(page-1)*10)
        return render_template('main_tags.html',data=data,\
                                page=page-((page-1)%5),orderby='tag')
    elif orderby == 'random':
        #a = func.rand() for mysql
        order = func.random()
    else:
        order = MarkNote.time
    data = qu.query(MarkNote,order,num=10,offset=(page-1)*10)
    print qu.count(MarkNote)
    return render_template('main.html',data=data,\
                            page=page-((page-1)%5),orderby=orderby)

@app.route("/marknote/tags/<tag_title>")
def tag_page(tag_title):
    rel = qu.query_bytitle(Tag,tag_title)
    for a in rel.relates:
        print a
    return redirect("/marknote/tag/1")

if __name__=='__main__':
    app.debug = True
    app.run(host='192.168.1.2')
