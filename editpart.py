#-*- coding:utf-8 -*-
from flask import Flask,request,redirect,render_template
from datetime import datetime
import sqltool
import marknote
from querypart import querypart as qu

app = Flask(__name__)
sql = sqltool.sqltool
MarkNote = marknote.MarkNote
Tag = marknote.Tag
Relate = marknote.Relate

@app.route("/add_page")
def add_page():
    return render_template('add_page.html')

@app.route("/add_new",methods=["POST"])
def add_new():
    a = request.form
    if a['title']!='' or a['link']!='':
        tags = a['tag'].replace(' ','')
        print 'tags: '+tags
        item = MarkNote(a['title'],a['link'],tags,a['note'],datetime.now())
        for tag in tags.split(','):
            rel = Relate(tag)
            a = qu.query_bytitle(Tag,tag)
            if a == None:
                print tag+" doesn't exist"
                t = Tag(tag)
                t.relates += [rel]
                item.relates += [rel]
                t.add()
                t.commit()
            else:
                a.relates += [rel]
                item.relates += [rel]

        item.add()
        item.commit()
        print 'Relates'
        for a in qu.query(Relate,Relate.id,num=50):
            print 'Relate: '+a.title+'| tagid: '\
                    +str(a.tagid)+' |noteid: '+str(a.marknoteid)
        print 'Tags'
        for r in qu.query(Tag,Tag.id,num=30):
            print str(r.id)+' '+r.title
        print 'MarkNotes'
        for r in qu.query(MarkNote,MarkNote.id,num=30):
            print r.title

    return redirect('/marknote')

@app.route("/edit/<id>")
def edit_page(id):
    item = qu.query_byid(id)
    print item.id
    return render_template('edit_page.html',data=item)

@app.route("/update/<id>",methods=["POST"])
def update(id):
    a = request.form
    item = qu.query_byid(id)
    update = {'title':item.title,'link':item.link,\
              'tag':item.tag,'note':item.note}
    for i in a.keys():
        if a[i] != '':
            update[i] = a[i]
    qu.query_update(id,update)
    return redirect('/marknote')

@app.route("/delete/<id>")
def delete(id):
    qu.delete_byid(id)
    return redirect('/marknote/time')
    
