from sqltool import sqltool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,String,DateTime,Text
from sqlalchemy import Column,MetaData,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship,backref

engine,Base = sqltool.init_eng("marknote")
Session = sessionmaker(bind=engine)
session = Session()

class MarkNote(Base):
    __tablename__ = "MarkNote"
    #__table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    title = Column(String)
    link = Column(String)
    tag = Column(String) 
    note = Column(Text)
    time = Column(DateTime)

    relates = relationship("Relate",order_by="Relate.id")

    def __init__(self,title,link,tag,note,time):
        self.title = title
        self.link = link
        self.tag = tag
        self.note = note
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
    #__table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    title = Column(String)

    relates = relationship("Relate",order_by="Relate.id")

    def __init__(self,title):
        self.title = title

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

    #marknote = relationship("MarkNote",backref=backref("MarkNote.title"))
    #tag = relationship("Tag",backref=backref("Tag.title"))

    def __init__(self,title):
        self.title = title

    def __repr__(self):
        return "id :%s|title:%s|tagid:%s|marknoteid:%s" %\
                (self.id,self.title,self.tagid,self.marknoteid)

    def add(self):
        session.add(self)
    
    def commit(self):
        session.commit()

#"test" is the base name for using mysql
sqltool.eng_con_db(engine,"marknote")
Base.metadata.create_all(engine)

