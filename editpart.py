#-*- coding:utf-8 -*-
from flask import Flask,request,redirect,render_template,url_for
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
        checktag = {}
        for tag in tags.split(','):
            if tag != '':
                checktag[tag] = 0
        for tag in tags.split(','):
            if tag != '':
                rel = Relate(tag)
                a = qu.query_bytitle(Tag,tag)
                if a == None:
                    print "new tag: "+tag
                    t = Tag(tag,1)
                    t.relates += [rel]
                    item.relates += [rel]
                    t.add()
                    t.commit()
                elif checktag[tag] == 0:
                    a.relates += [rel]
                    qu.query_update(Tag,a.id,{'count':a.count+1})
                    item.relates += [rel]
                checktag[tag] = 1

        item.add()
        item.commit()
        noteimg = url.procimgurl(item.id,imgurl)
        qu.query_update(MarkNote,item.id,{'img':noteimg})

        print item.img
        for s in item.note.split("\n"):
            print s
    return redirect('/marknote')

@app.route("/edit/<id>")
def edit_page(id):
    item = qu.query_byid(id)
    print 'edit', item.id
    return render_template('edit_page.html',data=item)

@app.route("/update/<noteid>",methods=["POST"])
def update(noteid):
    a = {}
    update = {}
    for i in request.form.keys():
        a[i] = request.form[i]
    item = qu.query_byid(noteid)
    if a['title']==item.title and a['link']==item.link\
        and a['tag']==item.tag and a['note']==item.note:
        return redirect('/marknote/')
    a['tag'] = a['tag'].replace(' ','')
    tag_dict = {}
    for t in item.tag.split(','):
        if t != '':
            tag_dict[t] = 0

    for i in a.keys():
        update[i] = a[i]
    if update['title'] == '':
        update['title'] = item.title

    imgurl, hasimg = url.getimgurl(update['note'])
    update['img'] = url.procimgurl(noteid,imgurl)
    print 'img',update['img']
    #if tag_dict[tags] == 0, remove relation between tags and note
    for t in update['tag'].split(','):
        if t != '':
            #new tags that's not in tag_dict
            if not (t in tag_dict.keys()): 
                newtag = qu.query_bytitle(Tag,t)
                if newtag == None:
                    newtag = Tag(t,1)
                    newtag.add()
                    newtag.commit()
                else :
                    qu.query_update(Tag,newtag.id,{'count':newtag.count+1})
                rel = Relate(t)
                newtag.relates += [rel]
                item.relates += [rel]
            tag_dict[t] = 1
    print 'tag',tag_dict.keys()
    for t in tag_dict.keys():
        if tag_dict[t] == 0:
            qu.delete_rel(noteid,t)

    qu.query_update(MarkNote,noteid,update)
    return redirect('/marknote/')

@app.route("/delete/<id>")
def delete(id):
    note = qu.query_byid(id)
    for tag in note.tag.split(','):
        if tag != '':
            t = qu.query_bytitle(Tag,tag)
            qu.query_update(Tag,t.id,{'count':t.count-1})
            if t.count == 0:
                qu.delete_tag(t.id)

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
        print str(r.id)+' '+r.title+' '+str(r.count)
    print 'MarkNotes'
    for r in qu.query(MarkNote,MarkNote.id,num=num):
        print '_______________'
        print r.title
        print r.link
        #print r.note
        if r.img !='':
            print r.img
    return redirect('/marknote/time/1')

# used to copy db
'''
@app.route("/marknote/copy")
def copy():
    out = open("notedata/copydb",'w')
    for r in qu.query(MarkNote,MarkNote.id):
        out.write(r.title.encode('utf-8')+'\n')
        out.write(r.link+'\n')
        out.write(str(r.tag)+'\n')
        out.write(r.note.encode('utf-8')+'\n###\n')
        out.write(r.img+'\n')
        out.write(str(r.time)+'\n')
    return redirect('/marknote/time/1')

@app.route("/marknote/loadcopy")
def loadcopy():
    c = 0
    beadd = ["","","","","",""]
    for a in open("notedata/copydb",'r'):
        if not ('###' in a) :
            beadd[c] += a.decode('utf-8')
        if c != 3 :
            c += 1
        elif c== 3 and ('###' in a) :
            c += 1
        if c == 6 :
            print beadd[5]
            item = MarkNote(beadd[0].replace('\n',''),beadd[1].replace('\n',''),beadd[2].replace('\n',''),beadd[3],beadd[4].replace('\n',''),datetime.strptime(beadd[5].replace('\n',''),"%Y-%m-%d %H:%M:%S.%f"))
            item.add()
            item.commit()
            checktag = {}
            beadd[2] = beadd[2].replace('\n','')
            for tag in beadd[2].split(','):
                if tag != '':
                    checktag[tag] = 0
            for tag in beadd[2].split(','):
                if tag != '':
                    rel = Relate(tag)
                    b = qu.query_bytitle(Tag,tag)
                    if b == None:
                        print "new tag: "+tag
                        t = Tag(tag,1)
                        t.relates += [rel]
                        item.relates += [rel]
                        t.add()
                        t.commit()
                    elif checktag[tag] == 0:
                        b.relates += [rel]
                        qu.query_update(Tag,b.id,{'count':b.count+1})
                        item.relates += [rel]
                    checktag[tag] = 1
            c = 0
            beadd = ["","","","","",""]

    return redirect("/marknote/time/1")
'''
