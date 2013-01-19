from sqlalchemy import or_,and_
from marknote import *

class querypart():
    @staticmethod
    def query(table,order,num=100,offset=0):
        data = session.query(table).order_by(order).offset(offset).limit(num)
        return data

    @staticmethod
    def query_byid(id):
        return session.query(MarkNote).filter(MarkNote.id==id).first()

    @staticmethod
    def query_join(major,relate,majorid):
        return session.query(major).join(relate).filter(relate.id==majorid).all()

    @staticmethod
    def query_bytitle(table,title):
        return session.query(table).filter(table.title==title).first()

    @staticmethod
    def delete_byid(id):
        session.query(MarkNote).filter(MarkNote.id==id).delete()
        session.query(Relate).filter(Relate.marknoteid==id).delete()
        session.commit()

    @staticmethod
    def delete_rel(noteid,tag):
        session.query(Relate).filter(and_(Relate.marknoteid==noteid,\
                                          Relate.title==tag)).delete()
        session.commit()

    @staticmethod
    def query_update(id,new):
        session.query(MarkNote).filter(MarkNote.id==id).update(new)
        session.commit()

    @staticmethod
    def count(table):
        return session.query(table).count()

    @staticmethod
    def search(term):
        return session.query(MarkNote).filter(\
            or_(MarkNote.title.like('%'+term+'%'),\
                MarkNote.tag.like('%'+term+'%')))
