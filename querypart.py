from marknote import *

class querypart():
    @staticmethod
    def query(table,order,num=15,offset=0):
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
        session.commit()

    @staticmethod
    def query_update(id,new):
        session.query(MarkNote).filter(MarkNote.id==id).update(new)

    @staticmethod
    def count(table):
        return session.query(table).count()
