#-*-coding:utf-8-*-
import sys
import re

class BatReplace(object):
    def __init__(self, mapFile):
        self.myDict=dict()
        self.add_keyword_from_file(mapFile)
    def add_keyword_from_file(self,mapFile):
        fn=open(mapFile,'r')
        for line in fn:
            line = line.strip()
            key,value=line.split(' ')
            self.myDict[key]=value
            #print key,value
        fn.close()
    def isChineseWorld(self,text):
        return len(re.findall(r"(\w+)\Z",text)) == 0
    def replaceText(self,text):
        self.count=0
        self.rate=0
        replaceLength=0
        text=text.strip()
        lines=text.split('\r\n')
        text='';
        for line in lines:
            for k,v in self.myDict.items():
                lenk=len(re.findall(k,line))
                lenv=len(re.findall(v,line))
                if lenk>lenv and lenk > 0 and self.isChineseWorld(k):
                    line=line.replace(k,v)
                    self.count+=lenk
                    replaceLength+=len(k)
                    print k.decode("utf-8"),'->',v.decode("utf-8"),lenk
                elif lenv > 0 and self.isChineseWorld(v):
                    line=line.replace(v,k)
                    self.count+=lenv
                    replaceLength+=len(v)
                    print v.decode("utf-8"),'->',k.decode("utf-8"),lenv
            text=text+line+'\r\n'
        self.rate=replaceLength*100.0/len(text)
        print 'count of  replaced words:%d'%self.count
        print 'rate:%.2f%%'%self.rate
        return text
#rep=BatReplace('similiar.txt')
#fn=open('html.txt')
#text=fn.read();
#fn.close();
#text=rep.replaceText(text)
#fn=open('html2.txt','w')
#fn.write(text)
#fn.close()
