from init import app 
from dbset import MarkNote,Tag,Relate
from query import Query
from flask import request,redirect,render_template,url_for
from datetime import datetime

qu = Query()

@app.route("/add_page")
def add_page():
    return render_template("add_page.html")

@app.route("/add_new",methods=["POST"])
def add_new():
    form = request.form
    if form["title"]=='' and form["link"]=='':
        return redirect(url_for("redir"))
    title,link,tags,note = form["title"],form["link"],\
                           form["tags"].replace(' ',''),\
                           form["note"]
    if title=='':
        title = "untitle"
    if tags=='':
        tags = "untag"
    
    new_data = MarkNote(title,link,tags,note,datetime.now())
    add_tags = {}
    for t in tags.split(','):
        if t == '':
            continue
        add_tags[t] = True
    
    for tag in tags.split(','):
        if tag == '':
            continue
        rel = Relate()
        t = qu.query_bytitle(Tag,tag).first()
        if t == None:
            print("new tag:"+tag)
            new_tag = Tag(tag,1)

            new_data.relates += [rel]
            new_tag.relates += [rel]

            new_tag.add()
            add_tags[tag] = False

        elif add_tags[tag]:
            new_data.relates += [rel]
            t.relates += [rel]
            qu.query_update(Tag,t.id,{"count":t.count+1})

        add_tags[tag] = False
    
    new_data.add()
    test()
    return redirect("/marknote/time/1")

@app.route("/delete/<int:id>")
def delete(id):
    qu.delete(id)
    test()
    return redirect("/marknote/time/1")

@app.route("/marknote/test/<int:num>")
def test(num=0):
    notes = qu.query(MarkNote,MarkNote.id,num,0)
    tags = qu.query(Tag,Tag.id,num,0)
    rels = qu.query(Relate,Relate.id,num,0)

    for a in notes:
        print("id: "+str(a.id)+"|title: "+a.title+"|tags: "+a.tags)
        print("link: "+a.link)
        print(a.note)
    print("----------------")
    for b in tags:
        print("id: "+str(b.id)+"|title: "+b.title+"|count: "+str(b.count))
    print("----------------")
    for c in rels:
        print("id: "+str(c.id)+"|noteid: "+str(c.marknoteid)+\
              "|tagid: "+str(c.tagid))

    return redirect("/marknote/time/1")
