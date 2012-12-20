from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class sqltool:

    @staticmethod
    def init_eng():
        #engine = create_engine('mysql://cfg:19921031@localhost/?charset=utf8')
        engine = create_engine('sqlite:///test1.db')
        Base = declarative_base()
        return engine,Base

    @staticmethod
    def eng_con_db(engine,dbname):
        #for mysql
        #engine.execute("CREATE DATABASE IF NOT EXISTS %s" % dbname)
        #engine.execute("USE %s" % dbname)
        engine.execute("select 1").scalar()

    @staticmethod
    def eng_del_db(engine,dbname):
        m = raw_input("Are You Sure?(Y/y)")
        print m
        if m == 'y' or m == 'Y':
            engine.execute("DROP DATABASE IF EXISTS %s" % dbname)

