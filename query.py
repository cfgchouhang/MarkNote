from init import session
from dbset import MarkNote,Tag,Relate
from sqlalchemy import or_,and_

class Query:
    def query(self,table,order,num=0,offset=0):
        data = session.query(table).order_by(order).offset(offset)
        if num!=0:
            return data.limit(num)
        return data

    def query_byid(self,table,id):
        return session.query(table).filter(table.id==id)

    def query_bytitle(self,table,title):
        return session.query(table).filter(table.title==title)
    
    def query_update(self,table,id,update):
        data = session.query(table).filter(table.id==id).update(update)
        session.commit()

    def delete_rel(self,noteid,tag):
        t = tag.first()
        session.query(Relate).filter(and_(Relate.marknoteid==noteid,
                                          Relate.tagid==t.id)).delete()
        session.commit()
        self.query_update(Tag,t.id,{'count':t.count-1})
        if t.count <= 0:
            tag.delete()
            session.commit()
            
    def delete(self,id):
        note = self.query_byid(MarkNote,id)
        for t in note.first().tags.split(','):
            if t != '':
                tag = self.query_bytitle(Tag,t)
                self.delete_rel(id,tag)
        note.delete()
        session.commit()
    
    def count(self,table):
        return session.query(table).count()
