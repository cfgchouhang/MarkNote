#!/usr/bin/env python
from flask import redirect,render_template
import editpart

app = editpart.app

@app.route("/")
def redir():
    return redirect('/keynote')

@app.route("/keynote")
def main():
    return render_template('main.html')
    
if __name__=='__main__':
    app.debug = True
    app.run(host='192.168.1.2')
