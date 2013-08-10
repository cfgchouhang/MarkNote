from init import Base,engine,session
from sqlalchemy import Integer,String,DateTime,Text
from sqlalchemy import Column,MetaData,ForeignKey
from sqlalchemy.orm import relationship,backref

class MarkNote(Base):
    __tablename__ = "MarkNote"
    #for mysql
    #__table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    title = Column(String)
    link = Column(String)
    tags = Column(String) 
    note = Column(Text)
    time = Column(DateTime)

    relates = relationship("Relate",order_by="Relate.id")

    def __init__(self,title,link,tags,note,time):
        self.title = title
        self.link = link
        self.tags = tags
        self.note = note
        self.time = time

    def add(self):
        session.add(self)
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

    def add(self):
        session.add(self)
        session.commit()

class Relate(Base):
    __tablename__ = "Relate"
    #__table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    tagid = Column(Integer,ForeignKey("Tag.id"))
    marknoteid = Column(Integer,ForeignKey("MarkNote.id"))

    def add(self):
        session.add(self)
        session.commit()

Base.metadata.create_all(engine)

