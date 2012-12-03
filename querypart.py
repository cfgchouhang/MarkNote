from marknote import *

class querypart():
    @staticmethod
    def query(table,order,num=15):
        data = session.query(table).order_by(order).limit(num)
        return data

    @staticmethod
    def query_byid(id):
        return session.query(MarkNote).filter(MarkNote.id==id).first()

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
