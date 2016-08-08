# -*- coding:utf-8 -*-
__author__ = 'deathsea'
import urllib
import urllib2
import hashlib
import json,os,time

imageSavePath = "E:\\mcd2\\img\\"
HTMLtemplate = u"""
<html>
    <head>
    <title>{title}</title>
    <link type="text/css" rel="stylesheet" href="css/style.css">
    </head>
    <body>
    {page}
    <div class="post_list">
    {content}
    </div>
    {page}
    </body>
</html>"""
postTemplate = u"""
    <div class="floor">
        {author}
        <div class="post">
            <div class="post_content">{content}</div>
            <div class="post_floor">{floor}楼</div>
            <div class="post_time">{time}</div>
        </div>
    </div>
"""
pageTemplate = u"""
    <div class="page">
        <a href="1.html">首页</a>
        <a href="{prepage}">上一页</a>
        {preotherpage}
        <a href="#">{thispage}</a>
        {nextotherpage}
        <a href="{nextpage}">下一页</a>
        <a href="{lastpage}">末页</a>
    </div>"""
authorTemplate = u"""
    <div class='author'>
        <ul>
            <li><img class="author_iron" src='{iron}' /></li>
            <li>{name}</li>
            <li>{levelname}</li>
            <li>{level}</li>
        </ul>
    </div>"""
def sign(keyValueMap):
    d = keyValueMap
    k = keyValueMap.keys()
    k.sort()
    pass

def getPbData(kz,pn,lz="1",rn="30"):
    pass

def downloadImg(url,filePath):
    with open(filePath,"wb") as f:
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request)
            content = response.read()
        except urllib2.HTTPError,p:
            content = ""
        f.write(content)

def createPageHtml(page,lastPage):
    preotherpage = ""
    for i in range(page-5,page):
        if i<=0:pass
        else:
            preotherpage += "<a href='%d.html'>%d</a>"%(i,i)
    nextotherpage = ""
    for i in range(page,page+6):
        if i>lastPage:pass
        else:
            nextotherpage += "<a href='%d.html'>%d</a>"%(i,i)
    if page == 1:prepage="#"
    else:prepage = "%d.html"%(page-1)
    if page == lastPage:nextpage = "#"
    else:nextpage = "%d.html"%(page+1)
    return pageTemplate.format(prepage=prepage,
        preotherpage=preotherpage,
        thispage="%d"%page,
        nextotherpage=nextotherpage,
        nextpage=nextpage,
        lastpage="%d.html"%lastPage)

def handlerData(jsonStr):
    # post_list
    D = json.loads(jsonStr)
    post_list = D["post_list"]
    title = post_list[0]["title"]
    authorName = post_list[0]["author"]["name"]
    authorLevel = post_list[0]["author"]["level_id"]
    authorLevelName = post_list[0]["author"]["level_name"]
    auhtor = authorTemplate.format(iron="img/iron.png",name=authorName,levelname=authorLevelName,level=authorLevel)
    # postTemplate
    page = D["page"]["current_page"]
    lastPage = D["page"]["total_page"]
    pageContent = createPageHtml(page,lastPage)
    htmlContent = []
    for post in post_list:
        ptime = time.strftime("%Y-%m-%d %H:%M",time.gmtime(post["time"]-time.timezone)) 
        floor = post["floor"]
        postcontent = post["content"]
        tmp = []
        imgindex = 0
        for x in postcontent:
            if x["type"] == 0:
                tmp.append("\n<br/>"+x["text"].replace("\n","<br/>"))
            elif x["type"] == 1:#链接
                tmp.append("\n<br/><a href='%s'>%s</a>\n<br/>"%(x["link"],x["text"]))
            elif x["type"] == 2:
                #表情
                tmp.append(u"[表情：%s]"%x["c"])
            elif x["type"] == 3:
                srcurl = x["src"]
                fileType = "."+srcurl.split(".")[-1]
                imagePath = imageSavePath+str(page)+"_"+str(floor)+"_"+str(imgindex)+fileType
                # downloadImg(srcurl,imagePath)
                tmp.append("\n<br/><img src='%s'></img>"%("img/%d_%d_%d%s"%(page,floor,imgindex,fileType)))
                imgindex+=1
            elif x["type"] == 4:#at 人
                tmp.append("<font style='color:blue'>%s</font>"%x["text"])
            elif x["type"] == 5:#视屏
                tmp.append('\n<br/><embed type="application/x-shockwave-flash" class="BDE_Flash" src="%s" width="500" height="450" scale="noborder" allowscriptaccess="never" menu="false" loop="loop" play="true" womode="transparent" pluginspage="http://www.macromedia.com/go/getflashplayer" allowfullscreen="true" flashvars="playMovie=true&amp;auto=1&amp;adss=0&amp;isAutoPlay=false" style="visibility: visible; display: block;">'%x["text"])
            else:
                print x
                raise TypeError
        c = "".join(tmp)
        htmlContent.append(
            postTemplate.format(floor=floor,
                author=auhtor,
                content=c,
                time=ptime))
    HTC = "".join(htmlContent)
    return HTMLtemplate.format(title=title,page=pageContent,content=HTC)

def Download(kz="1766018024",pageStart = 1,lastPage = 301,authorportrait = "9731646566616e697665324a06"):
    SavePath = ""
    # 看头像在不在
    fetchurl = "http://tb.himg.baidu.com/sys/portrait/item/"+authorportrait
    if not os.path.exists(imageSavePath+"iron.png"):
        downloadImg(fetchurl,imageSavePath+"iron.png")
    for page in range(pageStart,lastPage+1):
        # 
        f = open("%d.html"%page,"w")
        # if os.path.exists("json\\%d.json"%page):
        fjson = open("json\\%d.json"%page,"r")
        jsonStr = fjson.read()
        fjson.close()
        # else:
        #     fjson = open("json\\%d.json"%page,"w")
        #     jsonStr = getPbData(kz,str(page))
        #     fjson.write(jsonStr)
        #     fjson.close()
        f.write(handlerData(jsonStr).encode("u8"))
        f.close()
        print "page:"+str(page)+".done!"
Download()
# jsonStr = getPbData("1766018024","1")
# handlerData(jsonStr)
# baseURL = 'http://tieba.baidu.com/p/1766018024'
# bdtb = BDTB(baseURL,1)
# bdtb.getPage(1)