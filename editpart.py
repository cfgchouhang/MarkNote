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
        title = a['title']
        tags = a['tag'].replace(' ','')
        if title == '':
            title = 'untitle'
        if tags == '':
            tags += 'untag'
        print 'add new:\n'+title+'\nlink: '+a['link']+'\ntags: '+tags
        print a['note']
        item = MarkNote(title,a['link'],tags,a['note'],datetime.now())
        for tag in tags.split(','):
            if tag != '':
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
    return redirect('/marknote/')
    
@app.route("/marknote/test")
def test(num):
    print 'Relates'
    for a in qu.query(Relate,Relate.id):
        print 'Relate: '+a.title+'| tagid: '\
                +str(a.tagid)+' |noteid: '+str(a.marknoteid)
    print 'Tags'
    for r in qu.query(Tag,Tag.id):
        print str(r.id)+' '+r.title
    print 'MarkNotes'
    for r in qu.query(MarkNote,MarkNote.id):
        print r.title
    return redirect('/marknote/time/1')
