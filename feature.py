from init import app,status
from dbset import MarkNote,Tag,Relate
from query import Query
from flask import request,redirect,render_template,url_for
from datetime import datetime
from urllib import quote_plus

qu = Query()

@app.route("/marknote/add_byurl",methods=["POST"])
def add_byurl():
    form = request.form
    new_data = {}
    if form["title"]=='' and form["link"]=='':
        return redirect(url_for("redir"))
    for key in form.keys():
        new_data[key] = form[key]
    new_data['time'] = datetime.now()
    add(**new_data)
    return redirect("/marknote/time/1")

def add(title,link,tags,note,time):
    tags = tags.replace(' ','')
    tags = tags.strip(',')
    if title=='':
        title = "untitle"
    if tags=='':
        tags = "untag"
    new_data = MarkNote(title,link,tags,note,time)
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
    print("add new marknote:\n"+str(new_data))

@app.route("/marknote/update/<int:id>",methods=["GET","POST"])
def update(id):
    form = request.form
    new = {}
    old_tags = {}
    old_data = qu.query_byid(MarkNote,id).first()
    for key in form.keys():
        new[key] = form[key]
    new["tags"] = new["tags"].replace(' ','')
    new["tags"] = new["tags"].strip(',')
    if new["title"] == '':
        new["title"] = "untitle"
    if new["tags"] == '':
        new["tags"] = "untag"
    
    print("update:"+str(new))
    print new["tags"].split(',')
    for tag in old_data.tags.split(','):
        if tag == '':
            print("blank")
            continue
        old_tags[tag] = True

    for tag in new["tags"].split(','):
        if tag == '':
            continue
        if tag in old_tags.keys():
            old_tags[tag] = False
        else:
            rel = Relate()
            check_tag = qu.query_bytitle(Tag,tag).first()
            if check_tag == None:
                new_tag = Tag(tag,1)
                new_tag.relates += [rel]
                new_tag.add()
            else:
                check_tag.relates += [rel]
                qu.query_update(Tag,check_tag.id,{"count":check_tag.count+1})
            
            old_data.relates += [rel]
            old_tags[tag] = False

    for tag in old_tags.keys():
        if old_tags[tag]:
            qu.delete_rel(id,qu.query_bytitle(Tag,tag))
    
    #new["last_time"] = datetime.now()
    qu.query_update(MarkNote,id,new)

    next_url = request.args.get("next")
    return redirect(next_url)

@app.route("/marknote/search",methods=["GET"])
def search():
    s = request.args.get("term").strip(' ')
    term = s
    op = ""
    if '|' in s:
        op = s[s.rfind('|'):]
        term = s[:s.rfind('|')].strip(' ')

    if "all" in op:
        data = qu.search(term,findall=True)
    elif "tags:" in op:
        tags = op[op.find("tags:")+5:]
        data = qu.search(term,withtags=tags.replace(' ',''))
    else:
        data = qu.search(term)

    return render_template("search_page.html",data=data,
           term=term,options=op[1:],text=s,
           current_url=quote_plus(url_for("search",term=s)))

@app.route("/marknote/delete/<int:id>",methods=["GET"])
def delete(id):
    #if status.auth == 0:
    qu.delete(id)
    next_url = request.args.get("next")
    return redirect(next_url)

@app.route("/marknote/test/<int:num>")
def test_byurl(num=0):
    test(num)
    return redirect("/marknote/time/1")

def test(num=0):
    notes = qu.query(MarkNote,MarkNote.id,num,0)
    tags = qu.query(Tag,Tag.id,num,0)
    rels = qu.query(Relate,Relate.id,num,0)
    out = open("notedata/test",'w')
    
    out.write("note--------------\n")
    for a in notes:
        out.write(str(a))
    out.write("tag---------------\n")
    for b in tags:
        out.write(str(b)+'\n')
    out.write("rel---------------\n")
    for c in rels:
        out.write(str(c)+'\n')
    
@app.route("/marknote/export")
def export_db():
    out_data = open("notedata/exportdb",'w')
    for note in qu.query(MarkNote,MarkNote.id):
        out_data.write(note.title.encode('utf-8')+'\n')
        out_data.write(note.link+'\n')
        out_data.write(note.tags.encode('utf-8')+'\n')
        out_data.write(note.note.encode('utf-8')+'###\n')
        out_data.write(note.time.strftime("%Y-%m-%d %H:%M:%S.%f")+'\n')
    return redirect("/marknote/time/1")

@app.route("/marknote/import")
def import_db():
    count = 0
    data = {}
    for line in open("notedata/exportdb",'r'):
        if count == 0:
            data["title"] = line[:-1].decode('utf-8')
            count += 1
        elif count == 1:
            data["link"] = line[:-1].decode('utf-8')
            count += 1
        elif count == 2:
            data["tags"] = line[:-1].decode('utf-8')
            data["note"] = ""
            count += 1
        elif count == 3:
            if "###" in line:
                data["note"] += line[:line.rfind("###")].decode('utf-8')
                count += 1
                continue
            data["note"] += line.decode('utf-8')
        elif count == 4:
            timestr = line[:-1].decode('utf-8')
            data["time"] = datetime.strptime(timestr,"%Y-%m-%d %H:%M:%S.%f")
            add(**data)
            count = 0
    return redirect("/marknote/time/1")
