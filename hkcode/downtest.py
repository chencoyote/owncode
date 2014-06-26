#!/usr/bin/env python
#-*- coding:utf-8 -*-
from urllib import urlencode
import urllib2
import cookielib
import re

DOCRE=r"\d+x*_\d.doc"
XLSRE=r"\w*.xls"

cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler,proxy_support)
urllib2.install_opener(opener)

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36"
    }
formdata = urlencode({
    "loginfield":"username",
    'continueURI':'http://www.anying.org/forum-2-1.html',
    "questionid":0,
    'loginsubmit':'True'
    })
req = urllib2.Request(
        url = "http://qq.yynet.cn/adminer.sql",
        headers = headers
        )
resault = urllib2.urlopen(req).read()
#res = re.findall(r"<a.*?>.*?</a>",resault)
#for i in res:
#    filename = re.findall(XLSRE,i)
#    if filename:
#        url = "http://rczp.bhu.edu.cn/UserFiles/" + filename[0]
#        f = urllib2.urlopen(url)
#        data = f.read() 
#        print "read doc file"
with open("./doc/qq.yynet.cn", "wb") as code:     
   code.write(resault)
print "write %s success"%(filename[0])
code.close()
    
