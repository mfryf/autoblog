#-*-coding:utf-8-*-
import urllib,urllib2
import sys
from bat_replace import BatReplace
import time
import random
import json
import StringIO
import gzip
import getpass
import os

#db = MySQLdb.connect(host="localhost", user="root", passwd="", db="blog")
#cursor=db.cursor();

#设置代理
if getpass.getuser()=='brucemeng':
    opener = urllib2.build_opener( urllib2.ProxyHandler({'http':'proxy.tencent.com:8080'}) )
    urllib2.install_opener( opener )
def downloadDictionary(dictFileName):
    dictUrl=host+'/blog/similiar.txt'
    dictContent=urllib2.urlopen(urllib2.Request(dictUrl)).read()
    dictContent=dictContent.replace("\r","")
    fn=open(dictFileName,'w')
    fn.write(dictContent)
    fn.close()
def downloadOneUrl(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
    values = {'name' : 'WHY',  
              'location' : 'SDU',  
              'language' : 'Python' }

    headers = { 'User-Agent' : user_agent }  
    data = urllib.urlencode(values)  
    req = urllib2.Request(url, data, headers)  
    response = urllib2.urlopen(req)  
    html = response.read()

    titleStart=(html.find('<span class=\"link_title\">')+len('<span class=\"link_title\">'))
    titleStart=html.find("\r\n",titleStart)
    titleEnd=html.find('\r\n',titleStart+2);
    title=html[titleStart+2:titleEnd];
    if title == '        <font color=\"red\">[置顶]</font>':
        titleStart=titleEnd
        titleEnd=html.find('\r\n',titleStart+2);
        title=html[titleStart+2:titleEnd];

    startPos=html.find("<div id=\"article_content\"",0);
    endPos=html.find("<!-- Baidu Button BEGIN", startPos);
    content=html[startPos:endPos];
    if content=='':
        title=''
    title=batReplace.replaceText(title)
    content=batReplace.replaceText(content)
    value=[title,content,url];
    return value
def publish_one_blog(title,content,cookie,viewstate):
    if title=='' or content=='':
        print 'Failed:It is not a blog'
        return ''
    publishUrl='http://i.cnblogs.com/EditPosts.aspx?opt=1'
    sendheaders = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,ko;q=0.2,ms;q=0.2,zh-TW;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        #'Content-Length':'7845',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':cookie,
        'Host':'i.cnblogs.com',
        'Origin':'http://i.cnblogs.com',
        'Referer':'http://i.cnblogs.com/EditPosts.aspx?opt=1',
        'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
    }
    formData={
        '__VIEWSTATE':'/wEPDwUKLTg5MDEzODY0MQ8WAh4TVmFsaWRhdGVSZXF1ZXN0TW9kZQIBFgJmD2QWBgIGDxYCHgRUZXh0BUo8bGluayByZWw9InN0eWxlc2hlZXQiIHR5cGU9InRleHQvY3NzIiBocmVmPSIvY3NzL2FkbWluLmNzcz9pZD0yMDE0MDExMCIvPmQCCA8WAh8BBZ0BPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiIHNyYz0iL3NjcmlwdC9qcXVlcnkuY25ibG9ncy50aGlja2JveC5qcyI+PC9zY3JpcHQ+CjxzY3JpcHQgdHlwZT0idGV4dC9qYXZhc2NyaXB0IiBzcmM9Ii9zY3JpcHQvYWRtaW4uanM/aWQ9MjAxNDAxMTAiPjwvc2NyaXB0PmQCCg9kFgICAQ9kFhQCAQ8PFgIeC05hdmlnYXRlVXJsBSNodHRwOi8vd3d3LmNuYmxvZ3MuY29tL21lbmdmYW5yb25nL2RkAgMPDxYGHgZUYXJnZXRlHwIFI2h0dHA6Ly93d3cuY25ibG9ncy5jb20vbWVuZ2ZhbnJvbmcvHwEFC21lbmdmYW5yb25nZGQCBQ8PFgQfAgUXaHR0cDovL3d3dy5jbmJsb2dzLmNvbS8eCEltYWdlVXJsBS5odHRwOi8vc3RhdGljLmNuYmxvZ3MuY29tL2ltYWdlcy9hZG1pbmxvZ28uZ2lmZGQCDw8WAh4HVmlzaWJsZWdkAiMPZBYCAgEPZBYMAgEPDxYGHglDb2xsYXBzZWRnHgtDb2xsYXBzaWJsZWcfBWhkZAICD2QWBGYPZBYCZg8PFgIfAQUM5re75Yqg6ZqP56yUZGQCAQ9kFhACAQ8PFgQfAmUfBWhkZAIDDw9kFgIeCW9ua2V5ZG93bgUVdGl0bGVfa2V5ZG93bihldmVudCk7ZAIFDxYCHwEFEihUaW55TUNF57yW6L6R5ZmoKWQCCQ9kFgICAQ9kFggCAQ9kFgICAQ9kFgICAQ8QDxYGHg5EYXRhVmFsdWVGaWVsZAUKQ2F0ZWdvcnlJRB4NRGF0YVRleHRGaWVsZAUFVGl0bGUeC18hRGF0YUJvdW5kZ2QQFQAVABQrAwBkZAIDD2QWAgIBD2QWBgIBD2QWAgIBDxYCHghkaXNhYmxlZGRkAgMPFgIfDGRkAgQPFgIfAQU85Y+R5biD6Iez5Y2a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DxYCHw5oZGRkZAISDxAPFgIfDmhkZGRkAhQPFgIfBWhkAhYPEGRkFgBkAh8PEA8WAh8OaGRkZGQCDQ8PFgIfAQUG5Y+R5biDZGQCDw8PFgIfAQUM5a2Y5Li66I2J56i/ZGQCFQ9kFgICAQ9kFgICAg8PFgIfAQURMjAxNC81LzQgMjM6MjY6NDBkZAIEDxYCHwFlZAIFDxYCHwEFBjEwODY5N2QCBg8WAh8BBQM4MDhkAggPFgIfAQUBMGQCJQ8PFgQfAQULbWVuZ2ZhbnJvbmcfAgUmaHR0cDovL2hvbWUuY25ibG9ncy5jb20vdS9tZW5nZmFucm9uZy9kZAInDxYCHwEFXTxhIGhyZWY9Imh0dHA6Ly9zcGFjZS5jbmJsb2dzLmNvbS9tc2cvcmVjZW50IiB0YXJnZXQ9Il9ibGFuayIgaWQ9Imxua19zaXRlX21zZyI+55+t5raI5oGvPC9hPmQCKQ8WAh8BBaABPGEgaHJlZj0iaHR0cDovL3Bhc3Nwb3J0LmNuYmxvZ3MuY29tL2xvZ291dC5hc3B4P1JldHVyblVSTD1odHRwOi8vd3d3LmNuYmxvZ3MuY29tL21lbmdmYW5yb25nLyIgb25jbGljaz0icmV0dXJuIGNvbmZpcm0oJ+ehruiupOimgemAgOWHuueZu+W9leWQlz8nKSI+5rOo6ZSAPC9hPmQCKw8WAh8BBQQyMDE0ZAItDw8WBB8CBRdodHRwOi8vd3d3LmNuYmxvZ3MuY29tLx8BBQnljZrlrqLlm61kZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WCAU0RWRpdG9yJEVkaXQkQVBPcHRpb25zJEFkdmFuY2VkcGFuZWwxJGNrbENhdGVnb3JpZXMkMAUwRWRpdG9yJEVkaXQkQVBPcHRpb25zJEFQU2l0ZUhvbWUkY2JIb21lQ2FuZGlkYXRlBTZFZGl0b3IkRWRpdCRBUE9wdGlvbnMkQVBTaXRlSG9tZSRjYklzUHVibGlzaFRvU2l0ZUhvbWUFIUVkaXRvciRFZGl0JEFkdmFuY2VkJGNrYlB1Ymxpc2hlZAUnRWRpdG9yJEVkaXQkQWR2YW5jZWQkY2hrRGlzcGxheUhvbWVQYWdlBSdFZGl0b3IkRWRpdCRBZHZhbmNlZCRjaGtNYWluU3luZGljYXRpb24FHkVkaXRvciRFZGl0JEFkdmFuY2VkJGNoa1Bpbm5lZAUtRWRpdG9yJEVkaXQkQWR2YW5jZWQkY2hrSXNPbmx5Rm9yUmVnaXN0ZXJVc2Vy',
        'Editor$Edit$txbTitle':title,
        'Editor$Edit$EditorBody':content,
        'Editor$Edit$Advanced$ckbPublished':'on',
        'Editor$Edit$Advanced$chkDisplayHomePage':'on',
        'Editor$Edit$Advanced$chkMainSyndication':'',
        'Editor$Edit$Advanced$txbEntryName':'',
        'Editor$Edit$Advanced$txbExcerpt':'',
        'Editor$Edit$Advanced$txbTag':'',
        'Editor$Edit$Advanced$tbEnryPassword':'',
        'Editor$Edit$lkbPost':'发布'
    }
    #print formData['Editor$Edit$EditorBody']
    body=urllib.urlencode(formData)
    print "length:",sys.getsizeof(body)
    returnedReq=urllib2.Request(  
        url=publishUrl,  
        data=body,  
        headers=sendheaders)
    respone=urllib2.urlopen(returnedReq)
    print respone.info()
    print respone.code
    print respone.msg
    published_url=get_published_url(respone.read())
    return published_url
