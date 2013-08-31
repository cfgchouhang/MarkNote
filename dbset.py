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
    #last_time = Column(DateTime)

    relates = relationship("Relate",order_by="Relate.id")

    def __init__(self,title,link,tags,note,time):
        self.title = title
        self.link = link
        self.tags = tags
        self.note = note
        self.time = time

    def __repr__(self):
        s = "id: "+str(self.id)+"|title: "+self.title.encode('utf-8')+"\n"
        s += "tags: "+self.tags.encode('utf-8')+"\n"
        s += "link: "+self.link.encode('utf-8')+"\n"
        s += "note:\n"+self.note.encode('utf-8')+"\n"
        s += "time: "+str(self.time)
        return s

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

    def __repr__(self):
        s = "id: "+str(self.id)+"|title: "+self.title.encode('utf-8')
        s += "|count: "+str(self.count)
        return s

    def add(self):
        session.add(self)
        session.commit()


class Relate(Base):
    __tablename__ = "Relate"
    #__table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    id = Column(Integer,primary_key=True)
    tagid = Column(Integer,ForeignKey("Tag.id"))
    marknoteid = Column(Integer,ForeignKey("MarkNote.id"))

    def __repr__(self):
        s = "id: "+str(self.id)+"|marknoteid: "+str(self.marknoteid)
        s += "|tagid: "+str(self.tagid)
        return s

    def add(self):
        session.add(self)
        session.commit()

Base.metadata.create_all(engine)

