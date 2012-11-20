#-*- coding:utf-8 -*-
from flask import Flask,request,redirect,render_template
from datetime import datetime
import sqltool
import marknote

app = Flask(__name__)
sql = sqltool.sqltool
mrno = marknote.MarkNote

@app.route("/add_page")
def page():
    return render_template('add_page.html')

@app.route("/add_new",methods=["POST"])
def add_new():
    a = request.form
    tags = a['tags'].replace(' ','')
    item = mrno(a['title'],a['link'],a['tags'],a['note'],datetime.now())
    item.add()
    item.commit()
    return redirect('/keynote')