def get_published_url(html):
    fn=open('html.zip','wb')
    fn.write(html)
    fn.close()
    g = gzip.GzipFile(mode='rb', fileobj=open('html.zip','rb'))
    html = g.read()
    keyworld1='<a class=\"titlelink\" href=\"'
    keyworld2='<a id=\"link_post_title\" class=\"link-post-title\" href=\"'
    if html.find(keyworld1) < 0:
        urlStart=html.find(keyworld2)+len(keyworld2)
        urlEnd=html.find('html\">',urlStart)+len("html")
    else:
        urlStart=html.find(keyworld1)+len(keyworld1)
        urlEnd=html.find('\">\r',urlStart)
    return html[urlStart:urlEnd]
def check_program_update():
    try:
        print 'current version:%s'%version
        host2="http://10.173.27.108//data/hadoop/brucemeng/data/"
        versionUrl=host+'/blog/program/version'
        server_version=urllib2.urlopen(urllib2.Request(versionUrl)).read()
        server_version=server_version.strip()
        if server_version != version:
            programName='/csdnblog_publish.py'
            programUrl=host+'/blog/program/'+username+'/'+programName;
            programContent=urllib2.urlopen(urllib2.Request(programUrl)).read()
            programContent=programContent.replace("\r","")
            path=cur_file_dir()+'/'+programName;
            fn=open(path,'w')
            fn.write(programContent)
            fn.close()
            fn=open(path+'w','w')
            fn.write(programContent)
            fn.close()
            time.sleep(3)
            restart_program()
        else:
            print 'program is the latest version!'
            time.sleep(5)
    except Exception as e:
        print e
