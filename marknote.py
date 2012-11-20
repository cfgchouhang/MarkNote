from sqltool import sqltool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,String,DateTime,Text
from sqlalchemy import Column,MetaData
from sqlalchemy.orm import sessionmaker

engine,Base = sqltool.init_eng()
Session = sessionmaker(bind=engine)
session = Session()

class MarkNote(Base):
    __tablename__ = "MarkNote"
    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    title = Column(String(25))
    link = Column(String(250))
    tag = Column(String(100)) 
    note = Column(Text)
    time = Column(DateTime)

    def __init__(self,title,link,tag,note,time):
        self.title = title
        self.link = link
        self.tag = tag
        self.note = note
        self.time = time

    def __repr__(self):
        return "mark:title:'%s'\nlink:'%s'\n\
                tag:'%s'\nnote:'%s'\ntime:'%s'\n" %\
                (self.title,self.link,self.tag,self.note,self.time)

    def add(self):
        session.add(self)
    
    def get(self,num):
        return session.query(self).order_by(self.time)

    def commit(self):
        session.commit()


sqltool.eng_con_db(engine,"test")
Base.metadata.create_all(engine)
