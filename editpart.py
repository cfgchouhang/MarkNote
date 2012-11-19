from flask import Flask,request,redirect,render_template
import sqltool
import marknote

app = Flask(__name__)
sql = sqltool.sqltool
MrNo = marknote.MarkNote

@app.route("/add_page")
def page():
    return render_template('add_page.html')

@app.route("/add_new",methods=["POST"])
def add_new():
    form = request.form
    print form['title']
    print form['link']
    print form['tag']
    print form['note']
    return redirect('/keynote')