#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
def restart_program():
    path=cur_file_dir()
    print 'program is updated,now restart...'
    time.sleep(3)
    os.system(path+'/csdnblog_publish.py')
    sys.exit(1)
def publis_blog_by_url(url,cookie):
    values=downloadOneUrl(url)
    return publish_one_blog(values[0],values[1],cookie,'')
def auto_publish_blog():
    #time.sleep(100)
    while True:
        try:
            hour=time.localtime(time.time())[3]
            if hour >= 9 and hour <=22:
                check_program_update()
                getBlogUrl=host+'/blog/query.php?type=getOneBlog&username='+username
                respone=json.loads(urllib2.urlopen(urllib2.Request(getBlogUrl)).read())
                if respone['ret'] == 0:
                    try:
                        cookie=respone['cookie']
                        print cookie
                        published_url=publis_blog_by_url(respone['src_url'],cookie)
                        print 'published_url:',published_url
                        updateBlogUrl=host+'/blog/query.php?type=updateBlog&id='+respone['id']+'&user='+username+'&dst_url='+published_url
                        urllib2.urlopen(urllib2.Request(updateBlogUrl))
                    except Exception as e:
                        print 'error: url:'+respone['src_url']
                        print e
            length=random.randint(600,6000)
            print time.strftime('%Y-%m-%d %H:%M:%S'),'  sleep %s seconds for next publishing...'%length
            time.sleep(length)
        except Exception as e:
            print e
            time.sleep(100)
def load_cookie(filename):
    fn=open(filename,'r')
    cookie=fn.read()
    cookie=cookie.strip()
    fn.close()
    return cookie
if len(sys.argv) < 1:
    print 'USAGE:python %s url'%sys.argv[0]
    sys.exit(1)

host='http://autoblog.jd-app.com'
current_cookie='';
username='hrhguanli'
version="1.2"
downloadDictionary('similiar.txt')
batReplace=BatReplace('similiar.txt')
os.chdir(cur_file_dir())
auto_publish_blog()
