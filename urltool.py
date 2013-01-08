import urllib2

def getimgurl(note):
    n = note.count("<img>")
    url = []
    hasimg = False
    if n >0 :
        hasimg = True
    for i in range(n):
        s = note.find("<img>")
        e = note.find("</img>")
        for j in note[s+5:e].split("\n"):
            j = j.replace("\r","")
            if j != '':
                url += [j]
        note = note[e+6:]
    return url, hasimg
 
def procimgurl(noteid,imgurl):
    c = 0
    dir = "./static/images/"+str(noteid)
    imgdir = ""
    for u in imgurl:
        img = urllib2.urlopen(u)
        imgdir += str(noteid)+'_'+str(c)+u[u.rfind('.'):]+','
        lofile = open(dir+'_'+str(c)+u[u.rfind('.'):],'w')
        lofile.write(img.read())
        lofile.close()
        c += 1
    return imgdir[:imgdir.rfind(',')]
