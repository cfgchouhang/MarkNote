from marknote import *

class querypart():
    @staticmethod
    def query(order,num=15):
        data = session.query(MarkNote).order_by(order).limit(num)
        return data

    @staticmethod
    def query_byid(id):
        return session.query(MarkNote).filter(MarkNote.id==id).first()

    @staticmethod
    def delete_byid(id):
        session.query(MarkNote).filter(MarkNote.id==id).delete()
        session.commit()

    @staticmethod
    def query_update(id,new):
        session.query(MarkNote).filter(MarkNote.id==id).update(new)
