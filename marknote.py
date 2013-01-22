from sqltool import sqltool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,String,DateTime,Text
from sqlalchemy import Column,MetaData,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship,backref

dbname = "marknote"
engine,Base = sqltool.init_eng(dbname)
Session = sessionmaker(bind=engine)
session = Session()

class MarkNote(Base):
    __tablename__ = "MarkNote"
    #for mysql
    #__table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    title = Column(String)
    link = Column(String)
    tag = Column(String) 
    note = Column(Text)
    img = Column(Text)
    time = Column(DateTime)

    relates = relationship("Relate",order_by="Relate.id")

    def __init__(self,title,link,tag,note,img,time):
        self.title = title
        self.link = link
        self.tag = tag
        self.note = note
        self.img = img
        self.time = time

    def __repr__(self):
        return "MarkNote title:%s|link:%s|tag:%s\nnote:%s\ntime:%s\n" %\
                (self.title,self.link,self.tag,self.note,self.time)

    def add(self):
        session.add(self)
    
    def commit(self):
        session.commit()

class Tag(Base):
    __tablename__ = "Tag"
    #for mysql
    #__table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    title = Column(String)
    count = Column(Integer)

    relates = relationship("Relate",order_by="Relate.id")

    def __init__(self,title,count):
        self.title = title
        self.count = count

    def __repr__(self):
        return "Tag id:%s|title:%s" %\
                (self.id,self.title)

    def add(self):
        session.add(self)
    
    def commit(self):
        session.commit()

class Relate(Base):
    __tablename__ = "Relate"
    #__table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    title = Column(String)
    tagid = Column(Integer,ForeignKey("Tag.id"))
    marknoteid = Column(Integer,ForeignKey("MarkNote.id"))

    def __init__(self,title):
        self.title = title

    def __repr__(self):
        return "id :%s|title:%s|tagid:%s|marknoteid:%s" %\
                (self.id,self.title,self.tagid,self.marknoteid)

    def add(self):
        session.add(self)
    
    def commit(self):
        session.commit()

sqltool.eng_con_db(engine,dbname)
Base.metadata.create_all(engine)

