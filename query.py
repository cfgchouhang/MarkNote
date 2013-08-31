from init import session
from dbset import MarkNote,Tag,Relate
from sqlalchemy import or_,and_

class Query:
    def query(self,table,order,num=0,offset=0):
        data = session.query(table).order_by(order)
        if offset!=0:
            data = data.offset(offset)
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
        tags = {}
        for t in note.first().tags.split(','):
            if t != '':
                tags[t] = t
        for t in tags.keys():
            print("tag:"+t)
            tag = self.query_bytitle(Tag,t)
            self.delete_rel(id,tag)
        note.delete()
        session.commit()
    
    def search(self,term,withtags="",findall=False):
        if withtags != "":
            notes = session.query(MarkNote).filter(
                        MarkNote.title.like('%'+term+'%'))
            note = []
            notag = False
            for i in notes:
                fit = False
                rel = self.query(Relate,Relate.id).filter(
                            Relate.marknoteid==i.id)

                for tag in withtags.split(','):
                    try:
                        tagid = self.query_bytitle(Tag,tag).first().id
                    except:
                        notag = True
                        break

                    for j in rel:
                        if j.tagid == tagid:
                            fit = True
                            break
                    else:
                        fit = False

                    if not fit:
                        break

                if fit:
                    note += [i]

                if notag:
                    del note[:]
                    break

        elif findall:
            note = session.query(MarkNote).filter(
                        or_(MarkNote.tags.like('%'+term+'%'),
                        MarkNote.title.like('%'+term+'%')))
        else:
            note = session.query(MarkNote).filter(
                        MarkNote.title.like('%'+term+'%'))

        return note

    def count(self,table):
        return session.query(table).count()
