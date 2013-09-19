#!/usr/bin/env python
from flask import request,url_for,session
from flask import redirect,render_template
from urllib import quote_plus
from sqlalchemy.sql.expression import func
from sqlalchemy import desc
from init import app,status
from query import Query
from dbset import MarkNote,Tag,Relate
import feature

import facebook
import subprocess
import urlparse
import urllib
import httplib

app.secret_key = "As%.~56!dOfj90&/loEio!"

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
    fb_access = "unknown"
    if "fb_access" in session:
        fb_access = session["fb_id"]
    print(qu.count(MarkNote))
    
    pinterval = page-((page-1)%5)
    return render_template("index.html",data=data,orderby=orderby,
           pinterval=pinterval,page=page,
           current_url=quote_plus(url_for("index",orderby=orderby,
                                  page=page)),
           fb_access=fb_access)

@app.route("/marknote/add_page")
def add_page():
    if status.auth == 2:
        return redirect("/marknote/time/1")
    return render_template("add_page.html")

@app.route("/marknote/edit_page/<int:id>")
def edit_page(id):
    if status.auth == 2:
        return redirect("/marknote/time/1")
    data = qu.query_byid(MarkNote,id).first()
    print(data)
    return render_template("edit_page.html",data=data)

@app.route("/marknote/tags/<tag>")
def tag_page(tag):
    tagid = qu.query_bytitle(Tag,tag).first().id
    rel = qu.query(Relate,Relate.id).filter(Relate.tagid==tagid)
    data = []
    for i in rel:
        data += [qu.query_byid(MarkNote,i.marknoteid).first()]

    return render_template("tag_page.html",tag=tag,data=data,
           current_url=quote_plus(url_for("tag_page",tag=tag)))

@app.route("/marknote/load_data",methods=["GET"])
def load_data():
    offset = request.args.get("offset")
    orderby = request.args.get("orderby")
    if orderby == "random":
        return render_template("load.html",data="")
    data = get_data(orderby,int(offset))
    return render_template("load.html",data=data,
           current_url=quote_plus(url_for("index",orderby=orderby,
                                  page=1)))

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

@app.route("/marknote/authenticate",methods=["POST"])
def authenticate():
    token = request.form["token"]
    fb_id = request.form["fb_id"]
    s = request.form["status"]
    response = "not login"
    print("token: "+token)
    print("fb_id: "+fb_id)
    print("status: "+s)
    if s == "unknown" or s == "not_connected":
        response = "accept: guest"
        status.auth = 2
        session['fb_access'] = token
        session['fb_id'] = "unknown"
    elif fb_id == status.topuser:
        response = "accept: top user"
        status.auth = 0
        session['fb_access'] = token
        session['fb_id'] = fb_id
    else:
        response = "accept: normal user"
        status.auth = 1
        session['fb_access'] = token
        session['fb_id'] = fb_id

    print(response)
    return response

@app.context_processor
def processor():
    def log(s):
        print(s)

    def authenticate(id):
        print("fbid: " + str(id))
        FACEBOOK_APP_ID     = '635660229802178'
        FACEBOOK_APP_SECRET = 'ae469dde76158835e337cd739750931b'
        FACEBOOK_PROFILE_ID = '100000137841418'

        oauth_args = dict(client_id = FACEBOOK_APP_ID,
                          client_secret = FACEBOOK_APP_SECRET,
                          grant_type  = 'client_credentials')
        url = 'https://graph.facebook.com/oauth/access_token?'+\
               urllib.urlencode(oauth_args)
        print(url+"\n")
        f = urllib.urlopen(url)
        s = f.read()
        print(s)
        
        oauth_access_token = s[s.find("access_token=")+13:]
        print(oauth_access_token)
        #graph = facebook.GraphAPI(oauth_access_token)
        #profile = graph.get_object("me")

        #print(dir(profile))

    return dict(auth=authenticate, log=log)

if __name__=='__main__':
    app.debug = True
    #app.run(host='127.0.0.1')
    app.run(host='192.168.1.2')

