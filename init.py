from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask

dbname = "marknote"

engine = create_engine('sqlite:///notedata/'+dbname+'.db')
engine.execute("select 1").scalar()

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

class Status:
    def __init__(self,topuser,auth):
        self.topuser = topuser
        self.auth = 2
        # 0 top, 1 normal, 2 not connect/login

status = Status("100000137841418",False)

