#-*- coding:utf-8 -*-
from flask import Flask,request,redirect,render_template
from datetime import datetime
from querypart import querypart as qu
from werkzeug import SharedDataMiddleware
import sqltool,marknote
import urltool as url

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
        note = a['note']
        imgurl, hasimg = url.getimgurl(note)
        for i in imgurl:
            if i != '':
                print i

        if title == '':
            title = 'untitle'
        if tags == '':
            tags += 'untag'
        print 'add new:\n'+title+'\nlink: '+a['link']+'\ntags: '+tags
        print a['note']

        item = MarkNote(title,a['link'],tags,a['note'],"",datetime.now())
        for tag in tags.split(','):
            if tag != '':
                rel = Relate(tag)
                a = qu.query_bytitle(Tag,tag)
                if a == None:
                    print "new tag: "+tag
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
        noteimg = url.procimgurl(item.id,imgurl)
        qu.query_update(item.id,{'img':noteimg})

        print item.img
        for s in item.note.split("\n"):
            print s
    return redirect('/marknote')

@app.route("/edit/<id>")
def edit_page(id):
    item = qu.query_byid(id)
    print item.id
    return render_template('edit_page.html',data=item)

@app.route("/update/<noteid>",methods=["POST"])
def update(noteid):
    a = {}
    for i in request.form.keys():
        a[i] = request.form[i]
    item = qu.query_byid(noteid)
    update = {'title':item.title,'link':item.link,\
              'tag':item.tag,'note':item.note}
    a['tag'] = a['tag'].replace(' ','')
    tag_dict = {}
    for t in item.tag.split(','):
        if t != '':
            tag_dict[t] = 0

    for i in a.keys():
        if a[i] != '':
            update[i] = a[i]

    #if tag_dict[tags] == 0, remove relation between tags and note
    for t in update['tag'].split(','):
        if t != '':
            #new tags that's not in tag_dict
            if not (t in tag_dict.keys()): 
                newtag = qu.query_bytitle(Tag,t)
                if newtag == None:
                    newtag = Tag(t)
                rel = Relate(t)
                newtag.relates += [rel]
                item.relates += [rel]
            tag_dict[t] = 1
    print tag_dict
    for t in tag_dict.keys():
        if tag_dict[t] == 0:
            qu.delete_rel(noteid,t)

    print 'edit'
    qu.query_update(noteid,update)
    return redirect('/marknote/')

@app.route("/delete/<id>")
def delete(id):
    qu.delete_byid(id)
    return redirect('/marknote/')
    
@app.route("/marknote/test/<int:num>")
def test(num):
    print 'Relates'
    for a in qu.query(Relate,Relate.id,num=num):
        print 'Relate: '+a.title+'| tagid: '\
                +str(a.tagid)+' |noteid: '+str(a.marknoteid)
    print 'Tags'
    for r in qu.query(Tag,Tag.id,num=num):
        print str(r.id)+' '+r.title
    print 'MarkNotes'
    for r in qu.query(MarkNote,MarkNote.id,num=num):
        print r.title
    return redirect('/marknote/time/1')
